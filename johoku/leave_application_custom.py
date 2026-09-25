import frappe
import datetime 
import dateutil.relativedelta
from datetime import datetime, timedelta
from datetime import date
from frappe.utils.data import add_days, add_years, today,getdate
from frappe.utils.file_manager import get_file
from frappe.utils.csvutils import read_csv_content
from frappe.model.mapper import get_mapped_doc
from frappe.utils import date_diff, add_months, today,nowtime,nowdate,format_date,month_diff
from frappe import throw,_
from hrms.hr.doctype.leave_application.leave_application import get_leave_balance_on

@frappe.whitelist()
def update_approval_role_for_leave_application(workflow_state,name):
    if workflow_state == 'HOD Pending':
        frappe.db.set_value('Leave Application',{'name':name}, 'approver_role', 'HOD')
    elif workflow_state == 'TL Pending':
        frappe.db.set_value('Leave Application',{'name':name}, 'approver_role', 'TL')
    elif workflow_state == 'HR Pending':
        frappe.db.set_value('Leave Application',{'name':name}, 'approver_role', 'HR Manager')
    elif workflow_state == 'Director Pending':
        frappe.db.set_value('Leave Application',{'name':name}, 'approver_role', 'Director')
    elif workflow_state == 'MD Pending':
        frappe.db.set_value('Leave Application',{'name':name}, 'approver_role', 'MD')
    elif workflow_state in ['Approved', 'Rejected']:
        frappe.db.set_value('Leave Application',{'name':name}, 'approved_by', frappe.session.user)
    return "ok"




 
@frappe.whitelist()
def validate_leave(doc, method):
    user_roles = frappe.get_roles(frappe.session.user)
    hr = "Miss Punch" in user_roles
    admin = "Administrator" in user_roles
    if (not hr):
        allowed_days = 3
        current_date = today()
        if isinstance(current_date, str):
            current_date = datetime.strptime(current_date, "%Y-%m-%d").date()
        earliest_allowed = add_days(current_date, -3)
        if isinstance(doc.to_date, str):
            miss_date = datetime.strptime(doc.to_date, "%Y-%m-%d").date()
        else:
            miss_date = doc.to_date
        if miss_date < earliest_allowed:
            frappe.throw(
                _("Leave applications are allowed only for up to the previous {0} working days.")
                .format(allowed_days)
            )
        

@frappe.whitelist()
# when already leave application present in draft status for existing balance, then error will be thrown
def restrict_for_zero_balance(doc, method):
    if doc.leave_type!='Leave Without Pay': 
        total_leave_days_present=0
        total_lbalance=doc.leave_balance
        draft_leave_applications = frappe.get_all("Leave Application", {"employee": doc.employee,"docstatus":0,"leave_type": doc.leave_type,'name':('!=',doc.name)},["total_leave_days"])
        for i in draft_leave_applications:
            # frappe.errprint(i.name)
            total_leave_days_present+=i.total_leave_days
        total_leave_days_present += doc.total_leave_days
        available=total_lbalance-total_leave_days_present
        # frappe.errprint(total_lbalance)
        # frappe.errprint(total_leave_days_present)
        # frappe.errprint(available)
        if available < 0 :
            frappe.throw("Insufficient leave balance for this leave type")

@frappe.whitelist()
def update_status(doc,method):
    if doc.workflow_state =='Rejected':
        frappe.db.set_value('Leave Application',doc.name,'status','Rejected')  
        if doc.docstatus == 0:
            frappe.db.set_value('Leave Application',doc.name,'docstatus',1)
    if doc.workflow_state =='HR Pending':
        # if doc.docstatus == 0:
        #     frappe.db.set_value('Leave Application',doc.name,'docstatus',1)
        frappe.db.set_value('Leave Application',doc.name,'status','Approved')