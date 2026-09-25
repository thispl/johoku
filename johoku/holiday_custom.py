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
def validate_the_holiday_list(name,holiday_date):
    doc = frappe.get_doc('Holiday List', name)
    if doc.holidays:
        holiday_counts = frappe.db.get_all(
            'Holiday',
            {'parent': doc.name,'holiday_date':holiday_date},
            ['holiday_date', 'count(*) as count'],
            group_by='holiday_date'
        )
        for h in holiday_counts:
            count = h.get('count')
            if count > 0:
                holiday_date = h.get('holiday_date')
                holiday_date = frappe.utils.formatdate(holiday_date, 'dd-mm-yyyy')
                return f"Duplicate holiday found on {holiday_date}"