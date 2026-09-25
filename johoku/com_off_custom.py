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


@frappe.whitelist()
def compensatory_on_cancel(doc,method):	
    if doc.leave_allocation:
        leave_allocation = doc.leave_allocation
        # frappe.db.set_value("Compensatory Leave Request",self.name,'leave_allocation','')
        la=frappe.get_doc('Leave Allocation',leave_allocation)
        # frappe.errprint(doc.leave_allocation)
        # frappe.errprint(la)
        if doc.created_via:
            if frappe.db.exists('Attendance',{'name':doc.created_via}):
                frappe.db.set_value("Attendance",doc.created_via,'coff_updated',0)
                la.cancel()