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
def get_duplicate_attendance(employee,date,name):
    if frappe.db.exists("Attendance",{'name':['!=',name],'employee':employee,'attendance_date':date,'docstatus':("!=",2)}):
        att_name=frappe.db.get_value("Attendance",{'name':['!=',name],'employee':employee,'attendance_date':date,'docstatus':("!=",2)},['name'])
        return att_name
    
    
@frappe.whitelist()
#submit attendance when status is on leave
def submit_att(doc,method):  
    if doc.docstatus==0:
        if doc.status=='On Leave'and doc.leave_type:
            frappe.db.set_value('Attendance',doc.name,'docstatus',1)    
        