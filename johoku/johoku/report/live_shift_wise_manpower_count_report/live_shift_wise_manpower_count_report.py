# # Copyright (c) 2023, TEAMPRO and contributors
# # For license information, please see license.txt
# import frappe
# from frappe import _
# from frappe.utils import flt
# import erpnext
# import time
# import pytz
# from frappe.utils import get_datetime, now
# from frappe.utils import today, get_datetime
# from datetime import timedelta
# import pandas as pd

# def execute(filters=None):
#     columns = get_columns()
#     data = get_data(filters)
#     return columns, data

# def get_columns():
#     columns = []
#     columns += [
#         _('Date') + ":Date/:100",
#         _("Employee ID") + ":Data/:90",
#         _("Employee Name") + ":Data/:150",
#         _("Assigned Shift") + ":Data/:70",
#         # _("Attended Shift") + ":Data/:70",
#         _("Department") + ":Data/:100",
#         _("Designation") + ":Data/:100",
#         _("Category") + ":Data/:90",
#         _("Check In Time") + ":Data/:100",
#         _("Status") + ":Data/:100",
#     ]
	
#     return columns

# # def get_conditions(filters):
# # 	conditions = ""
# # 	if filters.get("attendance_date"):
# # 		conditions += "  attendance_date = %(attendance_date)s"
# # 	if filters.get("shift_type"):
# # 		conditions += " and shift = %(shift_type)s"
# # 	return conditions, filters

# def get_data(filters):
#     data = []
	
#     datetime_today_noon = get_datetime(f"{filters.attendance_date} 12:00:00")
#     current_date = now()

#     query = """
#         SELECT * 
#         FROM `tabEmployee Checkin` 
#         WHERE log_type = 'IN' 
#           AND time BETWEEN %s AND %s 
#           AND shift = %s
#     """
	
#     sa = frappe.db.sql(query, (datetime_today_noon, current_date, filters.shift), as_dict=True)
	
#     # sa = frappe.db.sql("""select * from `tabAttendance` where attendance_date = '%s' and shift='%s'"""%(filters.attendance_date,filters.shift),as_dict=True)
#     if sa:
#         for i in sa:
#             ass = ''
#             at_time =''
#             status = ''
#             shift_type = frappe.db.get_value(
#                 "Shift Assignment", 
#                 {'employee': i.employee, 'start_date': filters.attendance_date, 'docstatus': 1}, 
#                 'shift_type'
#             )
#             if not shift_type:
#                 if i.time:
#                     ass = "NSA"
#                     status='Present'
#                     at_time = i.time
#             elif i.time and i.shift == filters.shift and shift_type:
#                 frappe.errprint(i.name)
#                 frappe.errprint(i.time)
#                 ass = shift_type
#                 status='Present'
#                 at_time = i.time.strftime('%H:%M:%S')
#                 # else:
#                 # 	ass = "NSA"
#                 # 	status='Absent'
#                 # 	at_time = '-'
#             # elif shift_type in ['1','2','3']:
#             # 	if not i.time and shift_type == filters.shift:
#             # 		ass = shift_type
#             # 		status='Absent'
#             # 		at_time = '-'
#             # if i.status=='On Leave':
#             # 	ass = "Leave"
#             # 	status="On Leave"
#             # 	at_time='-'
#             # elif i.in_time is not None and (i.status == 'Absent' or 'Present') and i.shift == filters.shift:
#             # 	frappe.errprint(i.name)
#             # 	frappe.errprint(i.in_time)
#             # 	ass = i.shift
#             # 	status='Present'
#             # 	at_time = i.in_time.strftime('%H:%M:%S')
#             # elif i.assigned_shift in ['1','2','3']:
#             # 	if not i.in_time and i.status == 'Absent' and i.assigned_shift == filters.shift:
#             # 		ass = i.assigned_shift
#             # 		status='Absent'
#             # 		at_time = '-'
#             # elif i.assigned_shift not in ['1','2','3']:
#             # 	if not i.in_time and i.status == 'Absent':
#             # 		ass = "NSA"
#             # 		status='Absent'
#             # 		at_time = '-'
#             designation = frappe.db.get_value(
#                 "Employee", 
#                 {'name': i.employee}, 
#                 'designation'
#             )
#             employee_category = frappe.db.get_value(
#                 "Employee", 
#                 {'name': i.employee}, 
#                 'employee_category'
#             )
#             row=[filters.attendance_date,i.employee,i.employee_name,ass,i.department,designation,employee_category,time,status]
#             data.append(row)
#     return data



# @frappe.whitelist()
# def get_shift(attendance_date):
#     frappe.errprint("Hi")
#     timez = pytz.timezone('Asia/Kolkata')
#     nowtime = datetime.now(timez)
#     curtime = nowtime.strftime('%H:%M')
#     frappe.errprint(curtime)
#     return curtime

# # def get_data_new(filters):
# # 	data = []
# # 	# conditions, filters = get_conditions(filters)
# # 	datetime_today_noon = get_datetime(f"{filters.attendance_date} 12:00:00")
# # 	current_date = frappe.utils.now()
# # 	print(datetime_today_noon)

	 

import frappe
from frappe import _
from frappe.utils import flt, get_datetime, now
import pytz
from datetime import datetime


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	# columns = [
	# 	_('Date') + ":Date/:100",
	# 	_("Employee ID") + ":Data/:90",
	# 	_("Employee Name") + ":Data/:150",
	# 	_("Assigned Shift") + ":Data/:70",
	# 	_("Department") + ":Data/:100",
	# 	_("Designation") + ":Data/:100",
	# 	_("Category") + ":Data/:90",
	# 	_("Check In Time") + ":Data/:100",
	# 	_("Status") + ":Data/:100",
	# ]
	columns = [
		_('Date') + ":Date/:100",
		_("Employee ID") + ":Data/:150",
		_("Employee Name") + ":Data/:200",
		_("Assigned Shift") + ":Data/:100",
		_("Department") + ":Data/:150",
		_("Designation") + ":Data/:150",
		_("Category") + ":Data/:150",
		_("Check In Time") + ":Data/:100",
		_("Status") + ":Data/:100",
	]
	return columns

def get_data(filters):
	data = []
	
	sa = frappe.db.sql("""select distinct employee, employee_name, department,time,shift from `tabEmployee Checkin` where date(time)= '%s' and shift='%s' and log_type = "IN" group by employee order by time"""%(filters.attendance_date,filters.shift),as_dict=True)

	if sa:
		# frappe.log_error(sa)
		for i in sa:
			ass = ''
			at_time = ''
			status = ''
			shift_type = frappe.db.get_value(
				"Shift Assignment", 
				{'employee': i.employee, 'start_date': filters.attendance_date, 'docstatus': 1}, 
				'shift_type'
			)

			# if not shift_type:
			# 	frappe.log_error('Present')
			# 	if i.time:
			# 		frappe.log_error(i.time)
			# 		ass = "NSA"  # No shift assignment found
			# 		status = 'Present'
			# 		at_time = i.time
			if i.time and i.shift == filters.shift:
				frappe.log_error(shift_type)
				if shift_type:
					ass = shift_type
				else:
					ass ="NSA"
				status = 'Present'
				at_time = i.time.strftime('%H:%M:%S')
			elif shift_type in ['1','2','3']:
				if not i.shift and i.time:
					absent += 1
					frappe.errprint(i.employee)
					ass = "NSA"
					status = 'Absent'
					at_time = '-'

			designation = frappe.db.get_value(
				"Employee", 
				{'name': i.employee}, 
				'designation'
			)
			employee_category = frappe.db.get_value(
				"Employee", 
				{'name': i.employee}, 
				'employee_category'
			)
			
			# Prepare row for report
			row = [filters.attendance_date, i.employee, i.employee_name, ass, i.department, designation, employee_category, at_time, status]
			data.append(row)

	return data

@frappe.whitelist()
def get_shift(attendance_date):
	timez = pytz.timezone('Asia/Kolkata')
	nowtime = datetime.now(timez)
	curtime = nowtime.strftime('%H:%M')
	return curtime

	










