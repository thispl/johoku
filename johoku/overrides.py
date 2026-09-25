import frappe
from datetime import datetime
from email import message
import math
import pandas as pd
from frappe.frappeclient import FrappeException
from frappe.utils.data import add_days, date_diff
from hrms.hr.doctype.employee_checkin.employee_checkin import EmployeeCheckin
from hrms.hr.doctype.shift_request.shift_request import ShiftRequest
from hrms.hr.doctype.leave_application.leave_application import LeaveApplication
from hrms.hr.doctype.leave_allocation.leave_allocation import LeaveAllocation
from hrms.hr.doctype.compensatory_leave_request.compensatory_leave_request import CompensatoryLeaveRequest
from hrms.payroll.doctype.salary_slip.salary_slip import SalarySlip
from erpnext.setup.doctype.employee.employee import Employee
from datetime import date, timedelta,time
from datetime import date
import datetime as dt
from frappe.utils import cstr, cint, getdate,get_first_day, get_last_day, today, time_diff_in_hours
from frappe import _
from hrms.hr.utils import throw_overlap_error
from frappe.utils import (
	add_days,
	cint,
	cstr,
	date_diff,
	flt,
	formatdate,
	get_first_day,
	getdate,
	money_in_words,
	rounded,
)
from hrms.hr.utils import (
	create_additional_leave_ledger_entry,
	get_holiday_dates_for_employee,
	get_leave_period,
	validate_active_employee,
	validate_dates,
	validate_overlap,
)

@frappe.whitelist()
def get_employee():
	emp_details = frappe.db.get_value('Employee',{'user_id':frappe.session.user},['user_id'])
	return emp_details

class CustomSalarySlip(SalarySlip):
	def get_date_details(self):
		joining_date, relieving_date = frappe.get_cached_value(
			"Employee", self.employee, ["date_of_joining", "relieving_date"]
		)
		holidays = self.get_holidays_for_employee(self.start_date, self.end_date)
		dates_list = get_dates(self.start_date, self.end_date)
		if relieving_date and (getdate(self.start_date) <= relieving_date < getdate(self.end_date)):
			holidays = self.get_holidays_for_employee(self.start_date, relieving_date)
			dates_list = get_dates(self.start_date, relieving_date)
		if joining_date and (getdate(self.start_date) < joining_date <= getdate(self.end_date)):
			holidays = self.get_holidays_for_employee(joining_date,self.end_date)
			dates_list = get_dates(joining_date, self.end_date)
		holiday_count = len(holidays)
		working_days = date_diff(self.end_date, self.start_date) + 1
		self.total_present_days_in_a_month = working_days - holiday_count
		
		present_days_count = halfdays_count = 0
		for date in dates_list:
			if not check_holiday(date, self.employee):
				# frappe.errprint(date)
				present_days_count += frappe.db.count(
					"Attendance",
					{
						"attendance_date": date,
						"leave_application": ["is", "not set"],
						'employee': self.employee,
						"status": "Present",
						"docstatus": ["!=", 2],
					},
				)
				halfdays_count += frappe.db.count(
					"Attendance",
					{
						"attendance_date": date,
						"total_working_hours":[">",4],
						"status": "Half Day",
						'employee': self.employee,
						"docstatus": ["!=", 2],
					},
				)
		self.total_present_days_of_employee = present_days_count + (halfdays_count / 2)
		# frappe.errprint(present_days_count)
		# frappe.errprint(halfdays_count)
		compensatory_off_count = frappe.db.count(
			"Attendance",
			{
				"attendance_date": ["between", [self.start_date, self.end_date]],
				"leave_application": ["is", "set"],
				'employee': self.employee,
				"leave_type": "Compensatory Off",
				"status": "On Leave",
				"docstatus": ["!=", 2],
			},
		)
		compensatory_off_count_hd = frappe.db.count(
			"Attendance",
			{
				"attendance_date": ["between", [self.start_date, self.end_date]],
				"leave_application": ["is", "set"],
				'employee': self.employee,
				"leave_type": "Compensatory Off",
				"status": "Half Day",
				"docstatus": ["!=", 2],
			},
		)
		if compensatory_off_count_hd >0:
			compensatory_off_count_hd=compensatory_off_count_hd/2
		self.compensatory_off = compensatory_off_count+compensatory_off_count_hd


		monthly_ot_hours =0
		total_working_days = date_diff(getdate(self.end_date), self.start_date) + 1
		payroll_date = self.start_date
		ebr = frappe.db.sql(
			"""
			SELECT
				SUM(working_hours) as ot_hours
			FROM `tabEmployee Benefits Regularization`
			WHERE
				employee=%s
				AND docstatus=1 AND provision ='OT'
				AND workflow_state ='Approved'
				AND date  BETWEEN %s AND %s""",
			(self.employee, self.start_date, self.end_date),as_dict=True
		)
		ot = frappe.db.sql(
			"""
			SELECT
				SUM(permitted_overtime_hours) as ot_hours
			FROM `tabOvertime List`
			WHERE
				employee=%s AND docstatus=1
				AND ot_from_date BETWEEN %s AND %s""",
			(self.employee, self.start_date, self.end_date),as_dict=True
		)
		if ot and ot[0]['ot_hours'] is not None:
			monthly_ot_hours += ot[0]["ot_hours"]
			# frappe.errprint(f"ot_monthly_ot_hours {monthly_ot_hours}")
   

		if ebr and ebr[0]["ot_hours"] is not None:
			monthly_ot_hours += ebr[0]["ot_hours"]
			# frappe.errprint(f"monthly_ot_hours {monthly_ot_hours}")
   
		if monthly_ot_hours > 0:
			fixed_earning=frappe.db.get_value("Employee",{'name':self.employee},['fixed_earning']) or 0
			fixed_earning = float(fixed_earning) 
			monthly_ot_hours = float(monthly_ot_hours)
			ot_amount = (((fixed_earning/total_working_days)/8)*2)*monthly_ot_hours
			self.ot_amount =ot_amount
			self.ot_hours = monthly_ot_hours
			joining_date1= frappe.get_value("Employee", self.employee, ["date_of_joining"])
			# if not frappe.db.exists('Additional Salary', {'employee': self.employee, 'payroll_date': payroll_date, 'salary_component': "Overtime", 'docstatus': ('!=', 2)}):
			# 	additional_salary = frappe.new_doc("Additional Salary")
			# 	additional_salary.company = self.company
			# 	additional_salary.employee = self.employee
			# 	additional_salary.currency = 'INR'
			# 	additional_salary.salary_component = 'Overtime'
			# 	payroll_date_obj = getdate(payroll_date)
			# 	joining_date_obj = getdate(joining_date1)
			# 	if payroll_date_obj < joining_date_obj:
			# 		additional_salary.payroll_date = joining_date_obj
			# 	else:
			# 		additional_salary.payroll_date = payroll_date_obj
			# 	additional_salary.amount = ot_amount
			# 	additional_salary.submit()
			payroll_date_obj = getdate(payroll_date)
			joining_date_obj = getdate(joining_date1)
			if payroll_date_obj < joining_date_obj:
				payroll_date = joining_date_obj
			else:
				payroll_date = payroll_date_obj
			old_ot_list = frappe.get_all(
				"Additional Salary",
				filters={
					"employee": self.employee,
					"salary_component": "Overtime",
					"docstatus": 1,
					"payroll_date":payroll_date
				},
				fields=["name"]
			)

			for row in old_ot_list:
				frappe.delete_doc("Additional Salary", row.name, force=1)


			additional_salary = frappe.new_doc("Additional Salary")
			additional_salary.company = self.company
			additional_salary.employee = self.employee
			additional_salary.currency = 'INR'
			additional_salary.salary_component = 'Overtime'
			additional_salary.overwrite = 1

			payroll_date_obj = getdate(payroll_date)
			joining_date_obj = getdate(joining_date1)

			if payroll_date_obj < joining_date_obj:
				additional_salary.payroll_date = joining_date_obj
			else:
				additional_salary.payroll_date = payroll_date_obj

			additional_salary.amount = ot_amount
			# additional_salary.submit()
   
	def before_save(self):
		for d in self.deductions:
			round_up = frappe.db.get_value("Salary Component", d.salary_component, "round_up")
			if round_up:
				d.amount = math.ceil(d.amount)
	# def validate(self):
	# 	total_present_days = self.total_present_days_of_employee or 0

	# 	if total_present_days <= 4:
	# 		frappe.log_error(
	# 			title="Invalid Present Days - Salary Slip Issue",
	# 			message=f"""
	# 			Employee: {self.employee}
	# 			From: {self.start_date}
	# 			To: {self.end_date}
	# 			Total Present Days: {total_present_days}
	# 			Issue: Total present days ≤ 4
	# 			"""
	# 		)

	# 		if not getattr(self, "payroll_entry", None):
	# 			frappe.throw(
	# 				"Salary slip cannot be saved because total present days are less than or equal to 4."
	# 			)
	def after_insert(self):
		total_present_days = self.total_present_days_of_employee or 0
		status = frappe.db.get_value("Employee", self.employee, "status")

		if total_present_days <= 4 and status == "Left":
			frappe.log_error(
				title="Salary Slip Auto Deleted",
				message=f"""
				Employee: {self.employee}
				Salary Slip: {self.name}
				Total Present Days: {total_present_days}
				Status: {status}
				Reason: Present days ≤ 4 and employee is Left
				"""
			)

			frappe.delete_doc("Salary Slip", self.name, force=1)
class CustomEmployeeCheckin(EmployeeCheckin):
	def after_save(self):
		get_date = datetime.strptime(str(self.time),'%Y-%m-%d %H:%M:%S').date()
		self.checkin_log_date = get_date 
	def fetch_shift(self):
		# Define shift time ranges
		if self.log_type == 'IN':
			if isinstance(self.time, str):
				time_field = datetime.strptime(self.time, '%Y-%m-%d %H:%M:%S')
			checkin_date = time_field.date()
			checkin_time = time_field.time()
			min_in_time1 = datetime.strptime('07:00', '%H:%M').time()
			max_in_time1 = datetime.strptime('13:00', '%H:%M').time()
			min_in_time2 = datetime.strptime('15:00', '%H:%M').time()
			max_in_time2 = datetime.strptime('21:00', '%H:%M').time()
			min_in_time3 = datetime.strptime('01:00', '%H:%M').time()
			max_in_time3 = datetime.strptime('05:00', '%H:%M').time()

			if max_in_time1 >= checkin_time >= min_in_time1:
				self.shift = '1'
			elif max_in_time2 >= checkin_time >= min_in_time2:
				self.shift = '2'
			elif max_in_time3 > checkin_time >= min_in_time3:
				self.shift = '3'
			if self.shift:
				shift_start_time = frappe.db.get_value('Shift Type', {'name': self.shift}, 'start_time')
				shift_end_time = frappe.db.get_value('Shift Type', {'name': self.shift}, 'end_time')
				shift_start_time = datetime.strptime(str(shift_start_time), '%H:%M:%S').time()
				shift_end_time = datetime.strptime(str(shift_end_time), '%H:%M:%S').time()
				if self.shift == '1':
					shift_start_datetime = datetime.combine(checkin_date, shift_start_time)
					shift_end_datetime = datetime.combine(checkin_date, shift_end_time)
					actual_shift_start_time = shift_start_datetime + timedelta(hours=-1)
					actual_shift_end_time = shift_end_datetime + timedelta(hours=1)
				elif self.shift == '3':
					checkin_date = add_days(checkin_date, 1)
					shift_start_datetime = datetime.combine(checkin_date, shift_start_time)
					shift_end_datetime = datetime.combine(checkin_date, shift_end_time)
					actual_shift_start_time = shift_start_datetime + timedelta(hours=-1)
					actual_shift_end_time = shift_end_datetime + timedelta(hours=1)
				elif self.shift == '2':
					checkin_date_2 = add_days(checkin_date, 1)
					shift_start_datetime = datetime.combine(checkin_date, shift_start_time)
					shift_end_datetime = datetime.combine(checkin_date_2, shift_end_time)
					actual_shift_start_time = shift_start_datetime + timedelta(hours=-1)
					actual_shift_end_time = shift_end_datetime + timedelta(hours=1)
					
				self.shift_start = shift_start_datetime
				self.shift_end = shift_end_datetime
				self.shift_actual_start = actual_shift_start_time
				self.shift_actual_end = actual_shift_end_time

		if isinstance(self.time, str):
			time_field = datetime.strptime(self.time, '%Y-%m-%d %H:%M:%S')
			checkin_date = time_field.date()
			checkin_time = time_field.time()
		check_shift_assignment = frappe.db.exists('Shift Assignment',{'employee':self.employee,'start_date':checkin_date,'docstatus':1})  
		if check_shift_assignment:
			get_shift = frappe.get_value('Shift Assignment',{'name':check_shift_assignment},['shift_type'])  
			self.assigned_shift = get_shift

	

				
class CustomLeaveApplication(LeaveApplication):   
	def notice_period_leave(self):
		employee = frappe.db.get_value('Employee',{'status':'Active','employee':self.employee},['resignation_letter_date'])
		if employee:
			if self.leave_type == 'Casual Leave' or self.leave_type == 'Earned Leave':
				frappe.throw(_('Employee %s %s cannot be availed during the Notice period'%(self.employee,self.leave_type)))
			else:
				message = ('Employee %s to check only Casual and Earned Leave'%(self.employee))
				frappe.log_error('Leave Applcation',message)      
		else:
			message = ('Employee %s has no Resignation Letter Date'%(self.employee))
			frappe.log_error('Notice Period Leave Apply',message) 
			
	def leave_type_validation(self):
		if self.employee:
			if self.leave_type == 'Maternity Leave':
				emp = frappe.db.get_value('Employee',{'status':'Active','name':self.employee},['gender'])
				if emp == 'Male':
					frappe.throw(_('%s type only allowed for female employees'%(self.leave_type)))
					
class CustomCompensatoryLeaveRequest(CompensatoryLeaveRequest):
	def before_save(self):
		self.validation_total_hours()
		avail_days = date_diff(self.posting_date,self.work_from_date)
		user_roles = frappe.get_roles(frappe.session.user)
		hr = "Miss Punch" in user_roles
		admin = "Administrator" in user_roles
		if avail_days > 90 and not hr:
			frappe.throw(_('%s Leave Request cannot be Applied After 90 Days'%(self.leave_type)))
		else:
			message = ('Leave Applied Less than 90 Days')
			frappe.log_error('%s Leave Type'%(self.leave_type),message)  

	def validation_total_hours(self):
		att = frappe.db.get_value('Attendance',{'employee':self.employee,'attendance_date':self.work_from_date,'docstatus':('!=','2')},['total_working_hours'])
		# if float(att) < 6.0:
		#     frappe.throw(_('Employee %s Working Hours Should be Greater than 6 Hours' %(self.employee)))
		# else:
		#     message = ('Employee %s Working Hours Greater than 6'%(self.employee)) 
		#     frappe.log_error('Compensatory Leave Request',message)  
	def after_insert(self):
		dates = get_dates(self.work_from_date ,self.work_end_date)
		total_working_hours=0.0
		# for date in dates:
		total_working_hours = frappe.db.get_value("Attendance", {'employee': self.employee, 'attendance_date': self.work_from_date, 'status': ['!=', 'Absent'], 'docstatus': 1}, ['total_working_hours'])
		if not total_working_hours:
			total_working_hours=0
		frappe.db.set_value('Compensatory Leave Request',self.name,'working_hours',total_working_hours)
		if total_working_hours<4:
			frappe.throw(_('Employee %s Working Hours Should be Greater than or equal to 4 Hours to apply C-OFF' %(self.employee)))
	def validate_attendance(self):
		attendance = frappe.get_all(
			"Attendance",
			filters={
				"attendance_date": ["between", (self.work_from_date, self.work_end_date)],
				"status": "Present",
				"docstatus": 1,
				"employee": self.employee,
			},
			fields=["attendance_date", "status"],
		)
		
		if len(attendance) < date_diff(self.work_end_date, self.work_from_date) + 1:
			frappe.throw(_("You are not present all day(s) between compensatory leave request days"))
		
	# def on_submit(self):
	#     leave=0
	#     end_date = add_days(self.work_from_date,30)  
	#     if self.working_hours>=4:
	#         if self.working_hours>=4 and self.working_hours<8:
	#             leave=0.5
	#         elif self.working_hours>=8 and self.working_hours<12:
	#             leave=1
	#         elif self.working_hours>=12 and self.working_hours<16:
	#             leave=1.5
	#         elif self.working_hours>=16 and self.working_hours<20:
	#             leave=2
	#         elif self.working_hours>=20 and self.working_hours<24:
	#             leave=2.5
	#         else:
	#             leave=3
	#         frappe.errprint(self.work_from_date)
	#         frappe.errprint(end_date)
	#         date_list = get_dates(self.work_from_date ,end_date)
	#         leave_allocation  = frappe.db.sql(
	#             """
	#             SELECT
	#                 name
	#             FROM `tabLeave Allocation`
	#             WHERE employee=%(employee)s AND leave_type='Compensatory Off'
	#                 AND docstatus=1
	#                 AND (from_date between %(from_date)s AND %(to_date)s
	#                     OR to_date between %(from_date)s AND %(to_date)s
	#                     OR (from_date < %(from_date)s AND to_date > %(to_date)s))
	#         """,
	#             {"from_date": self.work_from_date, "to_date": end_date, "employee": self.employee},
	#             as_dict=1,
	#         )
	#         if leave_allocation:   
	#             la_name = leave_allocation[0].get('name')
	#             la = frappe.get_doc('Leave Allocation',la_name)
	#             if la.to_date < end_date:
	#                 la.to_date=end_date
	#             if la.from_date > self.work_from_date:
	#                 date_difference = date_diff(self.work_from_date,la.from_date)
	#                 from_date =self.work_from_date
	#                 from_date = add_days(from_date,date_difference) 
	#                 la.from_date=from_date
	#             la.new_leaves_allocated+= leave
	#             la.save(ignore_permissions=True)
	#             frappe.db.commit()
	#             frappe.db.set_value('Compensatory Leave Request',self.name,'leave_allocation',la_name)
	#             frappe.db.set_value('Compensatory Leave Request',self.name,'allocated_leaves',leave)
	#         else:
	#             frappe.errprint('la')
	#             la=frappe.new_doc('Leave Allocation')
	#             la.employee=self.employee
	#             la.leave_type='Compensatory Off'
	#             la.from_date=self.work_from_date
	#             la.to_date=end_date
	#             la.new_leaves_allocated=leave
	#             la.save(ignore_permissions=True)
	#             frappe.db.commit()
	#             la.submit()
	#             frappe.db.set_value('Compensatory Leave Request',self.name,'leave_allocation',la.name)
	#         if la.name:
	#             alloc=frappe.db.get_all('Leave Ledger Entry',{'transaction_name':la.name},['from_date','to_date','name'])
	#             for a in alloc:
	#                 fdate=frappe.db.get_value("Leave Allocation",{"name":la.name},['from_date'])
	#                 tdate=frappe.db.get_value("Leave Allocation",{"name":la.name},['to_date'])
	#                 if a.from_date!=fdate:
	#                     frappe.db.set_value("Leave Ledger Entry",a.name,'from_date',fdate)
	#                 if a.to_date!=tdate:
	#                     frappe.db.set_value("Leave Ledger Entry",a.name,'from_date',tdate)

	#     else:
	#         frappe.throw(_('Employee %s Working Hours Should be Greater than or equal to 4 Hours to apply C-OFF' %(self.employee)))
	
	def on_cancel(self):
		if self.leave_allocation:
			date_difference = date_diff(self.work_end_date, self.work_from_date) + 1
			leave=0
			if self.working_hours>=4:
				if self.working_hours>=4 and self.working_hours<8:
					leave=0.5
				elif self.working_hours>=8 and self.working_hours<12:
					leave=1
				elif self.working_hours>=12 and self.working_hours<16:
					leave=1.5
				elif self.working_hours>=16 and self.working_hours<20:
					leave=2
				elif self.working_hours>=20 and self.working_hours<24:
					leave=2.5
				else:
					leave=3
			leave_allocation = frappe.get_doc("Leave Allocation", self.leave_allocation)
			if leave_allocation:
				leave_allocation.new_leaves_allocated -= leave
				if leave_allocation.new_leaves_allocated - date_difference <= 0:
					leave_allocation.new_leaves_allocated = 0
				leave_allocation.validate()
				leave_allocation.db_set("new_leaves_allocated", leave_allocation.total_leaves_allocated)
				leave_allocation.db_set("total_leaves_allocated", leave_allocation.total_leaves_allocated)
				create_additional_leave_ledger_entry(
					leave_allocation, -1 *leave, add_days(self.work_end_date, 1)
				)
	# def on_cancel(self):	
	#     if self.leave_allocation:
	#         leave_allocation = self.leave_allocation
	#         # frappe.db.set_value("Compensatory Leave Request",self.name,'leave_allocation','')
	#         la=frappe.get_doc('Leave Allocation',leave_allocation)
	#         frappe.errprint(self.leave_allocation)
	#         frappe.errprint(la)
	#         if self.created_via:
	#             if frappe.db.exists('Attendance',{'name':self.created_via}):
	#                 frappe.db.set_value("Attendance",self.created_via,'coff_updated',0)
	#                 la.cancel()
			# frappe.db.set_value("Leave Allocation",{'name':self.name},'compensatory_request','')
			
class CustomLeaveAllocation(LeaveAllocation):
	def before_save(self):
		if self.employee:
			if self.leave_type == 'Maternity Leave':
				emp = frappe.db.get_value('Employee', {'status': 'Active', 'name': self.employee}, ['gender'])
				if emp == 'Male':
					frappe.throw(_('%s type only allowed for female employees' % (self.leave_type)))

class CustomEmployee(Employee):
	def before_save(self):
		frappe.errprint('self')
		# if self.grade != 'G-1':
		#     if self.ctc_amount:
		#         spl_allow = self.basic + self.house_rent_allowance + self.conveyance_allowance + self.education_allowance + self.food_allowance + self.attire_allowance + self.mobile_allowance + self.medical_allowance 
		#         overall_amount = spl_allow + self.pf_amount
		#         self.special_allowance = self.ctc_amount - overall_amount
		#         self.fixed_earning = spl_allow + self.special_allowance


@frappe.whitelist()
def get_dates(from_date ,to_date):
	no_of_days = date_diff(add_days(to_date, 1), from_date)
	dates = [add_days(from_date, i) for i in range(0, no_of_days)]
	return dates

@frappe.whitelist()
def check_holiday(date, emp):
		holiday_list = frappe.db.get_value('Employee', emp, 'holiday_list')
		
		query = """
			SELECT `tabHoliday`.holiday_date, `tabHoliday`.weekly_off
			FROM `tabHoliday List`
			LEFT JOIN `tabHoliday` ON `tabHoliday`.parent = `tabHoliday List`.name
			WHERE `tabHoliday List`.name = %s AND holiday_date = %s
		"""
		holiday = frappe.db.sql(query, (holiday_list, date), as_dict=True)
		if holiday:
			if holiday[0].weekly_off == 1:
				return "WW"
			else:
				return "HH"
		return None

def check_holiday_hh(date, emp):
	# Get the holiday list for the employee
	holiday_list = frappe.db.get_value('Employee', emp, 'holiday_list')
	
	# Parameterized query to prevent SQL injection and ensure proper handling of input values
	query = """
		SELECT `tabHoliday`.holiday_date, `tabHoliday`.weekly_off
		FROM `tabHoliday List`
		LEFT JOIN `tabHoliday` ON `tabHoliday`.parent = `tabHoliday List`.name
		WHERE `tabHoliday List`.name = %s AND holiday_date = %s
	"""
	holiday = frappe.db.sql(query, (holiday_list, date), as_dict=True)
	if holiday:
		if holiday[0].weekly_off == 1:
			return "WW"
		elif holiday[0].holiday_type == "FH":
			return "FH"
		elif holiday[0].holiday_type == "NH":
			return "NH"
		else:
			return "HH"
	return None

class CustomShiftRequest(ShiftRequest):
    
    def validate(self):
        from_date = getdate(self.from_date)
        today_date = getdate(today())
        tomorrow_date = add_days(today_date, 1)
        user = frappe.session.user
        roles = frappe.get_roles(user)
        if "Miss Punch" not in roles:
            if from_date > tomorrow_date:
             frappe.throw("The Shift Request should be raised within one day from the worked date.")
    def on_submit(self):
        employee = self.employee
        shift_type = self.shift_type
        from_date = getdate(self.from_date)
        to_date = getdate(self.to_date)

        existing_assignments = frappe.get_all(
            "Shift Assignment",
            filters={
                "employee": employee,
                "start_date": ["<=", to_date],
                "end_date": [">=", from_date],
            },
            fields=["name", "shift_type", "docstatus"]
        )

        for assignment in existing_assignments:
            existing_doc = frappe.get_doc("Shift Assignment", assignment.name)
            
            if existing_doc.shift_type == shift_type and existing_doc.docstatus == 1:
                frappe.throw(f"Shift Assignment already exists for {employee} with shift '{shift_type}' in the selected period.")
            
            if existing_doc.docstatus == 1:
                existing_doc.cancel()

        new_assignment = frappe.get_doc({
            "doctype": "Shift Assignment",
            "employee": employee,
            "shift_type": shift_type,
            "start_date": from_date,
            "end_date": to_date,
            "company": self.company,
            "shift_request": self.name  
        })
        new_assignment.insert(ignore_permissions=True)
        new_assignment.submit()  

        frappe.msgprint(f"Shift Assignment created ")

	
 
    def on_cancel(self):
        linked_assignments = frappe.get_all(
            "Shift Assignment",
            filters={"shift_request": self.name, "docstatus": 1},
            fields=["name"]
        )

        for assignment in linked_assignments:
            frappe.get_doc("Shift Assignment", assignment.name).cancel()
