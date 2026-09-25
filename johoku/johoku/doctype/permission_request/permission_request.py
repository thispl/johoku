# Copyright (c) 2022, TEAMPRO and contributors
# For license information, please see license.txt


from __future__ import unicode_literals
from itertools import count
from pickle import FALSE
from stat import FILE_ATTRIBUTE_REPARSE_POINT
import frappe
from frappe.model.document import Document
from frappe.model.document import Document
from datetime import datetime, timedelta, date, time
from frappe.utils import get_first_day, get_last_day, format_datetime, get_url_to_form,add_days
from frappe import msgprint
from frappe.utils import today
from frappe import _
from johoku.mark_attendance import mark_att_with_employee

class PermissionRequest(Document):
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
                if isinstance(self.permission_date, str):
                    miss_date = datetime.strptime(self.permission_date, "%Y-%m-%d").date()
                else:
                    miss_date = self.permission_date
                    
                if miss_date < earliest_allowed:
                    frappe.throw(
                        _("Permission request are allowed only for up to the previous {0} working days.")
                        .format(allowed_days)
                        )
        if self.docstatus == 0:
            month_start = get_first_day(self.permission_date)
            month_end = get_last_day(self.permission_date)
            doc=frappe.db.get_all('Permission Request',{"employee_id":self.employee_id,"permission_date":('Between',(month_start,month_end)),'workflow_state':('Not in',("Rejected","Cancelled")),'name':("!=",self.name)},['*'])
            tot=int(self.permission_hour)
            for i in doc:
                frappe.errprint(i.name)
                tot+=int(i.permission_hour)
                if tot > 2:
                    frappe.throw("Only 2 hour permission is allowed for a month")
            # count = frappe.db.count("Permission Request",{"employee_id":self.employee_id,"permission_date":self.permission_date})
            # if count >= 1:
            # 	frappe.throw("Only 1 permission are allowed for a day")
                
            # monthly_permission_count = frappe.db.count("Permission Request",{"employee_id":self.employee_id,"permission_date": ('between',(month_start,month_end)) }) 
            # if monthly_permission_count >=2:
            # 	frappe.throw("Only 2 permissions are allowed for a month")

            # per_exists = frappe.db.exists('Permission Request',{'employee_id':self.employee_id,"permission_date": ('between',(month_start,month_end))})    
            # if per_exists:
            # 	per_count = frappe.db.get_value('Permission Request',{'name':per_exists},['permission_hour'])
            # 	hours = int(per_count) + int(self.permission_hour)
            # 	if hours > 2:
            # 		frappe.throw("Only 2 Hours permissions are allowed for a month")
            # 	else:
            # 		message = ('Employee %s Permission Count Less than 2 Hours'%(self.employee_id))    
            # 		frappe.error_log('Permission Request',message)
            # else:
            # 	message = ('Employee %s Permission Request is not there')        
            # 	frappe.log_error('Permission Request',message)
            
            
                              
    # if count[0].count >= 1:
    # 	    # frappe.errprint('today')
    #     frappe.throw("Only 1 permission are allowed for a day")
    #     # count = frappe.db.sql("select count(*) as count from `tabPermission Request` where employee_id = '%s' and permission_date between '%s' and '%s' and employee_name != '%s' and workflow_state != 'Rejected' "%(self.employee_id, month_start, month_end, self.employee_name), as_dict=True)
    #     if count[0].count >= 2:
    #         frappe.throw("Only 2 permissions are allowed for a month")
    def on_submit(self):
        # frappe.db.set_value('Permission Request',self.name,'approved_by',frappe.session.user)
        if self.workflow_state == "Approved":
            att = frappe.db.exists("Attendance",{"attendance_date":self.permission_date,"employee":self.employee_id,"docstatus":["!=",2]})
            if att:
                doc = frappe.get_doc("Attendance",att)
                if doc.docstatus == 0:
                    doc.shift = self.shift
                    doc.attended_shift = self.shift
                    doc.permission = self.name
                    doc.save(ignore_permissions=True)
                    # doc.submit()
                    frappe.db.commit()
                elif doc.docstatus == 1:
                    doc.shift = self.shift
                    doc.attended_shift = self.shift
                    doc.permission = self.name
                    doc.save(ignore_permissions=True)
                    # doc.submit()
                    frappe.db.commit()
                # frappe.errprint(self.permission_date)
                if isinstance(self.permission_date, str):
                    date = datetime.strptime(self.permission_date, "%Y-%m-%d").date()
                else:
                    date = self.permission_date
                if self.shift == '1':
                    mark_att_with_employee(date,date,self.employee_id)
                else:
                    to_date = add_days(date,1)
                    mark_att_with_employee(date,to_date,self.employee_id)

            else:
                doc = frappe.new_doc("Attendance")
                doc.employee = self.employee_id
                doc.attendance_date = self.permission_date
                doc.status = "Absent"
                doc.shift = self.shift
                doc.attended_shift = self.shift
                doc.permission = self.name
                doc.save(ignore_permissions=True)
                # doc.submit()
                frappe.db.commit()
                if isinstance(self.permission_date, str):
                    date = datetime.strptime(self.permission_date, "%Y-%m-%d").date()
                else:
                    date = self.permission_date
                # date = datetime.strptime(self.permission_date, "%Y-%m-%d").date()
                if self.shift == '1':
                    mark_att_with_employee(date,date,self.employee_id)
                else:
                    to_date = add_days(date,1)
                    mark_att_with_employee(date,to_date,self.employee_id)

    def on_cancel(self):
        # att = frappe.db.get_value("Attendance",{"permission":self.name},["name"])
        # if att:
        #     att_doc=frappe.get_doc("Attendance",att)
        #     frappe.db.set_value("Attendance",att,"permission",'')
        #     if att_doc.in_time and att_doc.out_time:
        #         wh = att_doc.total_working_hours	
        #         if wh>=8:
        #             frappe.db.set_value("Attendance",att,"status","Present")
        #         elif wh >= 4 and wh < 8:
        #             frappe.db.set_value("Attendance",att,"status","Half Day")
        #         else:
        #             frappe.db.set_value("Attendance",att,"status","Absent")
        if isinstance(self.permission_date, str):
            date = datetime.strptime(self.permission_date, "%Y-%m-%d").date()
        else:
            date = self.permission_date
        if frappe.db.exists("Attendance",{"attendance_date":date,'employee':self.employee_id,'docstatus':("!=",2)}):
            att=frappe.get_doc("Attendance",{"attendance_date":date,'employee':self.employee_id,'docstatus':("!=",2)})
            frappe.db.set_value("Attendance",att.name,"permission",'')
            frappe.db.set_value("Attendance",att.name,"shift",self.shift)
            if self.shift == '1':
                mark_att_with_employee(date,date,self.employee_id)
            else:
                to_date = add_days(date,1)
                mark_att_with_employee(date,to_date,self.employee_id)

@frappe.whitelist()
def get_employee_approver(dept):
    get_approver = frappe.db.get_value('Department', {'name': dept}, ['hod'])
    return get_approver

@frappe.whitelist()
def get_endtime1(shift,session,per_hour):
    datalist = []
    data = {}
    if session == 'First Half':
        get_shift_time = frappe.db.get_value('Shift Type',{'name':shift},['start_time'])
        if per_hour == '1':
            one_hour = timedelta(hours=1) + get_shift_time
            data.update({
                'get_shift_time':get_shift_time,
                'one_hour':one_hour
            })
            datalist.append(data.copy())
        elif per_hour == '2':
            two_hour = timedelta(hours=2) + get_shift_time     
            data.update({
                'get_shift_time':get_shift_time,
                'two_hour':two_hour
            })
            datalist.append(data.copy())   
        # else:
        # 	frappe.throw("Not Allowed for 1.5 Hours Permission")   
    elif session == 'Second Half':
        get_shift_time = frappe.db.get_value('Shift Type',{'name':shift},['end_time'])
        if per_hour == '1':
            one_hour = get_shift_time - timedelta(hours=1) 
            data.update({
                'get_shift_time':one_hour,
                'one_hour':get_shift_time
            })
            datalist.append(data.copy())
        elif per_hour == '2':
            # shift_type = frappe.db.get_value('Shift Type',{'name':shift},['name'])
            if shift == "2":
                get_shift_time_str =str(get_shift_time)
                get_shift_time_new = datetime.strptime(get_shift_time_str, "%H:%M:%S")
                two_hour_time = get_shift_time_new - timedelta(hours=2)
                two_hour = two_hour_time.time()  
                data.update({
                'get_shift_time':two_hour,
                'two_hour':get_shift_time })
            else:
                two_hour = get_shift_time - timedelta(hours=2)   
                data.update({
                'get_shift_time':two_hour,
                'two_hour':get_shift_time
            })
            datalist.append(data.copy())
        # else:
        # 	frappe.throw("Not Allowed for 1.5 Hours Permission")                 
    return datalist        

#         shift = frappe.db.get_value('Shift Type', {'name': shift}, ['start_time'])
#         str_time = datetime.strptime(shift, '%H:%M:%S')

# @frappe.whitelist()
# def get_endtime1(Self, start_time):
#         time = datetime.strptime(start_time, "%H:%M:%S")
#         end_time = timedelta(hours=2) + time
#         return str(end_time.time())

# @frappe.whitelist()
# def get_endtime2(Self, end_time):
#         time = datetime.strptime(end_time, "%H:%M:%S")
#         start_time = time - timedelta(hours=2)
#         return str(start_time.time())

# @frappe.whitelist()
# def get_ceo(self):
#     	ceo = frappe.db.get_value('Department',self.department,"ceo")
#     	return ceo

# @frappe.whitelist()
#     def get_gm(self):
#     	gm = frappe.db.get_value('Department',self.department,"gm")
#     	return gm

@frappe.whitelist()
def get_hod(self):
        hod = frappe.db.get_value('Department', self.department, "hod")
        return hod

def after_insert(self):
        if self.workflow_state == 'Pending for HOD':
            link = get_url_to_form("Permission Request", self.name)
            content = """<p>Dear Sir,</p>
            Kindly find the below Permission Request from %s (%s).<br>""" % (self.employee_id, self.employee_name)
            table = """<table class=table table-bordered><tr><th colspan='4' style = 'border: 1px solid black;background-color:#ffedcc;'><center>PERMISSION REQUEST</center></th><tr>
            <tr><th style = 'border: 1px solid black'>Employee ID</th><td style = 'border: 1px solid black'>%s</td><th style = 'border: 1px solid black'>Department</th><td style = 'border: 1px solid black'>%s</td></tr>
            <tr><th style = 'border: 1px solid black'>Employee Name</th><td style = 'border: 1px solid black'>%s</td><th style = 'border: 1px solid black'>Designation</th><td style = 'border: 1px solid black'>%s</td></tr>
            <tr><th style = 'border: 1px solid black'>Permission Date</th><td style = 'border: 1px solid black'>%s</td><th style = 'border: 1px solid black'>Session</th><td style = 'border: 1px solid black'>%s</td></tr>
            <tr><th style = 'border: 1px solid black'>Shift</th><td style = 'border: 1px solid black'>%s</td><th style = 'border: 1px solid black'>From Time</th><td style = 'border: 1px solid black'>%s</td></tr>
            <tr><th rowspan='2' style = 'border: 1px solid black'>Reason</th><td rowspan='2' style = 'border: 1px solid black'>%s</td><th style = 'border: 1px solid black'>To Time</th><td style = 'border: 1px solid black'>%s</td></tr>
            <tr><th style = 'border: 1px solid black'>Hours</th><td style = 'border: 1px solid black'>%s</td></tr>
            <tr><th colspan='4' style = 'border: 1px solid black;background-color:#ffedcc;'><center><a href='%s'>VIEW</a></center></th></tr>
            </table><br>"""%(self.employee_id, self.department, self.employee_name, self.designation, format_datetime(self.permission_date),self.session,self.shift,self.from_time,self.reason,self.to_time,self.hours,link)
            regards = "Thanks & Regards,<br>HR"
            # frappe.sendmail(
            # recipients=[self.permission_approver,'abdulla.pi@groupteampro.com'],
            # subject='Reg.Permission Request Approval' ,
            # message = content+table+regards)


@frappe.whitelist()
def get_shift_assignment(employee_id, start_date):
    shift_assignment = frappe.get_all(
        "Shift Assignment",
        filters={
            "employee": employee_id,
            "start_date": start_date,
            "docstatus" :1
        },
        fields=["shift_type"],
        limit=1
    )

    if shift_assignment:
        return {"shift_type": shift_assignment[0].shift_type}

    return {}

@frappe.whitelist()
def update_approval_role(workflow_state,name):
    if workflow_state == 'HOD Pending':
        frappe.db.set_value('Permission Request',{'name':name}, 'approver_role', 'HOD')
    elif workflow_state == 'TL Pending':
        frappe.db.set_value('Permission Request',{'name':name}, 'approver_role', 'TL')
    elif workflow_state == 'HR Pending':
        frappe.db.set_value('Permission Request',{'name':name}, 'approver_role', 'HR Manager')
    elif workflow_state == 'Director Pending':
        frappe.db.set_value('Permission Request',{'name':name}, 'approver_role', 'Director')
    elif workflow_state == 'MD Pending':
        frappe.db.set_value('Permission Request',{'name':name}, 'approver_role', 'MD')
    elif workflow_state in ['Approved', 'Rejected']:
        frappe.db.set_value('Permission Request',{'name':name}, 'approved_by', frappe.session.user)
    return "ok"