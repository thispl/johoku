# Copyright (c) 2022, teampro and contributors
# For license information, please see license.txt
from re import S
from time import strftime, strptime
import frappe
import math
import pandas as pd
from frappe.model.document import Document
import frappe,os,base64
import requests
import datetime
import json,calendar
from johoku.mark_attendance import mark_wh_ot_with_employee,mark_att_present_with_employee,mark_att_with_employee
from datetime import datetime,timedelta,date,time
import datetime as dt
from frappe.utils import cint,today,flt,date_diff,add_days,add_months,date_diff,getdate,formatdate,cint,cstr
from frappe.desk.notifications import delete_notification_count_for
from frappe.utils import cstr, cint, getdate,get_first_day, get_last_day, today,get_datetime
from frappe import _
from frappe.utils import nowdate


class MissPunchApplication(Document):
    def on_submit(self):
        # frappe.db.set_value('Miss Punch Application',self.name,'approved_by',frappe.session.user)
    # def on_update(self):
        if self.workflow_state == "Approved":
            total_working_hr = self.validate()
            total_working_hours = total_working_hr[0]['working_hours']
            total_wh = self.validate()
            total_work_hours = total_wh[0]['wh']
            extra_hours = self.validate()
            extra_hr = extra_hours[0]['extra_hours']
            ot_hours = self.validate()
            ot_hr = ot_hours[0]['overtime_hours']
            att_doc = frappe.db.exists("Attendance",{"attendance_date":self.date,"employee":self.employee,"docstatus":["!=",2]})
            if att_doc:
                att = frappe.get_doc("Attendance",att_doc)
            # att = frappe.get_doc('Attendance',self.attendance_marked)
            # att.status = 'Present'
            frappe.db.set_value("Attendance",att.name,'in_time',self.in_time)
            frappe.db.set_value("Attendance",att.name,'out_time',self.out_time)
            att.in_time = self.in_time
            att.out_time = self.out_time
            if not att.att_in_time:
                frappe.db.set_value("Attendance",att.name,'att_in_time',self.in_time)
                # att.att_in_time = self.in_time
            if not att.att_out_time:
                frappe.db.set_value("Attendance",att.name,'att_out_time',self.out_time)
                # att.att_out_time = self.out_time
            if not att.attended_shift:
                frappe.db.set_value("Attendance",att.name,'attended_shift',self.shift)
                # att.attended_shift = self.shift
            # if not att.shift:
            frappe.db.set_value("Attendance",att.name,'shift',self.shift)
            # att.shift = self.shift
            if self.in_time and self.out_time:
                frappe.db.set_value("Attendance",att.name,'shift_status',self.shift)
                # att.shift_status = self.shift
            frappe.errprint(extra_hr)
            frappe.db.set_value("Attendance",att.name,'working_total_hours',total_working_hours)
            frappe.db.set_value("Attendance",att.name,'total_working_hours',total_work_hours)
            frappe.db.set_value("Attendance",att.name,'extra_hours',extra_hr)
            frappe.db.set_value("Attendance",att.name,'over_time_hours',ot_hr)
            # att.working_total_hours = total_working_hours
            # att.total_working_hours = total_work_hours
            # att.extra_hours = extra_hr
            # att.over_time_hours = ot_hr
            if att.assigned_shift and att.attended_shift:
                if att.assigned_shift == att.attended_shift:
                    frappe.db.set_value("Attendance",att.name,'shift_matched_or_unmatched','Matched')
                    # att.shift_matched_or_unmatched = 'Matched'
                else:
                    frappe.db.set_value("Attendance",att.name,'shift_matched_or_unmatched','Unmatched')
                    # att.shift_matched_or_unmatched = 'Unmatched'  
            frappe.db.set_value("Attendance",att.name,'miss_punch',self.name)
            att.miss_punch = self.name
            # att.save(ignore_permissions=True)
            # frappe.db.commit()
            # if att.in_time and att.out_time:
            #     mark_wh_ot_with_employee(self.date,self.date,self.employee)
            # else:
            #     frappe.db.set_value("Attendance",att.name,'status','Absent')
            if att.in_time and att.out_time:
                mark_wh_ot_with_employee(self.date, self.date, self.employee)

            else:
                frappe.db.set_value(
                    "Attendance",
                    att.name,
                    "status",
                    "Absent"
                )

            # Refresh Attendance data
            att.reload()
            
            is_unmatched = att.assigned_shift and att.attended_shift and att.assigned_shift != att.attended_shift
            if is_unmatched:
                frappe.db.set_value("Attendance",att.name,'status','Absent')
                
            mark_att_present_with_employee(self.date,self.date,self.employee)
            # if att.docstatus==0:
            #     frappe.errprint("Test")
            #     if att.status == 'Present':
            #         frappe.db.set_value("Attendance",att.name,'docstatus',1)
              
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
                        _("Miss Punch Application are allowed only for up to the previous {0} working days.")
                        .format(allowed_days)
                        )
            if frappe.db.exists("Miss Punch Application",{'employee':self.employee,'date':self.date,'docstatus':['!=',2],'name':['!=',self.name]}):
                frappe.throw(f"Already another application found for <b>{self.employee}</b> on <b>{self.date}</b> ")
        datalist = []
        data = {}
        in_time_str = str(self.in_time)
        out_time_str = str(self.out_time)

        if len(in_time_str.split(':')) == 2:  
            in_time_str += ":00"
        if len(out_time_str.split(':')) == 2:  
            out_time_str += ":00"

        try:
            in_time = datetime.strptime(in_time_str, '%Y-%m-%d %H:%M:%S')
            out_time = datetime.strptime(out_time_str, '%Y-%m-%d %H:%M:%S')
        except ValueError as e:
            raise ValueError(f"Invalid time format: {str(e)}")
        working_hours = out_time - in_time
        ftr = [3600,60,1]
        hr = sum([a*b for a,b in zip(ftr, map(int,str(working_hours).split(':')))])
        wh = round(hr/3600,1)
        shift_end_time = frappe.db.get_value('Shift Type',self.shift,'end_time')
        shift_end_time = pd.to_datetime(str(shift_end_time)).time() 
        get_date_time = get_datetime(self.out_time)
        get_date = get_date_time.date()
        shift_end_datetime = datetime.combine(get_date,shift_end_time)
        get_shift_hours = frappe.db.get_value('Shift Type',{'name':self.shift},['total_shift_hours'])
        total_shift_hours = (get_datetime(get_shift_hours)).time()
        total_working_hours = datetime.strptime(str(working_hours),'%H:%M:%S').time()
        if shift_end_datetime:
            extra_hours = pd.to_datetime('00:00').time()  
            overtime_hours = 0 
            extra_hours_formatted = "00:00"
            if get_date_time > shift_end_datetime:
                if total_working_hours > total_shift_hours:
                    extra_hours = get_date_time - shift_end_datetime
                    total_seconds = extra_hours.total_seconds()
                    hours = int(total_seconds // 3600)
                    minutes = int((total_seconds % 3600) // 60)
                    extra_hours_formatted = f"{hours:02}:{minutes:02}"
                    hr = sum([a*b for a,b in zip(ftr, map(int,str(extra_hours).split(':')))])
                    extras = round(hr/3600,1)
                    if extras > 1:
                        overtime_hours = math.floor(extras * 2) / 2
                    frappe.errprint(extras)
        # Miss Punch Restriction
        if self.is_new():
            start_of_month = nowdate()[:7] + "-01"
            miss_punch_count = frappe.db.count(
                "Miss Punch Application",
                filters={
                    "employee": self.employee,
                    "date": ["between", [start_of_month, nowdate()]],
                    "workflow_state": ['not in', ('Cancelled', 'Rejected')]
                },
            )

            user_roles = frappe.get_roles(frappe.session.user)
            hr = "Miss Punch" in user_roles
            admin = "Administrator" in user_roles

            if miss_punch_count >= 3 and not hr:
                frappe.throw("You have already submitted 3 Miss Punch applications this month.")
            if miss_punch_count >=3 and admin:
                frappe.throw("Administrator is not allowed to apply more than 3 miss punch")



        data.update({
            'working_hours':working_hours,
            'wh':wh,
            'extra_hours':extra_hours_formatted,
            'overtime_hours':overtime_hours  
        })   
        datalist.append(data.copy())         
        return datalist    
    
    def on_cancel(self):
        att = frappe.db.exists('Attendance',{'attendance_date':self.date,'employee':self.employee})
        if att:
            frappe.db.set_value('Attendance',att,'miss_punch','')  
            frappe.db.set_value('Attendance',att,'status','Absent')  
            frappe.db.set_value('Attendance',att,'working_total_hours',"00:00")             
            frappe.db.set_value('Attendance',att,'total_working_hours','0')
            if self.in_punch==1:
                frappe.db.set_value('Attendance',att,'in_time',None)         
            if self.out_punch==1:
                frappe.db.set_value('Attendance',att,'out_time',None)  
                if self.shift == '1':
                    mark_att_with_employee(self.date,self.date,self.employee)
                else:
                    to_date = add_days(self.date,1)
                    mark_att_with_employee(self.date,to_date,self.employee)
                

@frappe.whitelist()
def update_approval_role(workflow_state,name):
    if workflow_state == 'HOD Pending':
        frappe.db.set_value('Miss Punch Application',{'name':name}, 'approver_role', 'HOD')
    elif workflow_state == 'TL Pending':
        frappe.db.set_value('Miss Punch Application',{'name':name}, 'approver_role', 'TL')
    elif workflow_state == 'HR Pending':
        frappe.db.set_value('Miss Punch Application',{'name':name}, 'approver_role', 'HR Manager')
    elif workflow_state == 'Director Pending':
        frappe.db.set_value('Miss Punch Application',{'name':name}, 'approver_role', 'Director')
    elif workflow_state == 'MD Pending':
        frappe.db.set_value('Miss Punch Application',{'name':name}, 'approver_role', 'MD')
    elif workflow_state in ['Approved', 'Rejected']:
        frappe.db.set_value('Miss Punch Application',{'name':name}, 'approved_by', frappe.session.user)
    return "ok"    
    
    
    
       