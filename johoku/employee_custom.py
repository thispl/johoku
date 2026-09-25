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
#checks the employee number already
# exist if not it will update the employee numer and rename the document with the number.
def update_employee_no(name,employee_number):
    emp = frappe.get_doc("Employee",name)
    emps=frappe.get_all("Employee",{"status":"Active"},['*'])
    for i in emps:
        if emp.employee_number == employee_number:
            pass
        elif i.employee_number == employee_number:
            frappe.throw(f"Employee Number already exists for {i.name}")
        else:
            frappe.db.set_value("Employee",name,"employee_number",employee_number)
            frappe.rename_doc("Employee", name, employee_number, force=1)
            return employee_number
        
        
@frappe.whitelist()
def get_date_dictionary_format_for_cl_sl(from_date_):
    # current_date = date.today()
    year = from_date_.year
    # year = int("2024")
    # year -= 1
    previous_year = year
    from_date = f"01-01-{previous_year}"
    to_date = f"31-12-{year}"
    from_date = getdate(from_date)
    to_date = getdate(to_date)
    # print(from_date)
    # print(to_date)
    months = []
    current_date = from_date

    while current_date <= to_date:
        month_year = current_date.strftime("%Y-%m")
        month_name = current_date.strftime("%B")  

        start_date = current_date
        end_date = add_months(current_date, 1) - timedelta(days=1)

        months.append({
            "month": month_name,
            "month_year": month_year,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        })

        current_date = add_months(current_date, 1)

    return months



@frappe.whitelist()
def create_cl_sl_leave_allocation(employee_doc_name,probation_end_date):
    
    cl_data_dictionary = {
        "January": 10.0,
        "February": 9.0,
        "March": 8.0,
        "April": 7.5,
        "May": 7.0,
        "June": 6.0,
        "July": 5.0,
        "August": 4.0,
        "September": 3.0,
        "October": 2.5,
        "November": 2.0,
        "December": 1.0
  
    }
    sl_data_dictionary = {
        "January": 7.0,
        "February": 6.0,
        "March": 5.5,
        "April": 5.0,
        "May": 4.5,
        "June": 4.0,
        "July": 3.5,
        "August": 3.0,
        "September": 2.0,
        "October": 1.5,
        "November": 1.0,
        "December": 0.5
  
    }
    
    el_data_dictionary = {
        "January": 15.0,   
        "February": 14.0,    
        "March": 12.5,   
        "April": 11.0,      
        "May": 10.0,      
        "June": 9.0,        
        "July": 7.5,       
        "August": 6.0,        
        "September": 5.0,     
        "October": 4.0,   
        "November": 2.5,    
        "December": 1.0  
     
    }
    # date_data = get_date_dictionary_format()
    # frappe.errprint(date_data)
    # for cl_dates in date_data:
    #     start_date =cl_dates.get('start_date')
    #     end_date = cl_dates.get('end_date')
        # frappe.errprint(start_date)
        # frappe.errprint(end_date)
        
    new_join_employees = frappe.db.sql("""
        SELECT name, employee_name,date_of_joining,probation_end_date
        FROM `tabEmployee`
        WHERE
            employee = %(employee)s                         
            AND status = 'Active'
    """, {
        'employee': employee_doc_name,
    }, as_dict=True)

    for employee in new_join_employees:
        joining_year = getdate(employee.get('probation_end_date')).year
        # print(joining_year)
        to_date = f"{joining_year}-12-31"
        # from_date = getdate(start_date)
        from_date = add_months(getdate(employee.get('date_of_joining')),6)
        if employee.get('probation_end_date'):
            from_date = add_days(getdate(employee.get('probation_end_date')),1)

        doj = getdate(employee.get('date_of_joining'))
        el_from_date = add_years(doj, 1)

        joining_year = el_from_date.year
        el_to_date = f"{joining_year}-12-31"

        
        month_list = get_date_dictionary_format_for_cl_sl(from_date)
        # frappe.errprint(month_list)
        # frappe.errprint(f"{from_date} from Date")
        for i in month_list:
            # frappe.errprint(f"{i['start_date']} start date")
            # frappe.errprint(f"{i['end_date']} end date")
            if getdate(i['start_date']) <= from_date <= getdate(i['end_date']):
                month_name = i['month']
                # frappe.errprint(month_name)
                break
        
        if not frappe.db.exists("Leave Allocation", {"employee":  employee.get('name'), "leave_type": "Casual Leave",'from_date':from_date,'to_date':to_date,'docstatus':["!=",2]}):
            leaves = cl_data_dictionary.get(month_name)
            cl_doc = frappe.new_doc("Leave Allocation")
            cl_doc.employee = employee.get('name')
            cl_doc.leave_type = "Casual Leave"
            cl_doc.new_leaves_allocated = leaves
            cl_doc.total_leaves_allocated = leaves
            cl_doc.from_date = from_date
            cl_doc.to_date = to_date
            cl_doc.save(ignore_permissions=True)
            # cl_doc.submit()
        if not frappe.db.exists("Leave Allocation", {"employee":  employee.get('name'), "leave_type": "Sick Leave",'from_date':from_date,'to_date':to_date,'docstatus':["!=",2]}):
            leaves = sl_data_dictionary.get(month_name)
            sl_doc = frappe.new_doc("Leave Allocation")
            sl_doc.employee = employee.get('name')
            sl_doc.leave_type = "Sick Leave"
            sl_doc.new_leaves_allocated = leaves
            sl_doc.total_leaves_allocated = leaves
            sl_doc.from_date = from_date
            sl_doc.to_date = to_date
            sl_doc.save(ignore_permissions=True)
            # sl_doc.submit()
            
        el_month_list = get_date_dictionary_format_for_cl_sl(el_from_date)

        for i in el_month_list:
            if getdate(i['start_date']) <= el_from_date <= getdate(i['end_date']):
                el_month_name = i['month']
                break

        if not frappe.db.exists( "Leave Allocation", { "employee": employee.get('name'),"leave_type": "Earned Leave","from_date": el_from_date, "to_date": el_to_date,"docstatus": ["!=", 2]}):
            leaves = el_data_dictionary.get(el_month_name)
            el_doc = frappe.new_doc("Leave Allocation")
            el_doc.employee = employee.get('name')
            el_doc.leave_type = "Earned Leave"
            el_doc.new_leaves_allocated = leaves
            el_doc.total_leaves_allocated = leaves
            el_doc.from_date = el_from_date
            el_doc.to_date = el_to_date
            el_doc.save(ignore_permissions=True)



@frappe.whitelist()
#throws an error if the status is Active but relieving date is present
def inactive_employee(doc,method):
    if doc.status=="Active":
        if doc.relieving_date:
            throw(_("Please remove the relieving date for the Active Employee."))



@frappe.whitelist()
def calculate_age(doc,method):
    # frappe.errprint('Data Import')
    date_of_birth = getdate(doc.date_of_birth)
    today_date = getdate(today())
    age = today_date.year - date_of_birth.year - ((today_date.month, today_date.day) < (date_of_birth.month, date_of_birth.day))
    frappe.db.set_value('Employee', doc.name, 'age', age)


import frappe
from frappe.utils import today, getdate, add_days
@frappe.whitelist()
def alert_for_probation_emp_new():
    job = frappe.db.exists('Scheduled Job Type', 'send_probation_alerts_new')
    if not job:
        emc = frappe.new_doc("Scheduled Job Type")
        emc.update({
            "method": 'johoku.employee_custom.send_probation_alerts_emp',
            "frequency": 'Cron',
            "cron_format": '0 10 * * *'  
        })
        emc.save(ignore_permissions=True)

def send_probation_alerts_emp():
    today_date = getdate(today())
    end_date_limit = add_days(today_date, 30)
    
    employees = frappe.get_all(
        'Employee',
        filters={'status':'Active','employment_type': 'Probation','probation_start_date': ['is', 'set'],'probation_end_date': ['between', [today_date, end_date_limit]]},
        fields=['name', 'employee_name', 'probation_end_date']
    )
    
    expired_employees = frappe.get_all(
        'Employee',
        filters={'status':'Active','employment_type': 'Probation','probation_start_date': ['is', 'set'],'probation_end_date': ['<', today_date]},
        fields=['name', 'employee_name', 'probation_end_date']
    )
    
    rows = ""
    for emp in employees:
        days_remaining = (getdate(emp.probation_end_date) - today_date).days
        rows += f"""
            <tr>
                <td>{emp.name}</td>
                <td>{emp.employee_name}</td>
                <td>{emp.probation_end_date}</td>
                <td>{days_remaining} days remaining</td>
                <td style="color:orange;">Expiring Soon</td>
            </tr>
        """
    for emp in expired_employees:
        days_expired = (today_date - getdate(emp.probation_end_date)).days
        rows += f"""
            <tr>
                <td>{emp.name}</td>
                <td>{emp.employee_name}</td>
                <td>{emp.probation_end_date}</td>
                <td>Expired {days_expired} days ago</td>
                <td style="color:red;">Expired</td>
            </tr>
        """
    
    if rows:
        html = f"""
        <h3>Probation Period Alerts</h3>
        <table border="1" cellpadding="5" cellspacing="0">
            <tr>
                <th>Employee ID</th>
                <th>Employee Name</th>
                <th>Probation End Date</th>
                <th>Days Remaining / Expired Days</th>
                <th>Expiry Status</th>
            </tr>
            {rows}
        </table>
        """

        frappe.sendmail(
            recipients=["hr@johoku.co.in" , "jeniba.a@groupteampro.com" ,"t.kannadhasan@johoku.co.in" , "saranya.v@johoku.co.in"], 
            # recipients=["jeniba.a@groupteampro.com"], 
            subject="Daily Probation Alert Notification",
            message=html
        )
        
   
   
@frappe.whitelist()
def create_scheduled_job_new1():
    job = frappe.db.exists('Scheduled Job Type', 'Birthday Remainder')
    if not job:
        emc = frappe.new_doc("Scheduled Job Type")
        emc.update({
            "method": 'johoku.employee_custom.send_birthday_reminder_to_hr_new1',
            "frequency": 'Cron',
            "cron_format": '0 7 * * *'
        })
        emc.save(ignore_permissions=True)
        
from frappe.utils import nowdate
@frappe.whitelist()
def send_birthday_reminder_to_hr_new1():
    today = nowdate()
    month = today.split("-")[1]
    day = today.split("-")[2]

    employees = frappe.db.sql("""
        SELECT name, employee_name
        FROM `tabEmployee`
        WHERE status = 'Active'
        AND MONTH(date_of_birth) = %s
        AND DAY(date_of_birth) = %s
    """, (month, day), as_dict=True)

    if not employees:
        return

    emp_names = ", ".join([emp["employee_name"] for emp in employees])

    # hr_users = frappe.get_all(
    #     "Has Role",
    #     filters={"role": ["in", ["HR User"]]},
    #     pluck="parent"
    
    # )
    
    hr_users = frappe.get_all(
        "User",
        filters={
            "enabled": 1,
            "name": ["in", frappe.get_all(
                "Has Role",
                filters={
                    "role": "HR User",
                    "parenttype": "User"
                },
                pluck="parent"
            )]
        },
        pluck="email"
    )
    
    frappe.log_error(
        title="Birthday Debug - Employees",
        message=str(employees)
    )
    
    frappe.log_error(
        title="Birthday Debug - HR Users",
        message=str(hr_users)
    )
    if not hr_users:
        return

    subject = "Birthday Reminder 🎉"
    message = f"""
    Today is {emp_names}'s birthday 🎉<br><br>
    A friendly reminder for the HR team.
    """

    frappe.sendmail(
        recipients=list(set(hr_users)),
        subject=subject,
        message=message
    )
    
    