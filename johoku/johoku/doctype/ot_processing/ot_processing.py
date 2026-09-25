# Copyright (c) 2024, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import (getdate, cint, add_months, date_diff, add_days)
from johoku.custom import check_holiday_hh
class OTProcessing(Document):
	pass

# @frappe.whitelist()
# def create_ot(from_date,to_date):
# 	to_date=add_days(to_date,1)
# 	emp=frappe.db.get_all("Employee",{'grade':['!=','']},['*'])
# 	total_working_days=date_diff(to_date,from_date)
# 	if total_working_days < 30:
# 		frappe.throw("Total date difference should be minimum 30 days")
# 	for e in emp:
# 		att=frappe.db.get_all('Attendance',{"employee":e.name,"attendance_date":('between',(from_date,to_date)),'docstatus':['!=',2]},['*'])
# 		for a in att:
# 			hh=check_holiday_hh(a.attendance_date,a.employee)
# 			if e.grade in ['MG-3','MG-4','MG-5','MG-6','MG-7','MG-8','MG-9','MG-10','MG-11']:
# 				if hh=='FH' or hh=='NH' or hh=='WW':
# 					if a.total_working_hours>=4 and (a.status=='Present' or a.status=='Half Day'):
# 						if not frappe.db.exists('COFF and OT Request',{'employee':a.employee,'ot_date':a.attendance_date,'docstatus':['!=',2]}):
# 							coff=frappe.new_doc('COFF and OT Request')
# 							coff.employee=a.employee
# 							coff.request_type='COFF'
# 							coff.ot_date=a.attendance_date
# 							coff.working_hours=a.total_working_hours
# 							coff.save(ignore_permissions=True)
# 							frappe.db.commit()
# 			else:
# 				otamt=0
# 				fixed=e.fixed_earning or 0
# 				hh=check_holiday_hh(a.attendance_date,a.employee)
# 				if hh=='FH' or hh=='NH' or hh=='WW':
# 					count=0
# 					if hh=='NH':
# 						count=3
# 					elif hh=='FH':
# 						count=2
# 					else:
# 						count=2
					
# 				else:
# 					if a.over_time_hours and int(a.over_time_hours)>=2:
# 						count=2
# 					else:
# 						count=0
# 				if a.over_time_hours and int(a.over_time_hours)>=2 and count > 0:
# 					if fixed > 0:
# 						otamt+=((((e.fixed_earning/total_working_days)/8)*count)*int(a.over_time_hours))
# 					else:
# 						otamt+=0
# 				if otamt > 0:
# 					if (hh and hh in ['WW','NH','FH']) or not hh:
# 						if not frappe.db.exists('COFF and OT Request',{'employee':a.employee,'ot_date':a.attendance_date,'docstatus':['!=',2]}):
# 							coff=frappe.new_doc('COFF and OT Request')
# 							coff.employee=a.employee
# 							coff.request_type='OT'
# 							coff.ot_date=a.attendance_date
# 							coff.working_hours=a.over_time_hours
# 							coff.amount=otamt
# 							coff.save(ignore_permissions=True)
# 							frappe.db.commit()
# 						else:
# 							coff=frappe.get_doc('COFF and OT Request',{'employee':a.employee,'ot_date':a.attendance_date,'docstatus':0})
# 							coff.employee=a.employee
# 							coff.request_type='OT'
# 							coff.ot_date=a.attendance_date
# 							coff.working_hours=a.over_time_hours
# 							coff.amount=otamt
# 							coff.save(ignore_permissions=True)
# 							frappe.db.commit()

