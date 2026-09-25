# -*- coding: utf-8 -*-
# Copyright (c) 2018, VHRS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from ast import Gt
from email import message
import frappe
from frappe.model.document import Document
from datetime import datetime,timedelta,date
from frappe import _
import time

from frappe.utils import today,flt,add_days,date_diff,getdate,cint,formatdate, getdate, get_link_to_form, \
    comma_or, get_fullname
from frappe.utils import get_first_day, get_last_day, format_datetime,get_url_to_form
from datetime import datetime, time, timedelta
from johoku.mark_attendance import mark_att_with_employee
from johoku.mark_attendance import check_holiday


class LeaveApproverIdentityError(frappe.ValidationError): pass
class OverlapError(frappe.ValidationError): pass
class AttendanceAlreadyMarkedError(frappe.ValidationError): pass    

class OnDutyApplication(Document):
    
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
                if isinstance(self.to_date, str):
                    miss_date = datetime.strptime(self.to_date, "%Y-%m-%d").date()
                else:
                    miss_date = self.to_date

                if miss_date < earliest_allowed:
                    frappe.throw(
                    _("On Duty applications are allowed only for up to the previous {0} working days.")
                    .format(allowed_days)
                    )
    # def on_submit(self):
    #     # frappe.db.set_value('On Duty Application',self.name,'approver',frappe.session.user)
    #     # frappe.errprint('Welcome to On Submit')
    #     if self.status == "Applied":
    #         frappe.throw(_("Only Applications with status 'Approved' and 'Rejected' can be submitted"))
        
    #     if self.workflow_state == "Approved":
    #         no_of_days = date_diff(add_days(self.to_date, 1),self.od_date )
    #         dates = [add_days(self.od_date, i) for i in range(0, no_of_days)]
    #         for emp in self.multi_employee:
    #             for date in dates:
    #                 att = frappe.db.exists("Attendance",{"attendance_date":date,"employee":emp.employee,"docstatus":["!=",2]})
    #                 if att:
    #                     doc = frappe.get_doc("Attendance",att)
    #                     if doc.docstatus == 0:
    #                         doc.shift = self.shift
    #                         doc.attended_shift = self.shift
    #                         doc.on_duty_application = self.name
    #                         doc.session_from_time = self.from_time
    #                         if self.session != 'Hourly':
    #                             doc.session_to_time = self.to_time
    #                         else:
    #                             doc.session_to_time = self.to
    #                         doc.save(ignore_permissions=True)
    #                         # doc.submit()
    #                         frappe.db.commit()
    #                     elif doc.docstatus == 1:
    #                         doc.shift = self.shift
    #                         doc.attended_shift = self.shift
    #                         doc.on_duty_application = self.name
    #                         doc.session_from_time = self.from_time
    #                         if self.session != 'Hourly':
    #                             doc.session_to_time = self.to_time
    #                         else:
    #                             doc.session_to_time = self.to
    #                         doc.save(ignore_permissions=True)
    #                         # doc.submit()
    #                         frappe.db.commit()
    #                     if self.shift == '1':
    #                         mark_att_with_employee(date,date,self.employee)
    #                     else:
    #                         to_date = add_days(date,1)
    #                         mark_att_with_employee(date,to_date,self.employee)
        
    #                 else:
                        
    #                     doc = frappe.new_doc("Attendance")
    #                     doc.employee = emp.employee
    #                     doc.attendance_date = date
    #                     if self.session == "Full Day":
    #                         doc.status = "Present"
    #                     elif self.session == "First Half" or self.session == "Second Half":     
    #                         doc.status = "Half Day"
    #                     else:
    #                         doc.status = "Absent"
    #                     doc.shift = self.shift
    #                     doc.attended_shift = self.shift
    #                     doc.on_duty_application = self.name
    #                     doc.session_from_time = self.from_time
    #                     if self.session != 'Hourly':
    #                         doc.session_to_time = self.to_time
    #                     else:
    #                         doc.session_to_time = self.to
    #                     doc.save(ignore_permissions=True)
    #                     # doc.submit()
    #                     frappe.db.commit()
    #                     if self.shift == '1':
    #                         mark_att_with_employee(date,date,self.employee)
    #                     else:
    #                         to_date = add_days(date,1)
    #                         mark_att_with_employee(date,to_date,self.employee)
        
    #             hh = check_holiday(self.od_date, self.employee)
    #             if hh:
    #                 self.is_holiday = 1
    #             else:
    #                 self.is_holiday = 0    
    
    def on_submit(self):

        if self.status == "Applied":
            frappe.throw(_("Only Applications with status 'Approved' and 'Rejected' can be submitted"))

        if self.workflow_state == "Approved":

            no_of_days = date_diff(add_days(self.to_date, 1), self.od_date)
            dates = [add_days(self.od_date, i) for i in range(0, no_of_days)]

            for emp in self.multi_employee:
                for date in dates:

                    att = frappe.db.exists("Attendance", {
                        "attendance_date": date,
                        "employee": emp.employee,
                        "docstatus": ["!=", 2]
                    })

                    if att:
                        doc = frappe.get_doc("Attendance", att)

                        # Update existing attendance
                        doc.shift = self.shift
                        doc.attended_shift = self.shift
                        doc.on_duty_application = self.name
                        doc.session_from_time = self.from_time

                        if self.session != 'Hourly':
                            doc.session_to_time = self.to_time
                        else:
                            doc.session_to_time = self.to

                        doc.save(ignore_permissions=True)

                    else:
                        # Create new attendance
                        doc = frappe.new_doc("Attendance")
                        doc.employee = emp.employee
                        doc.attendance_date = date

                        if self.session == "Full Day":
                            doc.status = "Present"
                        elif self.session in ["First Half", "Second Half"]:
                            doc.status = "Half Day"
                        else:
                            doc.status = "Absent"

                        doc.shift = self.shift
                        doc.attended_shift = self.shift
                        doc.on_duty_application = self.name
                        doc.session_from_time = self.from_time

                        if self.session != 'Hourly':
                            doc.session_to_time = self.to_time
                        else:
                            doc.session_to_time = self.to

                        doc.save(ignore_permissions=True)

                    # Mark attendance
                    if self.shift == '1':
                        mark_att_with_employee(date, date, emp.employee)
                    else:
                        to_date = add_days(date, 1)
                        mark_att_with_employee(date, to_date, emp.employee)

            # Holiday Check & Comp Off Creation
            first_emp = self.multi_employee[0].employee if self.multi_employee else None
            hh = check_holiday(self.od_date, first_emp) if first_emp else False

            if hh:
                # self.is_holiday = 1

                created = False

                for emp in self.multi_employee:
                    exists = frappe.db.exists("Employee Benefits Regularization", {
                        "reference_name": self.name,
                        "employee": emp.employee
                    })

                    if not exists:
                        comp_doc = frappe.new_doc("Employee Benefits Regularization")
                        comp_doc.employee = emp.employee
                        comp_doc.date = self.od_date
                        comp_doc.shift = self.shift
                        comp_doc.from_on_duty = 1
                        comp_doc.reference_doctype = self.name
                        # comp_doc.from_time = self.from_time
                        # comp_doc.to_time = self.to_time
                        comp_doc.working_hours = self.total_od_hours
                        comp_doc.provision = 'C-OFF'
                        if self.session == "Full Day":
                            comp_doc.leaves = 1
                        else:
                            comp_doc.leaves = 0.5
                        comp_doc.insert(ignore_permissions=True)
                        # comp_doc.submit()  
                        created = True

                # if created:
                #     frappe.msgprint("Employee Benefits Regularization created")

           
        # if self.workflow_state == "Approved":
        # 	frappe.errprint(self.from_time)
        # 	frappe.errprint(self.to_time)
        # 	if isinstance(self.from_time, str):
        # 		frappe.errprint("A")
        # 		start_time = datetime.strptime(self.from_time, "%H:%M:%S").time() 
        # 	elif isinstance(self.from_time, timedelta):
        # 		frappe.errprint("B")
        # 		start_time = (datetime.min + self.from_time).time()
        # 	else:
        # 		frappe.errprint("C")
        # 		start_time = self.from_time 
        # 	if isinstance(self.to_time, str):
        # 		frappe.errprint("D")
        # 		end_time = datetime.strptime(self.to_time, "%H:%M:%S").time()  
        # 	elif isinstance(self.to_time, timedelta):
        # 		frappe.errprint("E")
        # 		end_time = (datetime.min + self.to_time).time()
        # 	else:
        # 		end_time = self.to_time  
        # 		frappe.errprint("F")
        # 	if isinstance(start_time, time) and isinstance(end_time, time):
        # 		time_difference = datetime.combine(datetime.today(), end_time) - datetime.combine(datetime.today(), start_time)
        # 		frappe.errprint(f"Time difference: {time_difference}")
        # 		frappe.errprint(time_difference)
        # 		total_seconds = time_difference.total_seconds()
        # 		formatted_total_hours =round((total_seconds/3600),1)
        # 		no_of_days = date_diff(add_days(self.to_date, 1),self.od_date )
        # 		dates = [add_days(self.od_date, i) for i in range(0, no_of_days)]
        # 		for emp in self.multi_employee:
        # 			for date in dates:
        # 				att = frappe.db.exists("Attendance",{"attendance_date":date,"employee":emp.employee,"docstatus":["!=","2"]})
        # 				if att:
        # 					doc = frappe.get_doc("Attendance",att)
        # 					if doc.docstatus == 0:
        # 						if self.session == "Full Day":
        # 							frappe.errprint("Full day")
        # 							if doc.total_working_hours:
        # 								total_working_hours = doc.total_working_hours 
        # 								total_working_hours += formatted_total_hours
        # 							else:
        # 								total_working_hours = formatted_total_hours
        # 							doc.status = "Present"
        # 						if self.session == "First Half":
        # 							if doc.total_working_hours:
        # 								total_working_hours = doc.total_working_hours 
        # 								total_working_hours += formatted_total_hours
        # 							else:
        # 								total_working_hours = formatted_total_hours
        # 							total_working_hours = float(total_working_hours)
        # 							if total_working_hours >= 8:
        # 								doc.status = "Present"
        # 							elif 4 <= total_working_hours <8:
        # 								doc.status = "Half Day"
        # 							else:
        # 								doc.status = "Absent"
        # 						if self.session == "Second Half":
        # 							if doc.total_working_hours:
        # 								total_working_hours = doc.total_working_hours 
        # 								total_working_hours += formatted_total_hours
        # 							else:
        # 								total_working_hours = formatted_total_hours
        # 							total_working_hours = float(total_working_hours)
        # 							if total_working_hours >= 8:
        # 								doc.status = "Present"
        # 							elif 4 <= total_working_hours <8:
        # 								doc.status = "Half Day"
        # 							else:
        # 								doc.status = "Absent"
        # 						if self.session == "Hourly":
        # 							if self.total_hourly == '1 Hour':
        # 								if doc.total_working_hours:
        # 									total_working_hours = doc.total_working_hours 
        # 									total_working_hours += 1
        # 								else:
        # 									total_working_hours = 1
        # 								total_working_hours = float(total_working_hours)
        # 								if total_working_hours >= 8:
        # 									doc.status = "Present"
        # 								elif 4 <= total_working_hours <8:
        # 									doc.status = "Half Day"
        # 								else:
        # 									doc.status = "Absent"
        # 							elif self.total_hourly == '2 Hours':	
        # 								if doc.total_working_hours:
        # 									total_working_hours = doc.total_working_hours 
        # 									total_working_hours += 2
        # 								else:
        # 									total_working_hours = 2
        # 								total_working_hours = float(total_working_hours)
        # 							elif self.total_hourly == '3 Hours':
        # 								if doc.total_working_hours:
        # 									total_working_hours = doc.total_working_hours 
        # 									total_working_hours += 3
        # 								else:
        # 									total_working_hours = 3
        # 								total_working_hours = float(total_working_hours)
        # 							elif self.total_hourly == '4 Hours':
        # 								if doc.total_working_hours:
        # 									total_working_hours = doc.total_working_hours 
        # 									total_working_hours += 4
        # 								else:
        # 									total_working_hours = 4
        # 								total_working_hours = float(total_working_hours)
        # 							if total_working_hours >= 8:
        # 								doc.status = "Present"
        # 							elif 4 <= total_working_hours <8:
        # 								doc.status = "Half Day"
        # 							else:
        # 								doc.status = "Absent"
        # 						doc.shift = self.shift
        # 						doc.on_duty_application = self.name
        # 						doc.session_from_time = self.from_time
        # 						doc.session_to_time = self.to_time
        # 						doc.save(ignore_permissions=True)
        # 						doc.submit()
        # 						frappe.db.commit()
        # 					elif doc.docstatus == 1:
        # 						if self.session == "Full Day":
        # 							frappe.errprint("Full day")
        # 							if doc.total_working_hours:
        # 								total_working_hours = doc.total_working_hours 
        # 								total_working_hours += formatted_total_hours
        # 							else:
        # 								total_working_hours = formatted_total_hours
        # 							doc.status = "Present"
        # 						if self.session == "First Half":
        # 							if doc.total_working_hours:
        # 								total_working_hours = doc.total_working_hours 
        # 								total_working_hours += formatted_total_hours
        # 							else:
        # 								total_working_hours = formatted_total_hours
        # 							total_working_hours = float(total_working_hours)
        # 							if total_working_hours >= 8:
        # 								doc.status = "Present"
        # 							elif 4 <= total_working_hours <8:
        # 								doc.status = "Half Day"
        # 							else:
        # 								doc.status = "Absent"
        # 						if self.session == "Second Half":
        # 							if doc.total_working_hours:
        # 								total_working_hours = doc.total_working_hours 
        # 								total_working_hours += formatted_total_hours
        # 							else:
        # 								total_working_hours = formatted_total_hours
        # 							total_working_hours = float(total_working_hours)
        # 							if total_working_hours >= 8:
        # 								doc.status = "Present"
        # 							elif 4 <= total_working_hours <8:
        # 								doc.status = "Half Day"
        # 							else:
        # 								doc.status = "Absent"
        # 						if self.session == "Hourly":
        # 							if self.total_hourly == '1 Hour':
        # 								if doc.total_working_hours:
        # 									total_working_hours = doc.total_working_hours 
        # 									total_working_hours += 1
        # 								else:
        # 									total_working_hours = 1
        # 								total_working_hours = float(total_working_hours)
        # 								if total_working_hours >= 8:
        # 									doc.status = "Present"
        # 								elif 4 <= total_working_hours <8:
        # 									doc.status = "Half Day"
        # 								else:
        # 									doc.status = "Absent"
        # 							elif self.total_hourly == '2 Hours':	
        # 								if doc.total_working_hours:
        # 									total_working_hours = doc.total_working_hours 
        # 									total_working_hours += 2
        # 								else:
        # 									total_working_hours = 2
        # 								total_working_hours = float(total_working_hours)
        # 							elif self.total_hourly == '3 Hours':
        # 								if doc.total_working_hours:
        # 									total_working_hours = doc.total_working_hours 
        # 									total_working_hours += 3
        # 								else:
        # 									total_working_hours = 3
        # 								total_working_hours = float(total_working_hours)
        # 							elif self.total_hourly == '4 Hours':
        # 								if doc.total_working_hours:
        # 									total_working_hours = doc.total_working_hours 
        # 									total_working_hours += 4
        # 								else:
        # 									total_working_hours = 4
        # 								total_working_hours = float(total_working_hours)
        # 							if total_working_hours >= 8:
        # 								doc.status = "Present"
        # 							elif 4 <= total_working_hours <8:
        # 								doc.status = "Half Day"
        # 							else:
        # 								doc.status = "Absent"
        # 						# doc.cancel()
        # 						frappe.db.set_value("Attendance",doc.name,'status',doc.status)
        # 						frappe.db.set_value("Attendance",doc.name,'shift',self.shift)
        # 						frappe.db.set_value("Attendance",doc.name,'on_duty_application',self.name)
        # 						frappe.db.set_value("Attendance",doc.name,'session_from_time',self.from_time)
        # 						frappe.db.set_value("Attendance",doc.name,'session_to_time',self.to_time)
        # 						# doc = frappe.new_doc("Attendance")
        # 						# doc.employee = emp.employee
        # 						# doc.attendance_date = date
        # 						# doc.status = 'Present'
        # 						# doc.shift = self.shift
        # 						# doc.on_duty_application = self.name
        # 						# doc.save(ignore_permissions=True)
        # 						# doc.submit()
        # 						# frappe.db.commit()
        # 				else: 
        # 					doc = frappe.new_doc("Attendance")
        # 					doc.employee = emp.employee
        # 					doc.attendance_date = date
        # 					if self.session == "Full Day":
        # 						frappe.errprint("Full day")
        # 						if doc.total_working_hours:
        # 							total_working_hours = doc.total_working_hours 
        # 							total_working_hours += formatted_total_hours
        # 						else:
        # 							total_working_hours = formatted_total_hours
        # 						doc.status = "Present"
        # 					if self.session == "First Half":
        # 						if doc.total_working_hours:
        # 							total_working_hours = doc.total_working_hours 
        # 							total_working_hours += formatted_total_hours
        # 						else:
        # 							total_working_hours = formatted_total_hours
        # 						total_working_hours = float(total_working_hours)
        # 						if total_working_hours >= 8:
        # 							doc.status = "Present"
        # 						elif 4 <= total_working_hours <8:
        # 							doc.status = "Half Day"
        # 						else:
        # 							doc.status = "Absent"
        # 					if self.session == "Second Half":
        # 						if doc.total_working_hours:
        # 							total_working_hours = doc.total_working_hours 
        # 							total_working_hours += formatted_total_hours
        # 						else:
        # 							total_working_hours = formatted_total_hours
        # 						total_working_hours = float(total_working_hours)
        # 						if total_working_hours >= 8:
        # 							doc.status = "Present"
        # 						elif 4 <= total_working_hours <8:
        # 							doc.status = "Half Day"
        # 						else:
        # 							doc.status = "Absent"
        # 					if self.session == "Hourly":
        # 						if self.total_hourly == '1 Hour':
        # 							if doc.total_working_hours:
        # 								total_working_hours = doc.total_working_hours 
        # 								total_working_hours += 1
        # 							else:
        # 								total_working_hours = 1
        # 							total_working_hours = float(total_working_hours)
        # 							if total_working_hours >= 8:
        # 								doc.status = "Present"
        # 							elif 4 <= total_working_hours <8:
        # 								doc.status = "Half Day"
        # 							else:
        # 								doc.status = "Absent"
        # 						elif self.total_hourly == '2 Hours':	
        # 							if doc.total_working_hours:
        # 								total_working_hours = doc.total_working_hours 
        # 								total_working_hours += 2
        # 							else:
        # 								total_working_hours = 2
        # 							total_working_hours = float(total_working_hours)
        # 						elif self.total_hourly == '3 Hours':
        # 							if doc.total_working_hours:
        # 								total_working_hours = doc.total_working_hours 
        # 								total_working_hours += 3
        # 							else:
        # 								total_working_hours = 3
        # 							total_working_hours = float(total_working_hours)
        # 						elif self.total_hourly == '4 Hours':
        # 							if doc.total_working_hours:
        # 								total_working_hours = doc.total_working_hours 
        # 								total_working_hours += 4
        # 							else:
        # 								total_working_hours = 4
        # 							total_working_hours = float(total_working_hours)
        # 						if total_working_hours >= 8:
        # 							doc.status = "Present"
        # 						elif 4 <= total_working_hours <8:
        # 							doc.status = "Half Day"
        # 						else:
        # 							doc.status = "Absent"
        # 					doc.shift = self.shift
        # 					doc.on_duty_application = self.name
        # 					doc.session_from_time = self.from_time
        # 					doc.session_to_time = self.to_time
        # 					doc.save(ignore_permissions=True)
        # 					doc.submit()
        # 					frappe.db.commit()

    # def before_save(self):
    #     current_date = today()
    #     previous_date = add_days(current_date,1)
    #     if previous_date:
    #         frappe.throw(_('On Duty Cannot be marked as Future Dates'))

    def on_cancel(self):
        # Fetch the attendance document linked with the custom on duty application
        no_of_days = date_diff(add_days(self.to_date, 1),self.od_date )
        dates = [add_days(self.od_date, i) for i in range(0, no_of_days)]
        for date in dates:
            if frappe.db.exists("Attendance",{"attendance_date":date,'employee':self.employee,'docstatus':("!=",2)}):
                att=frappe.get_doc("Attendance",{"attendance_date":date,'employee':self.employee,'docstatus':("!=",2)})
                frappe.db.set_value("Attendance",att.name,"on_duty_application",'')
                frappe.db.set_value("Attendance",att.name,"shift",self.shift)
                frappe.db.set_value("Attendance",att.name,"session_from_time","00:00")
                frappe.db.set_value("Attendance",att.name,"session_to_time","00:00")
                if self.shift == '1':
                    mark_att_with_employee(date,date,self.employee)
                else:
                    to_date = add_days(date,1)
                    mark_att_with_employee(date,to_date,self.employee)


        comp_docs = frappe.get_all("Employee Benefits Regularization",
            filters={
                "reference_doctype": self.name,
                "from_on_duty": 1
            },
            fields=["name", "docstatus", "employee", "leave_allocation", "working_hours"]
        )

        for comp in comp_docs:
            comp_doc = frappe.get_doc("Employee Benefits Regularization", comp.name)

            # 🔁 Revert Leave Allocation
            if comp_doc.leave_allocation:
                leave_alloc = frappe.get_doc("Leave Allocation", comp_doc.leave_allocation)

                # Assuming working_hours or days deducted
                revert_value = comp_doc.working_hours or 0

                leave_alloc.total_leaves_allocated += revert_value
                leave_alloc.save(ignore_permissions=True)
                
            if comp_doc.docstatus == 1:
                comp_doc.workflow_state = "Cancelled" 
                comp_doc.flags.ignore_validate = True
                comp_doc.cancel()

        # #  Delete
        # frappe.delete_doc("Employee Benefits Regularization", comp.name, force=1)




    def after_insert(self):
        if self.workflow_state == 'Pending for HOD':
            table = ''
            link = get_url_to_form("On Duty Application", self.name)
            content="""<p>Dear Sir,<br>Kindly find the below On Duty Application from %s (%s).</p><br>"""%(self.employee,self.employee_name)
            for idx,emp in enumerate(self.multi_employee):
                header = """<table class=table table-bordered><tr><td style = 'border: 1px solid black'>Serial No</td><th colspan='7' style = 'border: 1px solid black;background-color:#ffedcc;'><center>On Duty Application</center></th><tr>"""
                table += """<tr><td style = 'border: 1px solid black'>%s</td><th style = 'border: 1px solid black'>Employee ID</th><td style = 'border: 1px solid black'>%s</td><th style = 'border: 1px solid black'>Employee Name</th><td style = 'border: 1px solid black'>%s</td><th style = 'border: 1px solid black'>Department</th><td style = 'border: 1px solid black'>%s</td></tr>
                """%(idx+1,emp.employee,emp.employee_name,emp.department)
            data = """ </table><br><table class=table table-bordered><th colspan='6' style = 'border: 1px solid black;background-color:#ffedcc;'><center>On Duty Application Details</center></th><tr>
            <tr><th style = 'border: 1px solid black'>From Date</th><td style = 'border: 1px solid black'>%s</td><th style = 'border: 1px solid black'>To Date</th><td style = 'border: 1px solid black'>%s</td></tr>
            <tr><th style = 'border: 1px solid black'>From Time</th><td style = 'border: 1px solid black'>%s</td><th style = 'border: 1px solid black'>To Time</th><td style = 'border: 1px solid black'>%s</td></tr>
            <tr><th style = 'border: 1px solid black'>Total Number of Days</th><td style = 'border: 1px solid black'>%s</td><th style = 'border: 1px solid black'>Session</th><td style = 'border: 1px solid black'>%s</td></tr>
            <tr><th colspan='4' style = 'border: 1px solid black;background-color:#ffedcc;'><center><a href='%s'>VIEW</a></center></th></tr>
            </table><br>"""%(format_datetime(self.od_date),format_datetime(self.to_date),format_datetime(self.from_time),format_datetime(self.to_time),self.total_number_of_days,self.session,link)
            regards = "Thanks & Regards,<br>HR"
            # frappe.sendmail(
            # recipients=[self.approver,'abdulla.pi@groupteampro.com'],
            # subject='Reg.On Duty Application Approval' ,
            # message = content+header+table+data+regards)
        
    @frappe.whitelist()
    def show_html(self):
        if self.vehicle_request:
            html = "<h2><center>ON DUTY APPLICATION WITH VEHICLE</center></h2><table class='table table-bordered'><tr><th>From Date</th><th>To Date</th></tr><tr><td><h2>%s</h2></td><td><h2>%s</h2></td></tr><tr><th>From Time</th><th>To Time</th></tr><tr><td><h2>%s</h2></td><td><h2>%s</h2></td></tr></table>"%(frappe.utils.format_date(self.od_date),frappe.utils.format_date(self.to_date),self.from_time,self.to_time)
        else:
            html = "<h2><center>ON DUTY APPLICATION</center></h2><table class='table table-bordered'><tr><th>From Date</th><th>To Date</th></tr><tr><td><h2>%s</h2></td><td><h2>%s</h2></td></tr><tr><th>From Time</th><th>To Time</th></tr><tr><td><h2>%s</h2></td><td><h2>%s</h2></td></tr></table>"%(frappe.utils.format_date(self.od_date),frappe.utils.format_date(self.to_date),self.from_time,self.to_time)
        return html

    @frappe.whitelist()
    def throw_overlap_error(self, d):
        msg = _("Employee {0} has already applied for {1} between {2} and {3}").format(self.employee,
            d['on_duty_type'], formatdate(d['od_date']), formatdate(d['to_date'])) \
            + """ <br><b><a href="#Form/On Duty Application/{0}">{0}</a></b>""".format(d["name"])
        frappe.throw(msg, OverlapError)
        leave_count_on_half_day_date = frappe.db.sql("""select count(name) from `tabOn Duty Application`
            where employee = %(employee)s
            and docstatus < 2
            and status in ("Open","Applied", "Approved")
            and half_day = 1
            and half_day_date = %(half_day_date)s
            and name != %(name)s""", {
                "employee": self.employee,
                "half_day_date": self.half_day_date,
                "name": self.name
            })[0][0]
        return leave_count_on_half_day_date * 0.5

    @frappe.whitelist()
    def get_ceo(self,department):
        ceo = frappe.db.get_value('Department',department,"ceo")
        return ceo
    
    @frappe.whitelist()
    def get_gm(self,department):
        gm = frappe.db.get_value('Department',department,"gm")
        return gm

    @frappe.whitelist()
    def get_hod(self,department):
        hod = frappe.db.get_value('Department',department,"hod")
        return hod


def validate_if_attendance_not_applicable(employee, attendance_date):
    # Check if attendance_date is a Holiday
    if is_holiday(employee, attendance_date):
        frappe.msgprint(_("Attendance not submitted for {0} as it is a Holiday.").format(attendance_date), alert=1)
        return True
    # Check if employee on Leave
    leave_record = frappe.db.sql("""select half_day from `tabLeave Application`
            where employee = %s and %s between od_date and to_date
            and docstatus = 1""", (employee, attendance_date), as_dict=True)
    if leave_record:
        frappe.msgprint(_("Attendance not submitted for {0} as {1} on leave.").format(attendance_date, employee), alert=1)
        return True
    return False

def get_holiday_list_for_employee(employee, raise_exception=True):
    if employee:
        holiday_list, company = frappe.db.get_value("Employee", employee, ["holiday_list", "company"])
    else:
        holiday_list=''
        company=frappe.db.get_value("Global Defaults", None, "default_company")

    if not holiday_list:
        holiday_list = frappe.get_cached_value('Company',  company,  "default_holiday_list")

    if not holiday_list and raise_exception:
        frappe.throw(_('Please set a default Holiday List for Employee {0} or Company {1}').format(employee, company))
    return holiday_list

def is_holiday(employee, date=None):
    '''Returns True if given Employee has an holiday on the given date
    :param employee: Employee `name`
    :param date: Date to check. Will check for today if None'''
    holiday_list = get_holiday_list_for_employee(employee)
    if not date:
        date = today()
    if holiday_list:
        return frappe.get_all('Holiday List', dict(name=holiday_list, holiday_date=date)) and True or False

@frappe.whitelist()
def get_number_of_leave_days(employee, od_date, to_date,session,  to_date_session=None, date_dif=None):
    number_of_days = 0
    if od_date == to_date:
        # frappe.errprint(od_date)
        # frappe.log_error('ON Duty',session) 
        if session != 'Full Day':
            number_of_days = 0.5
            # frappe.errprint(to_date)
            # frappe.log_error('ON Duty',to_date)  
        else:
            number_of_days = 1
            # frappe.errprint(number_of_days)
            # frappe.log_error('ON Duty',number_of_days)  
    else:
        # frappe.errprint("welcome")
        # message = "welcome"
        # frappe.log_error('ON Duty',message)  
        if session == "Full Day" and to_date_session == "Full Day":
            number_of_days = flt(date_dif)
        if session == "Full Day" and to_date_session == "First Half":
            number_of_days = flt(date_dif) - 0.5
        if session == "Second Half" and to_date_session == "Full Day":
            number_of_days = flt(date_dif) - 0.5
        if session == "Second Half" and to_date_session == "First Half":
            number_of_days = flt(date_dif) - 1
    return number_of_days

@frappe.whitelist()
def check_attendance(employee, od_date, to_date):
    if employee:
        attendance = frappe.db.sql("""select status,attendance_date from `tabAttendance`
                    where employee = %s and attendance_date between %s and %s
                    and docstatus = 1""", (employee, od_date, to_date), as_dict=True)
        return attendance

@frappe.whitelist()
def validate_cutoff(od_date):
    cur_mon = datetime.strptime(today(), "%Y-%m-%d").strftime("%B")
    frappe.errprint(cur_mon)
    c = frappe.get_value("Application Cut Off Date",{'month':cur_mon},['cut_off_date','od_date','to_date'])
    curday = date.today()
    fromdate = datetime.strptime(str(od_date),"%Y-%m-%d").date()
    if fromdate < c[1]:
        return 'Expired'
    if fromdate > c[1] and fromdate < c[2]:
        frappe.errprint('true')

@frappe.whitelist()
def get_employees():
    # frappe.error_log(frappe.session.user)
    data = []
    employee_id = frappe.db.get_value('Employee',{'status':'Active','user_id':frappe.session.user},["name", "employee_name", "department", "designation"])
    data.append(employee_id[0])
    data.append(employee_id[1])
    data.append(employee_id[2])
    data.append(employee_id[3])    
    return data

@frappe.whitelist()
def get_time(shift,session):
    datalist = []
    data = {}
    if shift == '1':
        get_session_st_time = frappe.db.get_value('Shift Type',{'name':shift},['start_time'])
        get_session_ed_time = frappe.db.get_value('Shift Type',{'name':shift},['end_time'])
        if session == 'Full Day':
            data.update({
                'get_session_st_time':get_session_st_time,
                'get_session_ed_time':get_session_ed_time    
            })
            datalist.append(data.copy())
        elif session == 'First Half' :
            gt = get_session_st_time + timedelta(hours=4,minutes=25)
            data.update({
                'get_session_st_time':get_session_st_time,
                'get_session_ed_time':gt
            })
            datalist.append(data.copy())
        elif session == 'Second Half' :
            gc =  get_session_ed_time - timedelta(hours=4,minutes=25)
            data.update({
                'get_session_st_time':gc,
                'get_session_ed_time':get_session_ed_time
            })
            datalist.append(data.copy()) 
    elif shift == '2':
        get_session_st_time = frappe.db.get_value('Shift Type',{'name':shift},['start_time'])
        get_session_ed_time = frappe.db.get_value('Shift Type',{'name':shift},['end_time'])
        if session == 'Full Day':
            data.update({
                'get_session_st_time':get_session_st_time,
                'get_session_ed_time':get_session_ed_time    
            })
            datalist.append(data.copy())
        elif session == 'First Half' :
            gt = get_session_st_time + timedelta(hours=4,minutes=25)
            data.update({
                'get_session_st_time':get_session_st_time,
                'get_session_ed_time':gt
            })
            datalist.append(data.copy())
        elif session == 'Second Half' :
            gc =  get_session_st_time + timedelta(hours=4,minutes=25)
            data.update({
                'get_session_st_time':gc,
                'get_session_ed_time':get_session_ed_time
            })
            datalist.append(data.copy())     
    else: 
        get_session_st_time = frappe.db.get_value('Shift Type',{'name':shift},['start_time'])
        get_session_ed_time = frappe.db.get_value('Shift Type',{'name':shift},['end_time'])
        if session == 'Full Day':
            data.update({
                'get_session_st_time':get_session_st_time,
                'get_session_ed_time':get_session_ed_time,    
            })
            datalist.append(data.copy())
        elif session == 'First Half' :
            gt = get_session_st_time + timedelta(hours=3,minutes=10) 
            data.update({
                'get_session_st_time':get_session_st_time,
                'get_session_ed_time':gt
            })
            datalist.append(data.copy())
        elif session == 'Second Half' :
            gc = get_session_ed_time - timedelta(hours=3,minutes=10)
            data.update({
                'get_session_st_time':gc,
                'get_session_ed_time':get_session_ed_time
            })
            datalist.append(data.copy())   
    return datalist

@frappe.whitelist()
def total_od_hours(from_time,to_time,session):
    if session != 'Hourly':
        if isinstance(from_time, str):
            start_time = datetime.strptime(from_time, "%H:%M:%S").time() 
        elif isinstance(from_time, timedelta):
            start_time = (datetime.min + from_time).time()
        else:
            start_time = from_time 
        # if session != "Hourly":
        if isinstance(to_time, str):
            end_time = datetime.strptime(to_time, "%H:%M:%S").time()  
        elif isinstance(to_time, timedelta):
            end_time = (datetime.min + to_time).time()
        else:
            end_time = to_time  
        # else:
        #     if isinstance(to, str):
        #         frappe.errprint("D")
        #         end_time = datetime.strptime(to, "%H:%M").time()  
        #     elif isinstance(to, timedelta):
        #         frappe.errprint("E")
        #         end_time = (datetime.min + to).time()
        #     else:
        #         end_time = to  
        #         frappe.errprint("F")
        if isinstance(start_time, time) and isinstance(end_time, time):
            time_difference = datetime.combine(datetime.today(), end_time) - datetime.combine(datetime.today(), start_time)
            total_seconds = time_difference.total_seconds()
            formatted_total_hours =round((total_seconds/3600),1)
            formatted_total_hours = float(formatted_total_hours)
            frappe.errprint(formatted_total_hours)
            # frappe.errprint(name)
            # frappe.db.set_value("On Duty Application",self.name,"total_od_hours",formatted_total_hours)
        return formatted_total_hours


@frappe.whitelist()
def total_od_hours_with_to(from_time,to,session):
    if session == 'Hourly':
        if isinstance(from_time, str):
            start_time = datetime.strptime(from_time, "%H:%M:%S").time() 
        elif isinstance(from_time, timedelta):
            start_time = (datetime.min + from_time).time()
        else:
            start_time = from_time 
        if isinstance(to, str):
            end_time = datetime.strptime(to, "%H:%M").time()  
        elif isinstance(to, timedelta):
            end_time = (datetime.min + to).time()
        else:
            end_time = to  
        if isinstance(start_time, time) and isinstance(end_time, time):
            time_difference = datetime.combine(datetime.today(), end_time) - datetime.combine(datetime.today(), start_time)
            total_seconds = time_difference.total_seconds()
            formatted_total_hours =round((total_seconds/3600),1)
            formatted_total_hours = float(formatted_total_hours)
            # frappe.errprint(name)
            # frappe.db.set_value("On Duty Application",self.name,"total_od_hours",formatted_total_hours)
        return formatted_total_hours
    
@frappe.whitelist()
def update_approval_role(workflow_state,name):
    if workflow_state == 'HOD Pending':
        frappe.db.set_value('On Duty Application',{'name':name}, 'approver_role', 'HOD')
    elif workflow_state == 'TL Pending':
        frappe.db.set_value('On Duty Application',{'name':name}, 'approver_role', 'TL')
    elif workflow_state == 'HR Pending':
        frappe.db.set_value('On Duty Application',{'name':name}, 'approver_role', 'HR Manager')
    elif workflow_state == 'Director Pending':
        frappe.db.set_value('On Duty Application',{'name':name}, 'approver_role', 'Director')
    elif workflow_state == 'MD Pending':
        frappe.db.set_value('On Duty Application',{'name':name}, 'approver_role', 'MD')
    elif workflow_state in ['Approved', 'Rejected']:
        frappe.db.set_value('On Duty Application',{'name':name}, 'approver', frappe.session.user)
    return "ok"