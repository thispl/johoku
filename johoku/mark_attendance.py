from __future__ import print_function
from pickle import TRUE
from time import strptime
from traceback import print_tb
import frappe
from frappe.utils.data import ceil, get_time, get_year_start
import pandas as pd
import json
import datetime
import datetime as dt
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime, time_diff_in_hours)
from datetime import datetime
from calendar import monthrange
from frappe import _, msgprint
from frappe.utils import flt
from frappe.utils import cstr, cint, getdate,get_first_day, get_last_day, today, time_diff_in_hours
import requests
from datetime import date, timedelta,time
from frappe.utils import get_url_to_form
import math
import dateutil.relativedelta
# from frappe.utils import time_diff_in_timedelta
from frappe.utils import time_diff



status_map = {    
    "Earned Leave": "EL",
    "Casual Leave": "CL",
    "Sick Leave": "SL",
    "Privilege Leave": "PL",
    "Leave Without Pay": "LWP",
    "Medical Leave": "MdL",
    "Maternity Leave": "MaL",
    "Compensatory Off": "CO",
    }

def mark_att_aug():
    from_date = '2025-12-08'
    to_date = '2025-12-08'
    checkins = frappe.db.sql("""select * from `tabEmployee Checkin` where date(time) between '%s' and '%s' order by time  """%(from_date,to_date),as_dict=True)
    for c in checkins:
        employee = frappe.db.exists('Employee',{'status':'Active','date_of_joining':['<=',from_date],'name':c.employee})
        if employee:
            mark_attendance_from_checkin(c.name,c.employee,c.time,c.log_type)
    mark_absent(from_date,to_date)
    mark_wh_ot(from_date,to_date) 
    update_overtime_list(from_date,to_date)
    get_ot_compensation(from_date,to_date)   
    att_shift_status_updation(from_date,to_date)
    assigned_shift(from_date,to_date) 
    shift_matched(from_date,to_date)
    mark_late_early_updates(from_date,to_date)
    mark_att_present(from_date,to_date)
    remove_duplicate_attendance(from_date, to_date)
    return "ok" 

@frappe.whitelist()
def mark_att_with_employee_manual():
    from_date = '2026-01-08'
    to_date = '2026-01-08'
    employee='JMPLTT551'
    checkins = frappe.db.sql("""select * from `tabEmployee Checkin` where date(time) between '%s' and '%s' and employee = '%s' order by time  """%(from_date,to_date,employee),as_dict=True)
    for c in checkins:
        # print("Welcome to Employeee Checkin")
        employee_data = frappe.db.exists('Employee',{'status':'Active','date_of_joining':['<=',from_date],'name':c.employee})
        if employee_data:
            mark_attendance_from_checkin(c.name,c.employee,c.time,c.log_type)
    mark_absent_with_employee(from_date,to_date,employee)
    mark_wh_ot_with_employee_updates(from_date,to_date,employee) 
    
    update_overtime_list_with_employee(from_date,to_date,employee)
    # get_ot_compensation(from_date,to_date)   
    assigned_shift_with_employee(from_date,to_date,employee) 
    shift_matched_with_employee(from_date,to_date,employee)
    att_shift_status_updation_with_employee(from_date,to_date,employee)
    mark_late_early_updates_with_employee(from_date,to_date,employee)
    mark_att_present_with_employee(from_date,to_date,employee)
    remove_duplicate_attendance_with_employee(from_date, to_date, employee)
    return "ok"
@frappe.whitelist()
def mark_att_with_employee(from_date,to_date,employee):
    checkins = frappe.db.sql("""select * from `tabEmployee Checkin` where date(time) between '%s' and '%s' and employee = '%s' order by time  """%(from_date,to_date,employee),as_dict=True)
    for c in checkins:
        # print("Welcome to Employeee Checkin")
        employee_data = frappe.db.exists('Employee',{'status':'Active','date_of_joining':['<=',from_date],'name':c.employee})
        if employee_data:
            mark_attendance_from_checkin(c.name,c.employee,c.time,c.log_type)
    mark_absent_with_employee(from_date,to_date,employee)
    mark_wh_ot_with_employee_updates(from_date,to_date,employee) 
    update_overtime_list_with_employee(from_date,to_date,employee)
    # get_ot_compensation(from_date,to_date)   
    assigned_shift_with_employee(from_date,to_date,employee) 
    shift_matched_with_employee(from_date,to_date,employee)
    att_shift_status_updation_with_employee(from_date,to_date,employee)
    mark_late_early_updates_with_employee(from_date,to_date,employee)
    mark_att_present_with_employee(from_date,to_date,employee)
    update_status_on_leave_employee(from_date,to_date,employee)
    # remove_duplicate_attendance_with_employee(from_date, to_date, employee)
    return "ok"


@frappe.whitelist()
def mark_att_with_employee_shift(from_date,to_date,employee):
    checkins = frappe.db.sql("""select * from `tabEmployee Checkin` where date(time) between '%s' and '%s' and employee = '%s' order by time  """%(from_date,add_days(to_date, 1),employee),as_dict=True)
    for c in checkins:
        # print("Welcome to Employeee Checkin")
        employee_data = frappe.db.exists('Employee',{'status':'Active','date_of_joining':['<=',from_date],'name':c.employee})
        if employee_data:
            mark_attendance_from_checkin(c.name,c.employee,c.time,c.log_type)
    mark_absent_with_employee(from_date,to_date,employee)
    mark_wh_ot_with_employee_updates(from_date,to_date,employee) 
    update_overtime_list_with_employee(from_date,to_date,employee)
    # get_ot_compensation(from_date,to_date)   
    assigned_shift_with_employee(from_date,to_date,employee) 
    shift_matched_with_employee(from_date,to_date,employee)
    att_shift_status_updation_with_employee(from_date,to_date,employee)
    mark_late_early_updates_with_employee(from_date,to_date,employee)
    mark_att_present_with_employee(from_date,to_date,employee)
    update_status_on_leave_employee(from_date,to_date,employee)
    # remove_duplicate_attendance_with_employee(from_date, to_date, employee)
    return "ok"



@frappe.whitelist()
def mark_att():
    from_date = add_days(today(),-1)  
    to_date = today()
    # from_date = '2026-09-11'
    # to_date = '2026-09-12'
    checkins = frappe.db.sql("""select * from `tabEmployee Checkin` where date(time) between '%s' and '%s' order by time  """%(from_date,to_date),as_dict=True)
    for c in checkins:
        employee = frappe.db.exists('Employee',{'status':'Active','date_of_joining':['<=',from_date],'name':c.employee})
        if employee:
            mark_attendance_from_checkin(c.name,c.employee,c.time,c.log_type)
    mark_absent(from_date,to_date)
    mark_wh_ot(from_date,to_date)  
    update_overtime_list(from_date,to_date) 
    get_ot_compensation(from_date,to_date)   
    att_shift_status_updation(from_date,to_date)
    assigned_shift(from_date,to_date) 
    shift_matched(from_date,to_date)
    mark_late_early_updates(from_date,to_date)
    mark_att_present(from_date,to_date)
    update_status_on_leave(from_date,to_date)
    remove_duplicate_attendance(from_date, to_date)
    return "ok" 

@frappe.whitelist()
def update_status_on_leave(from_date,to_date):
    att=frappe.db.get_all("Attendance",{'attendance_date':('between',(from_date,to_date)),'leave_type':['!=',''],'docstatus':['!=',2]},['name'])
    for a in att:
        doc=frappe.get_doc("Attendance",a.name)
        if doc.leave_type and doc.leave_application and doc.status!="On Leave":
            if frappe.db.exists("Leave Application",{'name':doc.leave_application}):
                leave=frappe.get_doc("Leave Application",doc.leave_application)
                if leave.half_day==0:
                    frappe.db.get_value("Attendance",doc.name,'status','On Leave')
                    # doc.status='On Leave'
                else:
                    if leave.from_date==leave.to_date:
                        frappe.db.get_value("Attendance",doc.name,'status','Half Day')
                        # doc.status='Half Day'
                    else:
                        if leave.half_day_date==doc.attendance_date:
                            frappe.db.get_value("Attendance",doc.name,'status','Half Day')
                            # doc.status='Half Day'
                        else:
                            frappe.db.get_value("Attendance",doc.name,'status','On Leave')
                            # doc.status='On Leave'
        

@frappe.whitelist()
def update_status_on_leave_employee(from_date,to_date,employee):
    att=frappe.db.get_all("Attendance",{'employee':employee,'attendance_date':('between',(from_date,to_date)),'leave_type':['!=',''],'docstatus':['!=',2]},['name'])
    for a in att:
        doc=frappe.get_doc("Attendance",a.name)
        if doc.leave_type and doc.leave_application and doc.status!="On Leave":
            if frappe.db.exists("Leave Application",{'name':doc.leave_application}):
                leave=frappe.get_doc("Leave Application",doc.leave_application)
                if leave.half_day==0:
                    frappe.db.get_value("Attendance",doc.name,'status','On Leave')
                else:
                    if leave.from_date==leave.to_date:
                        frappe.db.get_value("Attendance",doc.name,'status','Half Day')
                    else:
                        if leave.half_day_date==doc.attendance_date:
                            frappe.db.get_value("Attendance",doc.name,'status','Half Day')
                        else:
                            frappe.db.get_value("Attendance",doc.name,'status','On Leave')
        doc.save()
@frappe.whitelist()   
def mark_attendance_from_checkin(checkin,employee,time,log_type):
    att_date = time.date()
    att_time = time.time()
    shift = ''
    print(employee)
    print(att_date)
    if log_type == 'IN':
        min_in_time = ''
        max_in_time = ''
        min_in_time1 = datetime.strptime('07:00', '%H:%M').time()
        max_in_time1 = datetime.strptime('13:00', '%H:%M').time()
        min_in_time2 = datetime.strptime('15:00', '%H:%M').time()
        max_in_time2 = datetime.strptime('21:00', '%H:%M').time()
        min_in_time3 = datetime.strptime('01:00', '%H:%M').time()
        max_in_time3 = datetime.strptime('05:00', '%H:%M').time()
        if max_in_time1 >= att_time >= min_in_time1:
            shift = '1'
            min_in_time = datetime.strptime('07:00', '%H:%M').time()
            max_in_time = datetime.strptime('15:00', '%H:%M').time()
        elif max_in_time2 >= att_time >= min_in_time2:
            shift = '2' 
            min_in_time = datetime.strptime('15:00', '%H:%M').time()
            max_in_time = datetime.strptime('21:00', '%H:%M').time()
        elif max_in_time3 > att_time >= min_in_time3:
            shift = '3'  
            min_in_time = datetime.strptime('01:00', '%H:%M').time()
            max_in_time = datetime.strptime('05:00', '%H:%M').time()  
            add_date = add_days(att_date,-1)
        if min_in_time and max_in_time:
            att = frappe.db.exists('Attendance',{"employee":employee,'attendance_date':att_date,'docstatus':['!=','2']})   
            if not att:
                if shift != '3':
                    checkins = frappe.db.sql(""" select name,time from `tabEmployee Checkin` where employee = '%s' and log_type = 'IN' and date(time) = '%s' and time(time) between '%s' and '%s'  order by time """%(employee,att_date,min_in_time,max_in_time),as_dict=True)
                else:
                    yesterday = add_days(att_date,1) 
                    checkins = frappe.db.sql(""" select name,time from `tabEmployee Checkin` where employee = '%s' and log_type = 'IN' and date(time) = '%s' and time(time) between '%s' and '%s' order by time """%(employee,yesterday,min_in_time,max_in_time),as_dict=True)
                if checkins:
                    try:
                        if not frappe.db.exists('Restriction',{'employee':employee,'restricted_date':att_date,'docstatus':1}):
                            att = frappe.new_doc("Attendance")
                            att.employee = employee
                            att.attendance_date = att_date
                            att.shift = shift
                            att.status = 'Absent'
                            att.in_time = checkins[0].time
                            att.working_total_hours = '00:00'
                            att.extra_hours = '00:00'
                            att.late_entry_time='00:00'
                            att.early_out_time='00:00'
                            att.save(ignore_permissions=True)
                            frappe.db.commit()
                            frappe.db.set_value('Employee Checkin',checkins[0].name,'skip_auto_attendance','1')
                            frappe.db.set_value('Employee Checkin',checkins[0].name,'attendance',att.name)
                            return att
                    except:
                        frappe.log_error(title="Restriction",message="Please Check Restriction on %s that Employee %s"%(att_date,employee))    
            else:
                if shift != '3':
                    checkins = frappe.db.sql("select name,time from `tabEmployee Checkin` where employee = '%s' and log_type = 'IN' and date(time) = '%s' and time(time) between '%s' and '%s' order by time "%(employee,att_date,min_in_time,max_in_time),as_dict=True)
                else:
                    yesterday = add_days(att_date,1)
                    checkins = frappe.db.sql("select name,time from `tabEmployee Checkin` where employee = '%s' and log_type = 'IN' and date(time) = '%s' and time(time) between '%s' and '%s' order by time "%(employee,yesterday,min_in_time,max_in_time),as_dict=True)
                if checkins:
                    att = frappe.get_doc("Attendance",att)
                    
                    if att.docstatus != 2:
                        # # att.employee = employee
                        # # att.attendance_date = att_date
                        # if att.in_time and att.in_time>checkins[0].time:
                        #     att.in_time = checkins[0].time
                        #     att.shift = shift
                        # elif not att.in_time:
                        #     att.in_time = checkins[0].time
                        #     att.shift = shift
                        # att.extra_hours = '00:00'
                        # att.late_entry_time='00:00'
                        # att.early_out_time='00:00'
                        if att.in_time and att.in_time>checkins[0].time:
                            frappe.db.set_value("Attendance",att.name, "in_time", checkins[0].time)
                            frappe.db.set_value("Attendance",att.name, "shift", shift)
                        elif not att.in_time:    
                            frappe.db.set_value("Attendance",att.name, "in_time", checkins[0].time)
                            frappe.db.set_value("Attendance",att.name, "shift", shift)
                        frappe.db.set_value("Attendance",att.name, "extra_hours", '00:00')
                        frappe.db.set_value("Attendance",att.name, "late_entry_time", '00:00')
                        frappe.db.set_value("Attendance",att.name, "early_out_time", '00:00')
                        # att.save(ignore_permissions=True)
                        # frappe.db.commit()
                        frappe.db.set_value('Employee Checkin',checkins[0].name,'skip_auto_attendance','1')
                        frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
                        return att
    if log_type == 'OUT':
        # print(checkin)
        max_out = datetime.strptime('08:30','%H:%M').time()
        if att_time < max_out:
            # print('Update yesterday Att or Todat Att')
            yesterday = add_days(att_date,-1)
            today_att = frappe.db.exists("Attendance",{'employee':employee,'attendance_date':att_date,'docstatus':('!=',2)})
            if today_att:
                today_att = frappe.get_doc("Attendance",today_att)
                if today_att and today_att.in_time:
                    max_out_checkin = today_att.in_time.time()
                    yesterday_checkins = frappe.db.sql("""select name,time from `tabEmployee Checkin` where employee = "%s" and log_type = 'OUT' and date(time) = '%s' and time(time) < '%s' order by time  """%(employee,att_date,max_out_checkin),as_dict=True)
                    today_checkins = frappe.db.sql("""select name,time from `tabEmployee Checkin` where employee = "%s" and log_type = 'OUT' and date(time) = '%s' and time(time) > '%s' order by time  """%(employee,att_date,max_out_checkin),as_dict=True)
                    if yesterday_checkins and checkin in [check['name'] for check in yesterday_checkins]:
                        checkins = frappe.db.sql("""select name,time from `tabEmployee Checkin` where employee = "%s" and log_type = 'OUT' and date(time) = '%s' and time(time) < '%s' order by time  """%(employee,att_date,max_out_checkin),as_dict=True)
                        att = frappe.db.exists('Attendance',{'employee':employee,'docstatus':('!=','2'),'attendance_date':yesterday})
                        attendance_date = yesterday
                    elif today_checkins and checkin in [check['name'] for check in today_checkins]:
                        checkins = frappe.db.sql("""select name,time from `tabEmployee Checkin` where employee = "%s" and log_type = 'OUT' and date(time) = '%s' and time(time) > '%s' order by time  """%(employee,att_date,max_out_checkin),as_dict=True)
                        att = frappe.db.exists('Attendance',{'employee':employee,'docstatus':('!=','2'),'attendance_date':att_date})
                        attendance_date = att_date
                    else:
                        max_out_checkin = datetime.strptime('08:30','%H:%M').time()
                        checkins = frappe.db.sql("""select * from `tabEmployee Checkin` where employee = '%s' and log_type = 'OUT' and date(time) = '%s' and TIME(time) < '%s'  order by time ASC """%(employee,att_date,max_out_checkin),as_dict=True)
                        att = frappe.db.exists('Attendance',{'employee':employee,'docstatus':('!=','2'),'attendance_date':yesterday})
                        attendance_date = yesterday
                else:
                    # If the employee have the attendance and the employee does not have In Punch for today, and the out punch time is before 8:30 AM,
                    # update the out punch to reflect yesterday's attendance.
                    max_out_checkin = datetime.strptime('08:30','%H:%M').time()
                    checkins = frappe.db.sql("""select * from `tabEmployee Checkin` where employee = '%s' and log_type = 'OUT' and date(time) = '%s' and TIME(time) < '%s'  order by time ASC """%(employee,att_date,max_out_checkin),as_dict=True)
                    att = frappe.db.exists('Attendance',{'employee':employee,'docstatus':('!=','2'),'attendance_date':yesterday})
                    attendance_date = yesterday
            else:
                # If today is a holiday and the employee does not have attendance for today, and the out punch time is before 8:30 AM,
                # update the out punch to reflect yesterday's attendance.
                max_out_checkin = datetime.strptime('08:30','%H:%M').time()
                checkins = frappe.db.sql("""select * from `tabEmployee Checkin` where employee = '%s' and log_type = 'OUT' and date(time) = '%s' and TIME(time) < '%s'  order by time ASC """%(employee,att_date,max_out_checkin),as_dict=True)
                att = frappe.db.exists('Attendance',{'employee':employee,'docstatus':('!=','2'),'attendance_date':yesterday})
                attendance_date = yesterday
            # yesterday = add_days(att_date,-1)
            # checkins = frappe.db.sql("select name,time from `tabEmployee Checkin` where employee = '%s' and log_type = 'OUT' and date(time) = '%s' and time(time) < '%s' order by time "%(employee,att_date,max_out),as_dict=True)
            # att = frappe.db.exists("Attendance",{'employee':employee,'attendance_date':yesterday})
            if att:
                att = frappe.get_doc("Attendance",att)
                if att.docstatus != 2:
                    if checkins:
                        if len(checkins) > 0:
                            frappe.db.set_value("Attendance",att.name, "out_time",checkins[-1].time)
                            if not att.shift:
                                frappe.db.set_value("Attendance",att.name, "shift",get_actual_shift(get_time(checkins[-1].time)))
                            frappe.db.set_value('Employee Checkin',checkins[-1].name,'skip_auto_attendance','1')
                            frappe.db.set_value("Employee Checkin",checkins[-1].name, "attendance", att.name)
                        else:
                            frappe.db.set_value("Attendance",att.name, "out_time",checkins[0].time)

                            if not att.shift:
                                frappe.db.set_value("Attendance",att.name, "shift",get_actual_shift(get_time(checkins[0].time)))
                            frappe.db.set_value('Employee Checkin',checkins[0].name,'skip_auto_attendance','1')
                            frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)   
                        frappe.db.commit()
                        return att
                    else:
                        return att
                else:
                    return att
            else:
                try: 
                    if not frappe.db.exists('Restriction',{'employee':employee,'restricted_date':attendance_date,'docstatus':1}):
                        att = frappe.new_doc("Attendance")
                        att.employee = employee
                        att.attendance_date = attendance_date
                        att.status = 'Absent'
                        att.late_entry_time='00:00:00'
                        att.early_out_time='00:00:00'
                        if checkins:
                            if len(checkins) > 0:
                                att.out_time = checkins[-1].time
                                att.shift = get_actual_shift(get_time(checkins[-1].time))
                                frappe.db.set_value('Employee Checkin',checkins[-1].name,'skip_auto_attendance','1')
                                frappe.db.set_value("Employee Checkin",checkins[-1].name, "attendance", att.name)
                            else:
                                att.out_time = checkins[0].time
                                att.shift = get_actual_shift(get_time(checkins[0].time))
                                frappe.db.set_value('Employee Checkin',checkins[0].name,'skip_auto_attendance','1')
                                frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
                            att.save(ignore_permissions=True)
                            frappe.db.commit()
                            
                            return att
                        else:
                            return att
                except:
                    frappe.log_error(title="Restriction",message="Please Check Restriction on %s that Employee %s"%(yesterday,employee))
     
        else:
            checkins = frappe.db.sql("select name,time,docstatus from `tabEmployee Checkin` where employee ='%s' and log_type = 'OUT' and date(time) = '%s' order by time "%(employee,att_date),as_dict=True)
            att = frappe.db.exists("Attendance",{'employee':employee,'attendance_date':att_date})
            if att:
                att = frappe.get_doc("Attendance",att)
                if att.docstatus != 2:
                    if checkins:
                        if len(checkins) > 0:
                            att.out_time = checkins[-1].time
                            frappe.db.set_value('Employee Checkin',checkins[-1].name,'skip_auto_attendance','1')
                            frappe.db.set_value("Employee Checkin",checkins[-1].name, "attendance", att.name)
                        else:
                            att.out_time = checkins[0].time
                            frappe.db.set_value('Employee Checkin',checkins[0].name,'skip_auto_attendance','1')
                            frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
                        if not att.shift:
                            if len(checkins) > 0:
                                att.out_time = checkins[-1].time
                                att.shift = get_actual_shift(get_time(checkins[-1].time))
                        # att.save(ignore_permissions=True)
                        # frappe.db.commit()
                        frappe.db.set_value("Attendance",att.name, "out_time",checkins[-1].time)
                       
                        return att
                    else:
                        return att
                else:
                    return att
            else:
                try: 
                    if not frappe.db.exists('Restriction',{'employee':employee,'restricted_date':att_date,'docstatus':1}):
                        att = frappe.new_doc("Attendance")
                        att.employee = employee
                        att.attendance_date = att_date
                        att.shift = shift
                        att.status = 'Absent'
                        att.late_entry_time='00:00:00'
                        att.early_out_time='00:00:00'
                        if checkins:
                            if len(checkins) > 0:
                                att.out_time = checkins[-1].time
                                att.shift = get_actual_shift(get_time(checkins[-1].time))
                                frappe.db.set_value('Employee Checkin',checkins[-1].name,'skip_auto_attendance','1')
                                frappe.db.set_value("Employee Checkin",checkins[-1].name, "attendance", att.name)
                            else:
                                att.out_time = checkins[0].time
                                att.shift = get_actual_shift(get_time(checkins[0].time))
                                frappe.db.set_value('Employee Checkin',checkins[0].name,'skip_auto_attendance','1')
                                frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
                            att.save(ignore_permissions=True)
                            frappe.db.commit()
                            
                            return att  
                except:
                    frappe.log_error(title="Restriction",message="Please Check Restriction on %s that Employee %s"%(att_date,employee))
     

@frappe.whitelist()
def is_between(time, time_range):
    if time_range[1] < time_range[0]:
        return time >= time_range[0] or time <= time_range[1]
    return time_range[0] <= time <= time_range[1]

@frappe.whitelist()
def get_actual_shift(get_shift_time):
    from datetime import datetime
    from datetime import date, timedelta,time
    nowtime = datetime.now()
    shift_1_time = [time(hour=13, minute=1, second=0),time(hour=17, minute=30, second=0)]
    shift_2_time = [time(hour=19, minute=1, second=0),time(hour=2, minute=0, second=0)]

    shift_3_time = [time(hour=6, minute=50, second=0),time(hour=8, minute=50, second=0)]
    shift = ''
    if is_between(get_shift_time,shift_1_time):
        shift = '1'
    if is_between(get_shift_time,shift_2_time):
        shift = '2'
    if is_between(get_shift_time,shift_3_time):
        shift = '3'
    return shift   

@frappe.whitelist()
def mark_absent(from_date,to_date):
    dates = [from_date,to_date]
    for date in dates:
        employee = frappe.db.get_all('Employee',{'status':'Active','date_of_joining':['<=',from_date]})
        for emp in employee:
            hh = check_holiday(date,emp.name)
            if not hh:
                if not frappe.db.exists('Attendance',{'attendance_date':date,'employee':emp.name,'docstatus':('!=','2')}):
                    try:
                        if not frappe.db.exists('Restriction',{'employee':emp.name,'restricted_date':date,'docstatus':1}):
                            att = frappe.new_doc("Attendance")
                            att.employee = emp.name
                            att.status = 'Absent'
                            att.attendance_date = date
                            att.total_working_hours = "0.0"
                            att.over_time_hours = "0.0"
                            att.working_total_hours = "00:00"
                            att.over_time_hours = "0.0"
                            att.extra_hours = "00:00:00"
                            att.att_in_time = "00:00:00"
                            att.att_out_time = "00:00:00"
                            att.late_entry_time='00:00:00'
                            att.early_out_time='00:00:00'
                            att.save(ignore_permissions=True)
                            frappe.db.commit()
                    except:
                        frappe.log_error(title="Restriction",message="Please Check Restriction on %s that Employee %s"%(date,emp.name))

@frappe.whitelist()
def check_holiday(date, emp):
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
        else:
            return "HH"
    return None





@frappe.whitelist()
def mark_wh_ot(from_date,to_date):
    attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2')},['*'])
    for att in attendance:
        od_hours = 0
        if att.on_duty_application:
            od_hours = frappe.db.get_value("On Duty Application",{'name':att.on_duty_application},["total_od_hours"])
            if od_hours:
                od_hours=int(od_hours)
            else:
                od_hours=0
        if att.in_time and att.out_time and att.shift:
            hh = check_holiday(att.attendance_date,att.employee)
            if not hh:
                if att.out_time < att.in_time:
                    total_wh= "00:00"
                else:
                    total_wh= att.out_time -att.in_time
                ftr = [3600,60,1]
                if att.out_time < att.in_time:
                    wh = 0
                else:
                    wh = time_diff_in_hours(att.out_time,att.in_time)
                perm_time=0
                wh += od_hours
                if wh < 4:
                    if att.permission:
                        perm=frappe.db.get_value("Permission Request",{'name':att.permission},['permission_hour'])
                        if perm:
                            perm=int(perm)
                        else:
                            perm=0
                        perm_time=wh+perm
                        if perm_time >= 4:
                            frappe.db.set_value('Attendance',att.name,'status','Half Day')
                        else:
                            frappe.db.set_value('Attendance',att.name,'status','Absent')
                    else:
                        frappe.db.set_value('Attendance',att.name,'status','Absent')
                    if att.leave_application:
                        leave=frappe.db.get_value("Leave Application",{'name':att.leave_application,'half_day':1,'docstatus':'1','half_day_date':att.attendance_date},['name'])
                        if leave:
                            frappe.db.set_value('Attendance',att.name,'status','Half Day')
                        else:
                            frappe.db.set_value('Attendance',att.name,'status','Absent')
                    else:
                        frappe.db.set_value('Attendance',att.name,'status','Absent')
                elif wh >= 4 and wh < 8:
                    if att.permission:
                        perm=frappe.db.get_value("Permission Request",{'name':att.permission},['permission_hour'])
                        if perm:
                            perm=int(perm)
                        else:
                            perm=0
                        perm_time=wh+perm
                        if perm_time >= 8:
                            frappe.db.set_value('Attendance',att.name,'status','Present')
                        else:
                            frappe.db.set_value('Attendance',att.name,'status','Half Day')
                    else:
                        frappe.db.set_value('Attendance',att.name,'status','Half Day')
                elif wh >= 8:
                    frappe.db.set_value('Attendance',att.name,'status','Present')   
                if att.out_time < att.in_time:
                    wh = 0
                else:
                    wh = time_diff_in_hours(att.out_time,att.in_time)
                shift_start_time = frappe.db.get_value('Shift Type',{'name':att.shift},['start_time'])
                shift_start_time = pd.to_datetime(str(shift_start_time)).time()

                shift_end_time = frappe.db.get_value('Shift Type',{'name':att.shift},['end_time'])
                shift_end_time = pd.to_datetime(str(shift_end_time)).time()

                in_date = att.in_time.date()
                out_date = att.out_time.date()
                get_shift_hours = frappe.db.get_value('Shift Type',{'name':att.shift},['total_shift_hours'])
                total_shift_hours = datetime.strptime(str(get_shift_hours),'%Y-%m-%d %H:%M:%S').time()
                shift_hr = sum([a*b for a,b in zip(ftr, map(int,str(total_shift_hours).split(':')))])
                shift_wh = round(shift_hr/3600,1) 
                shift_start_datetime = datetime.combine(in_date,shift_start_time)
                shift_end_datetime = datetime.combine(att.attendance_date,shift_end_time)
                if att.shift=='2':
                    next_day = add_days(att.attendance_date,1)
                    shift_end_datetime = datetime.combine(next_day,shift_end_time)
                if int(wh) > int(shift_wh):
                    extra_hrs =pd.to_datetime('00:00:00').time()
                    ot_hr = 0
                    try:
                        extra_hrs = att.out_time - shift_end_datetime
                        hr = sum([a*b for a,b in zip(ftr, map(int,str(extra_hrs).split(':')))])
                        extras = round(hr/3600,1)
                    except:
                        extra_hrs = '00:00' 
                        extras = 0 
                    if extras > 1:
                            ot_hr = math.floor(extras * 2) / 2  
                    if wh < 24:
                        frappe.db.set_value('Attendance',att.name,'working_total_hours',total_wh)             
                        frappe.db.set_value('Attendance',att.name,'total_working_hours',round(wh,2))                
                        frappe.db.set_value('Attendance',att.name,'extra_hours',extra_hrs)
                        frappe.db.set_value('Attendance',att.name,'over_time_hours',ot_hr)
                    else:
                        frappe.db.set_value('Attendance',att.name,'working_total_hours','23:59')             
                        frappe.db.set_value('Attendance',att.name,'total_working_hours',round(wh,2))                
                        frappe.db.set_value('Attendance',att.name,'extra_hours',extra_hrs)
                        frappe.db.set_value('Attendance',att.name,'over_time_hours',ot_hr)
                else:
                    if wh > 24:
                        none_time = pd.to_datetime('00:00:00').time()
                        frappe.db.set_value('Attendance',att.name,'working_total_hours','23:59')
                        frappe.db.set_value('Attendance',att.name,'total_working_hours',round(wh,2))  
                        frappe.db.set_value('Attendance',att.name,'extra_hours','00:00')
                        frappe.db.set_value('Attendance',att.name,'over_time_hours',0)
                    else:
                        none_time = pd.to_datetime('00:00:00').time()
                        frappe.db.set_value('Attendance',att.name,'working_total_hours',total_wh)
                        frappe.db.set_value('Attendance',att.name,'total_working_hours',round(wh,2))  
                        frappe.db.set_value('Attendance',att.name,'extra_hours','00:00')
                        frappe.db.set_value('Attendance',att.name,'over_time_hours',0)
            else:
                if att.out_time < att.in_time:
                    frappe.log_error(message=att.name, title="Attendance")
                    total_wh="00:00"
                else:
                    total_wh= att.out_time - att.in_time
                ftr = [3600,60,1]
                max_time = timedelta(hours=23, minutes=59)
                if total_wh < max_time:
                    hr = sum([a*b for a,b in zip(ftr, map(int,str(total_wh).split(':')))])
                    wh = round(hr/3600,1)
                else:
                    wh = round(total_wh.total_seconds() / 3600, 1)
                perm_time=0
                wh += od_hours
                if wh < 4:
                    if att.permission:
                        perm=frappe.db.get_value("Permission Request",{'name':att.permission},['permission_hour'])
                        perm=int(perm)
                        perm_time=wh+perm
                        if perm_time >= 4:
                            frappe.db.set_value('Attendance',att.name,'status','Half Day')
                        else:
                            frappe.db.set_value('Attendance',att.name,'status','Absent')
                    else:
                        frappe.db.set_value('Attendance',att.name,'status','Absent')
                elif wh >= 4 and wh < 8:
                    if att.permission:
                        perm=frappe.db.get_value("Permission Request",{'name':att.permission},['permission_hour'])
                        if perm:
                            perm=int(perm)
                        else:
                            perm=0
                        perm_time=wh+perm
                        if perm_time >= 8:
                            frappe.db.set_value('Attendance',att.name,'status','Present')
                        else:
                            frappe.db.set_value('Attendance',att.name,'status','Half Day')
                    else:
                        frappe.db.set_value('Attendance',att.name,'status','Half Day')
                elif wh >= 8:
                    frappe.db.set_value('Attendance',att.name,'status','Present')  
                if total_wh < max_time:
                    hr = sum([a*b for a,b in zip(ftr, map(int,str(total_wh).split(':')))])
                    wh = round(hr/3600,1)
                else:
                    wh = round(total_wh.total_seconds() / 3600, 1)
                if wh < 24:
                    ot_hr = (math.floor(wh * 2) / 2) - 0.5
                    if ot_hr >= 9:
                        ot_hr = ot_hr - 1
                        # total_wh_time = total_wh - timedelta(hours=1) 
                        # total_wh = str(total_wh_time)
                    frappe.db.set_value('Attendance',att.name,'over_time_hours',ot_hr)
                    none_time =pd.to_datetime('00:00:00').time()
                    frappe.db.set_value('Attendance',att.name,'extra_hours','00:00')
                    frappe.db.set_value('Attendance',att.name,'working_total_hours',total_wh)
                    frappe.db.set_value('Attendance',att.name,'total_working_hours',round(wh,2))
                elif wh >= 24:
                    ot_hr = (math.floor(wh * 2) / 2) - 0.5
                    ot_hr = ot_hr - 1
                    frappe.db.set_value('Attendance',att.name,'over_time_hours',ot_hr)
                    none_time =pd.to_datetime('00:00:00').time()
                    frappe.db.set_value('Attendance',att.name,'extra_hours','00:00')
                    frappe.db.set_value('Attendance',att.name,'working_total_hours','23:59')
                    frappe.db.set_value('Attendance',att.name,'total_working_hours',round(wh,2))
                else:
                    none_time =pd.to_datetime('00:00:00').time()
                    frappe.db.set_value('Attendance',att.name,'over_time_hours',0)
                    frappe.db.set_value('Attendance',att.name,'extra_hours','00:00')
                    frappe.db.set_value('Attendance',att.name,'working_total_hours','00:00')
                    frappe.db.set_value('Attendance',att.name,'total_working_hours',0)   
        else:
            none_time =pd.to_datetime('00:00:00').time()
            frappe.db.set_value('Attendance',att.name,'extra_hours','00:00')
            frappe.db.set_value('Attendance',att.name,'working_total_hours','00:00')
        if att.on_duty_application and ((not att.in_time and not att.out_time) or (att.in_time and not att.out_time) or (att.out_time and not att.in_time ) and att.shift):
            perm=0
            wh = att.total_working_hours
            if att.permission:
                perm=frappe.db.get_value("Permission Request",{'name':att.permission},['permission_hour'])
                if perm:
                    perm=int(perm)
                else:
                    perm=0
            od_hours = frappe.db.get_value("On Duty Application",{'name':att.on_duty_application},["total_od_hours"])
            if od_hours:
                od_hours=int(od_hours)
            else:
                od_hours=0
            od_time=wh+od_hours+perm
            if od_time >= 8:
                frappe.db.set_value('Attendance',att.name,'status','Present')
            elif od_time >= 4 and od_time < 8:
                frappe.db.set_value('Attendance',att.name,'status','Half Day')
            else:
                frappe.db.set_value('Attendance',att.name,'status','Absent')





@frappe.whitelist()
def permission_request(from_date,to_date):
    year_start = date(date.today().year, 1, 1)
    year_end = date(date.today().year, 12, 31)
    month_start_date =  from_date + dateutil.relativedelta.relativedelta(months=-1)
    payroll_start_date = add_days(get_first_day(month_start_date),20)
    payroll_end_date = add_days(get_first_day(from_date),19)
    attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2')},['in_time','shift','employee','attendance_date'])  
    if attendance:
        for att in attendance:
            if frappe.db.exists('Permission Request',{'permission_date':('between',(payroll_start_date,payroll_end_date)),'employee_id':att.employee,'docstatus':0}):
                per_count = frappe.db.count('Permission Request',{'permission_date':('between',(payroll_start_date,payroll_end_date)),'employee_id':att.employee,'docstatus':0})
                if per_count >= 2:
                    if att.in_time:
                        shift_start_time = frappe.db.get_value('Shift Type',{'name':att.shift},['start_time'])
                        shift_start_time = pd.to_datetime(str(shift_start_time)).time()
                        in_date = att.in_time.date()
                        shift_start_datetime = datetime.combine(in_date,shift_start_time)
                        att_in_time = datetime.strptime(str(att.in_time),'%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S')
                        att_shift_time = datetime.strptime(str(shift_start_time),'%H:%M:%S').strftime('%H:%M:%S')
                        if  att_in_time > att_shift_time:
                            late = att.in_time - shift_start_datetime
                            late_5_mins = timedelta(hours=0,minutes=5,seconds=0)
                            late_5_hr = timedelta(hours=5,minutes=0,seconds=0)
                            leave_allocation = frappe.db.exists('Leave Allocation',{'employee':att.employee,'from_date':('between',(year_start,year_end)),'docstatus':0})
                            if leave_allocation:
                                leave_type = frappe.db.get_value('Leave Allocation',{'name':leave_allocation,'docstatus':0},['leave_type'])
                                leave_allocation_count = frappe.db.get_value('Leave Allocation',{'name':leave_allocation,'docstatus':0},['new_leaves_allocated'])
                                leave_application_count = frappe.db.count('Leave Application',{'employee':att.employee,'from_date':('between',(year_start,year_end)),'leave_type':leave_type,'docstatus':0 })
                                balance_leaves = leave_allocation_count - leave_application_count
                                leave_approver = ''
                                if late > late_5_mins and late < late_5_hr:
                                    leave_approver = frappe.db.get_value('Employee',{'status':'Active','employee':att.employee},['leave_approver'])
                                    if leave_type == "Casual Leave" and balance_leaves > 0:
                                        new_leave_application = frappe.new_doc('Leave Application')
                                        new_leave_application.employee = att.employee
                                        new_leave_application.leave_type = 'Casual Leave'
                                        new_leave_application.from_date = att.attendance_date
                                        new_leave_application.to_date = att.attendance_date
                                        new_leave_application.half_day = 1
                                        new_leave_application.status = 'Open'
                                        new_leave_application.description = 'Late By %s'%late
                                        new_leave_application.leave_approver = leave_approver
                                        new_leave_application.save(ignore_permissions=TRUE)
                                        new_leave_application.submit()
                                        frappe.db.commit()
                                    elif leave_type == 'Sick Leave' and balance_leaves > 0 :
                                        new_leave_application = frappe.new_doc('Leave Application')
                                        new_leave_application.employee = att.employee
                                        new_leave_application.leave_type = 'Sick Leave'
                                        new_leave_application.from_date = att.attendance_date
                                        new_leave_application.to_date = att.attendance_date
                                        new_leave_application.half_day = 1
                                        new_leave_application.status = 'Open'
                                        new_leave_application.description = 'Late By %s'%late
                                        new_leave_application.leave_approver = leave_approver
                                        new_leave_application.save(ignore_permissions=TRUE)
                                        new_leave_application.submit()
                                        frappe.db.commit()
                                    elif leave_type == 'Earned Leave' and balance_leaves > 0:
                                        new_leave_application = frappe.new_doc('Leave Application')
                                        new_leave_application.employee = att.employee
                                        new_leave_application.leave_type = 'Earned Leave'
                                        new_leave_application.from_date = att.attendance_date
                                        new_leave_application.to_date = att.attendance_date
                                        new_leave_application.half_day = 1
                                        new_leave_application.status = 'Open'
                                        new_leave_application.description = 'Late By %s'%late
                                        new_leave_application.leave_approver = leave_approver
                                        new_leave_application.save(ignore_permissions=TRUE)
                                        new_leave_application.submit()
                                        frappe.db.commit()
                                    else:
                                        new_leave_application = frappe.new_doc('Leave Application')
                                        new_leave_application.employee = att.employee
                                        new_leave_application.leave_type = 'Leave Without Pay'
                                        new_leave_application.from_date = att.attendance_date
                                        new_leave_application.to_date = att.attendance_date
                                        new_leave_application.half_day = 1
                                        new_leave_application.status = 'Open'
                                        new_leave_application.description = 'Late By %s'%late
                                        new_leave_application.leave_approver = leave_approver
                                        new_leave_application.save(ignore_permissions=TRUE)
                                        new_leave_application.submit()
                                        frappe.db.commit()
                                elif late > late_5_hr:
                                    leave_approver = frappe.db.get_value('Employee',{'status':'Active','employee':att.employee},['leave_approver'])
                                    if leave_type == "Casual Leave" and balance_leaves > 0:
                                        new_leave_application = frappe.new_doc('Leave Application')
                                        new_leave_application.employee = att.employee
                                        new_leave_application.leave_type = 'Casual Leave'
                                        new_leave_application.from_date = att.attendance_date
                                        new_leave_application.to_date = att.attendance_date
                                        new_leave_application.half_day = 1
                                        new_leave_application.status = 'Open'
                                        new_leave_application.description = 'Late By %s'%late
                                        new_leave_application.leave_approver = leave_approver
                                        new_leave_application.save(ignore_permissions=TRUE)
                                        new_leave_application.submit()
                                        frappe.db.commit()
                                    elif leave_type == 'Sick Leave' and balance_leaves > 0 :
                                        new_leave_application = frappe.new_doc('Leave Application')
                                        new_leave_application.employee = att.employee
                                        new_leave_application.leave_type = 'Sick Leave'
                                        new_leave_application.from_date = att.attendance_date
                                        new_leave_application.to_date = att.attendance_date
                                        new_leave_application.half_day = 1
                                        new_leave_application.status = 'Open'
                                        new_leave_application.description = 'Late By %s'%late
                                        new_leave_application.leave_approver = leave_approver
                                        new_leave_application.save(ignore_permissions=TRUE)
                                        new_leave_application.submit()
                                        frappe.db.commit()
                                    elif leave_type == 'Earned Leave' and balance_leaves > 0:
                                        new_leave_application = frappe.new_doc('Leave Application')
                                        new_leave_application.employee = att.employee
                                        new_leave_application.leave_type = 'Earned Leave'
                                        new_leave_application.from_date = att.attendance_date
                                        new_leave_application.to_date = att.attendance_date
                                        new_leave_application.half_day = 1
                                        new_leave_application.status = 'Open'
                                        new_leave_application.description = 'Late By %s'%late
                                        new_leave_application.leave_approver = leave_approver
                                        new_leave_application.save(ignore_permissions=TRUE)
                                        new_leave_application.submit()
                                        frappe.db.commit()
                                    else:
                                        new_leave_application = frappe.new_doc('Leave Application')
                                        new_leave_application.employee = att.employee
                                        new_leave_application.leave_type = 'Leave Without Pay'
                                        new_leave_application.from_date = att.attendance_date
                                        new_leave_application.to_date = att.attendance_date
                                        new_leave_application.half_day = 1
                                        new_leave_application.status = 'Open'
                                        new_leave_application.description = 'Late By %s'%late
                                        new_leave_application.leave_approver = leave_approver
                                        new_leave_application.save(ignore_permissions=TRUE)
                                        new_leave_application.submit()
                                        frappe.db.commit()    
                        else:
                            frappe.log_error('Employee has no late')                
                    else:
                        frappe.log_error ('Employee has no INTIME')                            
                else:
                    if att.in_time:
                        shift_start_time = frappe.db.get_value('Shift Type',{'name':att.shift},['start_time'])
                        shift_start_time = pd.to_datetime(str(shift_start_time)).time()
                        in_date = att.in_time.date()
                        shift_start_datetime = datetime.combine(in_date,shift_start_time)
                        att_in_time = datetime.strptime(str(att.in_time),'%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S')
                        att_shift_time = datetime.strptime(str(shift_start_time),'%H:%M:%S').strftime('%H:%M:%S')
                        if  att_in_time > att_shift_time:
                            late = att.in_time - shift_start_datetime
                            late_time_15_mins = timedelta(hours=0,minutes=15,seconds=0)
                            late_time_1_hr = timedelta(hours=1,minutes=0,seconds=0)
                            if late > late_time_15_mins and late < late_time_1_hr:
                                if att.shift == '1':
                                    from_time = frappe.db.get_value('Shift Type',{'name':'1'},['start_time'])
                                    to_time = timedelta(hours=1) + from_time
                                    permission = frappe.new_doc('Permission Request')
                                    permission.employee_id = att.employee
                                    permission.permission_date = att.attendance_date
                                    permission.shift = att.shift
                                    permission.reason = 'Late By %s'%late
                                    permission.session = 'First Half'
                                    permission.permission_hour = '1'
                                    permission.from_time = from_time
                                    permission.to_time = to_time
                                    permission.save(ignore_permissions=True)
                                    permission.submit()
                                    frappe.db.commit()
                                elif att.shift == '2':
                                    from_time = frappe.db.get_value('Shift Type',{'name':'2'},['start_time'])
                                    to_time = timedelta(hours=1) + from_time
                                    permission = frappe.new_doc('Permission Request')
                                    permission.employee_id = att.employee
                                    permission.permission_date = att.attendance_date
                                    permission.shift = att.shift
                                    permission.reason = 'Late By %s'%late
                                    permission.session = 'First Half'
                                    permission.permission_hour = '1'
                                    permission.from_time = from_time
                                    permission.to_time = to_time
                                    permission.save(ignore_permissions=True)
                                    permission.submit()
                                    frappe.db.commit()
                                elif att.shift == '3':
                                    from_time = frappe.db.get_value('Shift Type',{'name':'3'},['start_time'])
                                    to_time = timedelta(hours=1) + from_time
                                    permission = frappe.new_doc('Permission Request')
                                    permission.employee_id = att.employee
                                    permission.permission_date = att.attendance_date
                                    permission.shift = att.shift
                                    permission.reason = 'Late By %s'%late
                                    permission.session = 'First Half'
                                    permission.permission_hour = '1'
                                    permission.from_time = from_time
                                    permission.to_time = to_time
                                    permission.save(ignore_permissions=True)
                                    permission.submit()
                                    frappe.db.commit()
                                else:
                                    frappe.error_log("No Shift ") 
                            elif  late > late_time_1_hr:
                                if att.shift == '1':
                                    from_time = frappe.db.get_value('Shift Type',{'name':'1'},['start_time'])
                                    to_time = timedelta(hours=2) + from_time
                                    permission = frappe.new_doc('Permission Request')
                                    permission.employee_id = att.employee
                                    permission.permission_date = att.attendance_date
                                    permission.shift = att.shift
                                    permission.reason = 'Late By %s'%late
                                    permission.session = 'First Half'
                                    permission.permission_hour = '1.5'
                                    permission.from_time = from_time
                                    permission.to_time = to_time
                                    permission.save(ignore_permissions=True)
                                    permission.submit()
                                    frappe.db.commit()
                                elif att.shift == '2':
                                    from_time = frappe.db.get_value('Shift Type',{'name':'2'},['start_time'])
                                    to_time = timedelta(hours=2) + from_time
                                    permission = frappe.new_doc('Permission Request')
                                    permission.employee_id = att.employee
                                    permission.permission_date = att.attendance_date
                                    permission.shift = att.shift
                                    permission.reason = 'Late By %s'%late
                                    permission.session = 'First Half'
                                    permission.permission_hour = '1.5'
                                    permission.from_time = from_time
                                    permission.to_time = to_time
                                    permission.save(ignore_permissions=True)
                                    permission.submit()
                                    frappe.db.commit()
                                elif att.shift == '3':
                                    from_time = frappe.db.get_value('Shift Type',{'name':'3'},['start_time'])
                                    to_time = timedelta(hours=2) + from_time
                                    permission = frappe.new_doc('Permission Request')
                                    permission.employee_id = att.employee
                                    permission.permission_date = att.attendance_date
                                    permission.shift = att.shift
                                    permission.reason = 'Late By %s'%late
                                    permission.session = 'First Half'
                                    permission.permission_hour = '1.5'
                                    permission.from_time = from_time
                                    permission.to_time = to_time
                                    permission.save(ignore_permissions=True)
                                    permission.submit()
                                    frappe.db.commit()    
                                else:
                                    frappe.log_error("No Shift")  
                            else:
                                error_msg = [att.employee.att.attendance_date,att.shift,att.in_time]
                                frappe.log_error("No Records",error_msg)   

@frappe.whitelist()
def get_ot_compensation(from_date,to_date):
    attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(from_date,to_date)),'docstatus':0},['*'])
    for att in attendance:
        hh = check_holiday(att.attendance_date,att.employee)
        if hh:
            if hh == "WW":
                if att.grade == 'G-0':
                    grade_g0 = 'Double Wages'
                    frappe.db.set_value('Attendance',att.name,'ot_compensation',grade_g0)
                elif att.grade in ['MG-0','MG-1','MG-2','MG-3']:
                    grade_mg_1_to_3 = 'Double Wages'  
                    frappe.db.set_value('Attendance',att.name,'ot_compensation',grade_mg_1_to_3) 
                elif att.grade in ['MG-4','MG-5','MG-6','MG-7','MG-8','MG-9','MG-10','MG-11']:
                    grade_mg_4_to_11 = 'Compensatory Off'
                    frappe.db.set_value('Attendance',att.name,'ot_compensation',grade_mg_4_to_11) 
                else:
                    frappe.db.set_value('Attendance',att.name,'ot_compensation','')
            elif hh == 'HH':
                if att.grade == 'G-0':
                    grade_g0 = 'Double Wages + Compensatory Off or Triple Wages'   
                    frappe.db.set_value('Attendance',att.name,'ot_compensation',grade_g0)
                elif att.grade in ['MG-0','MG-1','MG-2','MG-3']:
                    grade_mg_1_to_3 = 'Double Wages + Compensatory Off'
                    frappe.db.set_value('Attendance',att.name,'ot_compensation',grade_mg_1_to_3)
                elif att.grade in ['MG-4','MG-5','MG-6','MG-7','MG-8','MG-9','MG-10','MG-11']:
                    grade_mg_4_to_11 = 'Compensatory Off' 
                    frappe.db.set_value('Attendance',att.name,'ot_compensation',grade_mg_4_to_11)
                else:
                    frappe.db.set_value('Attendance',att.name,'ot_compensation','')
            else:
                message = ('No Holiday') 
                frappe.log_error('Holiday List Condition',message)   
        else:
            if att.shift == '1':
                shift_time = frappe.db.get_value('Shift Type',{'name':att.shift},['start_time'])
                shift_start_time = pd.to_datetime(str(shift_time)).time()
                att_date_str = datetime.strptime(str(att.attendance_date),'%Y-%m-%d').date()
                shift_start_datetime = datetime.combine(att_date_str,shift_start_time)
                total_hours = time_diff_in_hours(shift_start_datetime, att.in_time)
                ftr = [3600,60,1]
                try:
                    hr = sum([a*b for a,b in zip(ftr, map(int,str(total_hours).split(':')))])
                    ot_hour = round(hr/3600,1)  
                except:
                    ot_hour = 0     
                if ot_hour >= 2 :
                    if att.grade == 'G-0':
                        grade_g0 = 'Double Wages'
                        frappe.db.set_value('Attendance',att.name,'ot_compensation',grade_g0)
                    elif att.grade in ['MG-0','MG-1','MG-2','MG-3']:
                        grade_mg_1_to_3 = 'Double Wages'  
                        frappe.db.set_value('Attendance',att.name,'ot_compensation',grade_mg_1_to_3)
                    else:
                        grade_nil = 'NIL'      
                        frappe.db.set_value('Attendance',att.name,'ot_compensation',grade_nil)
                elif att.over_time_hours >=2 :
                    if att.grade == 'G-0':
                        grade_g0 = 'Double Wages'
                        frappe.db.set_value('Attendance',att.name,'ot_compensation',grade_g0)
                    elif att.grade in ['MG-0','MG-1','MG-2','MG-3']:
                        grade_mg_1_to_3 = '200 Rupees Allowance'  
                        frappe.db.set_value('Attendance',att.name,'ot_compensation',grade_mg_1_to_3)   
                    else:
                        grade_nil = 'NIL'      
                        frappe.db.set_value('Attendance',att.name,'ot_compensation',grade_nil)       
            elif att.shift == '2':
                if att.over_time_hours >=2 :
                    if att.grade == 'G-0':
                        grade_g0 = 'Double Wages'
                        frappe.db.set_value('Attendance',att.name,'ot_compensation',grade_g0)
                    elif att.grade in ['MG-0','MG-1','MG-2','MG-3']:
                        grade_mg_1_to_3 = 'Double Wages'  
                        frappe.db.set_value('Attendance',att.name,'ot_compensation',grade_mg_1_to_3)
                    else:
                        grade_nil = 'NIL'      
                        frappe.db.set_value('Attendance',att.name,'ot_compensation',grade_nil)   
            else:
                message = ('Shift Based Overtime closed')
            if att.over_time_hours >=3 :
                if att.shift != '3':
                    if att.grade == 'G-0':
                        grade_g0 = 'Double Wages'
                        frappe.db.set_value('Attendance',att.name,'ot_compensation',grade_g0)  
                    elif att.grade in ['MG-0','MG-1','MG-2','MG-3']:
                        grade_mg_1_to_3 = 'Double Wages'  
                        frappe.db.set_value('Attendance',att.name,'ot_compensation',grade_mg_1_to_3)
                    elif att.over_time_hours >=4 and att.over_time_hours <8 :
                        if att.grade in ['MG-4','MG-5','MG-6','MG-7','MG-8','MG-9','MG-10','MG-11']:
                            grade_mg_4_to_11 = 'Half Day Compensatory Off' 
                            frappe.db.set_value('Attendance',att.name,'ot_compensation',grade_mg_4_to_11) 
                        else:
                            message = ('Grade over less than MG-11')
                    elif att.over_time_hours >=8:
                        if att.grade in ['MG-4','MG-5','MG-6','MG-7','MG-8','MG-9','MG-10','MG-11']:
                            grade_mg_4_to_11 = 'Full Day Compensatory Off' 
                            frappe.db.set_value('Attendance',att.name,'ot_compensation',grade_mg_4_to_11)  
                        else:
                            message = ('Grade over less than MG-11')
            else:
                message = ('Overtime Hours lesser than 3 is not run')

@frappe.whitelist()
def att_shift_status(from_date,to_date):
    attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2')},['*'])  
    for att in attendance:
        shift_status = ''
        if att.status == 'Absent':
            if att.in_time and not att.out_time:
                if att.shift:
                    shift_status = str(att.shift) + 'M'
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
                else:
                    shift_status = 'NS/' + 'M'
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
            elif att.out_time and not att.in_time:
                if att.shift:
                    shift_status = 'M' + str(att.shift)
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
                else:
                    shift_status = 'M' + '/NS'
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
            elif att.out_time and att.in_time:
                if att.shift:
                    shift_status = 'AA'
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
                else:
                    shift_status = 'AA'
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
            else:
                shift_status = 'AA'
                frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
        elif att.status == 'Present':
            if att.shift:
                shift_status = str(att.shift)
                frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
            else:
                if att.on_duty_application:
                    shift_status = 'OD'
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
                else:
                    shift_status = 'NS/P'
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
        elif att.status == 'Work From Home':
            shift_status = 'WFH'
            frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
        elif att.status == 'Half Day':
            if att.leave_type:
                shift_status = 'HD/' + status_map.get(att.leave_type,'')
                frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
            else:
                shift_status = 'HD'
                frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
        elif att.status == 'On Leave':
            if att.leave_type:
                shift_status = status_map.get(att.leave_type)
                frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
            else:
                shift_status = 'L'
                frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
    return 'ok'
#update the assigned shift    

@frappe.whitelist()
def assigned_shift(from_date,to_date):
    datalist = []
    data = {}
    attendance = frappe.get_all('Attendance',{'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2')},['*'])
    for att in attendance:
        check_shift = frappe.db.exists('Shift Assignment',{'employee':att.employee,'start_date':att.attendance_date,'docstatus':1})  
        if check_shift:
            get_shift = frappe.get_value('Shift Assignment',{'name':check_shift},['shift_type'])  
            shift_start_time = frappe.get_value('Shift Type',{'name':get_shift},['start_time'])
            shift_end_time = frappe.get_value('Shift Type',{'name':get_shift},['end_time'])
            data.update({
                'get_shift':get_shift,
                'shift_start_time':shift_start_time,
                'shift_end_time':shift_end_time 
            })
            datalist.append(data.copy())
        else: 
            get_shift = 'No Shift Assigned'  
            shift_start_time = datetime.strptime(str('00:00:00'),'%H:%M:%S').strftime('%H:%M')
            shift_end_time = datetime.strptime(str('00:00:00'),'%H:%M:%S').strftime('%H:%M')
            data.update({
                'get_shift':get_shift,
                'shift_start_time':shift_start_time,
                'shift_end_time':shift_end_time 
            })
            datalist.append(data.copy())  
            
        if att.in_time and att.out_time:
            att_in_time = att.in_time
            att_out_time = att.out_time
            att_shift = att.shift or ' '
            data.update({
                'att_shift':att.shift or '-',
                'att_in_time':att_in_time,
                'att_out_time':'att_out_time',
            }) 
            datalist.append(data.copy())  
            frappe.db.set_value('Attendance',att.name,'attended_shift',att_shift or '')
            frappe.db.set_value('Attendance',att.name,'att_in_time',att_in_time)
            frappe.db.set_value('Attendance',att.name,'att_out_time',att_out_time)    
        elif att.in_time and not att.out_time:
            att_in_time = att.in_time 
            att_out_time = None
            att_shift = att.shift or '-'
            data.update({
                'att_shift':att.shift,
                'att_in_time':att_in_time,
                'att_out_time':att_out_time
            })
            datalist.append(data.copy())
            frappe.db.set_value('Attendance',att.name,'attended_shift',att_shift or '')
            frappe.db.set_value('Attendance',att.name,'att_in_time',att_in_time)
            frappe.db.set_value('Attendance',att.name,'att_out_time',att_out_time)    
        elif att.out_time and not att.in_time:
            att_in_time = None
            att_out_time = att.out_time
            att_shift = att.shift or '-'
            data.update({
                'att_shift':att.shift,
                'att_in_time':att_in_time,
                'att_out_time':att_out_time
            })
            datalist.append(data.copy()) 
            frappe.db.set_value('Attendance',att.name,'attended_shift',att_shift or '')
            frappe.db.set_value('Attendance',att.name,'att_in_time',att_in_time)
            frappe.db.set_value('Attendance',att.name,'att_out_time',att_out_time)  
        else:
            if att.on_duty_application:
                od_shift = frappe.db.get_value("On Duty Application",{'name':att.on_duty_application},["shift"])
                frappe.db.set_value('Attendance',att.name,'attended_shift',od_shift or '')
            else:
                att_in_time = None
                att_out_time = None
                att_shift = att.shift or '-'
                frappe.db.set_value('Attendance',att.name,'attended_shift',att_shift or '')
                frappe.db.set_value('Attendance',att.name,'att_in_time',att_in_time)
                frappe.db.set_value('Attendance',att.name,'att_out_time',att_out_time)         
        frappe.db.set_value('Attendance',att.name,'assigned_shift',get_shift)
        frappe.db.set_value('Attendance',att.name,'shift_in_time',shift_start_time)
        frappe.db.set_value('Attendance',att.name,'shift_out_time',shift_end_time)
          
    return "ok"

#checks the assigned shift and attended shift is matched or not    
@frappe.whitelist()   
def shift_matched(from_date,to_date):
    data = {}
    datalist = []
    status = ''
    attendance = frappe.get_all('Attendance',{'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2')},['*'])
    for att in attendance:
        if att.assigned_shift and att.attended_shift:
            if att.assigned_shift == att.attended_shift:
                status = 'Matched'
            else:
                status = 'Unmatched'  
        else:
            status = 'Unmatched'
        data.update({
            'status':status
        }) 
        datalist.append(data.copy())  
        frappe.db.set_value('Attendance',att.name,'shift_matched_or_unmatched',status)   
    absent_for_unmatched_shift(from_date,to_date)
        
#submit the attendance if the status is present
@frappe.whitelist()
def mark_att_present(from_date, to_date):
    attendance_docstatus_0 = frappe.db.get_all('Attendance', {
        'attendance_date': ('between', (from_date, to_date)),'docstatus': ('!=',2)}, ['*'])
    
    for att in attendance_docstatus_0:
        if att.get('status') == 'Present':
            frappe.db.set_value('Attendance', att.get('name'), 'docstatus', 1)
        if att.get('status') == 'On Leave' and att.get('leave_type'):
            frappe.db.set_value('Attendance', att.get('name'), 'docstatus', 1)
          
                      
@frappe.whitelist()
def mark_att_process(from_date, to_date):
    # to_date = from_date
    checkins = frappe.db.sql("""select * from `tabEmployee Checkin` where date(time) between '%s' and '%s' order by time  """%(from_date,to_date),as_dict=True)
    for c in checkins:
        employee = frappe.db.exists('Employee',{'status':'Active','date_of_joining':['<=',from_date],'name':c.employee})
        if employee:
            mark_attendance_from_checkin(c.name,c.employee,c.time,c.log_type)
    mark_absent(from_date,to_date)  
    mark_wh_ot(from_date,to_date)   
    update_overtime_list(from_date,to_date)
    get_ot_compensation(from_date,to_date)   
    att_shift_status_updation(from_date,to_date) 
    assigned_shift(from_date,to_date)
    shift_matched(from_date,to_date)
    mark_late_early_updates(from_date,to_date)
    mark_att_present(from_date,to_date)
    update_status_on_leave(from_date,to_date)
    return "ok"   
    
@frappe.whitelist()
def enqueue_mark_att_process(from_date,to_date):
    frappe.enqueue(
        mark_att_process, # python function or a module path as string
        queue="long", # one of short, default, long
        timeout=80000, # pass timeout manually
        is_async=True, # if this is True, method is run in worker
        now=False, # if this is True, method is run directly (not in a worker) 
        job_name='Attendance Setting Mark Attendance',
        from_date=from_date,
        to_date=to_date,
    ) 
    return 'OK'

@frappe.whitelist()
#checkin cron runs every 7mins
def push_punch():
    from cgi import print_environ
    import mysql.connector
    import requests,json
    from datetime import date
    from datetime import time,datetime

    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Pa55w0rd@",
    database="easytimepro"
    )

    from_date = add_days(today(),-1)  
    to_date = today()

    mycursor = mydb.cursor(dictionary=True)
    query = "SELECT  * FROM iclock_transaction where date(punch_time) between '%s'  and '%s' "%(from_date,to_date)
    mycursor.execute(query)
    attlog = mycursor.fetchall()
    if attlog:
        for a in attlog:
            url = "http://157.245.101.198/api/method/johoku.biometric_checkin.mark_checkin?employee=%s&time=%s&device_id=%s" % (a['emp_code'],a['punch_time'],a['terminal_alias'])
            headers = { 'Content-Type': 'application/json','Authorization': 'token b3df19e9615e0dc:b499d47b3041f94'}
            response = requests.request('GET',url,headers=headers,verify=False)
            res = json.loads(response.text)
            if res:
                if res['message'] == 'Checkin Marked':
                    mycursor = mydb.cursor()
                    sql = "UPDATE iclock_transaction SET checkin_marked = 1 WHERE id = %s " % a['id']
                    mycursor.execute(sql)
                    mydb.commit()   
        return "OK"

@frappe.whitelist()
def delete_urc_automatically():
    from_date = add_days(today(),-35)  
    to_date = add_days(today(),-34)  
    urc = frappe.db.sql("""delete from `tabUnregistered Employee Checkin` where date(biometric_time) between '%s' and '%s'  """%(from_date,to_date),as_dict = True)

@frappe.whitelist()
def absent_for_unmatched_shift(from_date,to_date):
    frappe.db.sql("""UPDATE `tabAttendance` SET status = 'Absent' WHERE assigned_shift != 'No Shift Assigned' AND status = 'Present' AND shift_matched_or_unmatched = 'Unmatched' AND attendance_date BETWEEN '%s' AND '%s' """ % (from_date, to_date), as_dict=1)
    frappe.db.sql("""UPDATE `tabAttendance` SET attended_shift = NULL,  att_in_time = NULL, att_out_time = NULL 
                        WHERE on_duty_application IS NULL AND in_time IS NULL AND out_time IS NULL AND attendance_date BETWEEN '%s' AND '%s' """ % (from_date, to_date), as_dict=1)




@frappe.whitelist()
def safe_time_conversion(time_value):
    # Safely convert timedelta within 24-hour range to time, avoid OverflowError for larger values
    if isinstance(time_value, timedelta):
        if time_value.days > 0:
            return None  # Handle or log as needed
        return (datetime.min + time_value).time()
    elif isinstance(time_value, time):
        return time_value
    return None
#updates late entry and early out
@frappe.whitelist()
def mark_late_early(from_date,to_date):
    now_date=datetime.today()
    now_date= getdate(now_date)
    if now_date.day >= 21:
        from_date_grace = now_date.replace(month=now_date.month, day=21)
    else:
        from_date_grace = now_date.replace(month=now_date.month-1, day=21)

    to_date_grace = now_date.replace(month=now_date.month, day=20)
    if now_date.day > 20:
        to_date_grace = (to_date_grace + timedelta(days=31)).replace(day=20)
    attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(from_date,to_date)),'docstatus':('!=',2),'status':['!=','On Leave']},['*'],order_by='attendance_date')
    for att in attendance:
        hh = check_holiday(att.attendance_date, att.employee)
        if not hh:
            perm_session=''
            if att.permission:
                perm_session=frappe.db.get_value('Permission Request',{"employee_id":att.employee,'permission_date':att.attendance_date,'docstatus':1},['session'])
                perm_to_time=frappe.db.get_value('Permission Request',{"employee_id":att.employee,'permission_date':att.attendance_date,'docstatus':1},['to_time'])
                perm_from_time=frappe.db.get_value('Permission Request',{"employee_id":att.employee,'permission_date':att.attendance_date,'docstatus':1},['from_time'])
                perm_from_time = safe_time_conversion(perm_from_time)
                perm_to_time = safe_time_conversion(perm_to_time)
                if perm_session and perm_session =='Second Half' :
                    if perm_from_time:
                        perm_hour=frappe.db.get_value('Permission Request',{"employee_id":att.employee,'permission_date':att.attendance_date,'docstatus':1},['permission_hour'])
                        att_date = att.attendance_date
                        if att.shift == '2':
                            if perm_hour == 1:
                                att_date = add_days(att_date,1)
                        permission_start_time = datetime.combine(att_date, perm_from_time)  
                if perm_session and perm_session =='First Half' :
                   if perm_to_time:                  
                        permission_end_time = datetime.combine(att.attendance_date, perm_to_time) 
            if att.status not in ['On Leave', 'Work From Home']:
                if att.shift and att.in_time:
                    shift_time_start = frappe.get_value("Shift Type", {'name': att.shift}, ["start_time"])
                    shift_start_time = datetime.strptime(str(shift_time_start), '%H:%M:%S').time()
                    start_time = dt.datetime.combine(att.attendance_date, shift_start_time)
                    grace_start_time = start_time + timedelta(minutes=6)
                    start_time += dt.timedelta(minutes=1)
                    grace_count_late = frappe.db.count('Attendance', {'employee': att.employee,'attendance_date': ('between', (from_date_grace, to_date_grace)),'late_grace_count': 1,'status':['!=','On Leave']})
                    if not att.permission:
                        if att.in_time > start_time:
                            if grace_count_late < 2:
                                if att.in_time < grace_start_time:
                                    frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
                                    frappe.db.set_value('Attendance', att.name, 'late_entry_time','00:00:00')
                                    frappe.db.set_value('Attendance', att.name, 'late_grace_count', 1)
                                else:
                                    frappe.db.set_value('Attendance', att.name, 'late_entry', 1)
                                    frappe.db.set_value('Attendance', att.name, 'late_entry_time', att.in_time - start_time)
                                    frappe.db.set_value('Attendance', att.name, 'late_grace_count', 1)
                                    if int(att.total_working_hours) >=4 and att.leave_application is None:
                                        frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                            else:
                                if att.late_grace_count == 1:
                                    if att.in_time < grace_start_time:
                                        frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
                                        frappe.db.set_value('Attendance', att.name, 'late_entry_time','00:00:00')
                                    else:
                                        frappe.db.set_value('Attendance', att.name, 'late_entry', 1)
                                        frappe.db.set_value('Attendance', att.name, 'late_entry_time', att.in_time - start_time)
                                        if int(att.total_working_hours) >=4 and att.leave_application is None:
                                            frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                                else:
                                    frappe.db.set_value('Attendance', att.name, 'late_entry', 1)
                                    frappe.db.set_value('Attendance', att.name, 'late_entry_time', att.in_time - start_time)
                                    if int(att.total_working_hours) >=4 and att.leave_application is None:
                                        frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                        else:
                            frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
                            frappe.db.set_value('Attendance', att.name, 'late_entry_time', "00:00:00")       
                    
                    elif att.permission:
                        if perm_session:
                            if perm_session == 'First Half': 
                                grace_start_time_for_permission = permission_end_time + timedelta(minutes=6)
                                if att.in_time > permission_end_time:
                                    if grace_count_late < 2:
                                        if att.in_time < grace_start_time_for_permission:
                                            frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
                                            frappe.db.set_value('Attendance', att.name, 'late_entry_time','00:00:00')
                                            frappe.db.set_value('Attendance', att.name, 'late_grace_count', 1)
                                        else:
                                            frappe.db.set_value('Attendance', att.name, 'late_entry', 1)
                                            frappe.db.set_value('Attendance', att.name, 'late_entry_time', att.in_time - permission_end_time)
                                            frappe.db.set_value('Attendance', att.name, 'late_grace_count', 1)
                                            if int(att.total_working_hours) >=4 and att.leave_application is None:
                                                frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                                    else:
                                        if att.late_grace_count == 1:
                                            if att.in_time < grace_start_time_for_permission:
                                                frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
                                                frappe.db.set_value('Attendance', att.name, 'late_entry_time','00:00:00')
                                            else:
                                                frappe.db.set_value('Attendance', att.name, 'late_entry', 1)
                                                frappe.db.set_value('Attendance', att.name, 'late_entry_time', att.in_time - permission_end_time)
                                                if int(att.total_working_hours) >=4 and att.leave_application is None:
                                                    frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                                        else:
                                            frappe.db.set_value('Attendance', att.name, 'late_entry', 1)
                                            frappe.db.set_value('Attendance', att.name, 'late_entry_time', att.in_time - permission_end_time)
                                            if int(att.total_working_hours) >=4 and att.leave_application is None:
                                                frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                                        
                                else:
                                    frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
                                    frappe.db.set_value('Attendance', att.name, 'late_entry_time', "00:00:00")

                    else:
                        frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
                        frappe.db.set_value('Attendance', att.name, 'late_entry_time', "00:00:00")

                if att.shift and att.out_time:
                    shift_time_end = frappe.get_value("Shift Type", {'name': att.shift}, ["end_time"])
                    shift_end_time = datetime.strptime(str(shift_time_end), '%H:%M:%S').time()
                    att_date = att.attendance_date
                    if att.shift == '2':
                        att_date = add_days(att_date,1)
                    end_time = dt.datetime.combine(att_date, shift_end_time)
                    grace_end_time = end_time - timedelta(minutes=6)
                    grace_count_early = frappe.db.count('Attendance', {'employee': att.employee,'attendance_date': ('between', (from_date_grace, to_date_grace)),'early_grace_count': 1,'status':['!=','On Leave']})
                    if not att.permission:
                        if att.out_time < end_time:
                            if grace_count_early < 2:
                                if att.out_time > grace_end_time:
                                    frappe.db.set_value('Attendance', att.name, 'early_exit', 0)
                                    frappe.db.set_value('Attendance', att.name, 'early_out_time', "00:00:00")
                                    frappe.db.set_value('Attendance', att.name, 'early_grace_count', 1)
                                else:
                                    frappe.db.set_value('Attendance', att.name, 'early_exit', 1)
                                    frappe.db.set_value('Attendance', att.name, 'early_out_time', end_time - att.out_time)
                                    frappe.db.set_value('Attendance', att.name, 'early_grace_count', 1)
                                    if int(att.total_working_hours) >=4 and att.leave_application is None:
                                        frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                            else:
                                if att.early_grace_count == 1:
                                    if att.out_time > grace_end_time:
                                        frappe.db.set_value('Attendance', att.name, 'early_exit', 0)
                                        frappe.db.set_value('Attendance', att.name, 'early_out_time', "00:00:00")
                                    else:
                                        frappe.db.set_value('Attendance', att.name, 'early_exit', 1)
                                        frappe.db.set_value('Attendance', att.name, 'early_out_time', end_time - att.out_time)
                                        if int(att.total_working_hours) >=4 and att.leave_application is None:
                                            frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                                else:
                                    frappe.db.set_value('Attendance', att.name, 'early_exit', 1)
                                    frappe.db.set_value('Attendance', att.name, 'early_out_time', end_time - att.out_time)
                                    if int(att.total_working_hours) >=4 and att.leave_application is None:
                                        frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                        else:
                            frappe.db.set_value('Attendance', att.name, 'early_exit', 0)
                            frappe.db.set_value('Attendance', att.name, 'early_out_time', "00:00:00")
                    
                    elif perm_session:
                        if perm_session =='Second Half':
                            grace_end_time_for_permission = permission_start_time - timedelta(minutes=6)
                            if att.out_time < permission_start_time:
                                if grace_count_early < 2:
                                    if att.out_time < grace_end_time_for_permission:
                                        frappe.db.set_value('Attendance', att.name, 'early_exit', 0)
                                        frappe.db.set_value('Attendance', att.name, 'early_out_time', "00:00:00")
                                        frappe.db.set_value('Attendance', att.name, 'early_grace_count', 1)
                                    else:
                                        frappe.db.set_value('Attendance', att.name, 'early_exit', 1)
                                        frappe.db.set_value('Attendance', att.name, 'early_out_time', permission_start_time - att.out_time)
                                        frappe.db.set_value('Attendance', att.name, 'early_grace_count', 1)
                                        if int(att.total_working_hours) >=4 and att.leave_application is None:
                                            frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                                else:
                                    if att.early_grace_count == 1:
                                        if att.out_time < grace_end_time_for_permission:
                                            frappe.db.set_value('Attendance', att.name, 'early_exit', 0)
                                            frappe.db.set_value('Attendance', att.name, 'early_out_time', "00:00:00")
                                            frappe.db.set_value('Attendance', att.name, 'early_grace_count', 1)
                                        else:
                                            frappe.db.set_value('Attendance', att.name, 'early_exit', 1)
                                            frappe.db.set_value('Attendance', att.name, 'early_out_time', permission_start_time - att.out_time)
                                            frappe.db.set_value('Attendance', att.name, 'early_grace_count', 1)
                                            if int(att.total_working_hours) >=4 and att.leave_application is None:
                                                frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                                    else:
                                        frappe.db.set_value('Attendance', att.name, 'early_exit', 1)
                                        frappe.db.set_value('Attendance', att.name, 'early_out_time', permission_start_time - att.out_time)
                                        if int(att.total_working_hours) >=4 and att.leave_application is None:
                                            frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                            else:
                                frappe.db.set_value('Attendance', att.name, 'early_exit', 0)
                                frappe.db.set_value('Attendance', att.name, 'early_out_time', "00:00:00")                                       
                    
        
        
            else:
                frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
                frappe.db.set_value('Attendance', att.name, 'late_entry_time', "00:00:00")
                frappe.db.set_value('Attendance', att.name, 'early_exit', 0)
                frappe.db.set_value('Attendance', att.name, 'early_out_time', "00:00:00")
        
        else:
            frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
            frappe.db.set_value('Attendance', att.name, 'late_entry_time', "00:00:00")
            frappe.db.set_value('Attendance', att.name, 'early_exit', 0)
            frappe.db.set_value('Attendance', att.name, 'early_out_time', "00:00:00")

    employee_records = frappe.db.get_all("Employee",{'status':'Active','date_of_joining': ['<=', to_date]},['name'])
    for emp in employee_records:
        attendance_records = frappe.db.get_all('Attendance', {'attendance_date': ('between', (from_date_grace, to_date_grace)),'docstatus': ('!=', 2),'late_entry': 1,'early_exit':1 ,'employee': emp.name}, ['name','employee','attendance_date','status','early_exit','late_entry'], order_by='attendance_date')
        for att in attendance_records:
            is_holiday = check_holiday(att.attendance_date, att.employee)
            if not is_holiday and att.status not in ['On Leave', 'Work From Home']:
                if att.late_entry and att.early_exit:
                    frappe.db.set_value('Attendance', att.name, 'status', 'Absent')


#use to update shift status
@frappe.whitelist()
def att_shift_status_updation(from_date,to_date):
    attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2')},['*'])  
    for att in attendance:
        shift_status = ''
        hh = check_holiday(att.attendance_date, att.employee)
        if att.status == 'Absent':
            if att.in_time and not att.out_time:
                if att.shift:
                    shift_status = str(att.shift) + 'M'
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
                else:
                    shift_status = 'NS/' + 'M'
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
            elif att.out_time and not att.in_time:
                if att.shift:
                    shift_status = 'M' + str(att.shift)
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
                else:
                    shift_status = 'M' + '/NS'
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
            elif att.out_time and att.in_time:
                if att.shift:
                    shift_status = 'AA'
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
                else:
                    shift_status = 'AA'
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
            else:
                if hh:
                    shift_status = 'HH'
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
                else:
                    shift_status = 'AA'
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
        elif att.status == 'Present':
            if att.shift:
                shift_status = str(att.shift)
                frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
            else:
                if att.on_duty_application:
                    shift_status = 'OD'
                    od = frappe.db.get_value("On Duty Application",{'docstatus':0,"name":att['on_duty_application']},['session'])
                    if od == 'First Half':
                        shift_status ='OD/P'
                    if od == 'Second Half':
                        shift_status ='P/OD'
                    if od == 'Full Day':
                        shift_status ='OD'
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
                else:
                    shift_status = 'NS/P'
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
        elif att.status == 'Work From Home':
            shift_status = 'WFH'
            frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
        elif att.status == 'Half Day':
            if att.leave_type:
                shift_status = 'HD/' + status_map.get(att.leave_type,'')
                frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
            else:
                if hh:
                    shift_status = 'HH/HD'
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
                else:
                    shift_status = 'HD'
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
        elif att.status == 'On Leave':
            if att.leave_type:
                leave_data = frappe.db.sql("""
                    select COUNT(name) as leave_count, leave_type
                    from `tabLeave Application`
                    where workflow_state = "Approved" 
                    and docstatus = 1 
                    and employee = %(employee)s and name != %(leave_application)s
                    and (from_date between %(from_date)s and %(to_date)s
                        or to_date between %(from_date)s and %(to_date)s
                        or (from_date < %(from_date)s and to_date > %(to_date)s))
                """, {
                    "from_date": att.attendance_date,
                    "to_date": att.attendance_date,
                    "employee": att.employee,
                    "leave_application": att.leave_application,
                })
                # frappe.log_error(leave_data, "Leave Data Error")
                # Get the first result (if any)
                if leave_data:
                    leave_count = leave_data[0][0] 
                    leave_type = leave_data[0][1]
                    shift_status_leave_type = status_map.get(leave_type)
                    shift_status = status_map.get(att.leave_type)
                    shift_status = f'{shift_status_leave_type}-{shift_status}'
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
                else:
                    shift_status = status_map.get(att.leave_type)
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
            else:
                shift_status = 'L'
                frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)

@frappe.whitelist()
def mark_absent_with_employee(from_date,to_date,employee):
    dates = [from_date,to_date]
    for date in dates:
        if getdate(date) <= getdate(today()):
            employee_data = frappe.db.get_all('Employee',{'employee':employee,'status':'Active','date_of_joining':['<=',from_date]})
            for emp in employee_data:
                hh = check_holiday(date,emp.name)
                if not hh:
                    if not frappe.db.exists('Attendance',{'attendance_date':date,'employee':emp.name,'docstatus':('!=','2')}):
                        try:
                            if not frappe.db.exists('Restriction',{'employee':emp.name,'restricted_date':date,'docstatus':1}):
                                att = frappe.new_doc("Attendance")
                                att.employee = emp.name
                                att.status = 'Absent'
                                att.attendance_date = date
                                att.total_working_hours = "0.0"
                                att.over_time_hours = "0.0"
                                att.working_total_hours = "00:00"
                                att.over_time_hours = "0.0"
                                att.extra_hours = "00:00:00"
                                att.att_in_time = "00:00:00"
                                att.att_out_time = "00:00:00"
                                att.late_entry_time='00:00:00'
                                att.early_out_time='00:00:00'
                                att.save(ignore_permissions=True)
                                frappe.db.commit()
                        except:
                            frappe.log_error(title="Restriction",message="Please Check Restriction on %s that Employee %s"%(date,emp.name))




@frappe.whitelist()
def mark_wh_ot_with_employee(from_date,to_date,employee):
    attendance = frappe.db.get_all('Attendance',{'employee':employee,'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2')},['*'])
    for att in attendance:
        
        od_hours = 0
        if att.on_duty_application:
            od_hours = frappe.db.get_value("On Duty Application",{'name':att.on_duty_application},["total_od_hours"])
            if od_hours:
                od_hours=int(od_hours)
            else:
                od_hours=0
        if att.in_time and att.out_time and att.shift:
            hh = check_holiday(att.attendance_date,att.employee)
            if not hh:
                if att.out_time < att.in_time:
                    total_wh= "00:00"
                else:
                    total_wh= att.out_time -att.in_time
                ftr = [3600,60,1]
                if att.out_time < att.in_time:
                    wh = 0
                else:
                    wh = time_diff_in_hours(att.out_time,att.in_time)
                perm_time=0
                wh += od_hours
                if wh < 4:
                    if att.permission:
                        perm=frappe.db.get_value("Permission Request",{'name':att.permission},['permission_hour'])
                        if perm:
                            perm=int(perm)
                        else:
                            perm=0
                        perm_time=wh+perm
                        if perm_time >= 4:
                            frappe.db.set_value('Attendance',att.name,'status','Half Day')
                        else:
                            frappe.db.set_value('Attendance',att.name,'status','Absent')
                    else:
                        frappe.db.set_value('Attendance',att.name,'status','Absent')
                    if att.leave_application:
                        leave=frappe.db.get_value("Leave Application",{'name':att.leave_application,'half_day':1,'docstatus':'1','half_day_date':att.attendance_date},['name'])
                        if leave:
                            frappe.db.set_value('Attendance',att.name,'status','Half Day')
                        else:
                            frappe.db.set_value('Attendance',att.name,'status','Absent')
                    else:
                        frappe.db.set_value('Attendance',att.name,'status','Absent')
                elif wh >= 4 and wh < 8:
                    if att.permission:
                        perm=frappe.db.get_value("Permission Request",{'name':att.permission},['permission_hour'])
                        if perm:
                            perm=int(perm)
                        else:
                            perm=0
                        perm_time=wh+perm
                        if perm_time >= 8:
                            frappe.db.set_value('Attendance',att.name,'status','Present')
                        else:
                            frappe.db.set_value('Attendance',att.name,'status','Half Day')
                    else:
                        frappe.db.set_value('Attendance',att.name,'status','Half Day')
                elif wh >= 8:
                    frappe.db.set_value('Attendance',att.name,'status','Present')   
                if att.out_time < att.in_time:
                    wh = 0
                else:
                    wh = time_diff_in_hours(att.out_time,att.in_time)
                shift_start_time = frappe.db.get_value('Shift Type',{'name':att.shift},['start_time'])
                shift_start_time = pd.to_datetime(str(shift_start_time)).time()

                shift_end_time = frappe.db.get_value('Shift Type',{'name':att.shift},['end_time'])
                shift_end_time = pd.to_datetime(str(shift_end_time)).time()

                in_date = att.in_time.date()
                out_date = att.out_time.date()
                get_shift_hours = frappe.db.get_value('Shift Type',{'name':att.shift},['total_shift_hours'])
                total_shift_hours = datetime.strptime(str(get_shift_hours),'%Y-%m-%d %H:%M:%S').time()
                shift_hr = sum([a*b for a,b in zip(ftr, map(int,str(total_shift_hours).split(':')))])
                shift_wh = round(shift_hr/3600,1) 
                shift_start_datetime = datetime.combine(in_date,shift_start_time)
                shift_end_datetime = datetime.combine(att.attendance_date,shift_end_time)
                if att.shift=='2':
                    next_day = add_days(att.attendance_date,1)
                    shift_end_datetime = datetime.combine(next_day,shift_end_time)
                if int(wh) > int(shift_wh):
                    extra_hrs =pd.to_datetime('00:00:00').time()
                    ot_hr = 0
                    try:
                        extra_hrs = att.out_time - shift_end_datetime
                        hr = sum([a*b for a,b in zip(ftr, map(int,str(extra_hrs).split(':')))])
                        extras = round(hr/3600,1)
                    except:
                        extra_hrs = '00:00' 
                        extras = 0 
                    if extras > 1:
                            ot_hr = math.floor(extras * 2) / 2  
                    if wh < 24:
                        frappe.db.set_value('Attendance',att.name,'working_total_hours',total_wh)             
                        frappe.db.set_value('Attendance',att.name,'total_working_hours',round(wh,2))                
                        frappe.db.set_value('Attendance',att.name,'extra_hours',extra_hrs)
                        frappe.db.set_value('Attendance',att.name,'over_time_hours',ot_hr)
                    else:
                        frappe.db.set_value('Attendance',att.name,'working_total_hours','23:59')             
                        frappe.db.set_value('Attendance',att.name,'total_working_hours',round(wh,2))                
                        frappe.db.set_value('Attendance',att.name,'extra_hours',extra_hrs)
                        frappe.db.set_value('Attendance',att.name,'over_time_hours',ot_hr)
                else:
                    if wh > 24:
                        none_time = pd.to_datetime('00:00:00').time()
                        frappe.db.set_value('Attendance',att.name,'working_total_hours','23:59')
                        frappe.db.set_value('Attendance',att.name,'total_working_hours',round(wh,2))  
                        frappe.db.set_value('Attendance',att.name,'extra_hours','00:00')
                        frappe.db.set_value('Attendance',att.name,'over_time_hours',0)
                    else:
                        none_time = pd.to_datetime('00:00:00').time()
                        frappe.db.set_value('Attendance',att.name,'working_total_hours',total_wh)
                        frappe.db.set_value('Attendance',att.name,'total_working_hours',round(wh,2))  
                        frappe.db.set_value('Attendance',att.name,'extra_hours','00:00')
                        frappe.db.set_value('Attendance',att.name,'over_time_hours',0)
            else:
                if att.out_time < att.in_time:
                    frappe.log_error(message=att.name, title="Attendance")
                    total_wh="00:00"
                else:
                    total_wh= att.out_time - att.in_time
                ftr = [3600,60,1]
                max_time = timedelta(hours=23, minutes=59)
                if total_wh < max_time:
                    hr = sum([a*b for a,b in zip(ftr, map(int,str(total_wh).split(':')))])
                    wh = round(hr/3600,1)
                else:
                    wh = round(total_wh.total_seconds() / 3600, 1)
                perm_time=0
                wh += od_hours
                if wh < 4:
                    if att.permission:
                        perm=frappe.db.get_value("Permission Request",{'name':att.permission},['permission_hour'])
                        perm=int(perm)
                        perm_time=wh+perm
                        if perm_time >= 4:
                            frappe.db.set_value('Attendance',att.name,'status','Half Day')
                        else:
                            frappe.db.set_value('Attendance',att.name,'status','Absent')
                    else:
                        frappe.db.set_value('Attendance',att.name,'status','Absent')
                elif wh >= 4 and wh < 8:
                    if att.permission:
                        perm=frappe.db.get_value("Permission Request",{'name':att.permission},['permission_hour'])
                        if perm:
                            perm=int(perm)
                        else:
                            perm=0
                        perm_time=wh+perm
                        if perm_time >= 8:
                            frappe.db.set_value('Attendance',att.name,'status','Present')
                        else:
                            frappe.db.set_value('Attendance',att.name,'status','Half Day')
                    else:
                        frappe.db.set_value('Attendance',att.name,'status','Half Day')
                elif wh >= 8:
                    frappe.db.set_value('Attendance',att.name,'status','Present')  
                if total_wh < max_time:
                    hr = sum([a*b for a,b in zip(ftr, map(int,str(total_wh).split(':')))])
                    wh = round(hr/3600,1)
                else:
                    wh = round(total_wh.total_seconds() / 3600, 1)
                if wh < 24:
                    ot_hr = (math.floor(wh * 2) / 2) - 0.5
                    if ot_hr >= 9:
                        ot_hr = ot_hr - 1
                        # total_wh_time = total_wh - timedelta(hours=1) 
                        # total_wh = str(total_wh_time)  
                    frappe.db.set_value('Attendance',att.name,'over_time_hours',ot_hr)
                    none_time =pd.to_datetime('00:00:00').time()
                    frappe.db.set_value('Attendance',att.name,'extra_hours','00:00')
                    frappe.db.set_value('Attendance',att.name,'working_total_hours',total_wh)
                    frappe.db.set_value('Attendance',att.name,'total_working_hours',round(wh,2))
                elif wh >= 24:
                    ot_hr = (math.floor(wh * 2) / 2) - 0.5
                    ot_hr = ot_hr - 1
                    frappe.db.set_value('Attendance',att.name,'over_time_hours',ot_hr)
                    none_time =pd.to_datetime('00:00:00').time()
                    frappe.db.set_value('Attendance',att.name,'extra_hours','00:00')
                    frappe.db.set_value('Attendance',att.name,'working_total_hours','23:59')
                    frappe.db.set_value('Attendance',att.name,'total_working_hours',round(wh,2))
                else:
                    none_time =pd.to_datetime('00:00:00').time()
                    frappe.db.set_value('Attendance',att.name,'over_time_hours',0)
                    frappe.db.set_value('Attendance',att.name,'extra_hours','00:00')
                    frappe.db.set_value('Attendance',att.name,'working_total_hours','00:00')
                    frappe.db.set_value('Attendance',att.name,'total_working_hours',0)   
        else:
            none_time =pd.to_datetime('00:00:00').time()
            frappe.db.set_value('Attendance',att.name,'extra_hours','00:00')
            frappe.db.set_value('Attendance',att.name,'working_total_hours','00:00')
        if att.on_duty_application and ((not att.in_time and not att.out_time) or (att.in_time and not att.out_time) or (att.out_time and not att.in_time ) and att.shift):
            perm=0
            wh = att.total_working_hours
            if att.permission:
                perm=frappe.db.get_value("Permission Request",{'name':att.permission},['permission_hour'])
                if perm:
                    perm=int(perm)
                else:
                    perm=0
            od_hours = frappe.db.get_value("On Duty Application",{'name':att.on_duty_application},["total_od_hours"])
            if od_hours:
                od_hours=int(od_hours)
            else:
                od_hours=0
            od_time=wh+od_hours+perm
            
            if od_time >= 8:
                frappe.db.set_value('Attendance',att.name,'status','Present')
            elif od_time >= 4 and od_time < 8:
                frappe.db.set_value('Attendance',att.name,'status','Half Day')
            else:
                frappe.db.set_value('Attendance',att.name,'status','Absent')

@frappe.whitelist()
def att_shift_status_updation_with_employee(from_date,to_date,employee):
    attendance = frappe.db.get_all('Attendance',{'employee':employee,'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2')},['*'])  
    for att in attendance:
        shift_status = ''
        hh = check_holiday(att.attendance_date, att.employee)
        if att.status == 'Absent':
            if att.in_time and not att.out_time:
                if att.shift:
                    shift_status = str(att.shift) + 'M'
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
                else:
                    shift_status = 'NS/' + 'M'
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
            elif att.out_time and not att.in_time:
                if att.shift:
                    shift_status = 'M' + str(att.shift)
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
                else:
                    shift_status = 'M' + '/NS'
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
            elif att.out_time and att.in_time:
                if att.shift:
                    shift_status = 'AA'
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
                else:
                    shift_status = 'AA'
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
            else:
                if hh:
                    shift_status = 'HH'
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
                else:
                    shift_status = 'AA'
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
        elif att.status == 'Present':
            if att.shift:
                shift_status = str(att.shift)
                frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
            else:
                if att.on_duty_application:
                    shift_status = 'OD'
                    od = frappe.db.get_value("On Duty Application",{'docstatus':0,"name":att['on_duty_application']},['session'])
                    if od == 'First Half':
                        shift_status ='OD/P'
                    if od == 'Second Half':
                        shift_status ='P/OD'
                    if od == 'Full Day':
                        shift_status ='OD'
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
                else:
                    shift_status = 'NS/P'
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
        elif att.status == 'Work From Home':
            shift_status = 'WFH'
            frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
        elif att.status == 'Half Day':
            if att.leave_type:
                shift_status = 'HD/' + status_map.get(att.leave_type,'')
                frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
            else:
                if hh:
                    shift_status = 'HH/HD'
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
                else:
                    shift_status = 'HD'
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
        elif att.status == 'On Leave':
            if att.leave_type:
                leave_data = frappe.db.sql("""
                    select COUNT(name) as leave_count, leave_type
                    from `tabLeave Application`
                    where workflow_state = "Approved" 
                    and docstatus = 1 
                    and employee = %(employee)s and name != %(leave_application)s
                    and (from_date between %(from_date)s and %(to_date)s
                        or to_date between %(from_date)s and %(to_date)s
                        or (from_date < %(from_date)s and to_date > %(to_date)s))
                """, {
                    "from_date": att.attendance_date,
                    "to_date": att.attendance_date,
                    "employee": att.employee,
                    "leave_application": att.leave_application,
                })
                # frappe.log_error(leave_data, "Leave Data Error")
                # Get the first result (if any)
                if leave_data:
                    leave_count = leave_data[0][0] 
                    leave_type = leave_data[0][1]
                    shift_status_leave_type = status_map.get(leave_type)
                    shift_status = status_map.get(att.leave_type)
                    shift_status = f'{shift_status_leave_type}-{shift_status}'
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
                else:
                    shift_status = status_map.get(att.leave_type)
                    frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
            else:
                shift_status = 'L'
                frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)

@frappe.whitelist()
def assigned_shift_with_employee(from_date,to_date,employee):
    datalist = []
    data = {}
    attendance = frappe.get_all('Attendance',{'employee':employee,'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2')},['*'])
    for att in attendance:
        check_shift = frappe.db.exists('Shift Assignment',{'employee':att.employee,'start_date':att.attendance_date,'docstatus':1})  
        if check_shift:
            get_shift = frappe.get_value('Shift Assignment',{'name':check_shift},['shift_type'])  
            shift_start_time = frappe.get_value('Shift Type',{'name':get_shift},['start_time'])
            shift_end_time = frappe.get_value('Shift Type',{'name':get_shift},['end_time'])
            data.update({
                'get_shift':get_shift,
                'shift_start_time':shift_start_time,
                'shift_end_time':shift_end_time 
            })
            datalist.append(data.copy())
        else: 
            get_shift = 'No Shift Assigned'  
            shift_start_time = datetime.strptime(str('00:00:00'),'%H:%M:%S').strftime('%H:%M')
            shift_end_time = datetime.strptime(str('00:00:00'),'%H:%M:%S').strftime('%H:%M')
            data.update({
                'get_shift':get_shift,
                'shift_start_time':shift_start_time,
                'shift_end_time':shift_end_time 
            })
            datalist.append(data.copy())  
            
        if att.in_time and att.out_time:
            att_in_time = att.in_time
            att_out_time = att.out_time
            att_shift = att.shift or ' '
            data.update({
                'att_shift':att.shift or '-',
                'att_in_time':att_in_time,
                'att_out_time':'att_out_time',
            }) 
            datalist.append(data.copy())  
            frappe.db.set_value('Attendance',att.name,'attended_shift',att_shift or '')
            frappe.db.set_value('Attendance',att.name,'att_in_time',att_in_time)
            frappe.db.set_value('Attendance',att.name,'att_out_time',att_out_time)    
        elif att.in_time and not att.out_time:
            att_in_time = att.in_time 
            att_out_time = None
            att_shift = att.shift or '-'
            data.update({
                'att_shift':att.shift,
                'att_in_time':att_in_time,
                'att_out_time':att_out_time
            })
            datalist.append(data.copy())
            frappe.db.set_value('Attendance',att.name,'attended_shift',att_shift or '')
            frappe.db.set_value('Attendance',att.name,'att_in_time',att_in_time)
            frappe.db.set_value('Attendance',att.name,'att_out_time',att_out_time)    
        elif att.out_time and not att.in_time:
            att_in_time = None
            att_out_time = att.out_time
            att_shift = att.shift or '-'
            data.update({
                'att_shift':att.shift,
                'att_in_time':att_in_time,
                'att_out_time':att_out_time
            })
            datalist.append(data.copy()) 
            frappe.db.set_value('Attendance',att.name,'attended_shift',att_shift or '')
            frappe.db.set_value('Attendance',att.name,'att_in_time',att_in_time)
            frappe.db.set_value('Attendance',att.name,'att_out_time',att_out_time)    
        else:
            if att.on_duty_application:
                od_shift = frappe.db.get_value("On Duty Application",{'name':att.on_duty_application},["shift"])
                frappe.db.set_value('Attendance',att.name,'attended_shift',od_shift or '')
            else:
                att_in_time = None
                att_out_time = None
                att_shift = att.shift or '-'
                frappe.db.set_value('Attendance',att.name,'attended_shift',att_shift or '')
                frappe.db.set_value('Attendance',att.name,'att_in_time',att_in_time)
                frappe.db.set_value('Attendance',att.name,'att_out_time',att_out_time)  

        frappe.db.set_value('Attendance',att.name,'assigned_shift',get_shift)
        frappe.db.set_value('Attendance',att.name,'shift_in_time',shift_start_time)
        frappe.db.set_value('Attendance',att.name,'shift_out_time',shift_end_time)
          
    return "ok"

@frappe.whitelist()
def shift_matched_with_employee(from_date,to_date,employee):
    data = {}
    datalist = []
    status = ''
    attendance = frappe.get_all('Attendance',{'employee':employee,'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2')},['*'])
    for att in attendance:
        if att.assigned_shift and att.attended_shift:
            if att.assigned_shift == att.attended_shift:
                status = 'Matched'
            else:
                status = 'Unmatched'  
        else:
            status = 'Unmatched'
        data.update({
            'status':status
        }) 
        datalist.append(data.copy())  
        frappe.db.set_value('Attendance',att.name,'shift_matched_or_unmatched',status)   
    absent_for_unmatched_shift_with_employee(from_date,to_date,employee)

def absent_for_unmatched_shift_with_employee(from_date,to_date,employee):
    # frappe.db.sql("""UPDATE `tabAttendance` SET status = 'Absent' WHERE assigned_shift != 'No Shift Assigned' AND status = 'Present' AND shift_matched_or_unmatched = 'Unmatched' AND attendance_date BETWEEN '%s' AND '%s' AND employee ='%s' """ % (from_date, to_date,employee), as_dict=1)
    frappe.db.sql("""UPDATE `tabAttendance` SET status = 'Absent' WHERE status = 'Present' AND shift_matched_or_unmatched = 'Unmatched' AND attendance_date BETWEEN '%s' AND '%s' AND employee ='%s' """ % (from_date, to_date,employee), as_dict=1)
    frappe.db.sql("""UPDATE `tabAttendance` SET attended_shift = NULL,  att_in_time = NULL, att_out_time = NULL 
                        WHERE on_duty_application IS NULL AND in_time IS NULL AND out_time IS NULL AND attendance_date BETWEEN '%s' AND '%s' AND employee ='%s' """ % (from_date, to_date,employee), as_dict=1)
def mark_late_early_with_employee(from_date,to_date,employee):
    now_date=datetime.today()
    now_date= getdate(from_date)
    if now_date.day >= 21:
        from_date_grace = now_date.replace(month=now_date.month, day=21)
    else:
        from_date_grace = now_date.replace(month=now_date.month-1, day=21)

    to_date_grace = now_date.replace(month=now_date.month, day=20)
    if now_date.day > 20:
        to_date_grace = (to_date_grace + timedelta(days=31)).replace(day=20)
    # from_date_grace = from_date
    # to_date_grace = to_date
    attendance = frappe.db.get_all('Attendance',{'employee':employee,'attendance_date':('between',(from_date,to_date)),'docstatus':('!=',2)},['*'],order_by='attendance_date')
    for att in attendance:
        hh = check_holiday(att.attendance_date, att.employee)
        if not hh:
            perm_session=''
            if att.permission:
                perm_session=frappe.db.get_value('Permission Request',{"employee_id":att.employee,'permission_date':att.attendance_date,'docstatus':1},['session'])
                perm_to_time=frappe.db.get_value('Permission Request',{"employee_id":att.employee,'permission_date':att.attendance_date,'docstatus':1},['to_time'])
                perm_from_time=frappe.db.get_value('Permission Request',{"employee_id":att.employee,'permission_date':att.attendance_date,'docstatus':1},['from_time'])
                perm_from_time = safe_time_conversion(perm_from_time)
                perm_to_time = safe_time_conversion(perm_to_time)
                if perm_session and perm_session =='Second Half' :
                    if perm_from_time:
                        perm_hour=frappe.db.get_value('Permission Request',{"employee_id":att.employee,'permission_date':att.attendance_date,'docstatus':1},['permission_hour'])
                        att_date = att.attendance_date
                        if att.shift == '2':
                            if perm_hour == 1:
                                att_date = add_days(att_date,1)
                        permission_start_time = datetime.combine(att_date, perm_from_time)  
                if perm_session and perm_session =='First Half' :
                   if perm_to_time:                  
                        permission_end_time = datetime.combine(att.attendance_date, perm_to_time) 
            if att.status not in ['On Leave', 'Work From Home']:
                if att.shift and att.in_time:
                    shift_time_start = frappe.get_value("Shift Type", {'name': att.shift}, ["start_time"])
                    shift_start_time = datetime.strptime(str(shift_time_start), '%H:%M:%S').time()
                    start_time = dt.datetime.combine(att.attendance_date, shift_start_time)
                    grace_start_time = start_time + timedelta(minutes=6)
                    start_time += dt.timedelta(minutes=1)
                    grace_count_late = frappe.db.count('Attendance', {'employee': att.employee,'attendance_date': ('between', (from_date_grace, to_date_grace)),'late_grace_count': 1,'status':['!=','On Leave']})
                    if not att.permission:
                        if att.in_time > start_time:
                            if grace_count_late < 2:
                                if att.in_time < grace_start_time:
                                    frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
                                    frappe.db.set_value('Attendance', att.name, 'late_entry_time','00:00:00')
                                    frappe.db.set_value('Attendance', att.name, 'late_grace_count', 1)
                                else:
                                    frappe.db.set_value('Attendance', att.name, 'late_entry', 1)
                                    frappe.db.set_value('Attendance', att.name, 'late_entry_time', att.in_time - start_time)
                                    frappe.db.set_value('Attendance', att.name, 'late_grace_count', 1)
                                    if int(att.total_working_hours) >=4 and att.leave_application is None:
                                        frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                            else:
                                if att.late_grace_count == 1:
                                    if att.in_time < grace_start_time:
                                        frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
                                        frappe.db.set_value('Attendance', att.name, 'late_entry_time','00:00:00')
                                    else:
                                        frappe.db.set_value('Attendance', att.name, 'late_entry', 1)
                                        frappe.db.set_value('Attendance', att.name, 'late_entry_time', att.in_time - start_time)
                                        if int(att.total_working_hours) >=4 and att.leave_application is None:
                                            frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                                else:
                                    frappe.db.set_value('Attendance', att.name, 'late_entry', 1)
                                    frappe.db.set_value('Attendance', att.name, 'late_entry_time', att.in_time - start_time)
                                    if int(att.total_working_hours) >=4 and att.leave_application is None:
                                        frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                        else:
                            frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
                            frappe.db.set_value('Attendance', att.name, 'late_entry_time', "00:00:00")       
                    
                    elif att.permission:
                        if perm_session:
                            if perm_session == 'First Half': 
                                grace_start_time_for_permission = permission_end_time + timedelta(minutes=6)
                                if att.in_time > permission_end_time:
                                    if grace_count_late < 2:
                                        if att.in_time < grace_start_time_for_permission:
                                            frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
                                            frappe.db.set_value('Attendance', att.name, 'late_entry_time','00:00:00')
                                            frappe.db.set_value('Attendance', att.name, 'late_grace_count', 1)
                                        else:
                                            frappe.db.set_value('Attendance', att.name, 'late_entry', 1)
                                            frappe.db.set_value('Attendance', att.name, 'late_entry_time', att.in_time - permission_end_time)
                                            frappe.db.set_value('Attendance', att.name, 'late_grace_count', 1)
                                            if int(att.total_working_hours) >=4 and att.leave_application is None:
                                                frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                                    else:
                                        if att.late_grace_count == 1:
                                            if att.in_time < grace_start_time_for_permission:
                                                frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
                                                frappe.db.set_value('Attendance', att.name, 'late_entry_time','00:00:00')
                                            else:
                                                frappe.db.set_value('Attendance', att.name, 'late_entry', 1)
                                                frappe.db.set_value('Attendance', att.name, 'late_entry_time', att.in_time - permission_end_time)
                                                if int(att.total_working_hours) >=4 and att.leave_application is None:
                                                    frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                                        else:
                                            frappe.db.set_value('Attendance', att.name, 'late_entry', 1)
                                            frappe.db.set_value('Attendance', att.name, 'late_entry_time', att.in_time - permission_end_time)
                                            if int(att.total_working_hours) >=4 and att.leave_application is None:
                                                frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                                        
                                else:
                                    frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
                                    frappe.db.set_value('Attendance', att.name, 'late_entry_time', "00:00:00")

                    else:
                        frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
                        frappe.db.set_value('Attendance', att.name, 'late_entry_time', "00:00:00")

                if att.shift and att.out_time:
                    shift_time_end = frappe.get_value("Shift Type", {'name': att.shift}, ["end_time"])
                    shift_end_time = datetime.strptime(str(shift_time_end), '%H:%M:%S').time()
                    att_date = att.attendance_date
                    if att.shift == '2':
                        att_date = add_days(att_date,1)
                        # print("2")
                    end_time = dt.datetime.combine(att_date, shift_end_time)
                    grace_end_time = end_time - timedelta(minutes=6)
                    grace_count_early = frappe.db.count('Attendance', {'employee': att.employee,'attendance_date': ('between', (from_date_grace, to_date_grace)),'early_grace_count': 1,'status':['!=','On Leave']})
                    if not att.permission:
                        if att.out_time < end_time:
                            # print(att.name)
                            if grace_count_early < 2:
                                # print(att.name)
                                if att.out_time > grace_end_time:
                                    frappe.db.set_value('Attendance', att.name, 'early_exit', 0)
                                    frappe.db.set_value('Attendance', att.name, 'early_out_time', "00:00:00")
                                    frappe.db.set_value('Attendance', att.name, 'early_grace_count', 1)
                                else:
                                    frappe.db.set_value('Attendance', att.name, 'early_exit', 1)
                                    frappe.db.set_value('Attendance', att.name, 'early_out_time', end_time - att.out_time)
                                    frappe.db.set_value('Attendance', att.name, 'early_grace_count', 1)
                                    if int(att.total_working_hours) >=4 and att.leave_application is None:
                                        frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                            else:
                                if att.early_grace_count == 1:
                                    if att.out_time > grace_end_time:
                                        frappe.db.set_value('Attendance', att.name, 'early_exit', 0)
                                        frappe.db.set_value('Attendance', att.name, 'early_out_time', "00:00:00")
                                    else:
                                        frappe.db.set_value('Attendance', att.name, 'early_exit', 1)
                                        frappe.db.set_value('Attendance', att.name, 'early_out_time', end_time - att.out_time)
                                        if int(att.total_working_hours) >=4 and att.leave_application is None:
                                            frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                                else:
                                    frappe.db.set_value('Attendance', att.name, 'early_exit', 1)
                                    frappe.db.set_value('Attendance', att.name, 'early_out_time', end_time - att.out_time)
                                    if int(att.total_working_hours) >=4 and att.leave_application is None:
                                        frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                        else:
                            # print(att.name)
                            # print(att.employee)
                            frappe.db.set_value('Attendance', att.name, 'early_exit', 0)
                            frappe.db.set_value('Attendance', att.name, 'early_out_time', "00:00:00")
                    
                    elif perm_session:
                        if perm_session =='Second Half':
                            grace_end_time_for_permission = permission_start_time - timedelta(minutes=6)
                            if att.out_time < permission_start_time:
                                if grace_count_early < 2:
                                    if att.out_time < grace_end_time_for_permission:
                                        frappe.db.set_value('Attendance', att.name, 'early_exit', 0)
                                        frappe.db.set_value('Attendance', att.name, 'early_out_time', "00:00:00")
                                        frappe.db.set_value('Attendance', att.name, 'early_grace_count', 1)
                                    else:
                                        frappe.db.set_value('Attendance', att.name, 'early_exit', 1)
                                        frappe.db.set_value('Attendance', att.name, 'early_out_time', permission_start_time - att.out_time)
                                        frappe.db.set_value('Attendance', att.name, 'early_grace_count', 1)
                                        if int(att.total_working_hours) >=4 and att.leave_application is None:
                                            frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                                else:
                                    if att.early_grace_count == 1:
                                        if att.out_time < grace_end_time_for_permission:
                                            frappe.db.set_value('Attendance', att.name, 'early_exit', 0)
                                            frappe.db.set_value('Attendance', att.name, 'early_out_time', "00:00:00")
                                            frappe.db.set_value('Attendance', att.name, 'early_grace_count', 1)
                                        else:
                                            frappe.db.set_value('Attendance', att.name, 'early_exit', 1)
                                            frappe.db.set_value('Attendance', att.name, 'early_out_time', permission_start_time - att.out_time)
                                            frappe.db.set_value('Attendance', att.name, 'early_grace_count', 1)
                                            if int(att.total_working_hours) >=4 and att.leave_application is None:
                                                frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                                    else:
                                        frappe.db.set_value('Attendance', att.name, 'early_exit', 1)
                                        frappe.db.set_value('Attendance', att.name, 'early_out_time', permission_start_time - att.out_time)
                                        if int(att.total_working_hours) >=4 and att.leave_application is None:
                                            frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                            else:
                                frappe.db.set_value('Attendance', att.name, 'early_exit', 0)
                                frappe.db.set_value('Attendance', att.name, 'early_out_time', "00:00:00")                                       
                    
        
        
            else:
                frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
                frappe.db.set_value('Attendance', att.name, 'late_entry_time', "00:00:00")
                frappe.db.set_value('Attendance', att.name, 'early_exit', 0)
                frappe.db.set_value('Attendance', att.name, 'early_out_time', "00:00:00")
        
        else:
            frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
            frappe.db.set_value('Attendance', att.name, 'late_entry_time', "00:00:00")
            frappe.db.set_value('Attendance', att.name, 'early_exit', 0)
            frappe.db.set_value('Attendance', att.name, 'early_out_time', "00:00:00")

    employee_records = frappe.db.get_all("Employee",{'status':'Active','date_of_joining': ['<=', to_date]},['name'])
    for emp in employee_records:
        attendance_records = frappe.db.get_all('Attendance', {'attendance_date': ('between', (from_date_grace, to_date_grace)),'docstatus': ('!=', 2),'late_entry': 1,'early_exit':1 ,'employee': emp.name}, ['name','employee','attendance_date','status','early_exit','late_entry'], order_by='attendance_date')
        for att in attendance_records:
            is_holiday = check_holiday(att.attendance_date, att.employee)
            if not is_holiday and att.status not in ['On Leave', 'Work From Home']:
                if att.late_entry and att.early_exit:
                    frappe.db.set_value('Attendance', att.name, 'status', 'Absent')

def mark_att_present_with_employee(from_date, to_date,employee):
    attendance_docstatus_0 = frappe.db.get_all('Attendance', {
        'attendance_date': ('between', (from_date, to_date)),'docstatus': ('!=',2),'employee':employee}, ['*'])
    
    for att in attendance_docstatus_0:
        if att.get('status') == 'Present':
            frappe.db.set_value('Attendance', att.get('name'), 'docstatus', 1)
        if att.get('status') == 'On Leave' and att.get('leave_type'):
            frappe.db.set_value('Attendance', att.get('name'), 'docstatus', 1)


def mark_late_early_updates(from_date,to_date):
    now_date=datetime.today()
    now_date= getdate(from_date)
    if now_date.day >= 21:
        from_date_grace = now_date.replace(month=now_date.month, day=21)
    else:
        # from_date_grace = now_date.replace(month=now_date.month-1, day=21)
        if now_date.month == 1:  # If January, go to December of the previous year
            from_date_grace = now_date.replace(year=now_date.year - 1, month=12, day=21)
        else:
            from_date_grace = now_date.replace(month=now_date.month - 1, day=21)
    to_date_grace = now_date.replace(month=now_date.month, day=20)
    if now_date.day > 20:
        to_date_grace = (to_date_grace + timedelta(days=31)).replace(day=20)
    # from_date_grace = from_date
    # to_date_grace = to_date
    # print(from_date_grace)
    # print(to_date_grace)
    attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(from_date,to_date)),'docstatus':('!=',2)},['*'],order_by='attendance_date')
    for att in attendance:
        hh = check_holiday(att.attendance_date, att.employee)
        if not hh:
            perm_session=''
            od_from_time =''
            od_to_time =''
            if att.on_duty_application:
                od_session = frappe.db.get_value("On Duty Application",{'name':att.on_duty_application},["session"])

                od_date = att.attendance_date
                od_from_time=att.session_from_time
                od_to_time=att.session_to_time
                od_from_time = safe_time_conversion(od_from_time)
                # att_date = add_days(att_date,1)
                od_from_time = datetime.combine(od_date, od_from_time) 
                
                od_to_time = safe_time_conversion(od_to_time)
                # if att.shift == '2':
                #     # if perm_hour == 1:
                #     od_date = add_days(od_date,1)
                od_to_time = datetime.combine(od_date, od_to_time)
            if att.permission:
                perm_session=frappe.db.get_value('Permission Request',{"employee_id":att.employee,'permission_date':att.attendance_date,'docstatus':1},['session'])
                perm_to_time=frappe.db.get_value('Permission Request',{"employee_id":att.employee,'permission_date':att.attendance_date,'docstatus':1},['to_time'])
                perm_from_time=frappe.db.get_value('Permission Request',{"employee_id":att.employee,'permission_date':att.attendance_date,'docstatus':1},['from_time'])
                perm_from_time = safe_time_conversion(perm_from_time)
                perm_to_time = safe_time_conversion(perm_to_time)
                if perm_session and perm_session =='Second Half' :
                    if perm_from_time:
                        perm_hour=frappe.db.get_value('Permission Request',{"employee_id":att.employee,'permission_date':att.attendance_date,'docstatus':1},['permission_hour'])
                        att_date = att.attendance_date
                        if att.shift == '2':
                            if perm_hour == 1:
                                att_date = add_days(att_date,1)
                        permission_start_time = datetime.combine(att_date, perm_from_time)  
                if perm_session and perm_session =='First Half' :
                   if perm_to_time:                  
                        permission_end_time = datetime.combine(att.attendance_date, perm_to_time) 
            if att.status not in ['On Leave', 'Work From Home']:
                if att.shift and att.in_time:
                    shift_time_start = frappe.get_value("Shift Type", {'name': att.shift}, ["start_time"])
                    shift_start_time = datetime.strptime(str(shift_time_start), '%H:%M:%S').time()
                    start_time = dt.datetime.combine(att.attendance_date, shift_start_time)
                    grace_start_time = start_time + timedelta(minutes=6)
                    start_time += dt.timedelta(minutes=1)
                    grace_count_late = frappe.db.count('Attendance', {'employee': att.employee,'attendance_date': ('between', (from_date_grace, to_date_grace)),'late_grace_count': 1,'status':['!=','On Leave']})
                    if att.on_duty_application and od_from_time and od_to_time and od_session != 'Full Day':
                        if od_from_time < att.in_time:
                            start_time = od_to_time
                            start_time += dt.timedelta(minutes=1)
                            grace_start_time = start_time + timedelta(minutes=6)
                            if od_session == 'Second Half':
                                att.in_time = od_from_time
                    if not att.permission:
                        if att.in_time > start_time:
                            if grace_count_late < 2:
                                if att.in_time < grace_start_time:
                                    frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
                                    frappe.db.set_value('Attendance', att.name, 'late_entry_time','00:00:00')
                                    frappe.db.set_value('Attendance', att.name, 'late_grace_count', 1)
                                else:
                                    frappe.db.set_value('Attendance', att.name, 'late_entry', 1)
                                    frappe.db.set_value('Attendance', att.name, 'late_entry_time', att.in_time - start_time)
                                    frappe.db.set_value('Attendance', att.name, 'late_grace_count', 1)
                                    if int(att.total_working_hours) >=4 and att.leave_application is None:
                                        frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                            else:
                                if att.late_grace_count == 1:
                                    if att.in_time < grace_start_time:
                                        frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
                                        frappe.db.set_value('Attendance', att.name, 'late_entry_time','00:00:00')
                                    else:
                                        frappe.db.set_value('Attendance', att.name, 'late_entry', 1)
                                        frappe.db.set_value('Attendance', att.name, 'late_entry_time', att.in_time - start_time)
                                        if int(att.total_working_hours) >=4 and att.leave_application is None:
                                            frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                                else:
                                    frappe.db.set_value('Attendance', att.name, 'late_entry', 1)
                                    frappe.db.set_value('Attendance', att.name, 'late_entry_time', att.in_time - start_time)
                                    if int(att.total_working_hours) >=4 and att.leave_application is None:
                                        frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                        else:
                            frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
                            frappe.db.set_value('Attendance', att.name, 'late_entry_time', "00:00:00")       
                    
                    elif att.permission:
                        if perm_session:
                            if perm_session == 'First Half': 
                                grace_start_time_for_permission = permission_end_time + timedelta(minutes=6)
                                if att.in_time > permission_end_time:
                                    if grace_count_late < 2:
                                        if att.in_time < grace_start_time_for_permission:
                                            frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
                                            frappe.db.set_value('Attendance', att.name, 'late_entry_time','00:00:00')
                                            frappe.db.set_value('Attendance', att.name, 'late_grace_count', 1)
                                        else:
                                            frappe.db.set_value('Attendance', att.name, 'late_entry', 1)
                                            frappe.db.set_value('Attendance', att.name, 'late_entry_time', att.in_time - permission_end_time)
                                            frappe.db.set_value('Attendance', att.name, 'late_grace_count', 1)
                                            if int(att.total_working_hours) >=4 and att.leave_application is None:
                                                frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                                    else:
                                        if att.late_grace_count == 1:
                                            if att.in_time < grace_start_time_for_permission:
                                                frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
                                                frappe.db.set_value('Attendance', att.name, 'late_entry_time','00:00:00')
                                            else:
                                                frappe.db.set_value('Attendance', att.name, 'late_entry', 1)
                                                frappe.db.set_value('Attendance', att.name, 'late_entry_time', att.in_time - permission_end_time)
                                                if int(att.total_working_hours) >=4 and att.leave_application is None:
                                                    frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                                        else:
                                            frappe.db.set_value('Attendance', att.name, 'late_entry', 1)
                                            frappe.db.set_value('Attendance', att.name, 'late_entry_time', att.in_time - permission_end_time)
                                            if int(att.total_working_hours) >=4 and att.leave_application is None:
                                                frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                                        
                                else:
                                    if att.late_grace_count:
                                        frappe.db.set_value('Attendance', att.name, 'late_grace_count', 0)
                                    frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
                                    frappe.db.set_value('Attendance', att.name, 'late_entry_time', "00:00:00")

                    else:
                        frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
                        frappe.db.set_value('Attendance', att.name, 'late_entry_time', "00:00:00")

                if att.shift and att.out_time:
                    shift_time_end = frappe.get_value("Shift Type", {'name': att.shift}, ["end_time"])
                    shift_end_time = datetime.strptime(str(shift_time_end), '%H:%M:%S').time()
                    att_date = att.attendance_date
                    if att.shift == '2':
                        att_date = add_days(att_date,1)
                        # print("2")
                    end_time = dt.datetime.combine(att_date, shift_end_time)
                    grace_end_time = end_time - timedelta(minutes=6)
                    grace_count_early = frappe.db.count('Attendance', {'employee': att.employee,'attendance_date': ('between', (from_date_grace, to_date_grace)),'early_grace_count': 1,'status':['!=','On Leave']})
                    if att.on_duty_application and od_from_time and od_to_time and od_session != 'Full Day':
                        if od_to_time > att.out_time:
                            end_time = od_from_time
                            grace_end_time = end_time - timedelta(minutes=6)
                            if od_session == 'First Half':
                                att.out_time = od_to_time
                    if not att.permission:
                        if att.out_time < end_time:
                            # print(att.name)
                            if grace_count_early < 2:
                                # print(att.name)
                                if att.out_time > grace_end_time:
                                    frappe.db.set_value('Attendance', att.name, 'early_exit', 0)
                                    frappe.db.set_value('Attendance', att.name, 'early_out_time', "00:00:00")
                                    frappe.db.set_value('Attendance', att.name, 'early_grace_count', 1)
                                else:
                                    frappe.db.set_value('Attendance', att.name, 'early_exit', 1)
                                    frappe.db.set_value('Attendance', att.name, 'early_out_time', end_time - att.out_time)
                                    frappe.db.set_value('Attendance', att.name, 'early_grace_count', 1)
                                    if int(att.total_working_hours) >=4 and att.leave_application is None:
                                        frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                            else:
                                if att.early_grace_count == 1:
                                    if att.out_time > grace_end_time:
                                        frappe.db.set_value('Attendance', att.name, 'early_exit', 0)
                                        frappe.db.set_value('Attendance', att.name, 'early_out_time', "00:00:00")
                                    else:
                                        frappe.db.set_value('Attendance', att.name, 'early_exit', 1)
                                        frappe.db.set_value('Attendance', att.name, 'early_out_time', end_time - att.out_time)
                                        if int(att.total_working_hours) >=4 and att.leave_application is None:
                                            frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                                else:
                                    frappe.db.set_value('Attendance', att.name, 'early_exit', 1)
                                    frappe.db.set_value('Attendance', att.name, 'early_out_time', end_time - att.out_time)
                                    if int(att.total_working_hours) >=4 and att.leave_application is None:
                                        frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                        else:
                            # print(att.name)
                            # print(att.employee)
                            frappe.db.set_value('Attendance', att.name, 'early_exit', 0)
                            frappe.db.set_value('Attendance', att.name, 'early_out_time', "00:00:00")
                    
                    elif perm_session:
                        if perm_session =='Second Half':
                            grace_end_time_for_permission = permission_start_time - timedelta(minutes=6)
                            if att.out_time < permission_start_time:
                                if grace_count_early < 2:
                                    if att.out_time < grace_end_time_for_permission:
                                        frappe.db.set_value('Attendance', att.name, 'early_exit', 0)
                                        frappe.db.set_value('Attendance', att.name, 'early_out_time', "00:00:00")
                                        frappe.db.set_value('Attendance', att.name, 'early_grace_count', 1)
                                    else:
                                        frappe.db.set_value('Attendance', att.name, 'early_exit', 1)
                                        frappe.db.set_value('Attendance', att.name, 'early_out_time', permission_start_time - att.out_time)
                                        frappe.db.set_value('Attendance', att.name, 'early_grace_count', 1)
                                        if int(att.total_working_hours) >=4 and att.leave_application is None:
                                            frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                                else:
                                    if att.early_grace_count == 1:
                                        if att.out_time < grace_end_time_for_permission:
                                            frappe.db.set_value('Attendance', att.name, 'early_exit', 0)
                                            frappe.db.set_value('Attendance', att.name, 'early_out_time', "00:00:00")
                                            frappe.db.set_value('Attendance', att.name, 'early_grace_count', 1)
                                        else:
                                            frappe.db.set_value('Attendance', att.name, 'early_exit', 1)
                                            frappe.db.set_value('Attendance', att.name, 'early_out_time', permission_start_time - att.out_time)
                                            frappe.db.set_value('Attendance', att.name, 'early_grace_count', 1)
                                            if int(att.total_working_hours) >=4 and att.leave_application is None:
                                                frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                                    else:
                                        frappe.db.set_value('Attendance', att.name, 'early_exit', 1)
                                        frappe.db.set_value('Attendance', att.name, 'early_out_time', permission_start_time - att.out_time)
                                        if int(att.total_working_hours) >=4 and att.leave_application is None:
                                            frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                            else:
                                if att.early_grace_count:
                                    frappe.db.set_value('Attendance', att.name, 'early_grace_count', 0)
                                frappe.db.set_value('Attendance', att.name, 'early_exit', 0)
                                frappe.db.set_value('Attendance', att.name, 'early_out_time', "00:00:00")                                       
                    
        
        
            else:
                frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
                frappe.db.set_value('Attendance', att.name, 'late_entry_time', "00:00:00")
                frappe.db.set_value('Attendance', att.name, 'early_exit', 0)
                frappe.db.set_value('Attendance', att.name, 'early_out_time', "00:00:00")
        
        else:
            frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
            frappe.db.set_value('Attendance', att.name, 'late_entry_time', "00:00:00")
            frappe.db.set_value('Attendance', att.name, 'early_exit', 0)
            frappe.db.set_value('Attendance', att.name, 'early_out_time', "00:00:00")

    employee_records = frappe.db.get_all("Employee",{'status':'Active','date_of_joining': ['<=', to_date]},['name'])
    for emp in employee_records:
        attendance_records = frappe.db.get_all('Attendance', {'attendance_date': ('between', (from_date_grace, to_date_grace)),'docstatus': ('!=', 2),'late_entry': 1,'early_exit':1 ,'employee': emp.name}, ['name','employee','attendance_date','status','early_exit','late_entry'], order_by='attendance_date')
        for att in attendance_records:
            is_holiday = check_holiday(att.attendance_date, att.employee)
            if not is_holiday and att.status not in ['On Leave', 'Work From Home']:
                if att.late_entry and att.early_exit:
                    frappe.db.set_value('Attendance', att.name, 'status', 'Absent')



def mark_late_early_updates_with_employee(from_date,to_date,employee):
    now_date=datetime.today()
    now_date= getdate(from_date)
    if now_date.day >= 21:
        from_date_grace = now_date.replace(month=now_date.month, day=21)
    else:
        # from_date_grace = now_date.replace(month=now_date.month-1, day=21)
        if now_date.month == 1:  # If January, go to December of the previous year
            from_date_grace = now_date.replace(year=now_date.year - 1, month=12, day=21)
        else:
            from_date_grace = now_date.replace(month=now_date.month - 1, day=21)
    to_date_grace = now_date.replace(month=now_date.month, day=20)
    if now_date.day > 20:
        to_date_grace = (to_date_grace + timedelta(days=31)).replace(day=20)
    # from_date_grace = from_date
    # to_date_grace = to_date
    print(from_date_grace)
    print(to_date_grace)
    attendance = frappe.db.get_all('Attendance',{'employee':employee,'attendance_date':('between',(from_date,to_date)),'docstatus':('!=',2)},['*'],order_by='attendance_date')
    for att in attendance:
        hh = check_holiday(att.attendance_date, att.employee)
        if not hh:
            perm_session=''
            od_from_time =''
            od_to_time =''
            if att.on_duty_application:
                od_session = frappe.db.get_value("On Duty Application",{'name':att.on_duty_application},["session"])

                od_date = att.attendance_date
                od_from_time=att.session_from_time
                od_to_time=att.session_to_time
                od_from_time = safe_time_conversion(od_from_time)
                # att_date = add_days(att_date,1)
                od_from_time = datetime.combine(od_date, od_from_time) 
                
                od_to_time = safe_time_conversion(od_to_time)
                # if att.shift == '2':
                #     # if perm_hour == 1:
                #     od_date = add_days(od_date,1)
                od_to_time = datetime.combine(od_date, od_to_time)
            # print(att.status)
            if att.permission:
                perm_session=frappe.db.get_value('Permission Request',{"employee_id":att.employee,'permission_date':att.attendance_date,'docstatus':1},['session'])
                perm_to_time=frappe.db.get_value('Permission Request',{"employee_id":att.employee,'permission_date':att.attendance_date,'docstatus':1},['to_time'])
                perm_from_time=frappe.db.get_value('Permission Request',{"employee_id":att.employee,'permission_date':att.attendance_date,'docstatus':1},['from_time'])
                perm_from_time = safe_time_conversion(perm_from_time)
                perm_to_time = safe_time_conversion(perm_to_time)
                if perm_session and perm_session =='Second Half' :
                    if perm_from_time:
                        perm_hour=frappe.db.get_value('Permission Request',{"employee_id":att.employee,'permission_date':att.attendance_date,'docstatus':1},['permission_hour'])
                        att_date = att.attendance_date
                        if att.shift == '2':
                            if perm_hour == 1:
                                att_date = add_days(att_date,1)
                        permission_start_time = datetime.combine(att_date, perm_from_time)  
                if perm_session and perm_session =='First Half' :
                   if perm_to_time:                  
                        permission_end_time = datetime.combine(att.attendance_date, perm_to_time) 
            if att.status not in ['On Leave', 'Work From Home']:
                if att.shift and att.in_time:
                    shift_time_start = frappe.get_value("Shift Type", {'name': att.shift}, ["start_time"])
                    shift_start_time = datetime.strptime(str(shift_time_start), '%H:%M:%S').time()
                    start_time = dt.datetime.combine(att.attendance_date, shift_start_time)
                    grace_start_time = start_time + timedelta(minutes=6)
                    start_time += dt.timedelta(minutes=1)
                    grace_count_late = frappe.db.count('Attendance', {'employee': att.employee,'attendance_date': ('between', (from_date_grace, to_date_grace)),'late_grace_count': 1,'status':['!=','On Leave']})
                    if att.on_duty_application and od_from_time and od_to_time and od_session != 'Full Day':
                        if od_from_time < att.in_time:
                            start_time = od_to_time
                            start_time += dt.timedelta(minutes=1)
                            grace_start_time = start_time + timedelta(minutes=6)
                            if od_session == 'Second Half':
                                att.in_time = od_from_time
                    if not att.permission:
                        if att.in_time > start_time:
                            if grace_count_late < 2:
                                if att.in_time < grace_start_time:
                                    frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
                                    frappe.db.set_value('Attendance', att.name, 'late_entry_time','00:00:00')
                                    frappe.db.set_value('Attendance', att.name, 'late_grace_count', 1)
                                else:
                                    frappe.db.set_value('Attendance', att.name, 'late_entry', 1)
                                    frappe.db.set_value('Attendance', att.name, 'late_entry_time', att.in_time - start_time)
                                    frappe.db.set_value('Attendance', att.name, 'late_grace_count', 1)
                                    if int(att.total_working_hours) >=4 and att.leave_application is None:
                                        frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                            else:
                                if att.late_grace_count == 1:
                                    if att.in_time < grace_start_time:
                                        frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
                                        frappe.db.set_value('Attendance', att.name, 'late_entry_time','00:00:00')
                                    else:
                                        frappe.db.set_value('Attendance', att.name, 'late_entry', 1)
                                        frappe.db.set_value('Attendance', att.name, 'late_entry_time', att.in_time - start_time)
                                        if int(att.total_working_hours) >=4 and att.leave_application is None:
                                            frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                                else:
                                    frappe.db.set_value('Attendance', att.name, 'late_entry', 1)
                                    frappe.db.set_value('Attendance', att.name, 'late_entry_time', att.in_time - start_time)
                                    if int(att.total_working_hours) >=4 and att.leave_application is None:
                                        frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                        else:
                            frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
                            frappe.db.set_value('Attendance', att.name, 'late_entry_time', "00:00:00")       
                    
                    elif att.permission:
                        if perm_session:
                            if perm_session == 'First Half': 
                                grace_start_time_for_permission = permission_end_time + timedelta(minutes=6)
                                if att.in_time > permission_end_time:
                                    if grace_count_late < 2:
                                        if att.in_time < grace_start_time_for_permission:
                                            frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
                                            frappe.db.set_value('Attendance', att.name, 'late_entry_time','00:00:00')
                                            frappe.db.set_value('Attendance', att.name, 'late_grace_count', 1)
                                        else:
                                            frappe.db.set_value('Attendance', att.name, 'late_entry', 1)
                                            frappe.db.set_value('Attendance', att.name, 'late_entry_time', att.in_time - permission_end_time)
                                            frappe.db.set_value('Attendance', att.name, 'late_grace_count', 1)
                                            if int(att.total_working_hours) >=4 and att.leave_application is None:
                                                frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                                    else:
                                        if att.late_grace_count == 1:
                                            if att.in_time < grace_start_time_for_permission:
                                                frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
                                                frappe.db.set_value('Attendance', att.name, 'late_entry_time','00:00:00')
                                            else:
                                                frappe.db.set_value('Attendance', att.name, 'late_entry', 1)
                                                frappe.db.set_value('Attendance', att.name, 'late_entry_time', att.in_time - permission_end_time)
                                                if int(att.total_working_hours) >=4 and att.leave_application is None:
                                                    frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                                        else:
                                            frappe.db.set_value('Attendance', att.name, 'late_entry', 1)
                                            frappe.db.set_value('Attendance', att.name, 'late_entry_time', att.in_time - permission_end_time)
                                            if int(att.total_working_hours) >=4 and att.leave_application is None:
                                                frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                                        
                                else:
                                    if att.late_grace_count:
                                        frappe.db.set_value('Attendance', att.name, 'late_grace_count', 0)
                                    frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
                                    frappe.db.set_value('Attendance', att.name, 'late_entry_time', "00:00:00")

                    else:
                        frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
                        frappe.db.set_value('Attendance', att.name, 'late_entry_time', "00:00:00")

                if att.shift and att.out_time:
                    shift_time_end = frappe.get_value("Shift Type", {'name': att.shift}, ["end_time"])
                    shift_end_time = datetime.strptime(str(shift_time_end), '%H:%M:%S').time()
                    att_date = att.attendance_date
                    if att.shift == '2':
                        att_date = add_days(att_date,1)
                        # print("2")
                    end_time = dt.datetime.combine(att_date, shift_end_time)
                    grace_end_time = end_time - timedelta(minutes=6)
                    grace_count_early = frappe.db.count('Attendance', {'employee': att.employee,'attendance_date': ('between', (from_date_grace, to_date_grace)),'early_grace_count': 1,'status':['!=','On Leave']})
                    if att.on_duty_application and od_from_time and od_to_time and od_session != 'Full Day':
                        if od_to_time > att.out_time:
                            end_time = od_from_time
                            grace_end_time = end_time - timedelta(minutes=6)
                            if od_session == 'First Half':
                                att.out_time = od_to_time
                    if not att.permission:
                        if att.out_time < end_time:
                            # print(att.name)
                            if grace_count_early < 2:
                                # print(att.name)
                                if att.out_time > grace_end_time:
                                    frappe.db.set_value('Attendance', att.name, 'early_exit', 0)
                                    frappe.db.set_value('Attendance', att.name, 'early_out_time', "00:00:00")
                                    frappe.db.set_value('Attendance', att.name, 'early_grace_count', 1)
                                else:
                                    frappe.db.set_value('Attendance', att.name, 'early_exit', 1)
                                    frappe.db.set_value('Attendance', att.name, 'early_out_time', end_time - att.out_time)
                                    frappe.db.set_value('Attendance', att.name, 'early_grace_count', 1)
                                    if int(att.total_working_hours) >=4 and att.leave_application is None:
                                        frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                            else:
                                if att.early_grace_count == 1:
                                    # print(att.early_grace_count)
                                    if att.out_time > grace_end_time:
                                        # print(att.out_time)
                                        frappe.db.set_value('Attendance', att.name, 'early_exit', 0)
                                        frappe.db.set_value('Attendance', att.name, 'early_out_time', "00:00:00")
                                    else:
                                        frappe.db.set_value('Attendance', att.name, 'early_exit', 1)
                                        frappe.db.set_value('Attendance', att.name, 'early_out_time', end_time - att.out_time)
                                        if int(att.total_working_hours) >=4 and att.leave_application is None:
                                            frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                                else:
                                    frappe.db.set_value('Attendance', att.name, 'early_exit', 1)
                                    frappe.db.set_value('Attendance', att.name, 'early_out_time', end_time - att.out_time)
                                    if int(att.total_working_hours) >=4 and att.leave_application is None:
                                        frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                        else:
                            # print(att.name)
                            # print(att.employee)
                            frappe.db.set_value('Attendance', att.name, 'early_exit', 0)
                            frappe.db.set_value('Attendance', att.name, 'early_out_time', "00:00:00")
                    
                    elif perm_session:
                        if perm_session =='Second Half':
                            grace_end_time_for_permission = permission_start_time - timedelta(minutes=6)
                            if att.out_time < permission_start_time:
                                # print(permission_start_time)
                                if grace_count_early < 2:
                                    if att.out_time < grace_end_time_for_permission:
                                        frappe.db.set_value('Attendance', att.name, 'early_exit', 0)
                                        frappe.db.set_value('Attendance', att.name, 'early_out_time', "00:00:00")
                                        frappe.db.set_value('Attendance', att.name, 'early_grace_count', 1)
                                    else:
                                        frappe.db.set_value('Attendance', att.name, 'early_exit', 1)
                                        frappe.db.set_value('Attendance', att.name, 'early_out_time', permission_start_time - att.out_time)
                                        frappe.db.set_value('Attendance', att.name, 'early_grace_count', 1)
                                        if int(att.total_working_hours) >=4 and att.leave_application is None:
                                            frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                                else:
                                    if att.early_grace_count == 1:
                                        if att.out_time < grace_end_time_for_permission:
                                            frappe.db.set_value('Attendance', att.name, 'early_exit', 0)
                                            frappe.db.set_value('Attendance', att.name, 'early_out_time', "00:00:00")
                                            frappe.db.set_value('Attendance', att.name, 'early_grace_count', 1)
                                        else:
                                            frappe.db.set_value('Attendance', att.name, 'early_exit', 1)
                                            frappe.db.set_value('Attendance', att.name, 'early_out_time', permission_start_time - att.out_time)
                                            frappe.db.set_value('Attendance', att.name, 'early_grace_count', 1)
                                            if int(att.total_working_hours) >=4 and att.leave_application is None:
                                                frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                                    else:
                                        frappe.db.set_value('Attendance', att.name, 'early_exit', 1)
                                        frappe.db.set_value('Attendance', att.name, 'early_out_time', permission_start_time - att.out_time)
                                        if int(att.total_working_hours) >=4 and att.leave_application is None:
                                            frappe.db.set_value('Attendance', att.name, 'status', 'Half Day')
                            else:
                                if att.early_grace_count:
                                    frappe.db.set_value('Attendance', att.name, 'early_grace_count', 0)
                                frappe.db.set_value('Attendance', att.name, 'early_exit', 0)
                                frappe.db.set_value('Attendance', att.name, 'early_out_time', "00:00:00")                                       
                    
        
        
            else:
                frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
                frappe.db.set_value('Attendance', att.name, 'late_entry_time', "00:00:00")
                frappe.db.set_value('Attendance', att.name, 'early_exit', 0)
                frappe.db.set_value('Attendance', att.name, 'early_out_time', "00:00:00")
        
        else:
            frappe.db.set_value('Attendance', att.name, 'late_entry', 0)
            frappe.db.set_value('Attendance', att.name, 'late_entry_time', "00:00:00")
            frappe.db.set_value('Attendance', att.name, 'early_exit', 0)
            frappe.db.set_value('Attendance', att.name, 'early_out_time', "00:00:00")

    employee_records = frappe.db.get_all("Employee",{'status':'Active','date_of_joining': ['<=', to_date]},['name'])
    for emp in employee_records:
        attendance_records = frappe.db.get_all('Attendance', {'attendance_date': ('between', (from_date_grace, to_date_grace)),'docstatus': ('!=', 2),'late_entry': 1,'early_exit':1 ,'employee': emp.name}, ['name','employee','attendance_date','status','early_exit','late_entry'], order_by='attendance_date')
        for att in attendance_records:
            is_holiday = check_holiday(att.attendance_date, att.employee)
            if not is_holiday and att.status not in ['On Leave', 'Work From Home']:
                if att.late_entry and att.early_exit:
                    frappe.db.set_value('Attendance', att.name, 'status', 'Absent')




def mark_wh_ot_with_employee_updates(from_date,to_date,employee):
    attendance = frappe.db.get_all('Attendance',{'employee':employee,'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2')},['*'])
    for att in attendance:
        od_hours = 0
        if att.on_duty_application:
            od_hours = frappe.db.get_value("On Duty Application",{'name':att.on_duty_application},["total_od_hours"])
            if od_hours:
                od_hours=int(od_hours)
            else:
                od_hours=0
        if att.in_time and att.out_time and att.shift:
            hh = check_holiday(att.attendance_date,att.employee)
            if not hh:
                if att.out_time < att.in_time:
                    total_wh= "00:00"
                else:
                    total_wh= att.out_time -att.in_time
                ftr = [3600,60,1]
                if att.out_time < att.in_time:
                    wh = 0
                else:
                    wh = time_diff_in_hours(att.out_time,att.in_time)
                perm_time=0
                wh += od_hours
                if wh < 4:
                    if att.permission:
                        perm=frappe.db.get_value("Permission Request",{'name':att.permission},['permission_hour'])
                        if perm:
                            perm=int(perm)
                        else:
                            perm=0
                        perm_time=wh+perm
                        if perm_time >= 4:
                            frappe.db.set_value('Attendance',att.name,'status','Half Day')
                        else:
                            frappe.db.set_value('Attendance',att.name,'status','Absent')
                    else:
                        frappe.db.set_value('Attendance',att.name,'status','Absent')
                    if att.leave_application:
                        leave=frappe.db.get_value("Leave Application",{'name':att.leave_application,'half_day':1,'docstatus':'1','half_day_date':att.attendance_date},['name'])
                        if leave:
                            frappe.db.set_value('Attendance',att.name,'status','Half Day')
                        else:
                            frappe.db.set_value('Attendance',att.name,'status','Absent')
                    else:
                        frappe.db.set_value('Attendance',att.name,'status','Absent')
                elif wh >= 4 and wh < 8:
                    if att.permission:
                        perm=frappe.db.get_value("Permission Request",{'name':att.permission},['permission_hour'])
                        if perm:
                            perm=int(perm)
                        else:
                            perm=0
                        perm_time=wh+perm
                        if perm_time >= 8:
                            frappe.db.set_value('Attendance',att.name,'status','Present')
                        else:
                            frappe.db.set_value('Attendance',att.name,'status','Half Day')
                    else:
                        frappe.db.set_value('Attendance',att.name,'status','Half Day')
                elif wh >= 8:
                    frappe.db.set_value('Attendance',att.name,'status','Present')   
                if att.out_time < att.in_time:
                    wh = 0
                else:
                    wh = time_diff_in_hours(att.out_time,att.in_time)
                shift_start_time = frappe.db.get_value('Shift Type',{'name':att.shift},['start_time'])
                shift_start_time = pd.to_datetime(str(shift_start_time)).time()

                shift_end_time = frappe.db.get_value('Shift Type',{'name':att.shift},['end_time'])
                shift_end_time = pd.to_datetime(str(shift_end_time)).time()

                in_date = att.in_time.date()
                out_date = att.out_time.date()
                get_shift_hours = frappe.db.get_value('Shift Type',{'name':att.shift},['total_shift_hours'])
                total_shift_hours = datetime.strptime(str(get_shift_hours),'%Y-%m-%d %H:%M:%S').time()
                shift_hr = sum([a*b for a,b in zip(ftr, map(int,str(total_shift_hours).split(':')))])
                shift_wh = round(shift_hr/3600,1) 
                shift_start_datetime = datetime.combine(in_date,shift_start_time)
                shift_end_datetime = datetime.combine(att.attendance_date,shift_end_time)
                if att.shift=='2':
                    next_day = add_days(att.attendance_date,1)
                    shift_end_datetime = datetime.combine(next_day,shift_end_time)
                if int(wh) > int(shift_wh):
                    extra_hrs =pd.to_datetime('00:00:00').time()
                    ot_hr = 0
                    try:
                        extra_hrs = att.out_time - shift_end_datetime
                        hr = sum([a*b for a,b in zip(ftr, map(int,str(extra_hrs).split(':')))])
                        extras = round(hr/3600,1)
                    except:
                        extra_hrs = '00:00' 
                        extras = 0 
                    if extras > 1:
                            ot_hr = math.floor(extras * 2) / 2  
                    if wh < 24:
                        frappe.db.set_value('Attendance',att.name,'working_total_hours',total_wh)             
                        frappe.db.set_value('Attendance',att.name,'total_working_hours',round(wh,2))                
                        frappe.db.set_value('Attendance',att.name,'extra_hours',extra_hrs)
                        frappe.db.set_value('Attendance',att.name,'over_time_hours',ot_hr)
                    else:
                        frappe.db.set_value('Attendance',att.name,'working_total_hours','23:59')             
                        frappe.db.set_value('Attendance',att.name,'total_working_hours',round(wh,2))                
                        frappe.db.set_value('Attendance',att.name,'extra_hours',extra_hrs)
                        frappe.db.set_value('Attendance',att.name,'over_time_hours',ot_hr)
                else:
                    if wh > 24:
                        none_time = pd.to_datetime('00:00:00').time()
                        frappe.db.set_value('Attendance',att.name,'working_total_hours','23:59')
                        frappe.db.set_value('Attendance',att.name,'total_working_hours',round(wh,2))  
                        frappe.db.set_value('Attendance',att.name,'extra_hours','00:00')
                        frappe.db.set_value('Attendance',att.name,'over_time_hours',0)
                    else:
                        none_time = pd.to_datetime('00:00:00').time()
                        frappe.db.set_value('Attendance',att.name,'working_total_hours',total_wh)
                        frappe.db.set_value('Attendance',att.name,'total_working_hours',round(wh,2))  
                        frappe.db.set_value('Attendance',att.name,'extra_hours','00:00')
                        frappe.db.set_value('Attendance',att.name,'over_time_hours',0)
            else:
                if att.out_time < att.in_time:
                    frappe.log_error(message=att.name, title="Attendance")
                    total_wh="00:00"
                else:
                    total_wh= att.out_time - att.in_time
                ftr = [3600,60,1]
                max_time = timedelta(hours=23, minutes=59)
                if total_wh < max_time:
                    hr = sum([a*b for a,b in zip(ftr, map(int,str(total_wh).split(':')))])
                    wh = round(hr/3600,1)
                else:
                    wh = round(total_wh.total_seconds() / 3600, 1)
                perm_time=0
                wh += od_hours
                if wh < 4:
                    if att.permission:
                        perm=frappe.db.get_value("Permission Request",{'name':att.permission},['permission_hour'])
                        perm=int(perm)
                        perm_time=wh+perm
                        if perm_time >= 4:
                            frappe.db.set_value('Attendance',att.name,'status','Half Day')
                        else:
                            frappe.db.set_value('Attendance',att.name,'status','Absent')
                    else:
                        frappe.db.set_value('Attendance',att.name,'status','Absent')
                elif wh >= 4 and wh < 8:
                    if att.permission:
                        perm=frappe.db.get_value("Permission Request",{'name':att.permission},['permission_hour'])
                        if perm:
                            perm=int(perm)
                        else:
                            perm=0
                        perm_time=wh+perm
                        if perm_time >= 8:
                            frappe.db.set_value('Attendance',att.name,'status','Present')
                        else:
                            frappe.db.set_value('Attendance',att.name,'status','Half Day')
                    else:
                        frappe.db.set_value('Attendance',att.name,'status','Half Day')
                elif wh >= 8:
                    frappe.db.set_value('Attendance',att.name,'status','Present')  
                if total_wh < max_time:
                    hr = sum([a*b for a,b in zip(ftr, map(int,str(total_wh).split(':')))])
                    wh = round(hr/3600,1)
                else:
                    wh = round(total_wh.total_seconds() / 3600, 1)
                if wh < 24:
                    ot_hr = (math.floor(wh * 2) / 2) - 0.5
                    if ot_hr >= 9:
                        ot_hr = ot_hr - 1
                        # total_wh_time = total_wh - timedelta(hours=1) 
                        # total_wh = str(total_wh_time)
                    frappe.db.set_value('Attendance',att.name,'over_time_hours',ot_hr)
                    none_time =pd.to_datetime('00:00:00').time()
                    frappe.db.set_value('Attendance',att.name,'extra_hours','00:00')
                    frappe.db.set_value('Attendance',att.name,'working_total_hours',total_wh)
                    frappe.db.set_value('Attendance',att.name,'total_working_hours',round(wh,2))
                elif wh >= 24:
                    ot_hr = (math.floor(wh * 2) / 2) - 0.5
                    ot_hr = ot_hr - 1
                    frappe.db.set_value('Attendance',att.name,'over_time_hours',ot_hr)
                    none_time =pd.to_datetime('00:00:00').time()
                    frappe.db.set_value('Attendance',att.name,'extra_hours','00:00')
                    frappe.db.set_value('Attendance',att.name,'working_total_hours','23:59')
                    frappe.db.set_value('Attendance',att.name,'total_working_hours',round(wh,2))
                else:
                    none_time =pd.to_datetime('00:00:00').time()
                    frappe.db.set_value('Attendance',att.name,'over_time_hours',0)
                    frappe.db.set_value('Attendance',att.name,'extra_hours','00:00')
                    frappe.db.set_value('Attendance',att.name,'working_total_hours','00:00')
                    frappe.db.set_value('Attendance',att.name,'total_working_hours',0)   
        else:
            none_time =pd.to_datetime('00:00:00').time()
            frappe.db.set_value('Attendance',att.name,'extra_hours','00:00')
            frappe.db.set_value('Attendance',att.name,'working_total_hours','00:00')
        if att.on_duty_application and ((not att.in_time and not att.out_time) or (att.in_time and not att.out_time) or (att.out_time and not att.in_time ) and att.shift):
            perm=0
            wh = att.total_working_hours
            if att.permission:
                perm=frappe.db.get_value("Permission Request",{'name':att.permission},['permission_hour'])
                if perm:
                    perm=int(perm)
                else:
                    perm=0
            od_hours = frappe.db.get_value("On Duty Application",{'name':att.on_duty_application},["total_od_hours"])
            if od_hours:
                od_hours=int(od_hours)
            else:
                od_hours=0
            od_time=wh+od_hours+perm
            if od_time >= 8:
                frappe.db.set_value('Attendance',att.name,'status','Present')
            elif od_time >= 4 and od_time < 8:
                frappe.db.set_value('Attendance',att.name,'status','Half Day')
            else:
                frappe.db.set_value('Attendance',att.name,'status','Absent')


@frappe.whitelist()
def att_draft_to_submit_with_employee():
    from_date = '2025-01-17'
    to_date = '2025-01-17'
    employee='JMPLGT228'
    draft = frappe.db.get_all('Attendance',
        filters = {
            'docstatus': 0,
            'attendance_date' : ['between', [from_date, to_date]],
            'employee': employee
        },
        fields = ['name'])
    
    for d in draft:
        att_doc = frappe.get_doc("Attendance", d['name'])
        att_doc.submit()

    return 'ok'

@frappe.whitelist()
# def att_draft_to_submit_without_employee(from_date, to_date):
def att_draft_to_submit_without_employee():
    from_date ='2024-12-25'
    to_date ='2024-12-31'
    draft = frappe.db.get_all('Attendance',
            filters = {
                'docstatus': 0,
                'attendance_date': ['between', [from_date, to_date]]
            })
    
    for d in draft:
        att_doc = frappe.get_doc("Attendance", d)
        att_doc.submit()

    return 'ok'

    
def update_overtime_list(from_date,to_date):
    attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2')},
                                   ['in_time','out_time','shift','employee','attendance_date','over_time_hours','total_working_hours','name','shift_status'])
    for att in attendance:
        if att.in_time and att.out_time and att.shift:
            print(att.in_time)
            if frappe.db.exists("Overtime List",{'employee':att.employee,'ot_from_date':att.attendance_date,'ot_to_date':att.attendance_date,'docstatus':['in',[0,1]]}):
                ot_list_doc = frappe.get_doc('Overtime List',{'employee': att.employee,'ot_from_date': att.attendance_date,'docstatus': ['!=',2]})
                print(ot_list_doc)
                if ot_list_doc and ot_list_doc.ot_from_plan:
                    if ot_list_doc.ot_from_plan >=att.over_time_hours:
                        ot_list_doc.attendance = att.name
                        ot_list_doc.in_time = att.in_time
                        ot_list_doc.out_time = att.out_time
                        ot_list_doc.attended_shift = att.shift
                        ot_list_doc.shift_status = att.shift_status
                        ot_list_doc.working_hours = att.total_working_hours
                        ot_list_doc.ot_from_attendance = att.over_time_hours
                        ot_list_doc.permitted_overtime_hours = att.over_time_hours
                        ot_list_doc.save(ignore_permissions=True)
                        frappe.db.commit()
                        frappe.db.set_value("Attendance",att.name,'ot_plan_document',ot_list_doc.name)
                        frappe.db.set_value("Attendance",att.name,'planned_ot_hours',ot_list_doc.ot_from_plan)
                        frappe.db.set_value("Attendance",att.name,'updated_ot_hours',att.over_time_hours)
                    elif ot_list_doc.ot_from_plan < att.over_time_hours:
                        ot_list_doc.attendance = att.name
                        ot_list_doc.in_time = att.in_time
                        ot_list_doc.out_time = att.out_time
                        ot_list_doc.attended_shift = att.shift
                        ot_list_doc.shift_status = att.shift_status
                        ot_list_doc.working_hours = att.total_working_hours
                        ot_list_doc.ot_from_attendance = att.over_time_hours
                        ot_list_doc.permitted_overtime_hours = ot_list_doc.ot_from_plan
                        ot_list_doc.save(ignore_permissions=True)
                        frappe.db.commit()
                        frappe.db.set_value("Attendance",att.name,'ot_plan_document',ot_list_doc.name)
                        frappe.db.set_value("Attendance",att.name,'planned_ot_hours',ot_list_doc.ot_from_plan)
                        frappe.db.set_value("Attendance",att.name,'updated_ot_hours',ot_list_doc.ot_from_plan)
                
    
def update_overtime_list_with_employee(from_date,to_date,employee):
    attendance = frappe.db.get_all('Attendance',{'employee':employee,'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2')},
                                   ['in_time','out_time','shift','employee','attendance_date','over_time_hours','total_working_hours','name','shift_status'])
    for att in attendance:
        if att.in_time and att.out_time and att.shift:
            print(att.in_time)
            if frappe.db.exists("Overtime List",{'employee':att.employee,'ot_from_date':att.attendance_date,'ot_to_date':att.attendance_date,'docstatus':['in',[0,1]]}):
                ot_list_doc = frappe.get_doc('Overtime List',{'employee': att.employee,'ot_from_date': att.attendance_date,'docstatus': ['!=',2]})
                print(ot_list_doc)
                if ot_list_doc and ot_list_doc.ot_from_plan:
                    if ot_list_doc.ot_from_plan >=att.over_time_hours:
                        ot_list_doc.attendance = att.name
                        ot_list_doc.in_time = att.in_time
                        ot_list_doc.out_time = att.out_time
                        ot_list_doc.attended_shift = att.shift
                        ot_list_doc.shift_status = att.shift_status
                        ot_list_doc.working_hours = att.total_working_hours
                        ot_list_doc.ot_from_attendance = att.over_time_hours
                        ot_list_doc.permitted_overtime_hours = att.over_time_hours
                        ot_list_doc.save(ignore_permissions=True)
                        frappe.db.commit()
                        frappe.db.set_value("Attendance",att.name,'ot_plan_document',ot_list_doc.name)
                        frappe.db.set_value("Attendance",att.name,'planned_ot_hours',ot_list_doc.ot_from_plan)
                        frappe.db.set_value("Attendance",att.name,'updated_ot_hours',att.over_time_hours)
                    elif ot_list_doc.ot_from_plan < att.over_time_hours:
                        ot_list_doc.attendance = att.name
                        ot_list_doc.in_time = att.in_time
                        ot_list_doc.out_time = att.out_time
                        ot_list_doc.attended_shift = att.shift
                        ot_list_doc.shift_status = att.shift_status
                        ot_list_doc.working_hours = att.total_working_hours
                        ot_list_doc.ot_from_attendance = att.over_time_hours
                        ot_list_doc.permitted_overtime_hours = ot_list_doc.ot_from_plan
                        ot_list_doc.save(ignore_permissions=True)
                        frappe.db.commit()
                        frappe.db.set_value("Attendance",att.name,'ot_plan_document',ot_list_doc.name)
                        frappe.db.set_value("Attendance",att.name,'planned_ot_hours',ot_list_doc.ot_from_plan)
                        frappe.db.set_value("Attendance",att.name,'updated_ot_hours',ot_list_doc.ot_from_plan)
                



@frappe.whitelist()
def update_overtime_list_with_department(from_date,to_date,department):
    attendance = frappe.db.get_all('Attendance',{'department':department,'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2')},
                                   ['in_time','out_time','shift','employee','attendance_date','over_time_hours','total_working_hours','name','shift_status'])
    for att in attendance:
        if att.in_time and att.out_time and att.shift:
            print(att.in_time)
            if frappe.db.exists("Overtime List",{'employee':att.employee,'ot_from_date':att.attendance_date,'ot_to_date':att.attendance_date,'docstatus':['in',[0,1]]}):
                ot_list_doc = frappe.get_doc('Overtime List',{'employee': att.employee,'ot_from_date': att.attendance_date,'docstatus': ['!=',2]})
                print(ot_list_doc)
                if ot_list_doc and ot_list_doc.ot_from_plan:
                    if ot_list_doc.ot_from_plan >=att.over_time_hours:
                        ot_list_doc.attendance = att.name
                        ot_list_doc.in_time = att.in_time
                        ot_list_doc.out_time = att.out_time
                        ot_list_doc.attended_shift = att.shift
                        ot_list_doc.shift_status = att.shift_status
                        ot_list_doc.working_hours = att.total_working_hours
                        ot_list_doc.ot_from_attendance = att.over_time_hours
                        ot_list_doc.permitted_overtime_hours = att.over_time_hours
                        ot_list_doc.save(ignore_permissions=True)
                        frappe.db.commit()
                        frappe.db.set_value("Attendance",att.name,'ot_plan_document',ot_list_doc.name)
                        frappe.db.set_value("Attendance",att.name,'planned_ot_hours',ot_list_doc.ot_from_plan)
                        frappe.db.set_value("Attendance",att.name,'updated_ot_hours',att.over_time_hours)
                    elif ot_list_doc.ot_from_plan < att.over_time_hours:
                        ot_list_doc.attendance = att.name
                        ot_list_doc.in_time = att.in_time
                        ot_list_doc.out_time = att.out_time
                        ot_list_doc.attended_shift = att.shift
                        ot_list_doc.shift_status = att.shift_status
                        ot_list_doc.working_hours = att.total_working_hours
                        ot_list_doc.ot_from_attendance = att.over_time_hours
                        ot_list_doc.permitted_overtime_hours = ot_list_doc.ot_from_plan
                        ot_list_doc.save(ignore_permissions=True)
                        frappe.db.commit()
                        frappe.db.set_value("Attendance",att.name,'ot_plan_document',ot_list_doc.name)
                        frappe.db.set_value("Attendance",att.name,'planned_ot_hours',ot_list_doc.ot_from_plan)
                        frappe.db.set_value("Attendance",att.name,'updated_ot_hours',ot_list_doc.ot_from_plan)
 


def remove_duplicate_attendance(from_date, to_date):

    records = frappe.db.sql("""
        SELECT employee, attendance_date, COUNT(*) as cnt
        FROM `tabAttendance`
        WHERE attendance_date BETWEEN %s AND %s
        GROUP BY employee, attendance_date
        HAVING cnt > 1
    """, (from_date, to_date), as_dict=True)

    for r in records:

        atts = frappe.get_all(
            "Attendance",
            filters={
                "employee": r.employee,
                "attendance_date": r.attendance_date
            },
            fields=["name","shift","in_time","out_time","status"]
        )

        if len(atts) > 1:

            # priority: attendance with in_time
            atts_with_in = [a for a in atts if a.in_time]

            if atts_with_in:
                keep_att = atts_with_in[0]
            else:
                keep_att = atts[0]

            for att in atts:
                if att.name != keep_att.name:
                    frappe.delete_doc("Attendance", att.name, force=1)              



def remove_duplicate_attendance_with_employee(from_date, to_date, employee):

    records = frappe.db.sql("""
        SELECT employee, attendance_date, COUNT(*) as cnt
        FROM `tabAttendance`
        WHERE attendance_date BETWEEN %s AND %s
        AND employee = %s
        GROUP BY employee, attendance_date
        HAVING cnt > 1
    """, (from_date, to_date, employee), as_dict=True)

    for r in records:

        atts = frappe.get_all(
            "Attendance",
            filters={
                "employee": r.employee,
                "attendance_date": r.attendance_date
            },
            fields=["name","shift","in_time","out_time","status"]
        )

        if len(atts) > 1:

            atts_with_in = [a for a in atts if a.in_time]

            if atts_with_in:
                keep_att = atts_with_in[0]
            else:
                keep_att = atts[0]

            for att in atts:
                if att.name != keep_att.name:
                    frappe.delete_doc("Attendance", att.name, force=1)
                    

