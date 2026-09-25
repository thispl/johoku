# Copyright (c) 2023, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt
import erpnext
import time
import pytz
from datetime import datetime
from datetime import timedelta
import pandas as pd
from frappe.model.document import Document

class LiveShiftwiseDashboard(Document):
    pass
@frappe.whitelist()
def get_shift():
    timez = pytz.timezone('Asia/Kolkata')
    nowtime = datetime.now(timez)
    curtime = nowtime.strftime('%H:%M')
    frappe.errprint(curtime)
    return curtime


@frappe.whitelist()
def live_data(attendance_date,shift):
    # frappe.errprint(shift)
    date_format = datetime.strptime(attendance_date, "%Y-%m-%d").strftime('%d-%m-%Y')
    data = ''
    data += '<h4><center><b>Total Employee Assigned for Shift %s on %s</b></center></h4>'%(shift,date_format)
    data += '<table class="table table-bordered">'
    data += '<tr>'
    data += '<td colspan=1 style="width:35%;padding:1px;border:1px solid black;font-size:14px;font-size:12px;background-color:#FFE5B4;color:black;"><center><b>Employees Present</b></center></td>'
    data += '<td colspan=1 style="width:32%;padding:1px;border:1px solid black;font-size:14px;font-size:12px;background-color:#FFE5B4;color:black;"><center><b>Employees Absent</b></center></td>'
    data += '<td colspan=1 style="width:32%;padding:1px;border:1px solid black;font-size:14px;font-size:12px;background-color:#FFE5B4;color:black;"><center><b>Employees On Leave</b></center></td>'
    # sa = frappe.db.sql("""select * from `tabAttendance` where attendance_date = '%s' and shift='%s'"""%(attendance_date,shift),as_dict=True)
    no_of_employee =0
    # query = """
    #     SELECT distinct employee, COUNT(*) as count
    #     FROM `tabEmployee Checkin`
    #     WHERE DATE(time) = %s AND log_type = "IN" AND shift = %s
    #     GROUP BY employee
    #     ORDER BY time
    # """
    # result = frappe.db.sql(query, (attendance_date,shift), as_dict=True)
    query = """
        SELECT DISTINCT employee, COUNT(*) as count
        FROM `tabEmployee Checkin`
        WHERE DATE(time) = %s 
        AND log_type = 'IN' 
        AND shift = %s 
        GROUP BY employee
        ORDER BY time
    """
    result = frappe.db.sql(query, (attendance_date, shift), as_dict=True)
    frappe.errprint(len(result))
    sa = frappe.db.sql("""select distinct employee,time,shift from `tabEmployee Checkin` where date(time)= '%s' and log_type = "IN" group by employee order by time"""%(attendance_date),as_dict=True)
    
    if sa:
        present = 0
        absent = 0
        leave = 0
        for i in sa:
            time=i.in_time
            shift_type = frappe.db.get_value(
                "Shift Assignment", 
                {'employee': i.employee, 'start_date': attendance_date, 'docstatus': 1}, 
                'shift_type'
            )
            if i.time and i.shift == shift:
                present += 1
            elif shift_type in ['1','2','3']:
                # if not i.time and shift_type == shift:
                # 	absent += 1
                # 	frappe.errprint(i.employee)
                if not i.shift and i.time:
                    absent += 1
                    frappe.errprint(i.employee)
            # elif shift_type not in ['1','2','3']:
            # 	if not i.time:
            # 		frappe.errprint(i.employee)
            # 		absent += 1
        # frappe.errprint(present)
        # frappe.errprint(absent)
        # frappe.errprint(leave)
        p = present
        a = absent
        o = leave 
        # frappe.errprint(p)
        # frappe.errprint(a)
        # frappe.errprint(o)
        p = len(result)
        data += '<tr><td style="text-align:center;border: 1px solid black" colspan=1>%s</td>'%(p or 0)
        data += '<td style="text-align:center;border: 1px solid black" colspan=1>%s</td>' %(a or 0)
        data += '<td style="text-align:center;border: 1px solid black" colspan=1>%s</td>' %(o or 0)
    else:
        data += '<tr><td style="text-align:center;border: 1px solid black" colspan=1>%s</td>' %(0)
        data += '<td style="text-align:center;border: 1px solid black" colspan=1>%s</td>' %(0)
        data += '<td style="text-align:center;border: 1px solid black" colspan=1>%s</td>' %(0)
    
    data += '</tr>'
    data += '</table>'
    return data



    # if sa:
    # 	present = 0
    # 	absent = 0
    # 	leave = 0
    # 	for i in sa:
    # 		time=i.in_time
    # 		if i.status=='On Leave':
    # 			leave += 1
    # 		elif time and i.status == 'Absent' or 'Present' and i.shift == shift:
    # 			present += 1
    # 		elif i.assigned_shift in ['1','2','3']:
    # 			if not time and i.status == 'Absent' and i.assigned_shift == shift:
    # 				absent += 1
    # 		elif i.assigned_shift not in ['1','2','3']:
    # 			if not time and i.status == 'Absent':
    # 				absent += 1
    # 	p = present
    # 	a = absent
    # 	o = leave 
    # 	data += '<tr><td style="text-align:center;border: 1px solid black" colspan=1>%s</td>'%(p or 0)
    # 	data += '<td style="text-align:center;border: 1px solid black" colspan=1>%s</td>' %(a or 0)
    # 	data += '<td style="text-align:center;border: 1px solid black" colspan=1>%s</td>' %(o or 0)
    # else:
    # 	data += '<tr><td style="text-align:center;border: 1px solid black" colspan=1>%s</td>' %(0)
    # 	data += '<td style="text-align:center;border: 1px solid black" colspan=1>%s</td>' %(0)
    # 	data += '<td style="text-align:center;border: 1px solid black" colspan=1>%s</td>' %(0)
    # data += '</tr>'
    # data += '</table>'
    # return data
