# Copyright (c) 2025, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_days, cint, date_diff, format_date, getdate
from frappe.utils.data import get_last_day
from hrms.hr.utils import get_holiday_dates_for_employee, create_additional_leave_ledger_entry
from datetime import date, timedelta,time
from datetime import datetime
from frappe.utils import today
class EmployeeBenefitsRegularization(Document):
    
    
    
    def validate(self):
        if self.is_new():
            user_roles = frappe.get_roles(frappe.session.user)
            hr = "Miss Punch" in user_roles
            admin = "Administrator" in user_roles
            if (not hr):
                allowed_days = 3
                current_date = today()
                if isinstance(current_date, str):
                    current_date = datetime.strptime(current_date, "%Y-%m-%d").date()
                earliest_allowed = add_days(current_date, -3)
                if isinstance(self.date, str):
                    miss_date = datetime.strptime(self.date, "%Y-%m-%d").date()
                else:
                    miss_date = self.date
                    
                if miss_date < earliest_allowed:
                    frappe.throw(
                        _("Employee Benefits Regularization are allowed only for up to the previous {0} working days.")
                        .format(allowed_days)
                        )   
        if self.employee and self.date:
            if isinstance(self.date, str):
                format_date = datetime.strptime(self.date, "%Y-%m-%d")  # Assuming the date format is 'YYYY-MM-DD'
                format_date=format_date.strftime('%d-%m-%Y')
            if frappe.db.exists('Employee Benefits Regularization',{'employee':self.employee,'date':self.date,'name':['!=',self.name],'docstatus':['!=',2]}):
                # frappe.throw(f"Employee Benefits Regularization already exists for Employee {self.employee} on {self.date.strftime('%d-%m-%Y')}.")
                frappe.throw(f"Employee Benefits Regularization already exists for Employee {self.employee} on {format_date}.")
            if frappe.db.exists('Overtime List',{'employee':self.employee,'ot_from_date':self.date,'docstatus':1}):
                permitted_overtime_hours =frappe.db.get_value('Overtime List',{'employee':self.employee,'ot_from_date':self.date,'docstatus':1},['permitted_overtime_hours'])
                ot_from_attendance =frappe.db.get_value('Overtime List',{'employee':self.employee,'ot_from_date':self.date,'docstatus':1},['ot_from_attendance'])
                if permitted_overtime_hours and ot_from_attendance:
                    ot_hours = ot_from_attendance - permitted_overtime_hours
                    working_hours = self.working_hours
                    self.working_hours =ot_hours  
                    if self.provision == "C-OFF": 
                        if (ot_hours - self.working_hours) < 4:
                            frappe.throw('Already used the OT Hours via Overtime List')
                        else:
                            self.leaves =get_leave_count(self.working_hours)
                    elif self.provision == "OT":  
                        self.ot_amount =get_ot_amount(self.employee,self.date,self.working_hours)               
            if self.provision == "C-OFF":
                if not self.working_hours or self.working_hours < 4:
                    frappe.throw(f"Employee {self.employee} must have at least 4 working hours to apply for C-OFF.")
            elif self.provision == "OT":
                if self.working_hours <= 0:  
                    frappe.throw(f"Employee {self.employee} must have working hours greater than 0 to apply for OT.")
            approved_leaves  = frappe.db.sql("""
                select name
                from `tabCompensatory Leave Request`
                where workflow_state="Approved" and docstatus =1 and employee = %(employee)s
                    and (work_from_date between %(work_from_date)s and %(work_end_date)s
                        or work_end_date between %(work_from_date)s and %(work_end_date)s
                        or (work_from_date < %(work_from_date)s and work_end_date > %(work_end_date)s))
                """, {
                    "work_from_date": self.date,
                    "work_end_date": self.date,
                    "employee":self.employee
                },as_dict = True)
            if approved_leaves:
                frappe.throw(f"Compensatory Leave Request already exists for Employee {self.employee} on {self.date.strftime('%d-%m-%Y')}.")
    def on_submit(self):
        if self.provision == 'C-OFF':
            leave=self.leaves
            end_date = add_days(self.date,90)  
            if self.working_hours>=4:
            #     if self.working_hours>=4 and self.working_hours<8:
            #         leave=0.5
            #     elif self.working_hours>=8 and self.working_hours<12:
            #         leave=1
            #     elif self.working_hours>=12 and self.working_hours<16:
            #         leave=1.5
            #     elif self.working_hours>=16 and self.working_hours<20:
            #         leave=2
            #     elif self.working_hours>=20 and self.working_hours<24:
            #         leave=2.5
            #     else:
            #         leave=3
                date_list = get_dates(self.date ,end_date)
                leave_allocation  = frappe.db.sql(
                    """
                    SELECT
                        name
                    FROM `tabLeave Allocation`
                    WHERE employee=%(employee)s AND leave_type='Compensatory Off'
                        AND docstatus=1
                        AND (from_date between %(from_date)s AND %(to_date)s
                            OR to_date between %(from_date)s AND %(to_date)s
                            OR (from_date < %(from_date)s AND to_date > %(to_date)s))
                """,
                    {"from_date": self.date, "to_date": end_date, "employee": self.employee},
                    as_dict=1,
                )
                if leave_allocation:   
                    la_name = leave_allocation[0].get('name')
                    la=frappe.get_doc('Leave Allocation',la_name)
                    if la.to_date < getdate(end_date):
                        la.to_date=end_date
                    # if la.from_date > getdate(self.date):
                        # date_difference = date_diff(self.date,la.from_date)
                        # from_date =la.from_date
                        # from_date = add_days(from_date,date_difference) 
                        # la.from_date=from_date
                    la.new_leaves_allocated+= leave
                    la.save(ignore_permissions=True)
                    frappe.db.commit()
                    frappe.db.set_value('Employee Benefits Regularization',self.name,'leave_allocation',la_name)
                else:
                    la=frappe.new_doc('Leave Allocation')
                    la.employee=self.employee
                    la.leave_type='Compensatory Off'
                    la.from_date=self.date
                    la.to_date=end_date
                    la.new_leaves_allocated=leave
                    la.save(ignore_permissions=True)
                    frappe.db.commit()
                    la.submit()
                    frappe.db.set_value('Employee Benefits Regularization',self.name,'leave_allocation',la.name)
                    # frappe.db.set_value('Employee Benefits Regularization',self.name,'leaves',leave)
        # if self.provision == 'OT':
        # 	frappe.errprint('frappe')
        # 	fixed_earning=frappe.db.get_value("Employee",{'name':self.employee},['fixed_earning']) or 0
        # 	now_date= getdate(self.date)
        # 	if now_date.day >= 21:
        # 		ot_from_date = now_date.replace(month=now_date.month, day=21)
        # 	else:
        # 		if now_date.month == 1: 
        # 			ot_from_date = now_date.replace(year=now_date.year - 1, month=12, day=21)
        # 		else:
        # 			ot_from_date = now_date.replace(month=now_date.month - 1, day=21)
        # 	ot_to_date = now_date.replace(month=now_date.month, day=20)
        # 	if now_date.day > 20:
        # 		ot_to_date = (ot_to_date + timedelta(days=31)).replace(day=20)
        # 	total_working_days = date_diff(ot_to_date, ot_from_date) + 1
        # 	ot_amount = (((fixed_earning/total_working_days)/8)*2)*self.working_hours
        # 	frappe.errprint(ot_amount)
        # 	frappe.db.set_value('Employee Benefits Regularization',self.name,'ot_amount',round(ot_amount))
        # 	frappe.db.set_value('Employee Benefits Regularization',self.name,'leaves',0)
        # 	frappe.errprint('ot_amount')


    def on_cancel(self):
        if self.leave_allocation:
            if self.leave_allocation:
                la=frappe.get_doc('Leave Allocation',self.leave_allocation)
                total_leaves_allocated = la.new_leaves_allocated -self.leaves
                # if la.from_date > getdate(self.date):
                    # date_difference = date_diff(self.date,la.from_date)
                    # from_date =la.from_date
                    # from_date = add_days(from_date,date_difference) 
                    # la.from_date=from_date
                la.new_leaves_allocated = total_leaves_allocated
                la.total_leaves_allocated = total_leaves_allocated
                la.save(ignore_permissions=True)
                frappe.db.commit()
                # total_leaves_allocated = frappe.db.get_value("Leave Allocation", self.leave_allocation,['total_leaves_allocated'])
                
                # frappe.db.set_value('Leave Allocation',{'name':self.leave_allocation,'docstatus':['!=',2]},"new_leaves_allocated", total_leaves_allocated)
                # frappe.db.set_value('Leave Allocation',{'name':self.leave_allocation,'docstatus':['!=',2]},"total_leaves_allocated", total_leaves_allocated)

        # if self.additional_salary:
        #     additional_salary = frappe.get_doc("Additional Salary", self.additional_salary)
        #     if additional_salary:
        #         if additional_salary.docstatus != 2:
        #             additional_salary.amount -= self.ot_amount
        #             additional_salary.save(ignore_permissions=True)
        #             frappe.db.commit()


@frappe.whitelist()
def get_dates(from_date ,to_date):
    no_of_days = date_diff(add_days(to_date, 1), from_date)
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]
    return dates

@frappe.whitelist()
def get_att_data(employee,date):
    att = frappe.db.get_value(
        "Attendance", 
        {"employee": employee, "attendance_date": date, "docstatus": ["!=", 2]}, 
        ["total_working_hours", "shift", "over_time_hours","out_time","in_time"], 
        as_dict=True
    )
    if att:
        working_hours = att.get("total_working_hours", 0)
        ot_hours = att.get("over_time_hours", 0)
        holidays = get_holiday_dates_for_employee(employee, date, date)
        if holidays:
            working_hours = working_hours  
        else:
            working_hours = ot_hours     
        return {
            'total_working_hours': working_hours,
            'shift': att.get('shift'),
            'in_time':att.get('in_time'),
            'out_time': att.get('out_time'),
        }
    else:
        frappe.throw(_('No attendance record found for the specified employee and date.'))

@frappe.whitelist()
def get_leave_count(working_hours):
    leave=0
    if float(working_hours)>=4:
        if float(working_hours)>=4 and float(working_hours)<8:
            leave=0.5
        elif float(working_hours)>=8 and float(working_hours)<12:
            leave=1
        elif float(working_hours)>=12 and float(working_hours)<16:
            leave=1.5
        elif float(working_hours)>=16 and float(working_hours)<20:
            leave=2
        elif float(working_hours)>=20 and float(working_hours)<24:
            leave=2.5
        else:
            leave=3
    return leave

@frappe.whitelist()
def get_ot_amount(employee,date,working_hours):
    ot_amount=0
    # frappe.errprint('frappe')
    fixed_earning=frappe.db.get_value("Employee",{'name':employee},['fixed_earning']) or 0
    fixed_earning = float(fixed_earning) 
    working_hours = float(working_hours)
    now_date= getdate(date)
    if now_date.day >= 21:
        ot_from_date = now_date.replace(month=now_date.month, day=21)
    else:
        if now_date.month == 1: 
            ot_from_date = now_date.replace(year=now_date.year - 1, month=12, day=21)
        else:
            ot_from_date = now_date.replace(month=now_date.month - 1, day=21)
    ot_to_date = now_date.replace(month=now_date.month, day=20)
    if now_date.day > 20:
        ot_to_date = (ot_to_date + timedelta(days=31)).replace(day=20)
    total_working_days = date_diff(ot_to_date, ot_from_date) + 1
    ot_amount = (((fixed_earning/total_working_days)/8)*2)*working_hours
    return ot_amount

@frappe.whitelist()
def create_additional_salary(from_date,to_date):
    now_date= getdate(from_date)
    if now_date.day >= 21:
        ot_from_date = now_date.replace(month=now_date.month, day=21)
    else:
        if now_date.month == 1: 
            ot_from_date = now_date.replace(year=now_date.year - 1, month=12, day=21)
        else:
            ot_from_date = now_date.replace(month=now_date.month - 1, day=21)
    ot_to_date = now_date.replace(month=now_date.month, day=20)
    if now_date.day > 20:
        ot_to_date = (ot_to_date + timedelta(days=31)).replace(day=20)
    total_working_days = date_diff(ot_to_date, ot_from_date) + 1
    payroll_date = ot_to_date
    employee_query = """
    SELECT name,company
    FROM tabEmployee
    WHERE
        status = 'Active'  """
    employee = frappe.db.sql(employee_query, as_dict=True)
    for emp in employee:
        ot_amount = frappe.db.sql(
            """
            SELECT
                SUM(ot_amount) as monthly_ot,currency
            FROM `tabEmployee Benefits Regularization`
            WHERE
                employee=%s
                AND docstatus=1 AND provision ='OT'
                AND date  BETWEEN %s AND %s""",
            (emp.name, ot_from_date, ot_to_date),as_dict=True
        )
        if ot_amount and ot_amount[0]["monthly_ot"] is not None:
            if not frappe.db.exists('Additional Salary', {'employee': emp.name, 'payroll_date': payroll_date, 'salary_component': "Overtime", 'docstatus': ('!=', 2)}):
                additional_salary = frappe.new_doc("Additional Salary")
                additional_salary.company = emp.company
                additional_salary.employee = emp.name
                additional_salary.currency = ot_amount[0]["currency"]
                additional_salary.salary_component = 'Overtime'
                additional_salary.payroll_date = payroll_date
                additional_salary.amount = ot_amount[0]["monthly_ot"]
                additional_salary.submit()

        

@frappe.whitelist()
def update_approval_role(workflow_state,name):
    if workflow_state == 'HOD Pending':
        frappe.db.set_value('Employee Benefits Regularization',{'name':name}, 'approver_role', 'HOD')
    elif workflow_state == 'TL Pending':
        frappe.db.set_value('Employee Benefits Regularization',{'name':name}, 'approver_role', 'TL')
    elif workflow_state == 'HR Pending':
        frappe.db.set_value('Employee Benefits Regularization',{'name':name}, 'approver_role', 'HR Manager')
    elif workflow_state == 'Director Pending':
        frappe.db.set_value('Employee Benefits Regularization',{'name':name}, 'approver_role', 'Director')
    elif workflow_state == 'MD Pending':
        frappe.db.set_value('Employee Benefits Regularization',{'name':name}, 'approver_role', 'MD')
    elif workflow_state in ['Approved', 'Rejected']:
        frappe.db.set_value('Employee Benefits Regularization',{'name':name}, 'approved_by', frappe.session.user)
    return "ok"    
    
    
    
       
