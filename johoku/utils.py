from email import message
import json
from operator import le
from re import M
import requests
import frappe
from frappe.utils import today, add_days, date_diff,cint
from time import strptime
from datetime import datetime
import pandas as pd
from frappe import _
import frappe
from frappe.utils import getdate, add_months

@frappe.whitelist()
#returns current date
def get_server_date():
    return today()

def application_allowed_from(date):
    return ''

@frappe.whitelist()
#return the basic,hra and pf by passing employee's grade
def salary_amount_update(grade):
    datalist = []
    data = {}
    emp_grade = frappe.db.get_value('Employee Grade',{'name':grade},['basic','hra','pf'])
    data.update({
        'basic':emp_grade[0],
        'hra':emp_grade[1],
        'pf':emp_grade[2],
    })
    datalist.append(data.copy())
    return datalist

@frappe.whitelist()
#validates the employee's gender
def leave_type_validation(emp,leave_type):
    data = []
    if leave_type == 'Maternity Leave':
        emp = frappe.db.get_value('Employee',{'name':emp,'status':'Active'},['gender'])
        if emp == 'Male':
            data.append("Maternity Leave")
    return data 


@frappe.whitelist()
#use to get the leave balance format in Pay Slip print format
def payslip_leave_data(employee, start_date, end_date, epf_ac_no, uan_no, department):
    
    data = ""
    data +="<tr>"
    data += "<td colspan ='12'  width='5' style ='text-align:left;font-size:12px'><b>Department</b></td>"
    data += f"<td colspan ='12'  width='5' style ='text-align:center;font-size:12px'><b>{department or '-'}</b></td>"
    data +=  "<td colspan ='12'  width='5' style ='text-align:left;font-size:12px'><b>Opening</b></td>"
    data += f"<td colspan ='3'  width='5' style ='text-align:center;font-size:12px'><b>{get_opening_balance(employee, 'Casual Leave', start_date,end_date) or 0}</b></td>"
    data +=  f"<td colspan ='3'  width='5' style ='text-align:center;font-size:12px'><b>{get_opening_balance(employee, 'Sick Leave', start_date,end_date) or 0}</b></td>"
    data += f"<td colspan ='2'  width='5' style ='text-align:center;font-size:12px'><b>{get_opening_balance(employee, 'Earned Leave', start_date,end_date) or 0}</b></td>"
    data += f"<td colspan ='2'  width='5' style ='text-align:center;font-size:12px'><b>{get_opening_balance(employee, 'Compensatory Off', start_date,end_date) or 0}</b></td>"
    data += f"<td colspan ='2'  width='5' style ='text-align:center;font-size:12px'><b>{get_opening_balance(employee, 'Leave Without Pay', start_date,end_date) or 0}</b></td>"
    data += "</tr>"
    availed_cl = frappe.db.sql("""SELECT SUM(total_leave_days) FROM `tabLeave Application` WHERE docstatus = 1 and status = 'Approved' and employee = %s AND leave_type = 'Casual Leave' AND from_date BETWEEN %s AND %s""", (employee, start_date, end_date))[0][0] or 0
    availed_sl = frappe.db.sql("""SELECT SUM(total_leave_days) FROM `tabLeave Application` WHERE docstatus = 1 and status = 'Approved' and employee = %s AND leave_type = 'Sick Leave' AND from_date BETWEEN %s AND %s""", (employee, start_date, end_date))[0][0] or 0
    availed_el = frappe.db.sql("""SELECT SUM(total_leave_days) FROM `tabLeave Application` WHERE docstatus = 1 and status = 'Approved' and employee = %s AND leave_type = 'Earned Leave' AND from_date BETWEEN %s AND %s""", (employee, start_date, end_date))[0][0] or 0
    availed_co = frappe.db.sql("""SELECT SUM(total_leave_days) FROM `tabLeave Application` WHERE docstatus = 1 and status = 'Approved' and employee = %s AND leave_type = 'Compensatory Off' AND from_date BETWEEN %s AND %s""", (employee, start_date, end_date))[0][0] or 0
    availed_lop = frappe.db.sql("""SELECT SUM(total_leave_days) FROM `tabLeave Application` WHERE docstatus = 1 and status = 'Approved' and employee = %s AND leave_type = 'Leave Without Pay' AND from_date BETWEEN %s AND %s""", (employee, start_date, end_date))[0][0] or 0
    data += "<tr>"
    data += "<td colspan ='12'  width='5' style ='text-align:left;font-size:12px'><b>EPF Account Number</b></td>"
    data += f"<td colspan ='12'  width='5' style ='text-align:center;font-size:12px'><b>{epf_ac_no or '-'}</b></td>"
    data += "<td colspan ='12'  width='5' style ='text-align:left;font-size:12px'><b>Availed</b></td>"
    data += f"<td colspan ='3'  width='5' style ='text-align:center;font-size:12px'><b>{get_availed_leaves(employee, 'Casual Leave', start_date, end_date)}</b></td>"
    data += f"<td colspan ='3'  width='5' style ='text-align:center;font-size:12px'><b>{get_availed_leaves(employee, 'Sick Leave', start_date, end_date)}</b></td>"
    data += f"<td colspan ='2'  width='5' style ='text-align:center;font-size:12px'><b>{get_availed_leaves(employee, 'Earned Leave', start_date, end_date)}</b></td>"
    data += f"<td colspan ='2'  width='5' style ='text-align:center;font-size:12px'><b>{get_availed_leaves(employee, 'Compensatory Off', start_date, end_date)}</b></td>"
    data += f"<td colspan ='2'  width='5' style ='text-align:center;font-size:12px'><b>{get_availed_leaves(employee, 'Leave Without Pay', start_date, end_date)}</b></td>"
    data += "</tr>"
    data += "<tr>"
    data += "<td colspan ='12'  width='5' style ='text-align:left;font-size:12px'><b>UAN Number</b></td>"
    data += f"<td colspan ='12'  width='5' style ='text-align:center;font-size:12px'><b>{uan_no or '-'}</b></td>"
    data += "<td colspan ='12'  width='5' style ='text-align:left;font-size:12px'><b>Balance</b></td>"
    data += f"<td colspan ='3'  width='5' style ='text-align:center;font-size:12px'><b>{balance_leave(employee, 'Casual Leave', start_date, end_date) or 0}</b></td>"
    data += f"<td colspan ='3'  width='5' style ='text-align:center;font-size:12px'><b>{balance_leave(employee, 'Sick Leave', start_date, end_date) or 0}</b></td>"
    data += f"<td colspan ='2'  width='5' style ='text-align:center;font-size:12px'><b>{balance_leave(employee, 'Earned Leave', start_date, end_date) or 0}</b></td>"
    data += f"<td colspan ='2'  width='5' style ='text-align:center;font-size:12px'><b>{balance_leave(employee, 'Compensatory Off', start_date, end_date) or 0}</b></td>"
    data += f"<td colspan ='2'  width='5' style ='text-align:center;font-size:12px'><b>{balance_leave(employee, 'Leave Without Pay', start_date, end_date) or 0}</b></td>"
    data += "</tr>"
    return data


@frappe.whitelist()
def payslip_leave_data_for_gt_and_tt(employee, start_date, end_date, epf_ac_no, uan_no):
    grade =frappe.db.get_value('Employee',{'name':employee},'grade')
    data = ""
    data +="<tr>"
    data += "<td colspan ='12'  width='5' style ='text-align:left;font-size:12px'><b>Grade</b></td>"
    data += f"<td colspan ='12'  width='5' style ='text-align:center;font-size:12px'><b>{grade or '-'}</b></td>"
    data +=  "<td colspan ='12'  width='5' style ='text-align:left;font-size:12px'><b>Opening</b></td>"
    data += f"<td colspan ='3'  width='5' style ='text-align:center;font-size:12px'><b>{get_opening_balance(employee, 'Casual Leave', start_date,end_date) or 0}</b></td>"
    data +=  f"<td colspan ='3'  width='5' style ='text-align:center;font-size:12px'><b>{get_opening_balance(employee, 'Sick Leave', start_date,end_date) or 0}</b></td>"
    data += f"<td colspan ='2'  width='5' style ='text-align:center;font-size:12px'><b>{get_opening_balance(employee, 'Earned Leave', start_date,end_date) or 0}</b></td>"
    data += f"<td colspan ='2'  width='5' style ='text-align:center;font-size:12px'><b>{get_opening_balance(employee, 'Compensatory Off', start_date,end_date) or 0}</b></td>"
    data += f"<td colspan ='2'  width='5' style ='text-align:center;font-size:12px'><b>{get_opening_balance(employee, 'Leave Without Pay', start_date,end_date) or 0}</b></td>"
    data += "</tr>"
    availed_cl = frappe.db.sql("""SELECT SUM(total_leave_days) FROM `tabLeave Application` WHERE docstatus = 1 and status = 'Approved' and employee = %s AND leave_type = 'Casual Leave' AND from_date BETWEEN %s AND %s""", (employee, start_date, end_date))[0][0] or 0
    availed_sl = frappe.db.sql("""SELECT SUM(total_leave_days) FROM `tabLeave Application` WHERE docstatus = 1 and status = 'Approved' and employee = %s AND leave_type = 'Sick Leave' AND from_date BETWEEN %s AND %s""", (employee, start_date, end_date))[0][0] or 0
    availed_el = frappe.db.sql("""SELECT SUM(total_leave_days) FROM `tabLeave Application` WHERE docstatus = 1 and status = 'Approved' and employee = %s AND leave_type = 'Earned Leave' AND from_date BETWEEN %s AND %s""", (employee, start_date, end_date))[0][0] or 0
    availed_co = frappe.db.sql("""SELECT SUM(total_leave_days) FROM `tabLeave Application` WHERE docstatus = 1 and status = 'Approved' and employee = %s AND leave_type = 'Compensatory Off' AND from_date BETWEEN %s AND %s""", (employee, start_date, end_date))[0][0] or 0
    availed_lop = frappe.db.sql("""SELECT SUM(total_leave_days) FROM `tabLeave Application` WHERE docstatus = 1 and status = 'Approved' and employee = %s AND leave_type = 'Leave Without Pay' AND from_date BETWEEN %s AND %s""", (employee, start_date, end_date))[0][0] or 0
    data += "<tr>"
    data += "<td colspan ='12'  width='5' style ='text-align:left;font-size:12px'><b>EPF A/c No</b></td>"
    data += f"<td colspan ='12'  width='5' style ='text-align:center;font-size:12px'><b>{epf_ac_no or '-'}</b></td>"
    data += "<td colspan ='12'  width='5' style ='text-align:left;font-size:12px'><b>Availed</b></td>"
    data += f"<td colspan ='3'  width='5' style ='text-align:center;font-size:12px'><b>{get_availed_leaves(employee, 'Casual Leave', start_date, end_date)}</b></td>"
    data += f"<td colspan ='3'  width='5' style ='text-align:center;font-size:12px'><b>{get_availed_leaves(employee, 'Sick Leave', start_date, end_date)}</b></td>"
    data += f"<td colspan ='2'  width='5' style ='text-align:center;font-size:12px'><b>{get_availed_leaves(employee, 'Earned Leave', start_date, end_date)}</b></td>"
    data += f"<td colspan ='2'  width='5' style ='text-align:center;font-size:12px'><b>{get_availed_leaves(employee, 'Compensatory Off', start_date, end_date)}</b></td>"
    data += f"<td colspan ='2'  width='5' style ='text-align:center;font-size:12px'><b>{get_availed_leaves(employee, 'Leave Without Pay', start_date, end_date)}</b></td>"
    data += "</tr>"
    data += "<tr>"
    data += "<td colspan ='12'  width='5' style ='text-align:left;font-size:12px'><b>UAN No.</b></td>"
    data += f"<td colspan ='12'  width='5' style ='text-align:center;font-size:12px'><b>{uan_no or '-'}</b></td>"
    data += "<td colspan ='12'  width='5' style ='text-align:left;font-size:12px'><b>Balance</b></td>"
    data += f"<td colspan ='3'  width='5' style ='text-align:center;font-size:12px'><b>{balance_leave(employee, 'Casual Leave', start_date, end_date) or 0}</b></td>"
    data += f"<td colspan ='3'  width='5' style ='text-align:center;font-size:12px'><b>{balance_leave(employee, 'Sick Leave', start_date, end_date) or 0}</b></td>"
    data += f"<td colspan ='2'  width='5' style ='text-align:center;font-size:12px'><b>{balance_leave(employee, 'Earned Leave', start_date, end_date) or 0}</b></td>"
    data += f"<td colspan ='2'  width='5' style ='text-align:center;font-size:12px'><b>{balance_leave(employee, 'Compensatory Off', start_date, end_date) or 0}</b></td>"
    data += f"<td colspan ='2'  width='5' style ='text-align:center;font-size:12px'><b>{balance_leave(employee, 'Leave Without Pay', start_date, end_date) or 0}</b></td>"
    data += "</tr>"
    return data

@frappe.whitelist()
#return the opening leave balance
def get_opening_balance(employee, leave_type, from_date,to_date):
    from_date = getdate(from_date)
    to_date = getdate(to_date)
    year = to_date.year
    previous_year = year - 1
    month = to_date.month
    
    allocation_start_date = getdate(f"{year}-01-01")
    allocation_end_date = getdate(f"{year}-12-31")
    previous_day = add_days(from_date, -1)
    
    total_leaves_allocated = frappe.db.sql("""
        select sum(total_leaves_allocated) as total_allocated_leaves
        from `tabLeave Allocation`
        where docstatus = 1 and employee = %(employee)s and leave_type = %(leave_type)s
            and (from_date between %(from_date)s and %(to_date)s
                or to_date between %(from_date)s and %(to_date)s
                or (from_date < %(from_date)s and to_date > %(to_date)s))
        """, {
            "from_date": allocation_start_date,
            "to_date": allocation_end_date,
            "employee":employee,
            "leave_type":leave_type
        },
    as_dict = True)
    if total_leaves_allocated and total_leaves_allocated[0].get('total_allocated_leaves') is not None:
        allocated_leaves = total_leaves_allocated[0].get('total_allocated_leaves') 
    else:
        allocated_leaves = 0

    previously_used_leaves = frappe.db.sql("""
        select SUM(total_leave_days) as total_leave_days
        from `tabLeave Application`
        where docstatus = 1 and employee = %(employee)s and leave_type = %(leave_type)s and status = 'Approved'
            and (from_date between %(from_date)s and %(to_date)s
                or to_date between %(from_date)s and %(to_date)s
                or (from_date < %(from_date)s and to_date > %(to_date)s))
        """, {
            "from_date": allocation_start_date,
            "to_date": previous_day,
            "employee":employee,
            "leave_type":leave_type
        },
    as_dict = True)
    if previously_used_leaves and previously_used_leaves[0].get('total_leave_days') is not None:
        used_leaves = previously_used_leaves[0].get('total_leave_days') 
    else:
        used_leaves = 0
    if month == 1 :
        opening_balance = allocated_leaves
    else:
        opening_balance = allocated_leaves - used_leaves
    return opening_balance

#returns the availed leave
@frappe.whitelist()
def get_availed_leaves(employee, leave_type, from_date, to_date):
    availed = frappe.db.sql("""
        SELECT SUM(total_leave_days) 
        FROM `tabLeave Application` 
        WHERE employee = %s 
        AND docstatus = 1 
        AND leave_type = %s 
        AND status = 'Approved'
        AND from_date >= %s 
        AND to_date <= %s
    """, (employee, leave_type, from_date, to_date))

    return availed[0][0] if availed and availed[0][0] is not None else 0

#returns the balance leave
@frappe.whitelist()
def balance_leave(employee, leave_type, from_date, to_date):
    opening_balance = get_opening_balance(employee, leave_type, from_date, to_date) or 0
    availed_leaves = get_availed_leaves(employee, leave_type, from_date, to_date) or 0
    return opening_balance - availed_leaves
