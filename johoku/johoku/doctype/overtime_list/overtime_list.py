import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate, formatdate,add_days
from frappe import _
from johoku.mark_attendance import update_overtime_list_with_department

class OvertimeList(Document):

    def validate(self):
        formatted_date = formatdate(self.ot_from_date, "dd-mm-yyyy")
        employee_details = frappe.db.get_value("Employee", self.employee, ["date_of_joining", "relieving_date", "employment_type"], as_dict=True)
        date_of_joining = employee_details.date_of_joining
        relieving_date = employee_details.relieving_date
        if frappe.db.exists('Overtime List',{'employee':self.employee,'ot_from_date':self.ot_from_date,'docstatus':['!=',2],'name':['!=',self.name]}):
            existing_doc = frappe.db.get_value('Overtime List',{'employee':self.employee,'ot_from_date':self.ot_from_date,'docstatus':['!=',2],'name':['!=',self.name]},['name'])
            msgcontent = """ <b><a href="/app/Form/Overtime List/{0}">{0}</a></b>""".format(existing_doc)
            msg = _("Overtime List {0} for the employee {1} is already marked for the date {2}.").format(msgcontent, self.employee, formatted_date)
            frappe.throw(msg)
        if date_of_joining and getdate(self.ot_from_date) < getdate(date_of_joining):
            frappe.throw(_("OT date can not be less than employee's joining date"))
        if relieving_date and getdate(self.ot_from_date) > getdate(relieving_date):
            frappe.throw(_("OT date can not be greater than employee's relieving date"))
        if self.ot_from_attendance and self.permitted_overtime_hours and self.permitted_overtime_hours > self.ot_from_attendance:
            frappe.throw('OT Hours cannot exceed Actual OT Hours')
        if self.permitted_overtime_hours and self.ot_from_plan and self.ot_from_plan < self.permitted_overtime_hours:
            frappe.throw('OT Hours cannot exceed Planned OT Hours')
        if self.ot_from_attendance and frappe.db.exists('Employee Benefits Regularization',{'employee':self.employee,'date':self.ot_from_date,'working_hours':self.ot_from_attendance,'docstatus':['!=',2]}):
            frappe.throw(f"Employee Benefits Regularization already exists for Employee {self.employee} on {formatted_date}.")
        if self.permitted_overtime_hours and frappe.db.exists('Employee Benefits Regularization',{'employee':self.employee,'date':self.ot_from_date,'working_hours':self.permitted_overtime_hours,'docstatus':['!=',2]}):
            frappe.throw(f"Employee Benefits Regularization already exists for Employee {self.employee} on {formatted_date}.")

    def on_submit(self):
        if frappe.db.exists('Attendance',{'employee': self.employee,'attendance_date': self.ot_from_date,'docstatus': ['!=', 2]}):
            att_doc = frappe.get_doc('Attendance',{'employee': self.employee,'attendance_date': self.ot_from_date,'docstatus': ['!=', 2]})
            if att_doc:
                att_doc.planned_ot_hours= self.ot_from_plan
                att_doc.ot_plan_document= self.overtime_plan_document
                att_doc.approved_ot_hours= self.permitted_overtime_hours
                att_doc.save(ignore_permissions=True)
                frappe.db.commit()
        self.reload()
        update_overtime_list_with_department(self.ot_from_date, add_days(self.ot_from_date,1),self.department)
    
    
    
    def on_cancel(self):
        self.attendance =None
        if frappe.db.exists('Attendance',{'employee': self.employee,'attendance_date': self.ot_from_date,'docstatus': ['!=', 2]}):
            att_doc = frappe.get_doc('Attendance',{'employee': self.employee,'attendance_date': self.ot_from_date,'docstatus': ['!=', 2]})
            if att_doc:
                att_doc.planned_ot_hours= 0
                att_doc.ot_plan_document= ''
                att_doc.updated_ot_hours= 0
                att_doc.save(ignore_permissions=True)
                frappe.db.commit()
    def on_update(self):
        if frappe.db.exists('Attendance',{'employee': self.employee,'attendance_date': self.ot_from_date,'docstatus': ['!=', 2]}):
            att_doc = frappe.get_doc('Attendance',{'employee': self.employee,'attendance_date': self.ot_from_date,'docstatus': ['!=', 2]})
            if att_doc:
                att_doc.planned_ot_hours= self.ot_from_plan
                att_doc.ot_plan_document= self.overtime_plan_document
                att_doc.approved_ot_hours= self.permitted_overtime_hours
                att_doc.save(ignore_permissions=True)
                frappe.db.commit()
