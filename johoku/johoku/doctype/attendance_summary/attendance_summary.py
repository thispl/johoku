# Copyright (c) 2025, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date, timedelta, datetime, time
from frappe.utils import cstr, add_days, date_diff,format_datetime

class AttendanceSummary(Document):
	pass



#Attendance summary showing HTML format
@frappe.whitelist()
def get_data_system(emp, from_date, to_date):
    no_of_days = date_diff(add_days(to_date, 1), from_date)
    dates = [add_days(from_date, i) for i in range(no_of_days)]

    emp_details = frappe.db.get_value('Employee', emp, ['employee_name', 'department'])
    data = "<table class='table table-bordered=1'>"	
    data += "<tr><td style='border: 1px solid black;background-color:#17479E;color:white;'><b><center>ID</b></center></b><td style='border: 1px solid black;background-color:#17479E;color:white;' colspan=3><b><center>%s</b></center></b><td style='border: 1px solid black;background-color:#17479E;color:white;'><b><center>Name</b></center></b><td style='border: 1px solid black;background-color:#17479E;color:white;' colspan=3><b><center>%s</b></center></b><td style='border: 1px solid black;background-color:#17479E;color:white;'><b><center>Dept</b></center></b><td style='border: 1px solid black;background-color:#17479E;color:white;' colspan=2><b><center>%s</b></center></b></tr>" % (emp, emp_details[0], emp_details[1])
    data += "<tr><td style='border: 1px solid black;' colspan=11><b><center>Attendance</b></center></td><tr>"
    data += "<tr><td style='border: 1px solid black;background-color:#17479E;color:white;'><b><center>Date</b></center></b><td style='border: 1px solid black;background-color:#17479E;color:white;'><b><center>Day</b></center></b><td style='border: 1px solid black;background-color:#17479E;color:white;'><b><center>Working</b></center></b><td style='border: 1px solid black;background-color:#17479E;color:white;'><b><center>In Time</b></center></b><td style='border: 1px solid black;background-color:#17479E;color:white;'><b><center>Out Time</b></center></b><td colspan=2 style='border: 1px solid black;background-color:#17479E;color:white;'><b><center>Shift</b></center></b><td style='border: 1px solid black;background-color:#17479E;color:white;'><b><center>Status</b></center></b><td style='border: 1px solid black;background-color:#17479E;color:white;'><b><center>Working Hours</b></center></b></td><td style='border: 1px solid black;background-color:#17479E;color:white;font-weight:bold;text-align:center;'>Assigned Shift</td><td style='border: 1px solid black;background-color:#17479E;color:white;font-weight:bold;text-align:center;'>OT</td></tr>"
    total_ot_hours = 0
    for date in dates:
        dt = datetime.strptime(date, '%Y-%m-%d')
        d = dt.strftime('%d-%b')
        day = datetime.date(dt).strftime('%a')
        assigned_shift = frappe.db.get_value(
            "Shift Assignment",
            {
                "employee": emp,
                "start_date": ("<=", date),
                "end_date": (">=", date),
                "docstatus": 1
            },
            "shift_type"
        ) or ""
        permitted_ot_hours = frappe.db.get_value("Overtime List",{"employee": emp,"ot_from_date": date,"docstatus": 1},"permitted_overtime_hours")
        if permitted_ot_hours:
            ot =permitted_ot_hours
        else :
            ot = "0.000"
        total_ot_hours += float(ot)        
        if frappe.db.exists('Attendance', {'employee': emp, "attendance_date": date, 'docstatus': ('!=', '2')}):
            
            att = frappe.get_doc("Attendance",{'attendance_date':date,'employee':emp,'docstatus':('!=','2')})
            
            in_time = att.in_time 
            out_time = att.out_time 
            shift = att.shift 
            status = att.status
            leave_type= att.leave_type
            twh=att.working_total_hours 
            leave_type = att.leave_type
            od = att.on_duty_application
            late = att.late_entry_time
            early = att.early_out_time
            # early = att.custom_early_out_time
            if leave_type :
                if leave_type =="Bereavement leave":
                    leave = "BL"
                if leave_type =="Casual Leave":
                    leave = "CL"
                if leave_type =="Compensatory Off":
                    leave = "C-OFF"
                if leave_type =="Earned Leave":
                    leave = "EL"
                if leave_type =="Leave Without Pay":
                    leave = "LOP"
                if leave_type =="Marriage leave":
                    leave = "MAL"
                if leave_type =="Maternity leave":
                    leave = "MTL"
                if leave_type =="Medical Leave":
                    leave = "MDL"
                if leave_type =="Menstruation Leave":
                    leave = "MSL"
                if leave_type =="Paternity leaves":
                    leave = "PL"
                if leave_type =="Privilege Leave":
                    leave = "PVL"
                if leave_type =="Sick Leave":
                    leave = "SL"
                if leave_type =="Sabbatical Leave":
                    leave = "SBL"
            else:
                leave = "LOP"
            custom_extra_hours = att.over_time_hours 
            # custom_overtime_hours = att.custom_ot_hours 
            holiday = check_holiday(date ,emp)
            if holiday[0]:
                if status == "Holiday":
                    data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#800080'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day,holiday[0],'','','',status or '', '',assigned_shift,ot)
                elif in_time or out_time:
                    if frappe.db.get_value("Employee",{"name":emp},["employment_type"]) == "Agency":
                        data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#800080'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d,day,"W", format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '', status or '', '',assigned_shift,ot)
                    else:
                        data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#800080'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day,holiday[0], format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '', holiday[1] or '', '',assigned_shift,ot)
                else:
                    if frappe.db.get_value("Employee",{"name":emp},["employment_type"]) == "Agency":
                        data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#800080'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" %  (d,day,"W",'','','',status or '','',assigned_shift,ot)
                    else:
                        data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#800080'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" %  (d,day,holiday[0],'','','',holiday[1],'',assigned_shift,ot)
            else:
                if status == "On Leave":
                    data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#964B00'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "L" , format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '',leave, twh or ' ',assigned_shift,ot)
                elif status == "Half Day":
                    if leave_type:
                        leave_applications = frappe.db.sql("""
                        SELECT leave_type 
                        FROM `tabLeave Application` 
                            WHERE from_date=%s AND employee=%s AND status='Approved'
                        """, (date, emp), as_dict=True)
                        if len(leave_applications) > 1:
                            leave_types = []
                            leave_type_map = {
                                "Earned Leave": "EL",
                                "Compensatory Off": "COFF",
                                "Casual Leave": "CL",
                                "Sick Leave": "SL",
                                "Leave Without Pay": "LOP"
                            }
                            for leave in leave_applications:
                                leave_types.append(leave_type_map.get(leave['leave_type'], leave['leave_type']))
                            lstatus = "/".join(leave_types)
                            data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#964B00'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W", format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '', lstatus, twh or '',assigned_shift,ot)
                        
                        elif leave_type and att.in_time and att.out_time:
                            if att.shift == 'G':
                                minute = 30
                            else:
                                minute = 15
                            if att.shift and att.shift == att.shift:
                                
                                if att.working_total_hours >= timedelta(hours=4,minutes=minute):
                                    if frappe.db.get_value("Leave Application",{"name":att.leave_application},["half_day_session"]) == "First Half":
                                        data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#964B00'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W", format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '', leave + "/P", twh or '',assigned_shift,ot)
                                    else:
                                        data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#964B00'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W", format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '', "P/" + leave, twh or '',assigned_shift,ot)
                                else:
                                    if att.permission:
                                        data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#964B00'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W", format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '', "P/" + leave, twh or '',assigned_shift,ot)
                                    else:
                                        if frappe.db.get_value("Leave Application",{"name":att.leave_application},["half_day_session"]) == "Second Half": 
                                            data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#964B00'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W", format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '', "A/" + leave, twh or '',assigned_shift,ot)
                                        else:
                                            data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#964B00'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W", format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '', leave + "/A", twh or '',assigned_shift,ot)
                            else:
                                if frappe.db.get_value("Leave Application",{"name":att.leave_application},["half_day_session"]) == "Second Half": 
                                    data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#964B00'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W", format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '', "A/" + leave, twh or '',assigned_shift,ot)
                                else:
                                    data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#964B00'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W", format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '', leave + "/A", twh or '',assigned_shift,ot)
                        elif leave_type and not att.in_time and not att.out_time:
                                data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#964B00'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W", format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '', "A/" + leave, twh or '',assigned_shift,ot)
                        elif leave_type and not att.in_time or not att.out_time:
                            data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#964B00'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W", format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '', "A/" + leave, twh or '',assigned_shift,ot)
                    elif att.permission:
                        pr = frappe.db.get_value("Permission Request",{'docstatus':('!=','2'),"name":att.permission},['session'])
                        if pr == 'Second Half':    
                            data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#9FF60E'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W", format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '', "A/PR",twh or '',assigned_shift,ot)
                        elif pr == 'First Half':    
                            data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#9FF60E'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W", format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '', "PR/A",twh or '',assigned_shift,ot)
                    elif att.on_duty_application:
                        od = frappe.db.get_value("On Duty Application",{'docstatus':('!=','2'),"name":att.on_duty_application},['session'])
                        time = frappe.db.get_value("On Duty Application",{'docstatus':('!=','2'),"name":att.on_duty_application},['od_time'])
                        if time >4:
                            if od == 'Second Half':
                                if att.working_total_hours >= timedelta(hours=4):
                                    data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#FFA500'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W", format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '', "P/OD",twh or '',assigned_shift,ot)
                                else:
                                    data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#FFA500'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W", format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '', "A/OD",twh or '',assigned_shift,ot)
                            elif od == 'First Half':
                                if att.working_total_hours >= timedelta(hours=4):
                                    data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#FFA500'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W", format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '', "OD/P",twh or '',assigned_shift,ot)
                                else:
                                    data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#FFA500'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W", format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '', "OD/A",twh or '',assigned_shift,ot)
                                    
                            else:
                                data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#FFA500'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W",  '', '', '', "OD/A",'',assigned_shift,ot)
                            if od == 'Second Half':
                                if att.working_total_hours >= timedelta(hours=4):
                                    data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#FFA500'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W", format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '', "P/A",twh or '',assigned_shift,ot)
                                else:
                                    data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#FFA500'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W", format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '', "A",twh or '',assigned_shift,ot)
                            elif od == 'First Half':
                                if att.working_total_hours >= timedelta(hours=4):
                                    data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#FFA500'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W", format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '', "A/P",twh or '',assigned_shift,ot)
                                else:
                                    data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#FFA500'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W", format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '', "A",twh or '',assigned_shift,ot)
                            else:
                                data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#FFA500'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W" , '', '', '',"OD/A", '',assigned_shift,ot)

                    else:
                        if att.late_entry:
                            data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#9FF60E'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W", format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '', "A/P",twh or '',assigned_shift,ot)
                        else:
                            data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#9FF60E'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W", format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '', "P/A",twh or '',assigned_shift,ot)
                elif status == "Present" and att.attendance_request:
                    data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#FFA500'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W" , '', '', '',"On Duty", '',assigned_shift,ot)
                elif status == "Present" and att.on_duty_application:
                    od = frappe.db.get_value("On Duty Application",{'docstatus':('!=','2'),"name":att.on_duty_application},['session'])
                    if od == 'Second Half':
                         data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#FFA500'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W" , format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '',"P/OD", twh or '',assigned_shift,ot)
                    elif od == 'First Half':
                         data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#FFA500'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W" , format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '',"OD/P", twh or '',assigned_shift,ot)
                    else:
                         data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#FFA500'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W" , '', '', '',"OD", '',assigned_shift,ot)
                elif status == "Present" and att.permission:
                    pr = frappe.db.get_value("Permission Request",{'docstatus':('!=','2'),"name":att.permission},['session'])
                    if pr == 'Second Half':    
                        data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#FFA500'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W", format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '', "P/PR",twh or '',assigned_shift,ot)
                    elif pr == 'First Half':    
                        data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#FFA500'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W", format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '', "PR/P",twh or '',assigned_shift,ot)
                
                
                elif status =="Present":
                    data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#008000'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W", format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '', status,twh or '',assigned_shift,ot)
                elif status =="Absent":
                    if att.on_duty_application:
                        od = frappe.db.get_value("On Duty Application",{'docstatus':('!=','2'),"name":att.on_duty_application},['session'])
                        if od == 'Second Half':
                            data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#FFA500'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W" , format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '',"A/OD", '',assigned_shift,ot)
                        elif od == 'First Half':
                            data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#FFA500'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W" , format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '',"OD/A", twh or '',assigned_shift,ot)
                        else:
                            data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#FF0000'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W" , '', '', '',"OD", '',assigned_shift,ot)
                    elif att.permission:
                        pr = frappe.db.get_value("Permission Request",{'docstatus':('!=','2'),"name":att.permission},['session'])
                        if pr == 'Second Half':
                            data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#FFA500'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W" , format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '',"A/PR", '',assigned_shift,ot)
                        elif pr == 'First Half':
                            data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#FFA500'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W" , format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '',"PR/A", twh or '',assigned_shift,ot)
                        
                    else:
                        data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#FF0000'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W", format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '', status,twh or '',assigned_shift,ot)
                else:
                    if att.permission :
                        data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#9FF60E'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W", format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '', status + "/PR",(str(twh)[:5] if twh else ''),twh or '',assigned_shift,ot)
                    else:
                        data += "<tr><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td colspan=2 style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;color:#6b8855'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td><td style='border: 1px solid black;'><center>%s</center></td></tr>" % (d, day, "W", format_datetime(in_time) or '', format_datetime(out_time) or '', shift or '', status,twh or '',assigned_shift,ot)

        else:
            # att=frappe.db.exists('Attendance', {'employee': emp, "attendance_date": date, 'docstatus': ('!=', '2')})
            holiday_list = frappe.db.get_value('Employee', {'name': emp}, 'holiday_list')
            holiday = frappe.db.sql("""
                SELECT `tabHoliday`.holiday_date, `tabHoliday`.weekly_off, `tabHoliday`.description
                FROM `tabHoliday List`
                LEFT JOIN `tabHoliday` ON `tabHoliday`.parent = `tabHoliday List`.name
                WHERE `tabHoliday List`.name = %s AND holiday_date = %s
            """, (holiday_list, date), as_dict=True)

            doj = frappe.db.get_value("Employee", {'name': emp}, "date_of_joining")
            status, desc = '', ''
            relieving_date = frappe.db.get_value('Employee',{'name':emp},'relieving_date')
            if holiday:
                if relieving_date and holiday[0].holiday_date >= relieving_date:
                    status ="L"
                    desc="Left"

                elif doj <= holiday[0].holiday_date:
                    if holiday[0].weekly_off == 1:
                        status = "WW"
                        desc = "Weekly Off"
                    else:
                        status = "HH"
                        desc = holiday[0].description
                else:
                    status = 'NJ'
                    desc = "Not Joined"

            if holiday and status == "WW":
                data += f"""
                    <tr>
                        <td style='border: 1px solid black;'><center>{d}</center></td>
                        <td style='border: 1px solid black;'><center>{day}</center></td>
                        <td style='border: 1px solid black;'><center>{status}</center></td>
                        <td style='border: 1px solid black;'><center></center></td>
                        <td style='border: 1px solid black;'><center></center></td>
                        <td colspan=2 style='border: 1px solid black;'><center></center></td>
                        <td style='border: 1px solid black; color:#00008C'><center>{desc}</center></td>
                        <td style='border: 1px solid black;'><center></center></td>
                        <td style='border: 1px solid black;'><center>{assigned_shift}</center></td>
                        <td style='border: 1px solid black;'><center>{ot}</center></td>
                    </tr>
                """
            elif holiday and status == "L":
                data += f"""
                    <tr>
                        <td style='border: 1px solid black;'><center>{d}</center></td>
                        <td style='border: 1px solid black;'><center>{day}</center></td>
                        <td style='border: 1px solid black;'><center>{status}</center></td>
                        <td style='border: 1px solid black;'><center></center></td>
                        <td style='border: 1px solid black;'><center></center></td>
                        <td colspan=2 style='border: 1px solid black;'><center></center></td>
                        <td style='border: 1px solid black; color:#00008C'><center>{desc}</center></td>
                        <td style='border: 1px solid black;'><center></center></td>
                        <td style='border: 1px solid black;'><center>{assigned_shift}</center></td>
                        <td style='border: 1px solid black;'><center>{ot}</center></td>
                    </tr>
                """
            elif holiday and status == "HH":
                data += f"""
                    <tr>
                        <td style='border: 1px solid black;'><center>{d}</center></td>
                        <td style='border: 1px solid black;'><center>{day}</center></td>
                        <td style='border: 1px solid black;'><center>{status}</center></td>
                        <td style='border: 1px solid black;'><center></center></td>
                        <td style='border: 1px solid black;'><center></center></td>
                        <td colspan=2 style='border: 1px solid black;'><center></center></td>
                        <td style='border: 1px solid black; color:#800080'><center>{desc}</center></td>
                        <td style='border: 1px solid black;'><center></center></td>
                        <td style='border: 1px solid black;'><center>{assigned_shift}</center></td>
                        <td style='border: 1px solid black;'><center>{ot}</center></td>
                    </tr>
                """
            else:
                data += f"""
                    <tr>
                        <td style='border: 1px solid black;'><center>{d}</center></td>
                        <td style='border: 1px solid black;'><center>{day}</center></td>
                        <td style='border: 1px solid black;'><center></center></td>
                        <td style='border: 1px solid black;'><center></center></td>
                        <td style='border: 1px solid black;'><center></center></td>
                        <td colspan=2 style='border: 1px solid black;'><center></center></td>
                        <td style='border: 1px solid black;'><center></center></td>
                        <td style='border: 1px solid black;'><center></center></td>
                        <td style='border: 1px solid black;'><center>{assigned_shift}</center></td>
                        <td style='border: 1px solid black;'><center>{ot}</center></td>
                    </tr>
                """
                
    data += f"""
        <tr style="background-color:#ffe6ee;">
            <td colspan="9"
                style="border:1px solid black;
                    text-align:center;
                    font-weight:bold;
                    color:black;">
                Total OT Hours
            </td>

            <td colspan="2"
                style="border:1px solid black;
                    text-align:center;
                    font-weight:bold;
                    color:red;">
                {round(total_ot_hours, 2)}
            </td>
        </tr>
        """

    data += "</table>"
    return data

def check_holiday(date,emp):
    holiday_list = frappe.db.get_value('Employee',{'name':emp},'holiday_list')
    holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off, `tabHoliday`.description from `tabHoliday List` 
    left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = '%s' and holiday_date = '%s' """%(holiday_list,date),as_dict=True)
    doj= frappe.db.get_value("Employee",{'name':emp},"date_of_joining")
    status = ''
    desc = ''
    week=''
    relieving_date = frappe.db.get_value('Employee',{'name':emp},'relieving_date')
    if holiday :
        if relieving_date and holiday[0].holiday_date >= relieving_date:
            status ="L"
            desc="Left"
        elif doj <= holiday[0].holiday_date:
            if holiday[0].weekly_off == 1:
                status = "WW"
                desc = "Weekly Off"
            else:
                status = "HH"
                desc = holiday[0].description
        else:
            status = 'NJ'
            desc = "Not Joined"
    return status,desc
        

# from frappe.utils import cstr, cint, getdate, get_last_day, get_first_day, add_days,date_diff
# @frappe.whitelist()
# def get_from_to_dates(month,year):
#     if month == 'January':
#         month1 = "01"
#     if month == 'February':
#         month1 = "02"
#     if month == 'March':
#         month1 = "03"
#     if month == 'April':
#         month1 = "04"
#     if month == 'May':
#         month1 = "05"
#     if month == 'June':
#         month1 = "06"
#     if month == 'July':
#         month1 = "07"
#     if month == 'August':
#         month1 = "08"
#     if month == 'September':
#         month1 = "09"
#     if month == 'October':
#         month1 = "10"
#     if month == 'November':
#         month1 = "11"
#     if month == 'December':
#         month1 = "12"
#     formatted_start_date = year + '-' + month1 + '-01'
#     formatted_end_date = get_last_day(formatted_start_date)
#     return formatted_start_date,formatted_end_date

from frappe.utils import getdate, add_months

@frappe.whitelist()
def get_from_to_dates(month, year):

    month_map = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12
    }

    month_no = month_map.get(month)
    if not month_no:
        frappe.throw("Invalid Month")

    start_date = getdate(f"{year}-{month_no:02d}-21")

    next_month_date = add_months(start_date, 1)
    end_date = getdate(f"{next_month_date.year}-{next_month_date.month:02d}-20")

    return start_date, end_date
