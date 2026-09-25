# Copyright (c) 2024, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import today,flt,add_days,date_diff,getdate,cint,formatdate, getdate, get_link_to_form
from frappe.model.document import Document
from johoku.custom import check_holiday_hh

class COFFandOTRequest(Document):
    pass
	# def validate(self):
		# att=frappe.db.get_all('Attendance',{"employee":self.employee,"attendance_date":self.ot_date,'docstatus':['!=',2]},['employee','attendance_date','over_time_hours',])
		# grade=frappe.db.get_value("Employee",{'name':self.employee},['grade'])
		# fixed_earning=frappe.db.get_value("Employee",{'name':self.employee},['fixed_earning']) or 0
		# if grade and grade not in ['MG-3','MG-4','MG-5','MG-6','MG-7','MG-8','MG-9','MG-10','MG-11']:
		# 	otamt=0
		# 	fixed=fixed_earning or 0
		# 	hh=check_holiday_hh(self.ot_date,self.employee)
		# 	if (hh and hh in ['WW','NH','FH']) or not hh:
		# 		if not frappe.db.exists('COFF and OT Request',{'employee':att.employee,'ot_date':att.attendance_date,'docstatus':['!=',2]}):
		# 			self.working_hours=att.over_time_hours
		# 			self.amount=0
		# 			self.save(ignore_permissions=True)
		# 			frappe.db.commit()
		# 		else:
		# 			frappe.throw("Dublicate Entry")
# 	def on_submit(self):
# 		# if self.workflow_state=='Approved':
# 		if self.request_type=='COFF':
# 			sdate=today()
# 			edate=add_days(sdate,30)
# 			leaves=0
# 			if self.working_hours and self.working_hours >= 4:
# 				if self.working_hours>=4 and self.working_hours<8:
# 					leaves=0.5
# 				elif self.working_hours>=8 and self.working_hours<12:
# 					leaves=1
# 				elif self.working_hours>=12 and self.working_hours<16:
# 					leaves=1.5
# 				elif self.working_hours>=16 and self.working_hours<20:
# 					leaves=2
# 				elif self.working_hours>=20 and self.working_hours<24:
# 					leaves=2.5
# 				else:
# 					leaves=3
# 			if not frappe.db.exists("Leave Allocation",{"employee":self.employee,'leave_type':"Compensatory Off",'from_date':sdate,'to_date':edate,'docstatus':['!=',2]}):
# 				coff=frappe.new_doc("Leave Allocation")
# 				coff.employee=self.employee
# 				coff.leave_type='Compensatory Off'
# 				coff.from_date=sdate
# 				coff.to_date=edate
# 				coff.new_leaves_allocated=leaves
# 				coff.save(ignore_permissions=True)
# 				frappe.db.commit()
# 				coff.submit()
# 			frappe.db.set_value("COFF and OT Request",self.name,'approved_date',sdate)
# 	def on_cancel(self):
# 		# if self.workflow_state=='Approved':
# 		if self.request_type=='COFF':
# 			sdate=today()
# 			edate=add_days(sdate,30)
# 			if frappe.db.exists("Leave Allocation",{"employee":self.employee,'leave_type':"Compensatory Off",'from_date':sdate,'to_date':edate,'docstatus':1}):
# 				coff=frappe.get_doc("Leave Allocation",{"employee":self.employee,'leave_type':"Compensatory Off",'from_date':sdate,'to_date':edate,'docstatus':1})
# 				coff.cancel()
# 				frappe.db.commit()

# @frappe.whitelist()
# def calculate_ot_hours(employee,ot_date):
# 	working_hours = 0
# 	att=frappe.db.get_all('Attendance',{"employee":employee,"attendance_date":ot_date,'docstatus':['!=',2]},['employee','attendance_date','over_time_hours'])
# 	grade=frappe.db.get_value("Employee",{'name':employee},['grade'])
# 	fixed_earning=frappe.db.get_value("Employee",{'name':employee},['fixed_earning']) or 0
# 	# if grade and grade not in ['MG-3','MG-4','MG-5','MG-6','MG-7','MG-8','MG-9','MG-10','MG-11']:
# 	otamt=0
# 	fixed=fixed_earning or 0
# 	frappe.errprint(att)
# 	hh=check_holiday_hh(ot_date,employee)
# 	if (hh and hh in ['WW','NH','FH']) or not hh:
# 		if not frappe.db.exists('COFF and OT Request',{'employee':employee,'ot_date':ot_date,'docstatus':['!=',2]}):
# 			working_hours = att[0].get('over_time_hours')
# 			frappe.errprint(f"att.over_time_hours {att[0].get('over_time_hours')}")
# 		else:
# 			frappe.throw("Dublicate Entry")
# 	return working_hours