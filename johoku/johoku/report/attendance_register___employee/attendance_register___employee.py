import frappe
from frappe import _
from datetime import timedelta
import pandas as pd

status_map = {
    'Permission Request': 'PR', 'On Duty': 'OD', 'Half Day': 'HD', "Absent": "A", "Holiday": "HH",
    "Weekly Off": "WW", "Present": "P", "On Leave": "On Leave", "Work From Home": "WFH", 
    "Leave Without Pay": "LOP", "Casual Leave": "CL", "Earned Leave": "EL", "Sick Leave": "SL", 
    "Maternity Leave": 'MTL', "Medical Leave": 'MDL', "Privilege Leave": "PVL", 
    "Compensatory Off": "C-OFF", "ESI Leave": "ESI"
}

def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data

def get_columns(filters):
    columns = [
        _("Employee ID") + ":Data/:150", _("Employee Name") + ":Data/:200", _("Department") + ":Data/:150",
        _("Designation") + ":Data/:150", _("Work Station") + ":Data/:150", _("Employee Category") + ":Data/:150",
        _("DOJ") + ":Date/:100", _("") + ":Data/:150"
    ]
    
    # Precompute date range
    dates = pd.date_range(start=filters.from_date, end=filters.to_date)
    for date in dates:
        day = date.strftime('%d')
        month = date.strftime('%b')
        columns.append(_(f"{day}/{month}") + ":Data/:70")
    
    columns += [_("Present") + ":Data/:100", _('Half Day') + ':Data/:100', _("Absent") + ":Data/:100", _("Casual Leave") + ':Data/:100',
    _("Sick Leave") + ':Data/:100',_("Earned Leave") + ':Data/:100',_("Leave Without Pay") + ':Data/:100',_("Compensatory Off") + ':Data/:100',_("On Duty in Days") + ':Data/:100',_("On Duty in Hours") + ':Data/:100',_("Permission") + ':Data/:100',_("Miss IN Punch") + ':Data/:100',_("Miss OUT Punch") + ':Data/:100',_("Holiday") + ':Data/:100',
    _("Weekly Off")]
    
    return columns

def get_data(filters):
    data = []
    employees = get_employees(filters)
    date_range = pd.date_range(start=filters.from_date, end=filters.to_date)
    attendance_data = fetch_attendance_data(filters, employees, date_range)
    # holiday_data = check_holiday(employees, date_range)
    holiday_data_new = fetch_holiday_data(employees)
    permission_data = fetch_permission_data(filters, employees, date_range)
    for emp in employees:
        emp_data = process_employee_data(emp, date_range, attendance_data, holiday_data_new, permission_data)
        data.extend(emp_data)
       
    return data
def fetch_permission_data(filters, employees, date_range):
    employee_ids = [emp.name for emp in employees]
    
    # Fetch all attendance in one query
    attendance = frappe.db.sql("""
        SELECT employee, attendance_date, status, in_time, out_time, shift, 
               over_time_hours, total_working_hours, leave_type, shift_status, 
               on_duty_application, permission 
        FROM `tabAttendance`
        WHERE attendance_date BETWEEN %s AND %s 
        AND employee IN %s
    """, (filters.from_date, filters.to_date, tuple(employee_ids)), as_dict=True)
    permission_hours = {}  
    
    for att in attendance:
        if att.permission:  
            permission_hour_data = frappe.db.sql("""
                SELECT permission_hour
                FROM `tabPermission Request`
                WHERE permission_date BETWEEN %s AND %s 
                AND employee_id IN %s AND name = %s
            """, (filters.from_date, filters.to_date, tuple(employee_ids), att.permission), as_dict=True)
            total_permission_hours = sum([float(p['permission_hour'] or 0) for p in permission_hour_data])
            
            if att.employee in permission_hours:
                permission_hours[att.employee] += total_permission_hours
            else:
                permission_hours[att.employee] = total_permission_hours
    
    return permission_hours
    

def fetch_attendance_data(filters, employees, date_range):
    employee_ids = [emp.name for emp in employees]
    
    attendance = frappe.db.sql("""
        SELECT employee, attendance_date, status, in_time, out_time, shift, 
               over_time_hours, total_working_hours, leave_type, shift_status, 
               on_duty_application, permission ,leave_application
        FROM `tabAttendance`
        WHERE attendance_date BETWEEN %s AND %s 
        AND employee IN %s AND docstatus != 2
    """, (filters.from_date, filters.to_date, tuple(employee_ids)), as_dict=True)
    
    attendance_map = {(att['employee'], att['attendance_date']): att for att in attendance}
    
    return attendance_map

    
def fetch_holiday_data(employees):
    holiday_data = {}
    for emp in employees:
        holiday_list = frappe.db.get_value('Employee', {'name': emp.name}, 'holiday_list')
        holidays = frappe.db.sql("""
            SELECT h.holiday_date, h.weekly_off, h.holiday_type
            FROM `tabHoliday` h 
            JOIN `tabHoliday List` hl ON hl.name = h.parent 
            WHERE hl.name = %s
        """, holiday_list, as_dict=True)
        holiday_data[emp.name] = {holiday['holiday_date']: holiday for holiday in holidays}
        for holiday in holidays:
            holiday_data[emp.name][holiday['holiday_type']] = holiday	
            holiday_data[emp.name][holiday['weekly_off']] = holiday	
        
    return holiday_data

def process_employee_data(emp, date_range, attendance_data, holiday_data_new, permission_data):
    row1, row2, row3, row4, row5, row6 = initialize_rows(emp)
    total_present = total_half_day = total_absent = total_sick_leave  = total_casual_leave = 0
    total_earned_leave = total_od = total_lwp = total_coff_leave = 0
    total_holiday = weekly_off = on_duty_hours = 0
    permission_hour = permission_data.get(emp.name, 0)
    miss_in =  miss_out =  0
    for date in date_range:
        att = attendance_data.get((emp.name, date.date()))
        holiday = holiday_data_new.get(emp.name, {}).get(date.date())
        if holiday:
            if holiday['weekly_off']:
                weekly_off += 1
            else:
                total_holiday += 1
        if att:
            status = process_attendance_status(att, holiday, row1)
            if att['status'] == 'Present' and not holiday:
                total_present += 1
            if att['on_duty_application']:
                od = frappe.db.get_value("On Duty Application",{'docstatus':('=','1'),"name":att['on_duty_application']},['session'])
                if od == 'First Half' and att['status'] == "Half Day" and not att['leave_type']:
                    total_od += 0.5
                    on_duty_hours += 4
                    if att['total_working_hours'] >= 4:
                        total_present += 0.5
                    else:  
                        total_absent += 0.5   
                elif od == 'First Half' and att['status'] == "Half Day" and att['leave_type']:
                    total_od += 0.5
                    on_duty_hours += 4
                    if att['leave_type']:
                        leave = status_map.get(att['leave_type'], "")
                        if leave == 'CL':
                            total_casual_leave += 0.5
                        if leave == 'EL':
                            total_earned_leave += 0.5
                        if leave == 'LOP':
                            total_lwp += 0.5
                        if leave == 'SL':
                            total_sick_leave += 0.5
                        if leave == 'C-OFF':
                            total_coff_leave += 0.5
                if od == 'Second Half' and att['status'] == "Half Day" and not att['leave_type']:
                    total_od += 0.5
                    on_duty_hours += 4
                    if att['total_working_hours'] >= 4:
                        total_present += 0.5  
                    else:  
                        total_absent += 0.5                    
                elif od == 'Second Half' and att['status'] == "Half Day" and att['leave_type']:
                    total_od += 0.5
                    on_duty_hours += 4
                    if att['leave_type']:
                        leave = status_map.get(att['leave_type'], "")
                        if leave == 'CL':
                            total_casual_leave += 0.5
                        if leave == 'EL':
                            total_earned_leave += 0.5
                        if leave == 'LOP':
                            total_lwp += 0.5
                        if leave == 'SL':
                            total_sick_leave += 0.5
                        if leave == 'C-OFF':
                            total_coff_leave += 0.5
                if od == 'Hourly':
                    total_hourly = frappe.db.get_value("On Duty Application",{'docstatus':('=','1'),"name":att['on_duty_application']},['total_hourly'])
                    # total_half_day += 0.5   
                    if total_hourly == '1 Hour':
                        on_duty_hours += 1
                    elif total_hourly == '2 Hours':
                        on_duty_hours += 2
                    elif total_hourly == '3 Hours':
                        on_duty_hours += 3
                    elif total_hourly == '4 Hours':
                        on_duty_hours += 4
                if od == 'Full Day':
                    total_od += 1
                    on_duty_hours += 8
            if att['status'] == 'Half Day' and not holiday and not att['on_duty_application']:
                if att['leave_type']:
                    if att['total_working_hours'] >= 4:
                        total_present += 0.5
                    else:  
                        total_absent += 0.5 
                    leave = status_map.get(att['leave_type'], "")
                    if leave == 'CL':
                        total_casual_leave += 0.5
                    if leave == 'EL':
                        total_earned_leave += 0.5
                    if leave == 'LOP':
                        total_lwp += 0.5
                    if leave == 'SL':
                        total_sick_leave += 0.5
                    if leave == 'C-OFF':
                        total_coff_leave += 0.5
                else:
                    total_half_day += 0.5
            elif att['status'] == 'Half Day' and holiday and not att['on_duty_application']:
                if att['leave_type']:
                    leave = status_map.get(att['leave_type'], "")
                    if leave == 'CL':
                        total_casual_leave += 0.5
                    if leave == 'EL':
                        total_earned_leave += 0.5
                    if leave == 'LOP':
                        total_lwp += 0.5
                    if leave == 'SL':
                        total_sick_leave += 0.5
                    if leave == 'C-OFF':
                        total_coff_leave += 0.5
            if att['status'] == 'Absent' and not holiday and not att['on_duty_application']:
                total_absent += 1
                
            if att['status'] == 'On Leave' and not holiday and not att['on_duty_application']:
                # Fetch the leave count and leave type from the database
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
                    "from_date": att['attendance_date'],
                    "to_date": att['attendance_date'],
                    "employee": att['employee'],
                    "leave_application": att['leave_application'],
                })
                # frappe.log_error(leave_data, "Leave Data Error")
                # Get the first result (if any)
                if leave_data:
                    leave_count = leave_data[0][0] 
                    leave_type = leave_data[0][1]
                else:
                    leave_count = 0
                    leave_type = None
                if leave_count == 1:
                    leave_type = status_map.get(leave_type, "")
                    leave = status_map.get(att['leave_type'], "")
                    if leave_type:
                        if leave_type == 'CL':
                            total_casual_leave += 0.5
                        if leave_type == 'EL':
                            total_earned_leave += 0.5
                        if leave_type == 'LOP':
                            total_lwp += 0.5
                        if leave_type == 'SL':
                            total_sick_leave += 0.5
                        if leave_type == 'C-OFF':
                            total_coff_leave += 0.5
                    if att['leave_type']:
                        if leave == 'CL':
                            total_casual_leave += 0.5
                        if leave == 'EL':
                            total_earned_leave += 0.5
                        if leave == 'LOP':
                            total_lwp += 0.5
                        if leave == 'SL':
                            total_sick_leave += 0.5
                        if leave == 'C-OFF':
                            total_coff_leave += 0.5
                else:
                    leave = status_map.get(att['leave_type'], "")
                    if leave == 'CL':
                        total_casual_leave += 1
                    if leave == 'EL':
                        total_earned_leave += 1
                    if leave == 'LOP':
                        total_lwp += 1
                    if leave == 'SL':
                        total_sick_leave += 1
                    if leave == 'C-OFF':
                        total_coff_leave += 1
            elif att['status'] == 'On Leave' and holiday and not att['on_duty_application']:
                    # Fetch the leave count and leave type from the database
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
                    "from_date": att['attendance_date'],
                    "to_date": att['attendance_date'],
                    "employee": att['employee'],
                    "leave_application": att['leave_application'],
                })

                # Get the first result (if any)
                if leave_data:
                    leave_count = leave_data[0][0] 
                    leave_type = leave_data[0][1]
                else:
                    leave_count = 0
                    leave_type = None
                if leave_count == 1:
                    leave_type = status_map.get(leave_type, "")
                    leave = status_map.get(att['leave_type'], "")
                    if leave_type:
                        if leave_type == 'CL':
                            total_casual_leave += 0.5
                        if leave_type == 'EL':
                            total_earned_leave += 0.5
                        if leave_type == 'LOP':
                            total_lwp += 0.5
                        if leave_type == 'SL':
                            total_sick_leave += 0.5
                        if leave_type == 'C-OFF':
                            total_coff_leave += 0.5
                    if att['leave_type']:
                        if leave == 'CL':
                            total_casual_leave += 0.5
                        if leave == 'EL':
                            total_earned_leave += 0.5
                        if leave == 'LOP':
                            total_lwp += 0.5
                        if leave == 'SL':
                            total_sick_leave += 0.5
                        if leave == 'C-OFF':
                            total_coff_leave += 0.5
                else:
                    leave = status_map.get(att['leave_type'], "")
                    if leave == 'CL':
                        total_casual_leave += 1
                    if leave == 'EL':
                        total_earned_leave += 1
                    if leave == 'LOP':
                        total_lwp += 1
                    if leave == 'SL':
                        total_sick_leave += 1
                    if leave == 'C-OFF':
                        total_coff_leave += 1
            if att['in_time'] and att['out_time']:
                if att['in_time']:
                    row2.append(att['in_time'].strftime('%H:%M'))
                if att['out_time']:
                    row3.append(att['out_time'].strftime('%H:%M'))
            elif not att['in_time'] and att['out_time']:
                row2.append('M')
                row3.append(att['out_time'].strftime('%H:%M'))
                miss_in += 1
            elif not att['out_time'] and att['in_time']:
                row2.append(att['in_time'].strftime('%H:%M'))
                row3.append('M')
                miss_out += 1
            else:
                row2.append('-')
                row3.append('-')
            if att['status'] == 'Absent' and holiday and not att['in_time'] and not att['out_time']:
                row4.append('-')
            else:
                row4.append(att['shift'] or att['shift_status'])
            row5.append(att['over_time_hours'] or '-')
            row6.append(att['total_working_hours'] or '-')
        else:
            append_holiday_or_default(holiday, row1, row2, row3, row4, row5, row6)

    finalize_row_data(row1, row2, row3, row4, row5, row6, total_present, total_half_day, total_absent,total_casual_leave,
    total_earned_leave,total_lwp, total_sick_leave,total_coff_leave,total_od,on_duty_hours, miss_in, miss_out,permission_hour,total_holiday,weekly_off)
    
    return [row1, row2, row3, row4, row5, row6]

def initialize_rows(emp):
    return (
        [emp.name, emp.employee_name, emp.department, emp.designation, emp.work_station or "-", emp.employee_category or "-", emp.date_of_joining, "Status"],
        ["", "", "", "", "", "", "", "In Time"],
        ["", "", "", "", "", "", "", "Out Time"],
        ["", "", "", "", "", "", "", "Shift"],
        ["", "", "", "", "", "", "", "Overtime"],
        ["", "", "", "", "", "", "", "Total Working Hours"]
    )

def process_attendance_status(att, holiday, row1):
    status = status_map.get(att['status'], "")
    leave = status_map.get(att['leave_type'], "")
    if status == "On Leave" and not att['on_duty_application']:
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
            "from_date": att['attendance_date'],
            "to_date": att['attendance_date'],
            "employee": att['employee'],
            "leave_application": att['leave_application'],
        })

        # Get the first result (if any)
        if leave_data:
            leave_count = leave_data[0][0] 
            leave_type = leave_data[0][1]
            leave_type = status_map.get(leave_type, "")
            if leave_count == 1:
                row1.append(f'{leave_type}-{leave}' or status)
            else:
                row1.append(leave or status)
        else:
            row1.append(leave or status)
    elif att['on_duty_application']:
        od = frappe.db.get_value("On Duty Application",{'docstatus':('=','1'),"name":att['on_duty_application']},['session'])
        if od == 'First Half':
            if att['status'] == "Half Day":
                if att['leave_type']:
                    row1.append(f"OD/{leave}")
                else:
                    if att['total_working_hours'] < 4:
                        row1.append('OD/A')
                    else:
                        row1.append('OD/P')
            if att['status'] == "Absent":
                row1.append('OD/A')
            if att['status'] == "Present":
                row1.append('OD/P')
        elif od == 'Second Half':
            if att['status'] == "Half Day": 
                if att['leave_type']:
                    row1.append(f"{leave}/OD")
                else:
                    if att['total_working_hours'] < 4:
                        row1.append('A/OD')
                    else:
                        row1.append('P/OD')
            if att['status'] == "Absent":
                row1.append('A/OD')
            if att['status'] == "Present":
                row1.append('P/OD')
        elif od == 'Full Day':
            if att['status'] == "Present":
                row1.append('OD')
            else:
                row1.append('OD')
        elif od == 'Hourly':
            total_hourly = frappe.db.get_value("On Duty Application",{'docstatus':('=','1'),"name":att['on_duty_application']},['total_hourly'])
            # if total_hourly == '1 Hour':
            #     total_hourly_value = 1
            total_hourly_value = 0
            if total_hourly == '1 Hour':
                total_hourly_value += 1
            elif total_hourly == '2 Hours':
                total_hourly_value += 2
            elif total_hourly == '3 Hours':
                total_hourly_value += 3
            elif total_hourly == '4 Hours':
                total_hourly_value += 4   
            if att['total_working_hours'] + total_hourly_value < 4:
                row1.append('A')
            elif 4 <= (att['total_working_hours'] + total_hourly_value) < 8:
                row1.append('HD')
            else:
                row1.append('P')
        # else:
        #     row1.append('ON DUTY')
    elif att['status'] == 'Absent' and not holiday and not att['permission'] and not att['on_duty_application']:
        if att['in_time'] and att['out_time']:  
            row1.append(status or '-')
        elif not att['in_time'] and att['out_time']:
            row1.append(status or '-')  
        elif att['in_time'] and not att['out_time']: 
            row1.append(status or '-')
        else:
            row1.append(status or '-')
    elif att['status'] == 'Absent' and holiday and not att['permission'] and not att['on_duty_application']:
        if att['in_time'] and att['out_time']:  
            row1.append(status or '-')
        elif not att['in_time'] and att['out_time']:
            row1.append(status or '-')  
        elif att['in_time'] and not att['out_time']: 
            row1.append(status or '-')
        else:
            append_holiday_or_default_new(holiday, row1) 
    elif att['status'] == "Half Day" and att['leave_type'] and not att['on_duty_application']:
        if att['permission']:
            perm=frappe.db.get_value("Permission Request",{'name':att['permission']},['permission_hour'])
            if perm:
                perm=float(perm)
            else:
                perm=0
            perm_time=att['total_working_hours']+perm
            if perm_time < 4:
                row1.append(f"A-{leave}")
            else:
                row1.append(f"P-{leave}")
        else:
            if att['total_working_hours'] < 4:
                row1.append(f"A-{leave}")
            else:
                row1.append(f"P-{leave}")
    elif att['permission'] and not att['leave_type'] and not att['on_duty_application']:
        row1.append(f"{status}- P")
    else:
        row1.append(status or '-')

    return status

# def update_totals(status, row1, total_present, total_half_day, total_absent, total_sick_leave):
#     if status == 'Present':
#         total_present += 1
#     elif status == 'Half Day':
#         total_half_day += 1
#     elif status == 'Absent':
#         total_absent += 1
#     elif status == 'On Leave':
#         total_sick_leave += 1
#     return total_present,total_half_day,total_absent,total_sick_leave

def append_holiday_or_default(holiday, row1, row2, row3, row4, row5, row6):
    if holiday:
        holiday_type = holiday.get('holiday_type', '-')
        row1.append(holiday['weekly_off'] and 'WW' or holiday_type)
    else:
        row1.append('-')
    row2.append('-')
    row3.append('-')
    row4.append('-')
    row5.append('-')
    row6.append('-')


def finalize_row_data(row1, row2, row3, row4, row5, row6, total_present, total_half_day, total_absent,total_casual_leave,total_earned_leave,total_lwp, total_sick_leave,total_coff_leave,total_od,on_duty_hours, miss_in, miss_out,permission_hour,total_holiday,weekly_off):
    # while len(row1) < len(columns):
    #     row1.append('-') 
    row1.extend([total_present, total_half_day, total_absent,total_casual_leave, total_sick_leave,total_earned_leave,total_lwp,total_coff_leave,total_od,on_duty_hours,permission_hour, miss_in, miss_out,total_holiday,weekly_off])
    row2.extend(['-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-','-'])
    row3.extend(['-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-','-'])
    row4.extend(['-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-','-'])
    row5.extend(['-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-','-'])
    row6.extend(['-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-','-'])

def get_employees(filters):
    conditions = []
    if filters.employee:
        conditions.append(f"employee = '{filters.employee}'")
    if filters.designation:
        conditions.append(f"designation = '{filters.designation}'")
    if filters.department:
        conditions.append(f"department = '{filters.department}'")
    if filters.work_station:
        conditions.append(f"work_station = '{filters.work_station}'")
    if filters.employee_category:
        conditions.append(f"employee_category = '{filters.employee_category}'")
    
    query_conditions = " AND ".join(conditions) if conditions else '1=1'
    
    employees = frappe.db.sql(f"""
        SELECT name, employee_name, department, designation, date_of_joining, holiday_list, employee_category, work_station 
        FROM `tabEmployee` 
        WHERE status = 'Active' AND {query_conditions}
    """, as_dict=True)
    
    left_employees = frappe.db.sql(f"""
        SELECT name, employee_name, department, designation, date_of_joining, holiday_list, employee_category, work_station 
        FROM `tabEmployee` 
        WHERE status = 'Left' AND relieving_date >= '{filters.from_date}' AND {query_conditions}
    """, as_dict=True)
    
    employees.extend(left_employees)
    return employees
def append_holiday_or_default_new(holiday, row1):
    if holiday:
        holiday_type = holiday.get('holiday_type', '-')
        row1.append(holiday['weekly_off'] and 'WW' or holiday_type)
    else:
        row1.append('-')
