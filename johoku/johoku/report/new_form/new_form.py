# Copyright (c) 2013, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from doctest import SKIP
from lzma import FORMAT_RAW
from unittest import skipUnless
import numpy as np
import frappe
from frappe.utils import cstr, cint, getdate,add_days
import datetime
from datetime import date, datetime
from frappe import msgprint, _
from calendar import monthrange
from hrms.payroll.doctype.payroll_entry.payroll_entry import get_start_end_dates, get_end_date

status_map = {    
    "A": "A",
    "a":"1M",
    "b":"2M",
    "c":"3M",
    "d":"M1",
    "e":"M2",
    "f":"M3",
    "g":"NS/M",
    "t":"M/NS",
    "i":"HD/MdL",
    "j":"HD/MaL",
    "k":"HD/CFF",
    "l":"HD/CL",
    "m":"HD/SL",
    "n":"HD/EL",
    "o":"HD/PL",
    "p":"HD/LWP",
    "q":"HD",
    "Holiday": "HH",
    "Weekly Off": "WW",
    "P": "P",
    "W": "WFH",
    "1":"1",
    "2":"2",
    "3":"3",
    "O":"OD",
    "N": "NS/P",
    "E": "EL",
    "C": "CL",
    "S": "SL",
    "P": "PL",
    "L": "LWP",
    "D": "MdL",
    "B": "MaL",
    "F": "CFF",
    "Z":"LE",
    
    }

day_abbr = [
    "Mon",
    "Tue",
    "Wed",
    "Thu",
    "Fri",
    "Sat",
    "Sun"
]

def execute(filters=None):
    frappe.log_error(filters)
    if not filters: filters = {}
    if filters.hide_year_field == 1:
        filters.year = 2020
    conditions, filters = get_conditions(filters)
    columns, days = get_columns(filters)
    att_map = get_attendance_list(conditions, filters)
    if not att_map:
        return columns, [], None, None
    if filters.group_by:
        emp_map, group_by_parameters = get_employee_details(filters.group_by, filters.company)
        holiday_list = []
        for parameter in group_by_parameters:
            h_list = [emp_map[parameter][d]["holiday_list"] for d in emp_map[parameter] if emp_map[parameter][d]["holiday_list"]]
            holiday_list += h_list
    else:
        emp_map = get_employee_details(filters.group_by, filters.company)
        holiday_list = [emp_map[d]["holiday_list"] for d in emp_map if emp_map[d]["holiday_list"]]
    default_holiday_list = frappe.get_cached_value('Company',  filters.get("company"),  "default_holiday_list")
    holiday_list.append(default_holiday_list)
    holiday_list = list(set(holiday_list))
    holiday_map = get_holiday(holiday_list, filters["month"],filters["year"])
    data = []
    leave_list = None
    leave_list = None
    if not filters.summarized_view:
        leave_types = frappe.db.sql("""select name from `tabLeave Type`""", as_list=True)
        leave_list = [d[0] + ":Float:120" for d in leave_types]
        l_list = [d[0] for d in leave_types]
        columns.extend(leave_list)
    if filters.group_by:
        emp_att_map = {}
        for parameter in group_by_parameters:
            emp_map_set = set([key for key in emp_map[parameter].keys()])
            att_map_set = set([key for key in att_map.keys()])
            if (att_map_set & emp_map_set):
                parameter_row = ["<b>"+ parameter + "</b>"] + ['' for day in range(filters["total_days_in_month"] + 2)]
                data.append(parameter_row)
                record, emp_att_data = add_data(emp_map[parameter], att_map, filters, holiday_map, conditions, default_holiday_list, leave_list=l_list)
                emp_att_map.update(emp_att_data)
                data += record
    else:
        record, emp_att_map = add_data(emp_map, att_map, filters, holiday_map, conditions, default_holiday_list, leave_list=l_list)
        data += record
    chart_data = get_chart_data(emp_att_map, days)
    return columns, data, None, chart_data

def get_chart_data(emp_att_map, days):
    labels = []
    datasets = [
        {"name": "Absent", "values": []},
        {"name": "Present", "values": []},
        {"name": "Leave", "values": []},
    ]
    for idx, day in enumerate(days, start=0):
        p = day.replace("::65", "")
        labels.append(day.replace("::65", ""))
        total_absent_on_day = 0
        total_leave_on_day = 0
        total_present_on_day = 0
        total_holiday = 0
        for emp in emp_att_map.keys():
            if emp_att_map[emp][idx]:
                frappe.errprint(emp_att_map[emp][idx])
                if emp_att_map[emp][idx] in ["A","1M","2M","3M","M1","M2","M3","NS/M","M/NS"]:
                    total_absent_on_day += 1
                if emp_att_map[emp][idx] in ["1","2","3","WFH","P","NS/P"]:
                    total_present_on_day += 1
                if emp_att_map[emp][idx] in ["HD/MdL","HD/MaL","HD/CFF","HD/CL","HD/SL","HD/EL","HD/PL","HD/LWP","HD"]:
                    total_present_on_day += 0.5
                    total_leave_on_day += 0.5
                if emp_att_map[emp][idx] in ["MdL","MaL","CFF","CL","SL","EL","PL","LWP","LE"]:
                    total_leave_on_day += 1
        datasets[0]["values"].append(total_absent_on_day)
        datasets[1]["values"].append(total_present_on_day)
        datasets[2]["values"].append(total_leave_on_day)
    chart = {
        "data": {
            'labels': labels,
            'datasets': datasets
        }
    }
    chart["type"] = "line"
    return chart

def add_data(employee_map, att_map, filters, holiday_map, conditions, default_holiday_list, leave_list=None):
    record = []
    emp_att_map = {}
    for emp in employee_map:
        emp_det = employee_map.get(emp)
        if not emp_det or emp not in att_map:
            continue
        row = []
        if filters.group_by:
            row += [" "]
        row += [emp, 
                emp_det.employee_name,
                emp_det.department,
                emp_det.designation,
                emp_det.date_of_birth,
                emp_det.date_of_joining,
                emp_det.work_station or "-",
                emp_det.employee_category or "-",
                emp_det.grade or "-"]
        total_p = 0.0
        total_a = 0.0
        total_h = 0.0
        total_um = 0.0
        total_1 = 0.0
        total_2 = 0.0
        total_3 = 0.0
        total_od = 0.0
        total_l = 0.0
        overtime = 0.0
        emp_status_map = []
        for day in range(filters["total_days_in_month"]):
            status = None
            status = att_map.get(emp).get(day + 1)
            from_date = str(filters.year) + "-" + str(filters.month)+ "-" + str(day+1)
            from_date = datetime.strptime(from_date, "%Y-%m-%d")
            doj = frappe.db.get_value("Employee",emp,'date_of_joining')
            status = None
            emp_holiday_list = emp_det.holiday_list if emp_det.holiday_list else default_holiday_list
            holiday = check_holiday(emp_holiday_list,from_date)
            if holiday:
                # frappe.errprint(holiday)
                status = holiday
                total_h += 1
            elif att_map:
                att = att_map.get(emp).get(day + 1) 
                if att:
                    try:
                        status = att[0]
                    except KeyError:
                        status = None
                                    
            att = att_map.get(emp).get(day + 1)            
            abbr = status_map.get(status, "")
            emp_status_map.append(abbr)
            if not filters.summarized_view:
                # frappe.errprint(status)
                if status == "W":
                    total_p += 1
                elif status == 'O':
                    total_od += 1
                elif status == 'N':
                    total_p += 1
                elif status == "1":
                    total_p += 1
                    total_1 += 1
                elif status == "2":
                    total_p += 1
                    total_2 += 1
                elif status == "3":
                    total_p += 1
                    total_3 += 1
                    # absent
                elif status in ["A","a","b","c","d","e","f","g","t"]:
                    total_a += 1
                    # half-day
                elif status in ["i","j","k","l","m","n","o","p","q"]:
                    total_p += 0.5
                    total_l += 0.5
                    # on leave
                elif status in ["E","C","S","P","L","D","B","F","Z"]:
                    total_l += 1
                elif not status:
                    total_um += 1
                    
        if not filters.summarized_view:
            row += emp_status_map
        if not filters.summarized_view:
            dates = get_start_end_dates('Monthly', filters.month)
            row += [total_1 or 0,
                    total_2 or 0,
                    total_3 or 0,
                    total_od or 0,
                    total_p,
                    total_a,
                    total_l,
                    total_h,
                    total_um]
        if not filters.get("employee"):
            filters.update({"employee": emp})
            conditions += " and employee = %(employee)s"
        elif not filters.get("employee") == emp:
            filters.update({"employee": emp})
        if not filters.summarized_view:
            leave_details = frappe.db.sql("""select leave_type, status, count(*) as count from `tabAttendance`\
                where leave_type is not NULL %s group by leave_type, status""" % conditions, filters, as_dict=1)
            leaves = {}
            for d in leave_details:
                if d.status == "Half Day":
                    d.count = d.count * 0.5
                if d.leave_type in leaves:
                    leaves[d.leave_type] += d.count
                else:
                    leaves[d.leave_type] = d.count
            for d in leave_list:
                if d in leaves:
                    row.append(leaves[d])
                else:
                    row.append("0.0")        
        emp_att_map[emp] = emp_status_map
        record.append(row)
    return record, emp_att_map

def get_columns(filters):
    columns = []
    if filters.group_by:
        columns = [_(filters.group_by)+ ":Link/Branch:120"]
    columns += [
        _("Employee") + ":Link/Employee:150",
        _("Employee Name") + ":Data/:150", 
        _("Department") + ":Data/:150", 
        _("Designation") + ":Data/:150", 
        _("DOB") + ":Date/:150", 
        _("DOJ") + ":date/:150", 
        _("Work Station") + ":Data/:150",
        _("Employee Category") + ":Data/:150",
        _("Grade") + ":Data/:150",
        _("Status") + ":Data/:120"
    ]
    days = []
    for day in range(filters["total_days_in_month"]):
        date = str(filters.year) + "-" + str(filters.month)+ "-" + str(day+1)
        day_name = day_abbr[getdate(date).weekday()]
        days.append(cstr(day+1)+ " " +day_name +"::65")
    if not filters.summarized_view:
        columns += days
    if not filters.summarized_view:
        columns += [_("1st Shift") + ":Float:120",
                    _("2nd Shift") + ":Float:120",
                    _("3rd Shift") + ":Float:120",
                    _("On Duty") + ":Float:120",
                    _("Total Present") + ":Float:120",
                    _("Total Absent") + ":Float:120", 
                    _("Total On Leave") + ":Float:120", 
                    _("Total Holidays") + ":Float:120", 
                    _("Unmarked Days")+ ":Float:120",
                    ]
    return columns, days

def get_attendance_list(conditions, filters):
    attendance_list = frappe.db.sql("""select employee, day(attendance_date) as day_of_month,
        status,shift,attendance_request,leave_type,shift_status,on_duty_application from tabAttendance where docstatus in (0,1) %s order by employee, attendance_date""" %
        conditions, filters, as_dict=1)
    if not attendance_list:
        msgprint(_("No attendance record found"), alert=True, indicator="blue")
    att_map = {}
    for d in attendance_list:
        att_map.setdefault(d.employee, frappe._dict()).setdefault(d.day_of_month,"")
        if d.status == "Present":
            if d.attendance_request:
                att_map[d.employee][d.day_of_month] = "O"
                return 'On Duty'
            elif d.on_duty_application:
                att_map[d.employee][d.day_of_month] = "O"
                # return 'On Duty'
            elif d.shift_status:
                att_map[d.employee][d.day_of_month] = d.shift_status               
        if d.status == 'On Leave':
            if d.leave_type == 'Medical Leave':
                att_map[d.employee][d.day_of_month] = "D"
            elif d.leave_type == 'Maternity Leave':
                att_map[d.employee][d.day_of_month] = "B"
            elif d.leave_type == 'Compensatory Off':
                att_map[d.employee][d.day_of_month] = "F"
            elif d.leave_type != 'Maternity Leave' or 'Medical Leave' or 'Compensatory Off':
                att_map[d.employee][d.day_of_month] = d.leave_type
            # elif d.leave_type == 'Casual Leave':
            #     att_map[d.employee][d.day_of_month] = "l"
            else:
                att_map[d.employee][d.day_of_month] = "Z"
        if d.status == 'Half Day':
            if d.leave_type == 'Medical Leave':
                att_map[d.employee][d.day_of_month] = "i"
            elif d.leave_type == 'Maternity Leave':
                att_map[d.employee][d.day_of_month] = "j"
            elif d.leave_type == 'Compensatory Off':
                att_map[d.employee][d.day_of_month] = "k"
            elif d.leave_type == 'Casual Leave':
                att_map[d.employee][d.day_of_month] = "l"
            elif d.leave_type == 'Sick Leave':
                att_map[d.employee][d.day_of_month] = "m"
            elif d.leave_type == 'Earned Leave':
                att_map[d.employee][d.day_of_month] = "n"
            elif d.leave_type == 'Privilege Leave':
                att_map[d.employee][d.day_of_month] = "0"
            elif d.leave_type == 'Leave Without Pay':
                att_map[d.employee][d.day_of_month] = "p"
            else:
                att_map[d.employee][d.day_of_month] = "q"
        if d.status in ["Work From Home"]:
            att_map[d.employee][d.day_of_month] = d.status
        if d.status == 'Absent':
            if d.shift_status == '1M':
                att_map[d.employee][d.day_of_month] = "a"
            if d.shift_status == '2M':
                att_map[d.employee][d.day_of_month] = "b"
            if d.shift_status == '3M':
                att_map[d.employee][d.day_of_month] = "c"
            if d.shift_status == 'M1':
                att_map[d.employee][d.day_of_month] = "d"
            if d.shift_status == 'M2':
                att_map[d.employee][d.day_of_month] = "e"
            if d.shift_status == 'M3':
                att_map[d.employee][d.day_of_month] = "f"
            if d.shift_status == 'NS/M':
                att_map[d.employee][d.day_of_month] = "g"
            if d.shift_status == 'M/NS':
                att_map[d.employee][d.day_of_month] = "t"
            if d.shift_status == 'AA':
                att_map[d.employee][d.day_of_month] = "A"
            if d.shift_status == '1':
                att_map[d.employee][d.day_of_month] = "A"
            if d.shift_status == '2':
                att_map[d.employee][d.day_of_month] = "A"
            if d.shift_status == '3':
                att_map[d.employee][d.day_of_month] = "A"
            if d.shift_status == '':
                att_map[d.employee][d.day_of_month] = "A"
            if d.shift_status == 'NS/P':
                att_map[d.employee][d.day_of_month] = "N"
            
    return att_map

def get_conditions(filters):
    if not (filters.get("month") and filters.get("year")):
        msgprint(_("Please select month and year"), raise_exception=1)
    filters["total_days_in_month"] = monthrange(cint(filters.year), cint(filters.month))[1]
    conditions = " and month(attendance_date) = %(month)s and year(attendance_date) = %(year)s"
    if filters.get("department"): conditions += " and department = %(department)s"
    if filters.get("company"): conditions += " and company = %(company)s"
    if filters.get("employee"): conditions += " and employee = %(employee)s"
    if filters.get("work_station"): conditions += "and work_station = %(work_station)s"
    # if filters.get("employee_category"): conditions += "and employee_category = %(employee_category)s"
    return conditions, filters

def get_employee_details(group_by, company):
    emp_map = {}
    query = """select name, employee_name, designation, date_of_birth, date_of_joining, grade, department, branch, company,employee_category,work_station,
        holiday_list from `tabEmployee` where company = %s and status = "Active" """ % frappe.db.escape(company)
    if group_by:
        group_by = group_by.lower()
        query += " order by " + group_by + " ASC"
    employee_details = frappe.db.sql(query , as_dict=1)
    group_by_parameters = []
    if group_by:
        group_by_parameters = list(set(detail.get(group_by, "") for detail in employee_details if detail.get(group_by, "")))
        for parameter in group_by_parameters:
                emp_map[parameter] = {}
    for d in employee_details:
        if group_by and len(group_by_parameters):
            if d.get(group_by, None):
                emp_map[d.get(group_by)][d.name] = d
        else:
            emp_map[d.name] = d
    if not group_by:
        return emp_map
    else:
        return emp_map, group_by_parameters

def get_holiday(holiday_list, month,year):
    holiday_map = frappe._dict()
    for d in holiday_list:
        if d:
            holiday_map.setdefault(d, frappe.db.sql('''select day(holiday_date), weekly_off from `tabHoliday`
                where parent=%s and month(holiday_date)=%s and year(holiday_date)=%s''', (d, month,year)))
    return holiday_map

@frappe.whitelist()
def get_attendance_years():
    year_list = frappe.db.sql_list("""select distinct YEAR(attendance_date) from tabAttendance ORDER BY YEAR(attendance_date) DESC""")
    if not year_list:
        year_list = [getdate().year]
    return "\n".join(str(year) for year in year_list)

def check_holiday(hl,date):
    holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
    left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = '%s' and holiday_date = '%s' """%(hl,date),as_dict=True)
    if holiday:
        if holiday[0].weekly_off == 1:
            return "Weekly Off"
        else:
            return "Holiday"