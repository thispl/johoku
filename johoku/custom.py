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
def get_approver(department, employee_id):
    user = frappe.db.get_value('Employee_id', employee_id, 'user_id')
    roles = frappe.get_roles(user)
    if 'GM' in roles:
        return frappe.db.get_value('Department', department, "ceo")
    elif 'HOD' in roles:
        return frappe.db.get_value('Department', department, "gm")
    else:
        return frappe.db.get_value('Department', department, "hod")  

@frappe.whitelist()
def get_day():
    today = getdate('2023-02-04')
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    print("Today: " + str(today))
    print("Start: " + str(start))
    print("End: " + str(end))

def get_year():
    today_day = date.today()
    previous_year = add_years(today_day,1)
    if today_day == today_day:
        print('hi')
    else:
        print('no')    
    print(today_day.year)
    print(previous_year.year)


@frappe.whitelist()
def department():
    result = frappe.db.sql("""SELECT employee_category, COUNT(*) AS count
                         FROM `tabShift Assignment`
                         WHERE start_date BETWEEN %s AND %s
                         AND department = %s
                         AND shift_type = %s
                         AND docstatus = 1
                         GROUP BY employee_category""",
                      ('2023-02-20', '2023-02-26', 'Production - JMPL', '1'),
                      as_dict=True)
    if result:
        for row in result:
            print("Employee Category:", row["employee_category"], "Count:", row["count"])
    else:
        print("No results found.")

def cancel_shift_assign():
    a = 0
    for i in range(1,6):
        a += i
    print(a)


@frappe.whitelist()
def create_lwf():
    # add lwf deduction amount 20 rupees by default on december.
    def is_december_1(date_to_check):
        return date_to_check.month == 12 and date_to_check.day == 1
    employee_query = """
    SELECT *
    FROM tabEmployee
    WHERE
        status = 'Active'  """
    employee = frappe.db.sql(employee_query, as_dict=True)
    date_to_check = date.today()
    if is_december_1(date_to_check):
        print("The date is December 1st.")
        year = date_to_check.year
        year = int(year)
        payroll_date = date(year, 12, 20) 
        for emp in employee:
            if frappe.db.exists("Salary Structure Assignment", {'employee': emp.name, 'docstatus': 1}):
                if not frappe.db.exists('Additional Salary', {'employee': emp.name, 'payroll_date': payroll_date, 'salary_component': "Labour Welfare Fund", 'docstatus': ('!=', 2)}):
                    lwf = frappe.new_doc("Additional Salary")
                    lwf.employee = emp.name
                    lwf.payroll_date = payroll_date
                    lwf.company = emp.company
                    lwf.salary_component = "Labour Welfare Fund"
                    lwf.currency = "INR"
                    lwf.amount = 20
                    lwf.save(ignore_permissions=True)
                    lwf.submit()
    else:
        print("The date is not December 1st.")

@frappe.whitelist()
def create_el_enhancement():
    def is_jan_1(date_to_check):
        return date_to_check.month == 1 and date_to_check.day == 20
    date_to_check = date.today()
    year = date_to_check.year
    year = int(year)
    employee_query = """
    SELECT *
    FROM `tabLeave Allocation`
    WHERE
        docstatus = 1 AND carry_forward = 1 AND leave_type = 'Earned Leave' AND YEAR(from_date) = %s
"""
    employee = frappe.db.sql(employee_query, (year,), as_dict=True)
    date_to_check = date.today()
    if is_jan_1(date_to_check):
        year = date_to_check.year
        year = int(year)
        payroll_date = date(year, 1, 20) 
        for emp in employee:
            if emp.total_leaves_allocated > 30:
                if frappe.db.exists("Salary Structure Assignment", {'employee': emp.employee, 'docstatus': 1}):
                    if not frappe.db.exists('Additional Salary', {'employee': emp.employee, 'payroll_date': payroll_date, 'salary_component': "EL Encashment", 'docstatus': ('!=', 2)}):
                        basic = frappe.db.get_value('Employee',emp.employee,'basic')
                        amount = (basic/31) * (emp.total_leaves_allocated - 30)
                        el_enhancement = frappe.new_doc("Additional Salary")
                        el_enhancement.employee = emp.employee
                        el_enhancement.payroll_date = payroll_date
                        el_enhancement.company = emp.company
                        el_enhancement.salary_component = "EL Encashment"
                        el_enhancement.currency = "INR"
                        el_enhancement.amount = amount
                        el_enhancement.save(ignore_permissions=True)
                        el_enhancement.submit()
   



# @frappe.whitelist()
# #update the employee checkin from Unregistered employee checkin by clicking process checkin in attendance settings
# def get_urc_to_ec(from_date, to_date):
#     print("HI")
#     urc = frappe.db.sql("""select biometric_pin,biometric_time,log_type,locationdevice_id,name from `tabUnregistered Employee Checkin` where date(biometric_time) between '%s' and '%s'"""%(from_date,to_date),as_dict=True)
#     for uc in urc:
#         pin = uc.biometric_pin
#         time = uc.biometric_time
#         dev = uc.locationdevice_id
#         typ = uc.log_type
#         nam = uc.name
#         if time != "":
#             if frappe.db.exists('Employee',{'name':pin}):
#                 if frappe.db.exists('Employee Checkin',{'name':pin,"time":time}):
#                     print("HI")
#                 else:
#                     print("HII")
#                     ec = frappe.new_doc('Employee Checkin')
#                     ec.biometric_pin = pin
#                     ec.employee = frappe.db.get_value('Employee',{'name':pin},['employee_number'])
#                     ec.time = time
#                     ec.device_id = dev
#                     ec.log_type = typ
#                     ec.save(ignore_permissions=True)
#                     frappe.db.commit()
#                     print("Created")
#                     attendance = frappe.db.sql(""" delete from `tabUnregistered Employee Checkin` where name = '%s' """%(nam))
#                     print("Deleted")       
#             else:				
#                 print("hello")	
#     return "ok"


from frappe.utils.background_jobs import enqueue
@frappe.whitelist()
def process_push_punch(from_date):
    enqueue(push_punch, queue='default', timeout=6000, event='enqueue_submit_schedule',from_date=from_date)


@frappe.whitelist()
#use to process checkin from frontend
def push_punch(from_date, to_date):
    from cgi import print_environ
    import mysql.connector
    import requests,json
    from datetime import date
    from datetime import time,datetime

    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Pa55w0rd@",
    database="easytimepro"
    )

    # from_date = "2023-06-21"
    # to_date = "2023-07-26"

    # pre_date = add_days(from_date(),-1)  

    mycursor = mydb.cursor(dictionary=True)
    query = "SELECT  * FROM iclock_transaction where date(punch_time) between '%s' and '%s' "%(from_date,to_date)
    mycursor.execute(query)
    attlog = mycursor.fetchall()
    if attlog:
        for a in attlog:
            url = "http://157.245.101.198/api/method/johoku.biometric_checkin.mark_checkin?employee=%s&time=%s&device_id=%s" % (a['emp_code'],a['punch_time'],a['terminal_alias'])
            headers = { 'Content-Type': 'application/json','Authorization': 'token b3df19e9615e0dc:b499d47b3041f94'}
            response = requests.request('GET',url,headers=headers,verify=False)
            res = json.loads(response.text)
            if res:
                if res['message'] == 'Checkin Marked':
                    mycursor = mydb.cursor()
                    sql = "UPDATE iclock_transaction SET checkin_marked = 1 WHERE id = %s " % a['id']
                    mycursor.execute(sql)
                    mydb.commit()  
            else:
                pass
    return 'ok' 


from frappe import _

# from frappe import _

# @frappe.whitelist()
# def validate_leave_application(doc, method):
# 	today = frappe.utils.getdate(frappe.utils.today())
# 	current_month = today.month
# 	current_year = today.year
                                                                                                                                       
# 	# Calculate payroll start and end dates based on the current month
# 	if current_month == 12:
# 		payroll_start_date = frappe.utils.getdate(f"21-12-{current_year}")
# 		payroll_end_date = frappe.utils.getdate(f"20-01-{current_year + 1}")
# 	else:
# 		payroll_start_date = frappe.utils.getdate(f"21-{current_month}-{current_year}")
# 		payroll_end_date = frappe.utils.getdate(f"20-{current_month + 1}-{current_year}")

# 	application_from_date = frappe.utils.getdate(doc.from_date)
# 	application_to_date = frappe.utils.getdate(doc.to_date)
    

# 	if (
# 		(payroll_start_date <= application_from_date <= payroll_end_date)
# 		and (application_from_date.day > 23 or application_to_date.day > 23)
# 	):
# 		frappe.throw(_(Permission Request on the 23rd of the month is not allowed."))

# 	if application_from_date > application_to_date:
# 		frappe.throw(_("From date should be before or equal to To date"))

# from frappe import _

# def validate_leave_application(doc, method):
# 	import datetime
    
# 	today = datetime.date.today()
# 	start_date = datetime.datetime.strptime(doc.from_date, "%Y-%m-%d").date()
    
# 	if today.day > 22 and start_date <= today:
# 		frappe.throw(_("Leave application is not allowed after the 22nd of the month."))




@frappe.whitelist()
def update_designation_from_staffing_plan(staffing):
    staff = frappe.get_all("Staffing Plan Detail",{'parent':staffing},['*'])
    return staff


@frappe.whitelist()
def delete_urc():
    urc = frappe.db.sql("""delete from `tabUnregistered Employee Checkin` """,as_dict = True)
    print(urc)
    
@frappe.whitelist()
#return the employee who are not having Salary Structure Assignment
def salary():
    emp=frappe.db.sql("""select * from `tabEmployee` where status='Active'""",as_dict=True)
    for e in emp:
        if not frappe.db.exists("""select * from `tabSalary Structure Assignment` where employee=%s"""%(e.name)):
            print(e.name)

# @frappe.whitelist()
# #throws an error if the status is Active but relieving date is present
# def inactive_employee(doc,method):
#     if doc.status=="Active":
#         if doc.relieving_date:
#             throw(_("Please remove the relieving date for the Active Employee."))


@frappe.whitelist()
#sends notification to each level of approvers of each level approval of leave applications.
def leave_application_notify():
    staff = """
        <div style="text-align: center;">
            <h2 style="font-size: 16px;">Leave Application Report</h2>
        </div>
        <table style="border-collapse: collapse; width: 100%; border: 1px solid black; font-size: 10px;">
            <tr style="border: 1px solid black;">
                <th style="padding: 4px; border: 1px solid black;">S.No</th>
                <th style="padding: 4px; border: 1px solid black;">Employee</th>
                <th style="padding: 4px; border: 1px solid black;">Employee Name</th>
                <th style="padding: 4px; border: 1px solid black;">Department</th>
                <th style="padding: 4px; border: 1px solid black;">Document ID</th>
                <th style="padding: 4px; border: 1px solid black;">From date</th>
                <th style="padding: 4px; border: 1px solid black;">To Date</th>
                <th style="padding: 4px; border: 1px solid black;">Leave Type</th>
            </tr>
    """
    staff_hod = staff
    staff_md = staff
    staff_department = staff
    staff_director = staff


    hr = frappe.db.sql_list(
                """select distinct hr_approval from `tabEmployee`
                where status = 'Active' """,
            )
    
    count = frappe.db.count('Leave Application',{'workflow_state':'HR Pending','docstatus':0})
    email_addresses = []
    if count != 0:
        for i in hr:
            hr_approver = frappe.get_all("Employee",{'status':'Active','hr_approval':i},['name'])
            email_addresses += [i]
            for j in hr_approver:
                hr_app = frappe.get_all("Leave Application",{'employee':j.name},['employee','employee_name','department','name','from_date','to_date','leave_type','workflow_state'])
                for leave in hr_app:
                    idx = 1
                    if leave.workflow_state == 'HR Pending':
                        
                        if leave:
                            staff += """
                                <tr style="border: 1px solid black;">
                                    <td style="padding: 4px; border: 1px solid black;">{0}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{1}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{2}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{3}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{4}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{5}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{6}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{7}</td>
                                </tr>
                            """.format(idx, leave.employee, leave.employee_name, leave.department, leave.name or ' ',format_date(leave.from_date),format_date(leave.to_date), leave.leave_type or '')
                        idx += 1
            
            if email_addresses:
                frappe.sendmail(
                    # recipients=['jothi.m@groupteampro.com'],
                    recipients = email_addresses,
                    subject='Leave Application Report - HR Pending',
                    message="""Dear Sir,<br><br>
                            Kindly Find the list of Leave Application waiting for your Approval:<br>{0}
                            """.format(staff)
                )
                del email_addresses[0]

           
    hr = frappe.db.sql_list(
                """select distinct department_approval from `tabEmployee`
                where status = 'Active' """,
            )
    count1 = frappe.db.count('Leave Application',{'workflow_state':'Department Pending','docstatus':0})
    email_addresses_dept = []
    department_mail = []
    new_leave =0
    if count1 != 0:
        for i in hr:
            hr_approver = frappe.get_all("Employee",{'status':'Active','department_approval':i},['name'])
            email_addresses_dept+= [i]
            for j in hr_approver:
                hr_app = frappe.get_all("Leave Application",{'employee':j.name},['employee','employee_name','department','name','from_date','to_date','leave_type','workflow_state'])
                for leave in hr_app:
                    idx = 1
                    if leave.workflow_state == 'Department Pending':
                        if leave:
                            department_mail += [idx] 
                            staff_department += """
                        <tr style="border: 1px solid black;">
                            <td style="padding: 4px; border: 1px solid black;">{0}</td>
                            <td style="padding: 4px; border: 1px solid black;">{1}</td>
                            <td style="padding: 4px; border: 1px solid black;">{2}</td>
                            <td style="padding: 4px; border: 1px solid black;">{3}</td>
                            <td style="padding: 4px; border: 1px solid black;">{4}</td>
                            <td style="padding: 4px; border: 1px solid black;">{5}</td>
                            <td style="padding: 4px; border: 1px solid black;">{6}</td>
                            <td style="padding: 4px; border: 1px solid black;">{7}</td>
                        </tr>
                    """.format(idx, leave.employee, leave.employee_name, leave.department, leave.name or ' ',format_date(leave.from_date),format_date(leave.to_date), leave.leave_type or '')
                        idx += 1
                        new_leave = 1
            if email_addresses_dept and new_leave == 1:
                print(email_addresses_dept)
                # frappe.sendmail(
                #     # recipients=['jothi.m@groupteampro.com'],
                #     recipients = email_addresses_dept,
                #     subject='Leave Application Report-Department Pending',
                #     message="""Dear Sir,<br><br>
                #             Kindly Find the list of Leave Application waiting for your Approval:<br>{0}
                #             """.format(staff_department)
                # )
            if email_addresses_dept:
                print(email_addresses_dept)
                del email_addresses_dept[0]
            if isinstance(staff_department, str) and staff_department:
                staff_department = staff_department[:1]
            if department_mail:
                del department_mail[0]
                print(email_addresses_dept)
    hr = frappe.db.sql_list(
                """select distinct md_approval from `tabEmployee`
                where status = 'Active' """,
            )
    count2 = frappe.db.count('Leave Application',{'workflow_state':'MD Pending','docstatus':0})
    email_addresses_md =[]
    if count2 != 0:
        for i in hr:
            email_addresses_md += [i]
            hr_approver = frappe.get_all("Employee",{'status':'Active','md_approval':i},['name'])

            for j in hr_approver:
                hr_app = frappe.get_all("Leave Application",{'employee':j.name},['employee','employee_name','department','name','from_date','to_date','leave_type','workflow_state'])
                for leave in hr_app:
                    idx = 1
                    if leave.workflow_state == 'MD Pending':
        
                        staff_md += """
                            <tr style="border: 1px solid black;">
                                <td style="padding: 4px; border: 1px solid black;">{0}</td>
                                <td style="padding: 4px; border: 1px solid black;">{1}</td>
                                <td style="padding: 4px; border: 1px solid black;">{2}</td>
                                <td style="padding: 4px; border: 1px solid black;">{3}</td>
                                <td style="padding: 4px; border: 1px solid black;">{4}</td>
                                <td style="padding: 4px; border: 1px solid black;">{5}</td>
                                <td style="padding: 4px; border: 1px solid black;">{6}</td>
                                <td style="padding: 4px; border: 1px solid black;">{7}</td>
                            </tr>
                        """.format(idx, leave.employee, leave.employee_name, leave.department, leave.name or ' ',format_date(leave.from_date),format_date(leave.to_date), leave.leave_type or '')
                        idx += 1
        if email_addresses_md:
            frappe.sendmail(
                # recipients=['jothi.m@groupteampro.com'],
                recipients = email_addresses_md,
                subject='Leave Application Report -MD Pending',
                message="""Dear Sir,<br><br>
                        Kindly Find the list of Leave Application waiting for your Approval:<br>{0}
                        """.format(staff_md)
            )
            del email_addresses_md[0]

    hr_app = frappe.get_all("Leave Application",
                        filters={'docstatus': ['!=', 2]},
                        fields=['employee', 'employee_name', 'department', 'name', 'from_date', 'to_date', 'leave_type', 'workflow_state'])

    count3 = frappe.db.count('Leave Application',{'workflow_state':'Director Pending','docstatus':0})
    if count3 != 0:
        for leave in hr_app:
            if leave.workflow_state == 'Director Pending':
                idx = 1
                staff_director += """
                    <tr style="border: 1px solid black;">
                        <td style="padding: 4px; border: 1px solid black;">{0}</td>
                        <td style="padding: 4px; border: 1px solid black;">{1}</td>
                        <td style="padding: 4px; border: 1px solid black;">{2}</td>
                        <td style="padding: 4px; border: 1px solid black;">{3}</td>
                        <td style="padding: 4px; border: 1px solid black;">{4}</td>
                        <td style="padding: 4px; border: 1px solid black;">{5}</td>
                        <td style="padding: 4px; border: 1px solid black;">{6}</td>
                        <td style="padding: 4px; border: 1px solid black;">{7}</td>
                    </tr>
                """.format(idx, leave.employee, leave.employee_name, leave.department, leave.name or ' ',format_date(leave.from_date),format_date(leave.to_date), leave.leave_type or '')
                idx += 1

        frappe.sendmail(
            # recipients=['jothi.m@groupteampro.com'],
            recipients=['suzuki-syu@johoku-kigyo.co.jp'],
            subject='Leave Application Report - Director Pending',
            message="""Dear Sir,<br><br>
                    Kindly Find the list of Leave Application waiting for your Approval:<br>{0}
                    """.format(staff_director)
        )
    hr_app = frappe.get_all(
        "Leave Application",
        filters={'docstatus': ['!=', 2]},
        fields=['employee', 'employee_name', 'department', 'name', 'from_date', 'to_date', 'leave_type', 'workflow_state']
    )
    
    count5 = frappe.db.count('Leave Application', {'workflow_state': 'HOD Pending', 'docstatus': 0})
    hod_list_1, hod_list_2, hod_list_3, hod_list_4 = "", "", "", ""
    idx = 1
    if count5 != 0:
        for leave in hr_app:
            if leave.workflow_state == 'HOD Pending':
                row = """
                    <tr style="border: 1px solid black;">
                        <td style="padding: 4px; border: 1px solid black;">{0}</td>
                        <td style="padding: 4px; border: 1px solid black;">{1}</td>
                        <td style="padding: 4px; border: 1px solid black;">{2}</td>
                        <td style="padding: 4px; border: 1px solid black;">{3}</td>
                        <td style="padding: 4px; border: 1px solid black;">{4}</td>
                        <td style="padding: 4px; border: 1px solid black;">{5}</td>
                        <td style="padding: 4px; border: 1px solid black;">{6}</td>
                        <td style="padding: 4px; border: 1px solid black;">{7}</td>
                    </tr>
                """.format(idx, leave.employee, leave.employee_name, leave.department, leave.name or ' ',
                        format_date(leave.from_date), format_date(leave.to_date), leave.leave_type or '')

                if leave.department in ['PPC - JMPL', 'Purchase - JMPL', 'Sales - JMPL']:
                    hod_list_1 += row
                elif leave.department in ['Finance - JMPL', 'HR and GA - JMPL']:
                    hod_list_2 += row
                elif leave.department in ['Technical - JMPL', 'QUALITY - JMPL']:
                    hod_list_3 += row
                elif leave.department in ['Stores - JMPL', 'Dispatch - JMPL', 'Assembly Shop - JMPL', 'Machine Shop - JMPL', 'MAINTENANCE - JMPL', 'Utility - JMPL']:
                    hod_list_4 += row
                idx += 1

        multiple_hod_list = [hod_list_1, hod_list_2, hod_list_3, hod_list_4]
        # for l in multiple_hod_list:
        #     if l: 
        #         if l == hod_list_1:
        #             frappe.sendmail(
        #             # recipients=['jothi.m@groupteampro.com'],
        #             recipients=['karthick.m@johoku.co.in'],
        #             subject='Leave Application Report - HOD Pending',
        #             message="""Dear Sir,<br><br>
        #                     Kindly Find the list of Leave Applications waiting for your Approval:<br>{0}{1}""".format(staff_hod,l)
        #         )
        #         if l == hod_list_2:
        #             frappe.sendmail(
        #                 recipients=['ramesh.b@johoku.co.in'],
        #             # recipients=['jothi.m@groupteampro.com'],
        #             subject='Leave Application Report - HOD Pending',
        #             message="""Dear Sir,<br><br>
        #                     Kindly Find the list of Leave Applications waiting for your Approval:<br>{0}{1}""".format(staff_hod,l)
        #         )
        #         if l == hod_list_3:
        #             frappe.sendmail(
        #                 recipients=['arunkumar.k@johoku.co.in'],
        #                 # recipients=['jothi.m@groupteampro.com'],
        #                 subject='Leave Application Report - HOD Pending',
        #                 message="""Dear Sir,<br><br>
        #                     Kindly Find the list of Leave Applications waiting for your Approval:<br>{0}{1}""".format(staff_hod,l)
        #         )
        #         if l == hod_list_4:
        #             frappe.sendmail(
        #                 recipients =['balaji.r@johoku.co.in'],
        #             # recipients=['jothi.m@groupteampro.com'],
        #                 subject='Leave Application Report - HOD Pending',
        #                 message="""Dear Sir,<br><br>
        #                     Kindly Find the list of Leave Applications waiting for your Approval:<br>{0}{1}""".format(staff_hod,l)
                # )


@frappe.whitelist()
#sends notification to each level of approvers of each level approval perimission request documents.
def permission_request_notify():
    staff = """
        <div style="text-align: center;">
            <h2 style="font-size: 16px;"Permission Request Report</h2>
        </div>
        <table style="border-collapse: collapse; width: 100%; border: 1px solid black; font-size: 10px;">
            <tr style="border: 1px solid black;">
                <th style="padding: 4px; border: 1px solid black;">S.No</th>
                <th style="padding: 4px; border: 1px solid black;">Employee</th>
                <th style="padding: 4px; border: 1px solid black;">Employee Name</th>
                <th style="padding: 4px; border: 1px solid black;">Department</th>
                <th style="padding: 4px; border: 1px solid black;">Document ID</th>
                <th style="padding: 4px; border: 1px solid black;">Permissions Date</th>
                <th style="padding: 4px; border: 1px solid black;">Session</th>
                <th style="padding: 4px; border: 1px solid black;">Permission hour</th>
            </tr>
    """
    staff_hod = staff
    staff_md = staff
    staff_department = staff
    staff_director = staff


    hr = frappe.db.sql_list(
                """select distinct hr_approval from `tabEmployee`
                where status = 'Active' """,
            )
    
    count = frappe.db.count('Permission Request',{'workflow_state':'HR Pending','docstatus':0})
    email_addresses = []
    if count != 0:
        for i in hr:
            hr_approver = frappe.get_all("Employee",{'status':'Active','hr_approval':i},['name'])
            email_addresses += [i]
            for j in hr_approver:
                hr_app = frappe.get_all("Permission Request",{'employee_id':j.name},['employee_id','employee_name','department','name','permission_date','session','permission_hour','workflow_state'])
                for leave in hr_app:
                    idx = 1
                    if leave.workflow_state == 'HR Pending':
                        
                        if leave:
                            staff += """
                                <tr style="border: 1px solid black;">
                                    <td style="padding: 4px; border: 1px solid black;">{0}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{1}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{2}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{3}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{4}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{5}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{6}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{7}</td>
                                </tr>
                            """.format(idx, leave.employee_id, leave.employee_name, leave.department, leave.name or ' ',
                        format_date(leave.attendance_date), leave.session, leave.permission_hour or '')
                            idx += 1
            if email_addresses:
                frappe.sendmail(
                    recipients = email_addresses,
                    # recipients=['jothi.m@groupteampro.com'],
                    subject='Permission Request Report - HR pending',
                    message="""Dear Sir,<br><br>
                            Kindly Find the list of Permission Request waiting for your Approval:<br>{0}
                            """.format(staff)
                )
            if email_addresses:
                del email_addresses[0]
    hr = frappe.db.sql_list(
                """select distinct department_approval from `tabEmployee`
                where status = 'Active' """,
            )
    count1 = frappe.db.count('Permission Request',{'workflow_state':'Department Pending','docstatus':0})
    email_addresses_dept = []
    department_mail = []
    if count1 != 0:
        for i in hr:
            hr_approver = frappe.get_all("Employee",{'status':'Active','department_approval':i},['name'])
            email_addresses_dept += [i]
            for j in hr_approver:
                hr_app = frappe.get_all(
                    "Permission Request",
                    filters={'employee_id':j.name,'docstatus': ['!=', 2]},
                    fields=['employee_id', 'employee_name', 'department', 'name', 'permission_date', 'session', 'permission_hour', 'workflow_state']
                )
                # hr_app = frappe.get_all("Permission Request",{'employee_id':j.name},['employee_id','employee_name','department','name','from_date','to_date','leave_type','workflow_state'])
                for leave in hr_app:
                    idx = 1
                    if leave.workflow_state == 'Department Pending':
                        if leave:
                            department_mail += [idx] 
                            staff_department += """
                                <tr style="border: 1px solid black;">
                                    <td style="padding: 4px; border: 1px solid black;">{0}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{1}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{2}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{3}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{4}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{5}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{6}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{7}</td>
                                </tr>
                            """.format(idx, leave.employee_id, leave.employee_name, leave.department, leave.name or ' ',
                                format_date(leave.attendance_date), leave.session, leave.permission_hour or '')
                            idx += 1
            if email_addresses_dept and len(department_mail) != 0: 
                # print(email_addresses_dept)
                frappe.sendmail(
                    # recipients=['jothi.m@groupteampro.com'],
                    recipients=email_addresses_dept,
                    subject='Permission Request Report - Department Pending',
                    message="""Dear Sir,<br><br>
                            Kindly Find the list of Permission Request waiting for your Approval:<br>{0}
                            """.format(staff_department)
                )
            if email_addresses_dept:
                del email_addresses_dept[0]
            if department_mail:
                del department_mail[0]
                # print("Hi" ,email_addresses_dept)
    hr = frappe.db.sql_list(
                """select distinct md_approval from `tabEmployee`
                where status = 'Active' """,
            )
    count2 = frappe.db.count('Permission Request',{'workflow_state':'MD Pending','docstatus':0})
    email_addresses_md =[]
    if count2 != 0:
        for i in hr:
            if i:
                email_addresses_md += [i]
                hr_approver = frappe.get_all("Employee",{'status':'Active','md_approval':i},['name'])
                for j in hr_approver:
                    # hr_app = frappe.get_all("Permission Request",{'employee':j.name},['employee','employee_name','department','name','from_date','to_date','leave_type','workflow_state'])
                    hr_app = frappe.get_all(
                        "Permission Request",
                        filters={'employee_id':j.name,'docstatus': ['!=', 2]},
                        fields=['employee_id', 'employee_name', 'department', 'name', 'permission_date', 'session', 'permission_hour', 'workflow_state']
                    )
                    for leave in hr_app:
                        idx = 1
                        if leave.workflow_state == 'MD Pending':
                            
                            staff_md += """
                                <tr style="border: 1px solid black;">
                                    <td style="padding: 4px; border: 1px solid black;">{0}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{1}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{2}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{3}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{4}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{5}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{6}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{7}</td>
                                </tr>
                            """.format(idx, leave.employee_id, leave.employee_name, leave.department, leave.name or ' ',
                                    format_date(leave.attendance_date), leave.session, leave.permission_hour or '')
                            idx += 1
        if email_addresses_md:
            frappe.sendmail(
            recipients =email_addresses_md,
                # recipients=['jothi.m@groupteampro.com'],
                subject='Permission Request Report - MD Pending',
                message="""Dear Sir,<br><br>
                        Kindly Find the list ofPermission Request waiting for your Approval:<br>{0}
                        """.format(staff_md)
            )
            del email_addresses_md[0]
    hr_app = frappe.get_all("Permission Request",
                        filters={'docstatus': ['!=', 2]},
                        fields=['employee_id', 'employee_name', 'department', 'name', 'permission_date', 'session', 'permission_hour', 'workflow_state'])

    # hr_app = frappe.get_all(Permission Request",{'docstatus', '!=', 2},['employee','employee_name','department','name','from_date','to_date','leave_type','workflow_status'])
    count3 = frappe.db.count('Permission Request',{'workflow_state':'Director Pending','docstatus':0})
    if count3 != 0:
        for leave in hr_app:
            idx = 1
            if leave.workflow_state == 'Director Pending':
                # idx = 1
                staff_director += """
                    <tr style="border: 1px solid black;">
                        <td style="padding: 4px; border: 1px solid black;">{0}</td>
                        <td style="padding: 4px; border: 1px solid black;">{1}</td>
                        <td style="padding: 4px; border: 1px solid black;">{2}</td>
                        <td style="padding: 4px; border: 1px solid black;">{3}</td>
                        <td style="padding: 4px; border: 1px solid black;">{4}</td>
                        <td style="padding: 4px; border: 1px solid black;">{5}</td>
                        <td style="padding: 4px; border: 1px solid black;">{6}</td>
                        <td style="padding: 4px; border: 1px solid black;">{7}</td>
                    </tr>
                """.format(idx, leave.employee_id, leave.employee_name, leave.department, leave.name or ' ',
                        format_date(leave.attendance_date), leave.session, leave.permission_hour or '')
                idx += 1

        frappe.sendmail(
            # recipients=['jothi.m@groupteampro.com'],
            recipients=['suzuki-syu@johoku-kigyo.co.jp'],
            subject='Permission Request Report - Director Pending',
            message="""Dear Sir,<br><br>
                    Kindly Find the list ofPermission Request waiting for your Approval:<br>{0}
                    """.format(staff_director)
        )
    hr_app = frappe.get_all(
        "Permission Request",
        filters={'docstatus': ['!=', 2]},
        fields=['employee_id', 'employee_name', 'department', 'name', 'permission_date', 'session', 'permission_hour', 'workflow_state']
    )

    count5 = frappe.db.count('Permission Request', {'workflow_state': 'HOD Pending', 'docstatus': 0})
    hod_list_1, hod_list_2, hod_list_3, hod_list_4 = "", "", "", ""
    idx = 1
    if count5 != 0:
        for leave in hr_app:
            if leave.workflow_state == 'HOD Pending':
                row = """
                    <tr style="border: 1px solid black;">
                        <td style="padding: 4px; border: 1px solid black;">{0}</td>
                        <td style="padding: 4px; border: 1px solid black;">{1}</td>
                        <td style="padding: 4px; border: 1px solid black;">{2}</td>
                        <td style="padding: 4px; border: 1px solid black;">{3}</td>
                        <td style="padding: 4px; border: 1px solid black;">{4}</td>
                        <td style="padding: 4px; border: 1px solid black;">{5}</td>
                        <td style="padding: 4px; border: 1px solid black;">{6}</td>
                        <td style="padding: 4px; border: 1px solid black;">{7}</td>
                    </tr>
                """.format(idx, leave.employee_id, leave.employee_name, leave.department, leave.name or ' ',
                        format_date(leave.attendance_date), leave.session, leave.permission_hour or '')

                if leave.department in ['PPC - JMPL', 'Purchase - JMPL', 'Sales - JMPL']:
                    hod_list_1 += row
                elif leave.department in ['Finance - JMPL', 'HR and GA - JMPL']:
                    hod_list_2 += row
                elif leave.department in ['Technical - JMPL', 'QUALITY - JMPL']:
                    hod_list_3 += row
                # elif leave.department in ['Stores - JMPL', 'Dispatch - JMPL', 'Assembly Shop - JMPL', 'Machine Shop - JMPL', 'MAINTENANCE - JMPL', 'Utility - JMPL']:
                else:
                    hod_list_4 += row
                idx += 1
        multiple_hod_list = [hod_list_1, hod_list_2, hod_list_3, hod_list_4]
        for l in multiple_hod_list:
            if l:
                if l == hod_list_1:
                    frappe.sendmail(
                    # recipients=['jothi.m@groupteampro.com'],
                    recipients=['karthick.m@johoku.co.in'],
                    subject='Permission Request Report - HOD Pending',
                    message="""Dear Sir,<br><br>
                            Kindly Find the list of Permission Requests waiting for your Approval:<br>{0}{1}""".format(staff_hod,l)
                )
                if l == hod_list_2:
                    frappe.sendmail(
                        recipients=['ramesh.b@johoku.co.in'],
                    # recipients=['jothi.m@groupteampro.com'],
                    subject='Permission Request Report - HOD Pending',
                    message="""Dear Sir,<br><br>
                            Kindly Find the list of Permission Requests waiting for your Approval:<br>{0}{1}""".format(staff_hod,l)
                )
                if l == hod_list_3:
                    frappe.sendmail(
                        recipients=['arunkumar.k@johoku.co.in'],
                        # recipients=['jothi.m@groupteampro.com'],
                        subject='Permission Request Report - HOD Pending',
                        message="""Dear Sir,<br><br>
                            Kindly Find the list of Permission Requests waiting for your Approval:<br>{0}{1}""".format(staff_hod,l)
                )
                if l == hod_list_4:
                    frappe.sendmail(
                        recipients =['balaji.r@johoku.co.in'],
                    # recipients=['jothi.m@groupteampro.com'],
                        subject='Permission Request Report - HOD Pending',
                        message="""Dear Sir,<br><br>
                            Kindly Find the list of Permission Requests waiting for your Approval:<br>{0}{1}""".format(staff_hod,l)
                )
        
        
@frappe.whitelist()
#sends notification to each level of approvers of each level approval Overtime request documents.
def overtime_request_notify():
    staff = """
        <div style="text-align: center;">
            <h2 style="font-size: 16px;"Overtime Request Report</h2>
        </div>
        <table style="border-collapse: collapse; width: 100%; border: 1px solid black; font-size: 10px;">
            <tr style="border: 1px solid black;">
                <th style="padding: 4px; border: 1px solid black;">S.No</th>
                <th style="padding: 4px; border: 1px solid black;">Employee</th>
                <th style="padding: 4px; border: 1px solid black;">Employee Name</th>
                <th style="padding: 4px; border: 1px solid black;">Department</th>
                <th style="padding: 4px; border: 1px solid black;">Document ID</th>
                <th style="padding: 4px; border: 1px solid black;">OT Date</th>
                <th style="padding: 4px; border: 1px solid black;">From Time</th>
                <th style="padding: 4px; border: 1px solid black;">To Time</th>
                <th style="padding: 4px; border: 1px solid black;">Overtime Hours</th>
            </tr>
    """
    staff_hod = staff
    staff_md = staff
    staff_department = staff
    staff_director = staff


    hr = frappe.db.sql_list(
                """select distinct hr_approval from `tabEmployee`
                where status = 'Active' """,
            )
    
    count = frappe.db.count('Overtime Request',{'workflow_state':'HR Pending','docstatus':0})
    email_addresses = []
    if count != 0:
        for i in hr:
            hr_approver = frappe.get_all("Employee",{'status':'Active','hr_approval':i},['name'])
            if i :
                email_addresses += [i]
            for j in hr_approver:
                hr_app = frappe.get_all("Overtime Request",{'employee':j.name},['employee','employee_name','department','name','ot_date','from_time','to_time','workflow_state','ot_hours'])
                for leave in hr_app:
                    idx = 1
                    if leave.workflow_state == 'HR Pending':
                        
                        if leave:
                            staff += """
                                <tr style="border: 1px solid black;">
                                    <td style="padding: 4px; border: 1px solid black;">{0}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{1}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{2}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{3}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{4}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{5}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{6}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{7}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{9}</td>
                                </tr>
                            """.format(idx, leave.employee_id, leave.employee_name, leave.department, leave.name or ' ',
                        format_date(leave.ot_date), leave.from_time, leave.to_time or '')
                            idx += 1
        if email_addresses:
            frappe.sendmail(
                # recipients=['jothi.m@groupteampro.com'],
                recipients = email_addresses,
                subject='Overtime Request Report - HR Pending',
                message="""Dear Sir,<br><br>
                        Kindly Find the list of Overtime Request waiting for your Approval:<br>{0}
                        """.format(staff)
            )
        if email_addresses:
                del email_addresses[0]
            
    hr = frappe.db.sql_list(
                """select distinct department_approval from `tabEmployee`
                where status = 'Active' """,
            )
    count1 = frappe.db.count('Overtime Request',{'workflow_state':'Department Pending','docstatus':0})
    email_addresses_dept = []
    department_mail = []
    if count1 != 0:
        
        for i in hr:
            hr_approver = frappe.get_all("Employee",{'status':'Active','department_approval':i},['name'])
            if i :
                email_addresses_dept += [i]
            for j in hr_approver:
                hr_app = frappe.get_all(
                    "Overtime Request",
                    filters={'employee':j.name,'docstatus': ['!=', 2]},
                    fields=['employee', 'employee_name', 'department', 'name', 'ot_date', 'from_time', 'to_time', 'workflow_state','ot_hours']
                )
                # hr_app = frappe.get_all("Overtime Request",{'employee':j.name},['employee','employee_name','department','name','from_date','to_date','leave_type','workflow_state'])
                for leave in hr_app:
                    idx = 1
                    if leave.workflow_state == 'Department Pending':
                        # idx = 1
                        if leave:
                            department_mail += [idx] 
                            staff_department += """
                                <tr style="border: 1px solid black;">
                                    <td style="padding: 4px; border: 1px solid black;">{0}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{1}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{2}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{3}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{4}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{5}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{6}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{7}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{9}</td>
                                </tr>
                            """.format(idx, leave.employee, leave.employee_name, leave.department, leave.name or ' ',
                                format_date(leave.ot_date), leave.from_time, leave.to_time or '')
                            idx += 1
            if email_addresses_dept and len(department_mail) != 0:
                frappe.sendmail(
                        # recipients=['jothi.m@groupteampro.com'],
                        recipients=email_addresses_dept,
                        subject='Overtime Request Report - Department Pending',
                        message="""Dear Sir,<br><br>
                                Kindly Find the list of Overtime Request waiting for your Approval:<br>{0}
                                """.format(staff_department)
                    )
            if email_addresses_dept:
                del email_addresses_dept[0]
            if department_mail:
                del department_mail[0]
    hr = frappe.db.sql_list(
                """select distinct md_approval from `tabEmployee`
                where status = 'Active' """,
            )
    count2 = frappe.db.count('Overtime Request',{'workflow_state':'MD Pending','docstatus':0})
    if count2 != 0:
        for i in hr:
            if i:
                email_addresses_md += [i]
                hr_approver = frappe.get_all("Employee",{'status':'Active','md_approval':i},['name'])
                for j in hr_approver:
                #     hr_app = frappe.get_all(Permission Request",{'employee':j.name},['employee','employee_name','department','name','from_date','to_date','leave_type','workflow_state'])
                    hr_app = frappe.get_all(
                        "Overtime Request",
                        filters={'employee':j.name,'docstatus': ['!=', 2]},
                        fields=['employee', 'employee_name', 'department', 'name', 'ot_date', 'from_time', 'to_time', 'workflow_state','ot_hours']
                    )
                    for leave in hr_app:
                        idx = 1
                        if leave.workflow_state == 'MD Pending':
                            
                            staff_md += """
                                <tr style="border: 1px solid black;">
                                    <td style="padding: 4px; border: 1px solid black;">{0}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{1}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{2}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{3}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{4}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{5}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{6}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{7}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{9}</td>
                                </tr>
                            """.format(idx, leave.employee, leave.employee_name, leave.department, leave.name or ' ',
                                    format_date(leave.ot_date), leave.from_time, leave.to_time or '')
                            idx += 1
        if email_addresses_md:
            frappe.sendmail(
                recipients =email_addresses_md,
                # recipients=['jothi.m@groupteampro.com'],
                subject='Overtime Request Report',
                message="""Dear Sir,<br><br>
                        Kindly Find the list of Overtime Request waiting for your Approval:<br>{0}
                        """.format(staff_md)
            )
            del email_addresses_md[0]

    hr_app = frappe.get_all("Overtime Request",
                        filters={'docstatus': ['!=', 2]},
                        fields=['employee', 'employee_name', 'department', 'name', 'ot_date', 'from_time', 'to_time', 'workflow_state','ot_hours'])

    # hr_app = frappe.get_all("Overtime Request",{'docstatus', '!=', 2},['employee','employee_name','department','name','from_date','to_date','leave_type','workflow_status'])
    count3 = frappe.db.count('Overtime Request',{'workflow_state':'Director Pending','docstatus':0})
    if count3 != 0:
        for leave in hr_app:
            idx = 1
            if leave.workflow_state == 'Director Pending':
                # idx = 1
                staff_director += """
                    <tr style="border: 1px solid black;">
                        <td style="padding: 4px; border: 1px solid black;">{0}</td>
                        <td style="padding: 4px; border: 1px solid black;">{1}</td>
                        <td style="padding: 4px; border: 1px solid black;">{2}</td>
                        <td style="padding: 4px; border: 1px solid black;">{3}</td>
                        <td style="padding: 4px; border: 1px solid black;">{4}</td>
                        <td style="padding: 4px; border: 1px solid black;">{5}</td>
                        <td style="padding: 4px; border: 1px solid black;">{6}</td>
                        <td style="padding: 4px; border: 1px solid black;">{7}</td>
                        <td style="padding: 4px; border: 1px solid black;">{9}</td>
                    </tr>
               """.format(idx, leave.employee, leave.employee_name, leave.department, leave.name or ' ',
                        format_date(leave.ot_date), leave.from_time, leave.to_time or '')
                idx += 1

        frappe.sendmail(
            # recipients=['jothi.m@groupteampro.com'],
            recipients=['suzuki-syu@johoku-kigyo.co.jp'],
            subject='Overtime Request Report',
            message="""Dear Sir,<br><br>
                    Kindly Find the list of Overtime Request waiting for your Approval:<br>{0}
                    """.format(staff_director)
        )
    hr_app = frappe.get_all(
        "Overtime Request",
        filters={'docstatus': ['!=', 2]},
        fields=['employee', 'employee_name', 'department', 'name', 'ot_date', 'from_time', 'to_time', 'workflow_state','ot_hours']
    )

    count5 = frappe.db.count('Overtime Request', {'workflow_state': 'HOD Pending', 'docstatus': 0})
    hod_list_1, hod_list_2, hod_list_3, hod_list_4 = "", "", "", ""
    idx = 1
    if count5 != 0:
        for leave in hr_app:
            if leave.workflow_state == 'HOD Pending':
                row = """
                    <tr style="border: 1px solid black;">
                        <td style="padding: 4px; border: 1px solid black;">{0}</td>
                        <td style="padding: 4px; border: 1px solid black;">{1}</td>
                        <td style="padding: 4px; border: 1px solid black;">{2}</td>
                        <td style="padding: 4px; border: 1px solid black;">{3}</td>
                        <td style="padding: 4px; border: 1px solid black;">{4}</td>
                        <td style="padding: 4px; border: 1px solid black;">{5}</td>
                        <td style="padding: 4px; border: 1px solid black;">{6}</td>
                        <td style="padding: 4px; border: 1px solid black;">{7}</td>
                        <td style="padding: 4px; border: 1px solid black;">{9}</td>
                    </tr>
                """.format(idx, leave.employee, leave.employee_name, leave.department, leave.name or ' ',
                        format_date(leave.ot_date), leave.from_time, leave.to_time or '')
                if leave.department in ['PPC - JMPL', 'Purchase - JMPL', 'Sales - JMPL']:
                    hod_list_1 += row
                elif leave.department in ['Finance - JMPL', 'HR and GA - JMPL']:
                    hod_list_2 += row
                elif leave.department in ['Technical - JMPL', 'QUALITY - JMPL']:
                    hod_list_3 += row
                # elif leave.department in ['Stores - JMPL', 'Dispatch - JMPL', 'Assembly Shop - JMPL', 'Machine Shop - JMPL', 'MAINTENANCE - JMPL', 'Utility - JMPL']:
                else:
                    hod_list_4 += row
                idx += 1
        multiple_hod_list = [hod_list_1, hod_list_2, hod_list_3, hod_list_4]
        for l in multiple_hod_list:
            if l: 
                if l == hod_list_1:
                    frappe.sendmail(
                    # recipients=['jothi.m@groupteampro.com'],
                    recipients=['karthick.m@johoku.co.in'],
                    subject='Overtime Request Report - HOD Pending',
                    message="""Dear Sir,<br><br>
                            Kindly Find the list of Overtime Requests waiting for your Approval:<br>{0}{1}""".format(staff_hod,l)
                )
                if l == hod_list_2:
                    frappe.sendmail(
                        recipients=['ramesh.b@johoku.co.in'],
                    # recipients=['jothi.m@groupteampro.com'],
                    subject='Overtime Request Report - HOD Pending',
                    message="""Dear Sir,<br><br>
                            Kindly Find the list of Overtime Requests waiting for your Approval:<br>{0}{1}""".format(staff_hod,l)
                )
                if l == hod_list_3:
                    frappe.sendmail(
                        recipients=['arunkumar.k@johoku.co.in'],
                        # recipients=['jothi.m@groupteampro.com'],
                        subject='Overtime Request Report - HOD Pending',
                        message="""Dear Sir,<br><br>
                            Kindly Find the list of Overtime Requests waiting for your Approval:<br>{0}{1}""".format(staff_hod,l)
                )
                if l == hod_list_4:
                    frappe.sendmail(
                        recipients =['balaji.r@johoku.co.in'],
                    # recipients=['jothi.m@groupteampro.com'],
                        subject='Overtime Request Report - HOD Pending',
                        message="""Dear Sir,<br><br>
                            Kindly Find the list of Overtime Requests waiting for your Approval:<br>{0}{1}""".format(staff_hod,l)
                )
        

@frappe.whitelist()
#sends notification to each level of approvers of each level approval on duty documents.
def on_duty_application_notify():
    staff = """
        <div style="text-align: center;">
            <h2 style="font-size: 16px;"On Duty Application Report</h2>
        </div>
        <table style="border-collapse: collapse; width: 100%; border: 1px solid black; font-size: 10px;">
            <tr style="border: 1px solid black;">
                <th style="padding: 4px; border: 1px solid black;">S.No</th>
                <th style="padding: 4px; border: 1px solid black;">Employee</th>
                <th style="padding: 4px; border: 1px solid black;">Employee Name</th>
                <th style="padding: 4px; border: 1px solid black;">Department</th>
                <th style="padding: 4px; border: 1px solid black;">Document ID</th>
                <th style="padding: 4px; border: 1px solid black;">On Duty Date</th>
                <th style="padding: 4px; border: 1px solid black;">From Time</th>
                <th style="padding: 4px; border: 1px solid black;">To Time</th>
            </tr>
    """
    staff_hod = staff
    staff_md = staff
    staff_department = staff
    staff_director = staff


    hr = frappe.db.sql_list(
                """select distinct hr_approval from `tabEmployee`
                where status = 'Active' """,
            )
    
    email_addresses = []
    count = frappe.db.count('On Duty Application',{'workflow_state':'HR Pending','docstatus':0})
    if count != 0:
        for i in hr:
            hr_approver = frappe.get_all("Employee",{'status':'Active','hr_approval':i},['name'])
            email_addresses += [i]
            for j in hr_approver:
                hr_app = frappe.get_all("On Duty Application",{'employee':j.name},['employee','employee_name','department','name','od_date','from_time','to_time','workflow_state'])
                for leave in hr_app:
                    idx = 1
                    if leave.workflow_state == 'HR Pending':
                        if leave:
                            staff += """
                                <tr style="border: 1px solid black;">
                                    <td style="padding: 4px; border: 1px solid black;">{0}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{1}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{2}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{3}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{4}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{5}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{6}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{7}</td>
                                </tr>
                            """.format(idx, leave.employee_id, leave.employee_name or '', leave.department, leave.name or ' ',
                        format_date(leave.od_date), leave.from_time, leave.to_time)
                            idx += 1
            if email_addresses:
                frappe.sendmail(
                    # recipients=['jothi.m@groupteampro.com'],
                    recipients = email_addresses,
                    subject='On Duty Applicationt Report - HR Pending',
                    message="""Dear Sir,<br><br>
                            Kindly Find the list of On Duty Application waiting for your Approval:<br>{0}
                            """.format(staff)
                )
            if email_addresses:
                del email_addresses[0]
            
            
    hr = frappe.db.sql_list(
                """select distinct department_approval from `tabEmployee`
                where status = 'Active' """,
            )
    count1 = frappe.db.count('On Duty Application',{'workflow_state':'Department Pending','docstatus':0})
    email_addresses_dept = []
    department_mail = []

    if count1 != 0:
        for i in hr:
            hr_approver = frappe.get_all("Employee",{'status':'Active','department_approval':i},['name'])
            email_addresses_dept+= [i]
            for j in hr_approver:
                # email_addresses_dept+= [i]
                # hr_app = frappe.get_all(On Duty Application",{'employee':j.name},['employee','employee_name','department','name','from_date','to_date','leave_type','workflow_state'])
                hr_app = frappe.get_all(
                    "On Duty Application",
                    filters={'employee':j.name,'docstatus': ['!=', 2]},
                    fields=['employee', 'employee_name', 'department', 'name', 'od_date', 'from_time', 'to_time', 'workflow_state']
                )
                for leave in hr_app:
                    idx = 1
                    if leave.workflow_state == 'Department Pending':
                        # idx = 1
                        if leave:
                            department_mail += [idx] 
                            staff_department += """
                                <tr style="border: 1px solid black;">
                                    <td style="padding: 4px; border: 1px solid black;">{0}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{1}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{2}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{3}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{4}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{5}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{6}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{7}</td>
                                </tr>
                            """.format(idx, leave.employee, leave.employee_name or '', leave.department, leave.name or ' ',
                                format_date(leave.od_date), leave.from_time, leave.to_time)
                            idx += 1
            if email_addresses_dept and len(department_mail) != 0:
                frappe.sendmail(
                    recipients = email_addresses_dept,
                    # recipients=['jothi.m@groupteampro.com'],
                    subject='On Duty Application Report - Department Pending',
                    message="""Dear Sir,<br><br>
                            Kindly Find the list of On Duty Application waiting for your Approval:<br>{0}
                            """.format(staff_department)
                )
            if email_addresses_dept:
                del email_addresses_dept[0]

            if department_mail:
                del department_mail[0]

    hr = frappe.db.sql_list(
                """select distinct md_approval from `tabEmployee`
                where status = 'Active' """,
            )
    count2 = frappe.db.count('On Duty Application',{'workflow_state':'MD Pending','docstatus':0})
    email_addresses_md =[]
    if count2 != 0:
        for i in hr:
            if i:
                hr_approver = frappe.get_all("Employee",{'status':'Active','md_approval':i},['name'])
                for j in hr_approver:
                    email_addresses_md += [i]
                #     hr_app = frappe.get_all(Permission Request",{'employee':j.name},['employee','employee_name','department','name','from_date','to_date','leave_type','workflow_state'])
                    hr_app = frappe.get_all(
                    "On Duty Application",
                    filters={'employee':j.name,'docstatus': ['!=', 2]},
                    fields=['employee', 'employee_name', 'department', 'name', 'od_date', 'from_time', 'to_time', 'workflow_state']
                )
                    for leave in hr_app:
                        idx = 1
                        if leave.workflow_state == 'MD Pending':
                            
                            staff_md += """
                                <tr style="border: 1px solid black;">
                                    <td style="padding: 4px; border: 1px solid black;">{0}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{1}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{2}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{3}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{4}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{5}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{6}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{7}</td>
                                </tr>
                            """.format(idx, leave.employee, leave.employee_name, leave.department, leave.name or ' ',
                                    format_date(leave.od_date), leave.from_time, leave.to_time or '')
                            idx += 1

        if email_addresses_md:
            frappe.sendmail(
                # recipients=['jothi.m@groupteampro.com'],
                recipients = email_addresses_md,
                subject='On Duty Application Report',
                message="""Dear Sir,<br><br>
                        Kindly Find the list of On Duty Application waiting for your Approval:<br>{0}
                        """.format(staff_md)
            )
            del email_addresses_md[0]

    hr_app = frappe.get_all("On Duty Application",
                        filters={'docstatus': ['!=', 2]},
                        fields=['employee', 'employee_name', 'department', 'name', 'od_date', 'from_time', 'to_time', 'workflow_state'])

    # hr_app = frappe.get_all("On Duty Application",{'docstatus', '!=', 2},['employee','employee_name','department','name','from_date','to_date','leave_type','workflow_status'])
    count3 = frappe.db.count('On Duty Application',{'workflow_state':'Director Pending','docstatus':0})
    if count3 != 0:
        for leave in hr_app:
            idx = 1
            if leave.workflow_state == 'Director Pending':
                # idx = 1
                staff_director += """
                    <tr style="border: 1px solid black;">
                        <td style="padding: 4px; border: 1px solid black;">{0}</td>
                        <td style="padding: 4px; border: 1px solid black;">{1}</td>
                        <td style="padding: 4px; border: 1px solid black;">{2}</td>
                        <td style="padding: 4px; border: 1px solid black;">{3}</td>
                        <td style="padding: 4px; border: 1px solid black;">{4}</td>
                        <td style="padding: 4px; border: 1px solid black;">{5}</td>
                        <td style="padding: 4px; border: 1px solid black;">{6}</td>
                        <td style="padding: 4px; border: 1px solid black;">{7}</td>
                    </tr>
               """.format(idx, leave.employee, leave.employee_name, leave.department, leave.name or ' ',
                        format_date(leave.od_date), leave.from_time, leave.to_time or '')
                idx += 1

        frappe.sendmail(
            # recipients=['jothi.m@groupteampro.com'],
            recipients=['suzuki-syu@johoku-kigyo.co.jp'],
            subject='On Duty Application Report',
            message="""Dear Sir,<br><br>
                    Kindly Find the list of On Duty Application waiting for your Approval:<br>{0}
                    """.format(staff_director)
        )
    hr_app = frappe.get_all(
        "On Duty Application",
        filters={'docstatus': ['!=', 2]},
        fields=['employee', 'employee_name', 'department', 'name', 'od_date', 'from_time', 'to_time', 'workflow_state']
    )

    count5 = frappe.db.count('On Duty Application', {'workflow_state': 'HOD Pending', 'docstatus': 0})
    hod_list_1, hod_list_2, hod_list_3, hod_list_4 = "", "", "", ""
    idx = 1
    if count5 != 0:
        for leave in hr_app:
            if leave.workflow_state == 'HOD Pending':
                row = """
                    <tr style="border: 1px solid black;">
                        <td style="padding: 4px; border: 1px solid black;">{0}</td>
                        <td style="padding: 4px; border: 1px solid black;">{1}</td>
                        <td style="padding: 4px; border: 1px solid black;">{2}</td>
                        <td style="padding: 4px; border: 1px solid black;">{3}</td>
                        <td style="padding: 4px; border: 1px solid black;">{4}</td>
                        <td style="padding: 4px; border: 1px solid black;">{5}</td>
                        <td style="padding: 4px; border: 1px solid black;">{6}</td>
                        <td style="padding: 4px; border: 1px solid black;">{7}</td>
                    </tr>
                """.format(idx, leave.employee, leave.employee_name, leave.department, leave.name or ' ',
                        format_date(leave.od_date), leave.from_time, leave.to_time or '')
                if leave.department in ['PPC - JMPL', 'Purchase - JMPL', 'Sales - JMPL']:
                    hod_list_1 += row
                elif leave.department in ['Finance - JMPL', 'HR and GA - JMPL']:
                    hod_list_2 += row
                elif leave.department in ['Technical - JMPL', 'QUALITY - JMPL']:
                    hod_list_3 += row
                # elif leave.department in ['Stores - JMPL', 'Dispatch - JMPL', 'Assembly Shop - JMPL', 'Machine Shop - JMPL', 'MAINTENANCE - JMPL', 'Utility - JMPL']:
                else:
                    hod_list_4 += row
                idx += 1
        multiple_hod_list = [hod_list_1, hod_list_2, hod_list_3, hod_list_4]
        for l in multiple_hod_list:
            if l: 
                if l == hod_list_1:
                    frappe.sendmail(
                    # recipients=['jothi.m@groupteampro.com'],
                    recipients=['karthick.m@johoku.co.in'],
                    subject='On Duty Application Report - HOD Pending',
                    message="""Dear Sir,<br><br>
                            Kindly Find the list of On Duty Applications waiting for your Approval:<br>{0}{1}""".format(staff_hod,l)
                )
                if l == hod_list_2:
                    frappe.sendmail(
                        recipients=['ramesh.b@johoku.co.in'],
                    # recipients=['jothi.m@groupteampro.com'],
                    subject='On Duty Application Report - HOD Pending',
                    message="""Dear Sir,<br><br>
                            Kindly Find the list of On Duty Applications waiting for your Approval:<br>{0}{1}""".format(staff_hod,l)
                )
                if l == hod_list_3:
                    frappe.sendmail(
                        recipients=['arunkumar.k@johoku.co.in'],
                        # recipients=['jothi.m@groupteampro.com'],
                        subject='On Duty Application Report - HOD Pending',
                        message="""Dear Sir,<br><br>
                            Kindly Find the list of On Duty Applications waiting for your Approval:<br>{0}{1}""".format(staff_hod,l)
                )
                if l == hod_list_4:
                    frappe.sendmail(
                        recipients =['balaji.r@johoku.co.in'],
                    # recipients=['jothi.m@groupteampro.com'],
                        subject='On Duty Application Report - HOD Pending',
                        message="""Dear Sir,<br><br>
                            Kindly Find the list of On Duty Applications waiting for your Approval:<br>{0}{1}""".format(staff_hod,l)
                )


@frappe.whitelist()
#sends notification to each level of approvers of each level approval c-off documents.
def compensatory_application_notify():
    staff = """
        <div style="text-align: center;">
            <h2 style="font-size: 16px;">Compensatory Leave Request Report</h2>
        </div>
        <table style="border-collapse: collapse; width: 100%; border: 1px solid black; font-size: 10px;">
            <tr style="border: 1px solid black;">
                <th style="padding: 4px; border: 1px solid black;">S.No</th>
                <th style="padding: 4px; border: 1px solid black;">Employee</th>
                <th style="padding: 4px; border: 1px solid black;">Employee Name</th>
                <th style="padding: 4px; border: 1px solid black;">Department</th>
                <th style="padding: 4px; border: 1px solid black;">Document ID</th>
                <th style="padding: 4px; border: 1px solid black;">From date</th>
                <th style="padding: 4px; border: 1px solid black;">To Date</th>
                <th style="padding: 4px; border: 1px solid black;">Leave Type</th>
            </tr>
    """
    staff_hod = staff
    staff_md = staff
    staff_department = staff
    staff_director = staff


    hr = frappe.db.sql_list(
                """select distinct hr_approval from `tabEmployee`
                where status = 'Active' """,
            )
    
    count = frappe.db.count('Compensatory Leave Request',{'workflow_state':'HR Pending','docstatus':0})
    email_addresses = []
    if count != 0:
        for i in hr:
            hr_approver = frappe.get_all("Employee",{'status':'Active','hr_approval':i},['name'])
            email_addresses += [i]
            for j in hr_approver:
                hr_app = frappe.get_all("Compensatory Leave Request",{'employee':j.name},['employee','employee_name','department','name','work_from_date','work_end_date','leave_type','workflow_state'])
                for leave in hr_app:
                    idx = 1
                    if leave.workflow_state == 'HR Pending':
                        
                        if leave:
                            staff += """
                                <tr style="border: 1px solid black;">
                                    <td style="padding: 4px; border: 1px solid black;">{0}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{1}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{2}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{3}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{4}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{5}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{6}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{7}</td>
                                </tr>
                hr_app = frappe.get_all("Compensatory Leave Request",{'employee':j.name},['employee','employee_name','department','name','work_from_date','work_end_date','leave_type','workflow_state'])
                            """.format(idx, leave.employee, leave.employee_name, leave.department, leave.name or ' ',format_date(leave.work_from_date),format_date(leave.work_end_date), leave.leave_type or '')
                            idx += 1
            if email_addresses:
                frappe.sendmail(
                    recipients =email_addresses,
                    # recipients=['jothi.m@groupteampro.com'],
                    subject='Compensatory Leave Request Report - HR Pending',
                    message="""Dear Sir,<br><br>
                            Kindly Find the list of Compensatory Leave Request waiting for your Approval:<br>{0}
                            """.format(staff)
                )
            if email_addresses:
                del email_addresses[0]
            
    hr = frappe.db.sql_list(
                """select distinct department_approval from `tabEmployee`
                where status = 'Active' """,
            )
    count1 = frappe.db.count('Compensatory Leave Request',{'workflow_state':'Department Pending','docstatus':0})
    email_addresses_dept =[]
    if count1 != 0:
        for i in hr:
            hr_approver = frappe.get_all("Employee",{'status':'Active','department_approval':i},['name'])
            for j in hr_approver:
                # hr_app = frappe.get_all("Compensatory Leave Request",{'employee':j.name},['employee','employee_name','department','name','from_date','to_date','leave_type','workflow_state'])
                hr_app = frappe.get_all(
                    "Compensatory Leave Request",
                    filters={'employee':j.name,'docstatus': ['!=', 2]},
                    fields=['employee', 'employee_name', 'department', 'name', 'work_from_date', 'work_end_date', 'leave_type', 'workflow_state']
                )
                for leave in hr_app:
                    idx = 1
                    if leave.workflow_state == 'Department Pending':
                        # idx = 1
                        if leave:
                            staff_department += """
                                <tr style="border: 1px solid black;">
                                    <td style="padding: 4px; border: 1px solid black;">{0}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{1}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{2}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{3}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{4}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{5}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{6}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{7}</td>
                                </tr>
                        hr_app = frappe.get_all("Compensatory Leave Request",{'employee':j.name},['employee','employee_name','department','name','work_from_date','work_end_date','leave_type','workflow_state'])
                            """.format(idx, leave.employee, leave.employee_name, leave.department, leave.name or ' ',format_date(leave.work_from_date),format_date(leave.work_end_date), leave.leave_type or '')
                            idx += 1
            if email_addresses_dept:
                frappe.sendmail(
                        # recipients=['jothi.m@groupteampro.com'],
                        recipients = email_addresses_dept,
                        subject='Compensatory Leave Request Report - Department Pending',
                        message="""Dear Sir,<br><br>
                                Kindly Find the list of Compensatory Leave Request waiting for your Approval:<br>{0}
                                """.format(staff_department)
                    )
            if email_addresses_dept:
                del email_addresses_dept[0]
    hr = frappe.db.sql_list(
                """select distinct md_approval from `tabEmployee`
                where status = 'Active' """,
            )
    count2 = frappe.db.count('Compensatory Leave Request',{'workflow_state':'MD Pending','docstatus':0})
    email_addresses_md =[]
    if count2 != 0:
        for i in hr:
            if i:
                email_addresses_md += [i]
                hr_approver = frappe.get_all("Employee",{'status':'Active','md_approval':i},['name'])
                for j in hr_approver:
                    # hr_app = frappe.get_all("Compensatory Leave Request",{'employee':j.name},['employee','employee_name','department','name','from_date','to_date','leave_type','workflow_state'])
                    hr_app = frappe.get_all(
                        "Compensatory Leave Request",
                        filters={'employee':j.name,'docstatus': ['!=', 2]},
                        fields=['employee', 'employee_name', 'department', 'name', 'work_from_date', 'work_end_date', 'leave_type', 'workflow_state']
                    )
                    for leave in hr_app:
                        idx = 1
                        if leave.workflow_state == 'MD Pending':
                            staff_md += """
                                <tr style="border: 1px solid black;">
                                    <td style="padding: 4px; border: 1px solid black;">{0}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{1}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{2}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{3}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{4}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{5}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{6}</td>
                                    <td style="padding: 4px; border: 1px solid black;">{7}</td>
                                </tr>
                            hr_app = frappe.get_all("Compensatory Leave Request",{'employee':j.name},['employee','employee_name','department','name','work_from_date','work_end_date','leave_type','workflow_state'])
                            """.format(idx, leave.employee, leave.employee_name, leave.department, leave.name or ' ',format_date(leave.work_from_date),format_date(leave.work_end_date), leave.leave_type or '')
                            idx += 1
        if email_addresses_md:
            frappe.sendmail(
                    # recipients=['jothi.m@groupteampro.com'],
                    recipients =email_addresses_md,
                    subject='Compensatory Leave Request Report',
                    message="""Dear Sir,<br><br>
                            Kindly Find the list of Compensatory Leave Request waiting for your Approval:<br>{0}
                            """.format(staff_md)
                )
        if email_addresses:
            del email_addresses_md[0]
    hr_app = frappe.get_all("Compensatory Leave Request",
                        filters={'docstatus': ['!=', 2]},
                        fields=['employee', 'employee_name', 'department', 'name', 'work_from_date', 'work_end_date', 'leave_type', 'workflow_state'])

    # hr_app = frappe.get_all("Compensatory Leave Request",{'docstatus', '!=', 2},['employee','employee_name','department','name','from_date','to_date','leave_type','workflow_status'])
    count3 = frappe.db.count('Compensatory Leave Request',{'workflow_state':'Director Pending','docstatus':0})
    if count3 != 0:
        for leave in hr_app:
            if leave.workflow_state == 'Director Pending':
                idx = 1
                staff_director += """
                    <tr style="border: 1px solid black;">
                        <td style="padding: 4px; border: 1px solid black;">{0}</td>
                        <td style="padding: 4px; border: 1px solid black;">{1}</td>
                        <td style="padding: 4px; border: 1px solid black;">{2}</td>
                        <td style="padding: 4px; border: 1px solid black;">{3}</td>
                        <td style="padding: 4px; border: 1px solid black;">{4}</td>
                        <td style="padding: 4px; border: 1px solid black;">{5}</td>
                        <td style="padding: 4px; border: 1px solid black;">{6}</td>
                        <td style="padding: 4px; border: 1px solid black;">{7}</td>
                    </tr>
                hr_app = frappe.get_all("Compensatory Leave Request",{'employee':j.name},['employee','employee_name','department','name','work_from_date','work_end_date','leave_type','workflow_state'])
                """.format(idx, leave.employee, leave.employee_name, leave.department, leave.name or ' ',format_date(leave.work_from_date),format_date(leave.work_end_date), leave.leave_type or '')
                idx += 1

        frappe.sendmail(
            # recipients=['jothi.m@groupteampro.com'],
            recipients =['suzuki-syu@johoku-kigyo.co.jp'],
            subject='Compensatory Leave Request Report',
            message="""Dear Sir,<br><br>
                    Kindly Find the list of Compensatory Leave Request waiting for your Approval:<br>{0}
                    """.format(staff_director)
        )
    hr_app = frappe.get_all(
        "Compensatory Leave Request",
        filters={'docstatus': ['!=', 2]},
        fields=['employee', 'employee_name', 'department', 'name', 'work_from_date', 'work_end_date', 'leave_type', 'workflow_state']
    )

    count5 = frappe.db.count('Compensatory Leave Request', {'workflow_state': 'HOD Pending', 'docstatus': 0})
    hod_list_1, hod_list_2, hod_list_3, hod_list_4 = "", "", "", ""
    idx = 1
    if count5 != 0:
        for leave in hr_app:
            if leave.workflow_state == 'HOD Pending':
                row = """
                    <tr style="border: 1px solid black;">
                        <td style="padding: 4px; border: 1px solid black;">{0}</td>
                        <td style="padding: 4px; border: 1px solid black;">{1}</td>
                        <td style="padding: 4px; border: 1px solid black;">{2}</td>
                        <td style="padding: 4px; border: 1px solid black;">{3}</td>
                        <td style="padding: 4px; border: 1px solid black;">{4}</td>
                        <td style="padding: 4px; border: 1px solid black;">{5}</td>
                        <td style="padding: 4px; border: 1px solid black;">{6}</td>
                        <td style="padding: 4px; border: 1px solid black;">{7}</td>
                    </tr>
                """.format(idx, leave.employee, leave.employee_name, leave.department, leave.name or ' ',
                        format_date(leave.work_from_date), format_date(leave.work_end_date), leave.leave_type or '')

                if leave.department in ['PPC - JMPL', 'Purchase - JMPL', 'Sales - JMPL']:
                    hod_list_1 += row
                elif leave.department in ['Finance - JMPL', 'HR and GA - JMPL']:
                    hod_list_2 += row
                elif leave.department in ['Technical - JMPL', 'QUALITY - JMPL']:
                    hod_list_3 += row
                else:
                # elif leave.department in ['Stores - JMPL', 'Dispatch - JMPL', 'Assembly Shop - JMPL', 'Machine Shop - JMPL', 'MAINTENANCE - JMPL', 'Utility - JMPL']:
                    hod_list_4 += row
                idx += 1
        multiple_hod_list = [hod_list_1, hod_list_2, hod_list_3, hod_list_4]
        for l in multiple_hod_list:
            if l: 
                frappe.sendmail(
                    recipients=['jothi.m@groupteampro.com'],
                    subject='Compensatory Leave Request Report',
                    message="""Dear Sir,<br><br>
                            Kindly Find the list of Compensatory Leave Requests waiting for your Approval:<br>{0}{1}""".format(staff_hod,l)
                )
                if l == hod_list_1:
                    frappe.sendmail(
                    # recipients=['jothi.m@groupteampro.com'],
                    recipients=['karthick.m@johoku.co.in'],
                    subject='Compensatory Leave Requests Report - HOD Pending',
                    message="""Dear Sir,<br><br>
                            Kindly Find the list of Compensatory Leave Requestss waiting for your Approval:<br>{0}{1}""".format(staff_hod,l)
                )
                if l == hod_list_2:
                    frappe.sendmail(
                        recipients=['ramesh.b@johoku.co.in'],
                    # recipients=['jothi.m@groupteampro.com'],
                    subject='Compensatory Leave Requests Report - HOD Pending',
                    message="""Dear Sir,<br><br>
                            Kindly Find the list of Compensatory Leave Requestss waiting for your Approval:<br>{0}{1}""".format(staff_hod,l)
                )
                if l == hod_list_3:
                    frappe.sendmail(
                        recipients=['arunkumar.k@johoku.co.in'],
                        # recipients=['jothi.m@groupteampro.com'],
                        subject='Compensatory Leave Requests Report - HOD Pending',
                        message="""Dear Sir,<br><br>
                            Kindly Find the list of Compensatory Leave Requestss waiting for your Approval:<br>{0}{1}""".format(staff_hod,l)
                )
                if l == hod_list_4:
                    frappe.sendmail(
                        recipients =['balaji.r@johoku.co.in'],
                    # recipients=['jothi.m@groupteampro.com'],
                        subject='Compensatory Leave Requests Report - HOD Pending',
                        message="""Dear Sir,<br><br>
                            Kindly Find the list of Compensatory Leave Requestss waiting for your Approval:<br>{0}{1}""".format(staff_hod,l)
                )
        
 
# @frappe.whitelist()
# def miss_punch_application_notify():
#     staff = """
#         <div style="text-align: center;">
#             <h2 style="font-size: 16px;">Miss Punch Application Report</h2>
#         </div>
#         <table style="border-collapse: collapse; width: 100%; border: 1px solid black; font-size: 10px;">
#             <tr style="border: 1px solid black;">
#                 <th style="padding: 4px; border: 1px solid black;">S.No</th>
#                 <th style="padding: 4px; border: 1px solid black;">Employee</th>
#                 <th style="padding: 4px; border: 1px solid black;">Date</th>
#                 <th style="padding: 4px; border: 1px solid black;">Department</th>
#                 <th style="padding: 4px; border: 1px solid black;">Document ID</th>
#                 <th style="padding: 4px; border: 1px solid black;">IN Time</th>
#                 <th style="padding: 4px; border: 1px solid black;">OUT Time</th>
#                 <th style="padding: 4px; border: 1px solid black;">Shift</th>
#             </tr>
#     """
#     hr = frappe.db.sql_list(
#                 """select distinct hr_approval from `tabEmployee`
#                 where status = 'Active' """,
#             )
#     count = frappe.db.count('Miss Punch Application', {'workflow_state': 'HR Pending','docstatus':0})
#     if count != 0:
#         for i in hr:
#             hr_approver = frappe.get_all("Employee",{'status':'Active','hr_approval':i},['name'])
#             for j in hr_approver:
#                 hr_app = frappe.get_all("Miss Punch Application",{'employee':j.name},['employee','date','department','name','in_tme','out_time','shift','workflow_state'])
#                 for leave in hr_app:
#                     if leave.workflow_state == 'HR Pending':
#                         idx = 1
#                         staff += """
#                             <tr style="border: 1px solid black;">
#                                 <td style="padding: 4px; border: 1px solid black;">{0}</td>
#                                 <td style="padding: 4px; border: 1px solid black;">{1}</td>
#                                 <td style="padding: 4px; border: 1px solid black;">{2}</td>
#                                 <td style="padding: 4px; border: 1px solid black;">{3}</td>
#                                 <td style="padding: 4px; border: 1px solid black;">{4}</td>
#                                 <td style="padding: 4px; border: 1px solid black;">{5}</td>
#                                 <td style="padding: 4px; border: 1px solid black;">{6}</td>
#                                 <td style="padding: 4px; border: 1px solid black;">{7}</td>
#                             </tr>
#                         """.format(idx, leave.employee, format_date(leave.date), leave.department, leave.name or ' ',leave.in_tme or ' ',leave.out_time or ' ', leave.shift_type or '')
#                         idx += 1

#         frappe.sendmail(
#                     recipients=['jothi.m@groupteampro.com'],
#                     subject='Miss Punch Application Report',
#                     message="""Dear Sir,<br><br>
#                             Kindly Find the list of Miss Punch Application waiting for your Approval:<br>{0}
#                             """.format(staff)
#                 )
    
#     hr = frappe.db.sql_list(
#                 """select distinct department_approval from `tabEmployee`
#                 where status = 'Active' """,
#             )
#     count1 = frappe.db.count('Miss Punch Application', {'workflow_state': 'Department Pending','docstatus':0})
#     if count1 != 0:
#         for i in hr:
#             hr_approver = frappe.get_all("Employee",{'status':'Active','department_approval':i},['name'])
#             for j in hr_approver:
#                 hr_app = frappe.get_all("Miss Punch Application",{'employee':j.name},['employee','date','department','name','in_tme','out_time','shift','workflow_state'])
#                 for leave in hr_app:
#                     if leave.workflow_state == 'Department Pending':
#                         idx = 1
#                         staff += """
#                             <tr style="border: 1px solid black;">
#                                 <td style="padding: 4px; border: 1px solid black;">{0}</td>
#                                 <td style="padding: 4px; border: 1px solid black;">{1}</td>
#                                 <td style="padding: 4px; border: 1px solid black;">{2}</td>
#                                 <td style="padding: 4px; border: 1px solid black;">{3}</td>
#                                 <td style="padding: 4px; border: 1px solid black;">{4}</td>
#                                 <td style="padding: 4px; border: 1px solid black;">{5}</td>
#                                 <td style="padding: 4px; border: 1px solid black;">{6}</td>
#                                 <td style="padding: 4px; border: 1px solid black;">{7}</td>
#                             </tr>
#                         """.format(idx, leave.employee, format_date(leave.date), leave.department, leave.name or ' ',leave.in_tme or ' ',leave.out_time or ' ', leave.shift_type or '')
#                         idx += 1

#         frappe.sendmail(
#                         recipients=['jothi.m@groupteampro.com'],
#                         subject='Miss Punch Application Report',
#                         message="""Dear Sir,<br><br>
#                                 Kindly Find the list of Miss Punch Application waiting for your Approval:<br>{0}
#                                 """.format(staff)
#                     )
#     hr = frappe.db.sql_list(
#                 """select distinct department_approval from `tabEmployee`
#                 where status = 'Active' """,
#             )
#     count2 = frappe.db.count('Miss Punch Application', {'workflow_state': 'Department Pending','docstatus':0})
#     if count2 != 0:
#         for i in hr:
#             hr_approver = frappe.get_all("Employee",{'status':'Active','department_approval':i},['name'])
#             for j in hr_approver:
#                 hr_app = frappe.get_all("Miss Punch Application",{'employee':j.name},['employee','date','department','name','in_tme','out_time','shift','workflow_state'])
#                 for leave in hr_app:
#                     if leave.workflow_state == 'Department Pending':
#                         idx = 1
#                         staff += """
#                                 <tr style="border: 1px solid black;">
#                                     <td style="padding: 4px; border: 1px solid black;">{0}</td>
#                                     <td style="padding: 4px; border: 1px solid black;">{1}</td>
#                                     <td style="padding: 4px; border: 1px solid black;">{2}</td>
#                                     <td style="padding: 4px; border: 1px solid black;">{3}</td>
#                                     <td style="padding: 4px; border: 1px solid black;">{4}</td>
#                                     <td style="padding: 4px; border: 1px solid black;">{5}</td>
#                                     <td style="padding: 4px; border: 1px solid black;">{6}</td>
#                                     <td style="padding: 4px; border: 1px solid black;">{7}</td>
#                                 </tr>
#                         """.format(idx, leave.employee, format_date(leave.date), leave.department, leave.name or ' ',leave.in_tme or ' ',leave.out_time or ' ', leave.shift_type or '')
#                         idx += 1

#         frappe.sendmail(
#                 recipients=['jothi.m@groupteampro.com'],
#                 subject='Miss Punch Application Report',
#                 message="""Dear Sir,<br><br>
#                         Kindly Find the list of Miss Punch Application waiting for your Approval:<br>{0}
#                         """.format(staff)
#             )
    
#     hr_app = frappe.get_all("Miss Punch Application",
#                         filters={'docstatus': ['!=', 2]},
#                         fields=['employee', 'date', 'department', 'name', 'in_time', 'out_time', 'shift', 'workflow_state'])
#     count3 = frappe.db.count('Miss Punch Application', {'workflow_state': 'Department Pending','docstatus':0})
#     if count3 != 0:
#         for leave in hr_app:
#             if leave.workflow_state == 'Department Pending':
#                 idx = 1
#                 staff += """
#                     <tr style="border: 1px solid black;">
#                         <td style="padding: 4px; border: 1px solid black;">{0}</td>
#                         <td style="padding: 4px; border: 1px solid black;">{1}</td>
#                         <td style="padding: 4px; border: 1px solid black;">{2}</td>
#                         <td style="padding: 4px; border: 1px solid black;">{3}</td>
#                         <td style="padding: 4px; border: 1px solid black;">{4}</td>
#                         <td style="padding: 4px; border: 1px solid black;">{5}</td>
#                         <td style="padding: 4px; border: 1px solid black;">{6}</td>
#                         <td style="padding: 4px; border: 1px solid black;">{7}</td>
#                     </tr>
#                         """.format(idx, leave.employee, format_date(leave.date), leave.department, leave.name or ' ',leave.in_tme or ' ',leave.out_time or ' ', leave.shift_type or '')
#                 idx += 1

#         frappe.sendmail(
#             recipients=['jothi.m@groupteampro.com'],
#             subject='Miss Punch Application Report',
#             message="""Dear Sir,<br><br>
#                     Kindly Find the list of Miss Punch Application waiting for your Approval:<br>{0}
#                     """.format(staff)
#         )
#     hr_app = frappe.get_all("Miss Punch Application",
#                         filters={'docstatus': ['!=', 2]},
#                         fields=['employee', 'date', 'department', 'name', 'in_time', 'out_time', 'shift', 'workflow_state'])

#     # id = 1
#     # hr_app = frappe.get_all("Leave Application",{'docstatus', '!=', 2},['employee','employee_name','department','name','from_date','to_date','leave_type','workflow_status'])
#     count4 = frappe.db.count('Miss Punch Application', {'workflow_state': 'MD Pending','docstatus':0})
#     if count4 != 0:
#         for leave in hr_app:
#             if leave.workflow_state == 'MD Pending':
#                 idx = 1
#                 staff += """
#                     <tr style="border: 1px solid black;">
#                         <td style="padding: 4px; border: 1px solid black;">{0}</td>
#                         <td style="padding: 4px; border: 1px solid black;">{1}</td>
#                         <td style="padding: 4px; border: 1px solid black;">{2}</td>
#                         <td style="padding: 4px; border: 1px solid black;">{3}</td>
#                         <td style="padding: 4px; border: 1px solid black;">{4}</td>
#                         <td style="padding: 4px; border: 1px solid black;">{5}</td>
#                         <td style="padding: 4px; border: 1px solid black;">{6}</td>
#                         <td style="padding: 4px; border: 1px solid black;">{7}</td>
#                     </tr>
#                         """.format(idx, leave.employee, format_date(leave.date), leave.department, leave.name or ' ',leave.in_tme or ' ',leave.out_time or ' ', leave.shift_type or '')
#                 idx += 1
#         # if id !=0:
#         frappe.sendmail(
#                     recipients=['jothi.m@groupteampro.com'],
#                     subject='Miss Punch Application Report',
#                     message="""Dear Sir,<br><br>
#                             Kindly Find the list of Miss Punch Application waiting for your Approval:<br>{0}
#                             """.format(staff)
#                 )
    
   

#     hr_app = frappe.get_all(
#     "Miss Punch Application",
#     filters={'docstatus': ['!=', 2]},  # Ensure that 2 correctly represents cancelled documents
#     fields=['employee', 'date', 'department', 'name', 'in_time', 'out_time', 'shift', 'workflow_state'])
#     count5 = frappe.db.count('Miss Punch Application', {'workflow_state': 'HOD Pending','docstatus':0})
#     if count5 != 0:
#         for leave in hr_app:
#             if leave.department == 'PPC - JMPL' or leave.department == 'Purchase - JMPL' or leave.department == 'Sales - JMPL':
#                 if leave.workflow_state == 'HOD Pending':
#                     idx = 1
#                     staff += """
#                         <tr style="border: 1px solid black;">
#                             <td style="padding: 4px; border: 1px solid black;">{0}</td>
#                             <td style="padding: 4px; border: 1px solid black;">{1}</td>
#                             <td style="padding: 4px; border: 1px solid black;">{2}</td>
#                             <td style="padding: 4px; border: 1px solid black;">{3}</td>
#                             <td style="padding: 4px; border: 1px solid black;">{4}</td>
#                             <td style="padding: 4px; border: 1px solid black;">{5}</td>
#                             <td style="padding: 4px; border: 1px solid black;">{6}</td>
#                             <td style="padding: 4px; border: 1px solid black;">{7}</td>
#                         </tr>
#                         """.format(idx, leave.employee, format_date(leave.date), leave.department, leave.name or ' ',leave.in_tme or ' ',leave.out_time or ' ', leave.shift_type or '')
#                     idx += 1

#         frappe.sendmail(
#                 recipients=['jothi.m@groupteampro.com'],
#                 subject='Miss Punch Application Report',
#                 message="""Dear Sir,<br><br>
#                         Kindly Find the list of Miss Punch Application waiting for your Approval:<br>{0}
#                         """.format(staff)
#             )
#     hr_app = frappe.get_all("Miss Punch Application",
#                         filters={'docstatus': ['!=', 2]},
#                         fields=['employee', 'date', 'department', 'name', 'in_time', 'out_time', 'shift', 'workflow_state'])
#     count6 = frappe.db.count('Miss Punch Application', {'workflow_state': 'HOD Pending','docstatus':0})
#     if count6 != 0:
#         for leave in hr_app:
#             if leave.department == 'Finance - JMPL' or leave.department == 'HR and GA - JMPL':
#                 if leave.workflow_state == 'HOD Pending':
#                     idx = 1
#                     staff += """
#                         <tr style="border: 1px solid black;">
#                             <td style="padding: 4px; border: 1px solid black;">{0}</td>
#                             <td style="padding: 4px; border: 1px solid black;">{1}</td>
#                             <td style="padding: 4px; border: 1px solid black;">{2}</td>
#                             <td style="padding: 4px; border: 1px solid black;">{3}</td>
#                             <td style="padding: 4px; border: 1px solid black;">{4}</td>
#                             <td style="padding: 4px; border: 1px solid black;">{5}</td>
#                             <td style="padding: 4px; border: 1px solid black;">{6}</td>
#                             <td style="padding: 4px; border: 1px solid black;">{7}</td>
#                         </tr>
#                         """.format(idx, leave.employee, format_date(leave.date), leave.department, leave.name or ' ',leave.in_tme or ' ',leave.out_time or ' ', leave.shift_type or '')
#                     idx += 1
#         frappe.sendmail(
#             recipients='jothi.m@groupteampro.com',
#             subject='Miss Punch Application Report',
#             message="""Dear Sir,<br><br>
#                     Kindly Find the list of Miss Punch Application waiting for your Approval:<br>{0}
#                     """.format(staff)
#         )
    
#     hr_app = frappe.get_all("Miss Punch Application",
#                         filters={'docstatus': ['!=', 2]},
#                         fields=['employee', 'date', 'department', 'name', 'in_time', 'out_time', 'shift', 'workflow_state'])
#     count7 = frappe.db.count('Miss Punch Application', {'workflow_state': 'HOD Pending','docstatus':0})
#     if count7 != 0:
#         for leave in hr_app:
#             if leave.department == 'Technical - JMPL' or leave.department == 'QUALITY - JMPL':
#                 if leave.workflow_state == 'HOD Pending':
#                     idx = 1
#                     staff += """
#                         <tr style="border: 1px solid black;">
#                             <td style="padding: 4px; border: 1px solid black;">{0}</td>
#                             <td style="padding: 4px; border: 1px solid black;">{1}</td>
#                             <td style="padding: 4px; border: 1px solid black;">{2}</td>
#                             <td style="padding: 4px; border: 1px solid black;">{3}</td>
#                             <td style="padding: 4px; border: 1px solid black;">{4}</td>
#                             <td style="padding: 4px; border: 1px solid black;">{5}</td>
#                             <td style="padding: 4px; border: 1px solid black;">{6}</td>
#                             <td style="padding: 4px; border: 1px solid black;">{7}</td>
#                         </tr>
#                         """.format(idx, leave.employee, format_date(leave.date), leave.department, leave.name or ' ',leave.in_tme or ' ',leave.out_time or ' ', leave.shift_type or '')
#                     idx += 1
#         frappe.sendmail(
#             recipients='jothi.m@groupteampro.com',
#             subject='Leave Application Report',
#             message="""Dear Sir,<br><br>
#                     Kindly Find the list of Miss Punch Application waiting for your Approval:<br>{0}
#                     """.format(staff)
#         )
#     hr_app = frappe.get_all("Miss Punch Application",
#                         filters={'docstatus': ['!=', 2]},
#                         fields=['employee', 'date', 'department', 'name', 'in_time', 'out_time', 'shift', 'workflow_state'])
#     count8 = frappe.db.count('Miss Punch Application', {'workflow_state': 'HOD Pending','docstatus':0})
#     if count8 != 0:
#         for leave in hr_app:
#             if leave.department == 'Stores - JMPL' or leave.department == 'Dispatch - JMPL' or leave.department == 'Assembly Shop - JMPL' or leave.department == 'Machine Shop - JMPL' or leave.department == 'MAINTENANCE - JMPL' or leave.department == 'Utility - JMPL':
#                 if leave.workflow_state == 'HOD Pending':
#                     idx = 1
#                     staff += """
#                         <tr style="border: 1px solid black;">
#                             <td style="padding: 4px; border: 1px solid black;">{0}</td>
#                             <td style="padding: 4px; border: 1px solid black;">{1}</td>
#                             <td style="padding: 4px; border: 1px solid black;">{2}</td>
#                             <td style="padding: 4px; border: 1px solid black;">{3}</td>
#                             <td style="padding: 4px; border: 1px solid black;">{4}</td>
#                             <td style="padding: 4px; border: 1px solid black;">{5}</td>
#                             <td style="padding: 4px; border: 1px solid black;">{6}</td>
#                             <td style="padding: 4px; border: 1px solid black;">{7}</td>
#                         </tr>
#                         """.format(idx, leave.employee, format_date(leave.date), leave.department, leave.name or ' ',leave.in_tme or ' ',leave.out_time or ' ', leave.shift_type or '')
            
#                     idx += 1
#         frappe.sendmail(
#             subject='Miss Punch Application Report',
#             recipients='jothi.m@groupteampro.com',
#             message="""Dear Sir,<br><br>
#                     Kindly Find the list of Miss Punch Application waiting for your Approval:<br>{0}
#                     """.format(staff)
# #         )	    
# def leave_allocation_deletion_process():
#     # Fetch active employees with category 'TT'
#     employees = frappe.db.get_all(
#         "Employee",
#         filters={'status': 'Active', 'employee_category': 'GT'},
#         fields=['name']
#     )
    
#     if employees:
#         # day_index = 0
#         for emp in employees:
#             # Delete leave allocation records for the employee
#             frappe.db.sql("""
#                 DELETE FROM `tabLeave Allocation` WHERE employee = %s
#             """, (emp['name'],))
#             # day_index+=1
#             # print(day_index)
#         print("Leave allocations deleted for active 'TT' employees.")
#     else:
#         print("No employees found.")
# @frappe.whitelist()
# def update_status(doc,method):
#     if doc.workflow_state =='Rejected':
#         frappe.db.set_value('Leave Application',doc.name,'status','Rejected')  
#         if doc.docstatus == 0:
#             frappe.db.set_value('Leave Application',doc.name,'docstatus',1)
#     if doc.workflow_state =='HR Pending':
#         # if doc.docstatus == 0:
#         #     frappe.db.set_value('Leave Application',doc.name,'docstatus',1)
#         frappe.db.set_value('Leave Application',doc.name,'status','Approved')
  
# @frappe.whitelist()
# def validate_leave(doc, method):
#     user_roles = frappe.get_roles(frappe.session.user)
#     hr = "Miss Punch" in user_roles
#     admin = "Administrator" in user_roles
#     if (not hr):
#         allowed_days = 3
#         current_date = today()
#         if isinstance(current_date, str):
#             current_date = datetime.strptime(current_date, "%Y-%m-%d").date()
#         earliest_allowed = add_days(current_date, -3)
#         if isinstance(doc.to_date, str):
#             miss_date = datetime.strptime(doc.to_date, "%Y-%m-%d").date()
#         else:
#             miss_date = doc.to_date
#         if miss_date < earliest_allowed:
#             frappe.throw(
#                 _("Leave applications are allowed only for up to the previous {0} working days.")
#                 .format(allowed_days)
#             )
        
        
@frappe.whitelist()
def validate_com_off(doc, method):
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

# @frappe.whitelist()
# # when already leave application present in draft status for existing balance, then error will be thrown
# def restrict_for_zero_balance(doc, method):
#     if doc.leave_type!='Leave Without Pay': 
#         total_leave_days_present=0
#         total_lbalance=doc.leave_balance
#         draft_leave_applications = frappe.get_all("Leave Application", {"employee": doc.employee,"docstatus":0,"leave_type": doc.leave_type,'name':('!=',doc.name)},["total_leave_days"])
#         for i in draft_leave_applications:
#             # frappe.errprint(i.name)
#             total_leave_days_present+=i.total_leave_days
#         total_leave_days_present += doc.total_leave_days
#         available=total_lbalance-total_leave_days_present
#         # frappe.errprint(total_lbalance)
#         # frappe.errprint(total_leave_days_present)
#         # frappe.errprint(available)
#         if available < 0 :
#             frappe.throw("Insufficient leave balance for this leave type")


@frappe.whitelist()
#send a mail alert if any scheduled job failed
def schedule_log_fail(doc,method):
    if doc.status=='Failed':
        message = """
        The schedule Job type <b>{}</b> is failed.<br> Kindly check the log <b>{}</b>
        """.format(doc.scheduled_job_type,doc.name)
        frappe.sendmail(
                recipients=["erp@groupteampro.com"],
                subject='Scheduled Job type failed(JOHOKU)',
                message=message
            )
  
        
@frappe.whitelist()
#submit attendance when status is on leave
def submit_att(doc,method):  
    if doc.docstatus==0:
        if doc.status=='On Leave'and doc.leave_type:
            frappe.db.set_value('Attendance',doc.name,'docstatus',1)    
        
@frappe.whitelist()
#submit attendance when status is on leave
def submit_att_leave(doc,method):  
    if doc.docstatus==0:
        if doc.status=='On Leave'and doc.leave_type:
            frappe.db.set_value('Attendance',doc.name,'docstatus',1)    

# @frappe.whitelist()
# def create_coff(doc,method):
#     grade=frappe.db.get_value("Employee",{'name':doc.employee},['grade'])
#     if grade:
#         if grade in ['MG-3','MG-4','MG-5','MG-6','MG-7','MG-8','MG-9','MG-10','MG-11']:
#             hh=check_holiday_hh(doc.attendance_date,doc.employee)
#             if hh=='FH' or hh=='NH' or hh=='WW':
#                 if doc.total_working_hours>=4 and (doc.status=='Present' or doc.status=='Half Day'):
#                     if not frappe.db.exists('COFF and OT Request',{'employee':doc.employee,'ot_date':doc.attendance_date,'docstatus':['!=',2]}):
#                         coff=frappe.new_doc('COFF and OT Request')
#                         coff.employee=doc.employee
#                         coff.request_type='COFF'
#                         coff.ot_date=doc.attendance_date
#                         coff.working_hours=doc.total_working_hours
#                         coff.save(ignore_permissions=True)
#                         frappe.db.commit()
#         else:
#             otamt=0
#             fixed=frappe.db.get_value("Employee",{'name':doc.employee},['fixed_earning'])
#             hh=check_holiday_hh(doc.attendance_date,doc.employee)
#             if hh:
#                 count=0
#                 if hh=='NH':
#                     count=3
#                 elif hh=='FH':
#                     count=2
#                 elif hh=='WW':
#                     count=2
#                 else:
#                     count=1
#             else:
#                 if doc.over_time_hours and doc.over_time_hours>=2:
#                     count=2
#                 else:
#                     count=1
#             if doc.over_time_hours:
#                 otamt+=((((fixed/total_working_days)/8)*count)*doc.over_time_hours)
        
    
        
def check_holiday_hh(date, emp):
    holiday_list = frappe.db.get_value('Employee', emp, 'holiday_list')
    
    query = """
        SELECT `tabHoliday`.holiday_date, `tabHoliday`.weekly_off
        FROM `tabHoliday List`
        LEFT JOIN `tabHoliday` ON `tabHoliday`.parent = `tabHoliday List`.name
        WHERE `tabHoliday List`.name = %s AND holiday_date = %s
    """
    holiday = frappe.db.sql(query, (holiday_list, date), as_dict=True)
    if holiday:
        if holiday[0].weekly_off == 1:
            return "WW"
        elif holiday[0].holiday_type == "FH":
            return "FH"
        elif holiday[0].holiday_type == "NH":
            return "NH"
        else:
            return "HH"
    return None


# @frappe.whitelist()
# def get_duplicate_attendance(employee,date,name):
#     if frappe.db.exists("Attendance",{'name':['!=',name],'employee':employee,'attendance_date':date,'docstatus':("!=",2)}):
#         att_name=frappe.db.get_value("Attendance",{'name':['!=',name],'employee':employee,'attendance_date':date,'docstatus':("!=",2)},['name'])
#         return att_name
    
    
@frappe.whitelist()
def validate_leave_application(doc,method):
# def validate_leave_application():
    # employee ='JMPLS0001'
    # start_date ='2025-02-12'
    # leave_type ='Casual Leave'
    # frappe.db.exists("Leave Application",{'employee':employee,'attendance_date':date,'docstatus':("!=",2)}):
    doj=frappe.db.get_value("Employee",{'name':doc.employee},['date_of_joining'])
    # start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
    # doj_obj = datetime.strptime(doj, '%Y-%m-%d').date()
    doj_obj = doj
    start_date_obj = doc.from_date
    s_year = start_date_obj.year
    s_month = start_date_obj.month
    s_date_ =start_date_obj.day
    d_year = doj_obj.year
    d_month = doj_obj.month
    d_date_ =doj_obj.day
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()  # Adjust the format as needed
    # doj = datetime.strptime(doj, '%Y-%m-%d').date()
    if d_year == s_year:
        month_diff_var = month_diff(doj,start_date)
        date_diff_var = date_diff(doj,start_date)
    if d_year != s_year:
        if start_date < doj:
            month_diff_var = month_diff(doj,start_date)
        else:
            month_diff_var = month_diff(start_date,doj)
        # date_diff_var = date_diff(doj,start_date)
        # print(month_diff_var)
        if month_diff_var < 6:
            frappe.throw('You are not eligible for the Leave Application Because your Date of joining is less than 6 months ')


# @frappe.whitelist()
# def validate_leave_application():
#     employee = 'JMPLS0001'
#     start_date = '2025-02-12'
#     leave_type = 'Casual Leave'

#     # Fetching Date of Joining (DOJ)
#     doj = frappe.db.get_value("Employee", {'name': employee}, 'date_of_joining')

#     if not doj:
#         frappe.msgprint(f"No Date of Joining found for employee {employee}")
#         return

#     # Converting string dates to datetime objects
#     start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
#     # doj_obj = datetime.strptime(doj, '%Y-%m-%d').date()  # Convert DOJ to date object
#     doj_obj = doj
#     # Extracting year, month, and day for both start_date and doj
#     s_year, s_month, s_date_ = start_date_obj.year, start_date_obj.month, start_date_obj.day
#     d_year, d_month, d_date_ = doj_obj.year, doj_obj.month, doj_obj.day

#     # Calculating the date differences
#     if d_year == s_year:
#         month_diff_var = month_diff(doj_obj, start_date_obj)
#         date_diff_var = date_diff(doj_obj, start_date_obj)
#     else:
#         # If the years are different, ensure that the correct month difference is calculated
#         if start_date_obj < doj_obj:
#             month_diff_var = month_diff(doj_obj, start_date_obj)
#         else:
#             month_diff_var = month_diff(start_date_obj, doj_obj)

#         date_diff_var = date_diff(doj_obj, start_date_obj)

#         # Checking the eligibility based on the date difference (6 months check)
#         if month_diff_var < 6:
#             frappe.msgprint('You are not eligible for the Leave Application because your Date of Joining is less than 6 months.')
#             return

#     # Optional: you can add further logic to return or print the result
#     print(f"Month Difference: {month_diff_var}")
#     print(f"Date Difference: {date_diff_var}")



@frappe.whitelist()
def create_el_leave_allocation():
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

    date_data = get_date_dictionary_format()
    current_date = date.today()
    year = current_date.year

    from_date = getdate(f"{year}-01-01")
    to_date = getdate(f"{year}-12-31")
    from_date = getdate(from_date)
    to_date = getdate(to_date)
    new_join_employees = frappe.db.sql("""
        SELECT name, employee_name,date_of_joining
        FROM `tabEmployee`
        WHERE
            (date_of_joining > %(start_date)s OR date_of_joining > %(end_date)s)
            AND status = 'Active'
    """, {
        'start_date': from_date,
        'end_date': to_date,
    }, as_dict=True)
    print(len(new_join_employees))
    for employee in new_join_employees:
        if employee.get("name") != "JM11":
            continue
        print(employee.get('name'))
        print(employee.get('date_of_joining'))
        current_date = date.today()
        year = current_date.year
        year += 1
        to_date = f"{year}-12-31"
        joining_year = getdate(employee.get('date_of_joining')).year + 1

        from_date = getdate(employee.get('date_of_joining')).replace(year=joining_year)
        month_list = get_date_dictionary_format()
        for i in month_list:
            if getdate(i['start_date']) <= from_date <= getdate(i['end_date']):
                month_name = i['month']
                break
        leaves = el_data_dictionary.get(month_name)
        # print(leaves)
        # if employee.get('name') =='HRMS-200':
        if not frappe.db.exists("Leave Allocation", {"employee":  employee.get('name'), "leave_type": "Earned Leave",'from_date':from_date,'to_date':to_date}):
            # print(current_date)
            # print(employee)
            el_doc = frappe.new_doc("Leave Allocation")
            el_doc.employee = employee.get('name')
            el_doc.leave_type = "Earned Leave"
            el_doc.new_leaves_allocated = leaves
            el_doc.from_date = from_date
            el_doc.to_date = "2100-12-31"
            el_doc.company = 'JOHOKU MANUFACTURING PVT LTD'
            # el_doc.carry_forward = 1
            el_doc.save(ignore_permissions=True)
            # el_doc.submit()

# @frappe.whitelist()
# #checks the employee number already
# # exist if not it will update the employee numer and rename the document with the number.
# def update_employee_no(name,employee_number):
#     emp = frappe.get_doc("Employee",name)
#     emps=frappe.get_all("Employee",{"status":"Active"},['*'])
#     for i in emps:
#         if emp.employee_number == employee_number:
#             pass
#         elif i.employee_number == employee_number:
#             frappe.throw(f"Employee Number already exists for {i.name}")
#         else:
#             frappe.db.set_value("Employee",name,"employee_number",employee_number)
#             frappe.rename_doc("Employee", name, employee_number, force=1)
#             return employee_number
        

# @frappe.whitelist()
# def create_cl_sl_leave_allocation(employee_doc_name,probation_end_date):
    
#     cl_data_dictionary = {
#         "January": 10.0,
#         "February": 9.0,
#         "March": 8.0,
#         "April": 7.5,
#         "May": 7.0,
#         "June": 6.0,
#         "July": 5.0,
#         "August": 4.0,
#         "September": 3.0,
#         "October": 2.5,
#         "November": 2.0,
#         "December": 1.0
  
#     }
#     sl_data_dictionary = {
#         "January": 7.0,
#         "February": 6.0,
#         "March": 5.5,
#         "April": 5.0,
#         "May": 4.5,
#         "June": 4.0,
#         "July": 3.5,
#         "August": 3.0,
#         "September": 2.0,
#         "October": 1.5,
#         "November": 1.0,
#         "December": 0.5
  
#     }
    
#     el_data_dictionary = {
#         "January": 15.0,   
#         "February": 14.0,    
#         "March": 12.5,   
#         "April": 11.0,      
#         "May": 10.0,      
#         "June": 9.0,        
#         "July": 7.5,       
#         "August": 6.0,        
#         "September": 5.0,     
#         "October": 4.0,   
#         "November": 2.5,    
#         "December": 1.0  
     
#     }
#     # date_data = get_date_dictionary_format()
#     # frappe.errprint(date_data)
#     # for cl_dates in date_data:
#     #     start_date =cl_dates.get('start_date')
#     #     end_date = cl_dates.get('end_date')
#         # frappe.errprint(start_date)
#         # frappe.errprint(end_date)
        
#     new_join_employees = frappe.db.sql("""
#         SELECT name, employee_name,date_of_joining,probation_end_date
#         FROM `tabEmployee`
#         WHERE
#             employee = %(employee)s                         
#             AND status = 'Active'
#     """, {
#         'employee': employee_doc_name,
#     }, as_dict=True)

#     for employee in new_join_employees:
#         joining_year = getdate(employee.get('probation_end_date')).year
#         # print(joining_year)
#         to_date = f"{joining_year}-12-31"
#         # from_date = getdate(start_date)
#         from_date = add_months(getdate(employee.get('date_of_joining')),6)
#         if employee.get('probation_end_date'):
#             from_date = add_days(getdate(employee.get('probation_end_date')),1)

#         doj = getdate(employee.get('date_of_joining'))
#         el_from_date = add_years(doj, 1)

#         joining_year = el_from_date.year
#         el_to_date = f"{joining_year}-12-31"

        
#         month_list = get_date_dictionary_format_for_cl_sl(from_date)
#         # frappe.errprint(month_list)
#         # frappe.errprint(f"{from_date} from Date")
#         for i in month_list:
#             # frappe.errprint(f"{i['start_date']} start date")
#             # frappe.errprint(f"{i['end_date']} end date")
#             if getdate(i['start_date']) <= from_date <= getdate(i['end_date']):
#                 month_name = i['month']
#                 # frappe.errprint(month_name)
#                 break
        
#         if not frappe.db.exists("Leave Allocation", {"employee":  employee.get('name'), "leave_type": "Casual Leave",'from_date':from_date,'to_date':to_date,'docstatus':["!=",2]}):
#             leaves = cl_data_dictionary.get(month_name)
#             cl_doc = frappe.new_doc("Leave Allocation")
#             cl_doc.employee = employee.get('name')
#             cl_doc.leave_type = "Casual Leave"
#             cl_doc.new_leaves_allocated = leaves
#             cl_doc.total_leaves_allocated = leaves
#             cl_doc.from_date = from_date
#             cl_doc.to_date = to_date
#             cl_doc.save(ignore_permissions=True)
#             # cl_doc.submit()
#         if not frappe.db.exists("Leave Allocation", {"employee":  employee.get('name'), "leave_type": "Sick Leave",'from_date':from_date,'to_date':to_date,'docstatus':["!=",2]}):
#             leaves = sl_data_dictionary.get(month_name)
#             sl_doc = frappe.new_doc("Leave Allocation")
#             sl_doc.employee = employee.get('name')
#             sl_doc.leave_type = "Sick Leave"
#             sl_doc.new_leaves_allocated = leaves
#             sl_doc.total_leaves_allocated = leaves
#             sl_doc.from_date = from_date
#             sl_doc.to_date = to_date
#             sl_doc.save(ignore_permissions=True)
#             # sl_doc.submit()
            
#         el_month_list = get_date_dictionary_format_for_cl_sl(el_from_date)

#         for i in el_month_list:
#             if getdate(i['start_date']) <= el_from_date <= getdate(i['end_date']):
#                 el_month_name = i['month']
#                 break

#         if not frappe.db.exists( "Leave Allocation", { "employee": employee.get('name'),"leave_type": "Earned Leave","from_date": el_from_date, "to_date": el_to_date,"docstatus": ["!=", 2]}):
#             leaves = el_data_dictionary.get(el_month_name)
#             el_doc = frappe.new_doc("Leave Allocation")
#             el_doc.employee = employee.get('name')
#             el_doc.leave_type = "Earned Leave"
#             el_doc.new_leaves_allocated = leaves
#             el_doc.total_leaves_allocated = leaves
#             el_doc.from_date = el_from_date
#             el_doc.to_date = el_to_date
#             el_doc.save(ignore_permissions=True)


# def create_leave_allocation_for_previuos_employees():
# 	current_date = date.today()
# 	year = current_date.year
# 	year = int(year)
# 	year -= 1
# 	next_year = year + 1
# 	from_date = f"21-12-{year}"
# 	to_date = f"20-12-{next_year}"
# 	from_date = getdate(from_date)
# 	to_date = getdate(to_date)
# 	print(from_date)
# 	print(to_date)
# 	previous_employees = frappe.db.sql("""
# 		SELECT name, employee_name, date_of_joining, basic
# 		FROM `tabEmployee`
# 		WHERE
# 			(date_of_joining < %(start_date)s OR date_of_joining > %(end_date)s)
# 			AND status = 'Active'
# 		""", {
# 			'start_date': from_date,
# 			'end_date': to_date,
# 		}, as_dict=True)
# 	for employee in previous_employees:  
# 		if not frappe.db.exists("Leave Allocation", {"employee":  employee.get('name'), "leave_type": "Casual Leave",'from_date':from_date,'to_date':to_date,'docstatus':["!=",2]}):
# 			# print(current_date)
# 			# print(employee)
# 			cl_doc = frappe.new_doc("Leave Allocation")
# 			cl_doc.employee = employee.get('name')
# 			cl_doc.leave_type = "Casual Leave"
# 			cl_doc.new_leaves_allocated = 10
# 			cl_doc.total_leaves_allocated = 10
# 			cl_doc.from_date = from_date
# 			cl_doc.to_date = to_date
# 			cl_doc.company = 'JOHOKU MANUFACTURING PVT LTD'
# 			cl_doc.save(ignore_permissions=True)
# 		if not frappe.db.exists("Leave Allocation", {"employee":  employee.get('name'), "leave_type": "Sick Leave",'from_date':from_date,'to_date':to_date,'docstatus':["!=",2]}):
# 			# print(current_date)
# 			# print(employee)
# 			cl_doc = frappe.new_doc("Leave Allocation")
# 			cl_doc.employee = employee.get('name')
# 			cl_doc.leave_type = "Sick Leave"
# 			cl_doc.new_leaves_allocated = 7
# 			cl_doc.total_leaves_allocated = 7
# 			cl_doc.from_date = from_date
# 			cl_doc.to_date = to_date
# 			cl_doc.company = 'JOHOKU MANUFACTURING PVT LTD'
# 			cl_doc.save(ignore_permissions=True)
# 			# cl_doc.submit()
# 		# if not frappe./.save(ignore_permissions=True)
# 			# sl_doc.submit()
# 		if not frappe.db.exists("Leave Allocation", {"employee":  employee.get('name'), "leave_type": "Earned Leave",'docstatus':["!=",2]}):
# 			el_doc = frappe.new_doc("Leave Allocation")
# 			el_doc.employee = employee.get('name')
# 			el_doc.leave_type = "Earned Leave"
# 			el_doc.new_leaves_allocated = 15
# 			el_doc.total_leaves_allocated = 15
# 			el_doc.from_date = from_date
# 			el_doc.to_date = to_date
# 			el_doc.company = 'JOHOKU MANUFACTURING PVT LTD'
# 			el_doc.save(ignore_permissions=True)
# 			el_doc.submit()
# 			print("test")
# 		else:
# 			# print("Else")
# 			# 'from_date':from_date,'to_date':to_date,
# 			if frappe.db.exists("Leave Allocation", {"employee":  employee.get('name'), "leave_type": "Earned Leave",'docstatus':["!=",2]}):
# 				if employee.get('name')=='JMPLGT198':
# 					allocated_leaves = -15
# 					leave_allocation_name = frappe.db.get_value(
# 						"Leave Allocation",
# 						{"employee": employee.get('name'), "leave_type": "Earned Leave", 'docstatus': ["!=", 2]},
# 						"name"
# 					)
                    
# 					el_doc = frappe.get_doc("Leave Allocation", leave_allocation_name)
# 					# print(f"Leave Allocation {el_doc}")
# 					previously_allocated_leaves= el_doc.new_leaves_allocated
# 					leaves_data = get_leave_balance_on(el_doc.employee,
# 						el_doc.leave_type,
# 						el_doc.from_date,
# 						el_doc.to_date,
# 						consider_all_leaves_in_the_allocation_period=True,
# 						for_consumption=True,
# 					)
# 					# print(f"Previous leaves {previously_allocated_leaves}")
# 					leave_balance = leaves_data.get('leave_balance')
# 					total_leaves = allocated_leaves + previously_allocated_leaves
# 					# print(total_leaves)
# 					used_leaves = previously_allocated_leaves - leave_balance
# 					# print(f"Used Leaves {used_leaves}")
# 					leaves = total_leaves - used_leaves
# 					# print(leaves)
# 					if leaves != 0:
# 						enhasment_leaves = leaves - 30
# 						basic = employee.get('basic')
# 						amount = (basic/31) * enhasment_leaves
# 						# print(f"Leave Encashment {enhasment_leaves}")
# 						leave_period ='HR-LPR-2025-00001'
# 						el_enhance_doc = frappe.new_doc("Leave Encashment")
# 						el_enhance_doc.employee = employee.get('name')
# 						el_enhance_doc.leave_type = el_doc.leave_type
# 						el_enhance_doc.leave_balance =enhasment_leaves
# 						el_enhance_doc.leave_period = leave_period
# 						el_enhance_doc.encashable_days = enhasment_leaves
# 						el_enhance_doc.encashment_date = date.today()
# 						el_enhance_doc.encashment_amount =amount
# 						el_enhance_doc.save(ignore_permissions=True)
# 						new_leaves_allocated = leaves - enhasment_leaves
# 						# new_leaves_allocated = total_leaves - enhasment_leaves
# 						# new_leaves_allocated = total_leaves
# 						# print(new_leaves_allocated)
# 					el_doc.new_leaves_allocated = new_leaves_allocated
# 					el_doc.save(ignore_permissions=True)
                        
    
def create_leave_allocation_for_previous_employees1():
    current_date = date.today()
    year = current_date.year
    year = int(year)
    # year -= 1
    next_year = year + 1
    from_date = f"01-01-{next_year}"
    print(from_date , "1")
    to_date = f"31-12-{next_year}"
    print(to_date , "1")
    from_date = getdate(from_date)
    print(from_date , "2")
    to_date = getdate(to_date)
    print(to_date,"2")
    # print(from_date)
    # print(to_date)
    previous_employees = frappe.db.sql("""
        SELECT name, employee_name, date_of_joining, basic
        FROM `tabEmployee`
        WHERE
            (date_of_joining < %(start_date)s OR date_of_joining > %(end_date)s)
            AND status = 'Active'
        """, {
            'start_date': from_date,
            'end_date': to_date,
        }, as_dict=True)
    
    for employee in previous_employees: 
        # print(employee.get("name"))
        # if employee.get("name") != "JMPLS151":
        #     continue
        if not frappe.db.exists("Leave Allocation", {"employee":  employee.get('name'), "leave_type": "Casual Leave",'from_date':from_date,'to_date':to_date,'docstatus':["!=",2]}):
            # print(current_date)
            # print(employee)
            cl_doc = frappe.new_doc("Leave Allocation")
            cl_doc.employee = employee.get('name')
            cl_doc.leave_type = "Casual Leave"
            cl_doc.new_leaves_allocated = 10
            cl_doc.total_leaves_allocated = 10
            cl_doc.from_date = from_date
            cl_doc.to_date = to_date
            cl_doc.company = 'JOHOKU MANUFACTURING PVT LTD'
            cl_doc.save(ignore_permissions=True)
        if not frappe.db.exists("Leave Allocation", {"employee":  employee.get('name'), "leave_type": "Sick Leave",'from_date':from_date,'to_date':to_date,'docstatus':["!=",2]}):
            # print(current_date)
            # print(employee)
            cl_doc = frappe.new_doc("Leave Allocation")
            cl_doc.employee = employee.get('name')
            cl_doc.leave_type = "Sick Leave"
            cl_doc.new_leaves_allocated = 7
            cl_doc.total_leaves_allocated = 7
            cl_doc.from_date = from_date
            cl_doc.to_date = to_date
            cl_doc.company = 'JOHOKU MANUFACTURING PVT LTD'
            cl_doc.save(ignore_permissions=True)
        
        # if not frappe.db.exists("Leave Allocation", {"employee":  employee.get('name'), "leave_type": "Earned Leave",'docstatus':["!=",2]}):
        #     el_doc = frappe.new_doc("Leave Allocation")
        #     el_doc.employee = employee.get('name')
        #     el_doc.leave_type = "Earned Leave"
        #     el_doc.new_leaves_allocated = 15
        #     el_doc.total_leaves_allocated = 15
        #     el_doc.from_date = from_date
        #     el_doc.to_date = "2100-12-31"
        #     el_doc.company = 'JOHOKU MANUFACTURING PVT LTD'
        #     el_doc.save(ignore_permissions=True)
        #     el_doc.submit()
        #     print("test")
        # else:
        #     print("Else123")
        #     # 'from_date':from_date,'to_date':to_date,
        #     if frappe.db.exists("Leave Allocation", {"employee":  employee.get('name'), "leave_type": "Earned Leave",'docstatus':["!=",2]}):
        #         print("Else1")
        #         # if employee.get('name')=='JMPLS105':
        #             # print("Else2")
        #         allocated_leaves = 15
        #         leave_allocation_name = frappe.db.get_value(
        #             "Leave Allocation",
        #             {"employee": employee.get('name'), "leave_type": "Earned Leave", 'docstatus': ["!=", 2]},
        #             "name"
        #         )
                
        #         el_doc = frappe.get_doc("Leave Allocation", leave_allocation_name)
        #         # print(f"Leave Allocation {el_doc}")
        #         previously_allocated_leaves= el_doc.new_leaves_allocated
        #         leaves_data = get_leave_balance_on(el_doc.employee,
        #             el_doc.leave_type,
        #             el_doc.from_date,
        #             el_doc.to_date,
        #             consider_all_leaves_in_the_allocation_period=True,
        #             for_consumption=True,
        #         )
        #         print(f"Previous leaves {previously_allocated_leaves}")
        #         leave_balance = leaves_data.get('leave_balance')
        #         print(f"leave_balance {leave_balance}")
        #         total_leaves = allocated_leaves + previously_allocated_leaves
        #         print(total_leaves , "total_leaves")
        #         used_leaves = previously_allocated_leaves - leave_balance
        #         print(f"Used Leaves {used_leaves}")
        #         leaves = total_leaves - used_leaves
        #         print(leaves , "leaves")
        #         if leaves > 30:
        #             enhasment_leaves = leaves - 30
        #             # enhasment_leaves_count = leaves
        #             enhasment_leaves_count = enhasment_leaves
        #             basic = employee.get('basic')
        #             amount = (basic/26) * enhasment_leaves
        #             # print(f"Leave Encashment {enhasment_leaves}")
        #             leave_period ='HR-LPR-2025-00002'
        #             el_enhance_doc = frappe.new_doc("Leave Encashment")
        #             el_enhance_doc.employee = employee.get('name')
        #             el_enhance_doc.leave_type = el_doc.leave_type
        #             el_enhance_doc.leave_balance =enhasment_leaves_count
        #             el_enhance_doc.leave_period = leave_period
        #             el_enhance_doc.encashable_days = enhasment_leaves_count
        #             el_enhance_doc.encashment_date = date.today()
        #             el_enhance_doc.encashment_amount =amount
        #             el_enhance_doc.save(ignore_permissions=True)
        #             new_leaves_allocated = leaves - enhasment_leaves
        #             # new_leaves_allocated = total_leaves - enhasment_leaves
        #             # new_leaves_allocated = total_leaves
        #             # print(new_leaves_allocated)
        #             el_doc.new_leaves_allocated = new_leaves_allocated
        #         else : 
        #             el_doc.new_leaves_allocated = leaves      
        #         el_doc.save(ignore_permissions=True)
                        
    
from frappe.utils import getdate, add_months
from datetime import date, timedelta

@frappe.whitelist()
def get_date_dictionary_format():
    current_date = date.today()
    year = current_date.year
    # year = int("2024")
    # year -= 1
    next_year = year + 1
    from_date = f"01-01-{next_year}"
    to_date = f"31-12-{next_year}"
    from_date = getdate(from_date)
    to_date = getdate(to_date)
    print(from_date)
    print(to_date)
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

# @frappe.whitelist()
# def get_date_dictionary_format_for_cl_sl(from_date_):
#     # current_date = date.today()
#     year = from_date_.year
#     # year = int("2024")
#     # year -= 1
#     previous_year = year
#     from_date = f"01-01-{previous_year}"
#     to_date = f"31-12-{year}"
#     from_date = getdate(from_date)
#     to_date = getdate(to_date)
#     # print(from_date)
#     # print(to_date)
#     months = []
#     current_date = from_date

#     while current_date <= to_date:
#         month_year = current_date.strftime("%Y-%m")
#         month_name = current_date.strftime("%B")  

#         start_date = current_date
#         end_date = add_months(current_date, 1) - timedelta(days=1)

#         months.append({
#             "month": month_name,
#             "month_year": month_year,
#             "start_date": start_date.strftime("%Y-%m-%d"),
#             "end_date": end_date.strftime("%Y-%m-%d")
#         })

#         current_date = add_months(current_date, 1)

#     return months


# @frappe.whitelist()
# def compensatory_on_cancel(doc,method):	
#     if doc.leave_allocation:
#         leave_allocation = doc.leave_allocation
#         # frappe.db.set_value("Compensatory Leave Request",self.name,'leave_allocation','')
#         la=frappe.get_doc('Leave Allocation',leave_allocation)
#         # frappe.errprint(doc.leave_allocation)
#         # frappe.errprint(la)
#         if doc.created_via:
#             if frappe.db.exists('Attendance',{'name':doc.created_via}):
#                 frappe.db.set_value("Attendance",doc.created_via,'coff_updated',0)
#                 la.cancel()
@frappe.whitelist()
def ledger_update_coff(doc,method):	
    if doc.leave_allocation:
        alloc=frappe.db.get_all('Leave Ledger Entry',{'transaction_name':doc.leave_allocation},['from_date','to_date','name'])
        for a in alloc:
            frappe.errprint("Ledger")
            if a.from_date!=doc.from_date:
                frappe.errprint("Ledger1")
                frappe.errprint(a.name)
                frappe.db.set_value("Leave Ledger Entry",a.name,'from_date',doc.from_date)
            if a.to_date!=doc.to_date:
                frappe.errprint("Ledger2")
                frappe.errprint(a.name)
                frappe.db.set_value("Leave Ledger Entry",a.name,'from_date',doc.to_date)

# @frappe.whitelist()
# def update_workflow_state():	
#     frappe.db.set_value("Employee Benefits Regularization","HR-25-0645",'workflow_state','Cancelled')

# @frappe.whitelist()
# def calculate_age(doc,method):
#     # frappe.errprint('Data Import')
#     date_of_birth = getdate(doc.date_of_birth)
#     today_date = getdate(today())
#     age = today_date.year - date_of_birth.year - ((today_date.month, today_date.day) < (date_of_birth.month, date_of_birth.day))
#     frappe.db.set_value('Employee', doc.name, 'age', age)

@frappe.whitelist()
def update_employee_ages():
    today_date = getdate(today())
    employees = frappe.db.sql("""SELECT name, date_of_birth FROM `tabEmployee` WHERE DAY(date_of_birth) = %s AND MONTH(date_of_birth) = %s ORDER BY name""", (today_date.day, today_date.month), as_dict=True)
    for employee in employees:
        # print(employee)
        date_of_birth = getdate(employee.date_of_birth)
        today_date = getdate(today())
        age = today_date.year - date_of_birth.year - ((today_date.month, today_date.day) < (date_of_birth.month, date_of_birth.day))
        frappe.db.set_value('Employee', employee.name, 'age', age)

    
# @frappe.whitelist()
# def update_approval_role_for_leave_application(workflow_state,name):
#     if workflow_state == 'HOD Pending':
#         frappe.db.set_value('Leave Application',{'name':name}, 'approver_role', 'HOD')
#     elif workflow_state == 'TL Pending':
#         frappe.db.set_value('Leave Application',{'name':name}, 'approver_role', 'TL')
#     elif workflow_state == 'HR Pending':
#         frappe.db.set_value('Leave Application',{'name':name}, 'approver_role', 'HR Manager')
#     elif workflow_state == 'Director Pending':
#         frappe.db.set_value('Leave Application',{'name':name}, 'approver_role', 'Director')
#     elif workflow_state == 'MD Pending':
#         frappe.db.set_value('Leave Application',{'name':name}, 'approver_role', 'MD')
#     elif workflow_state in ['Approved', 'Rejected']:
#         frappe.db.set_value('Leave Application',{'name':name}, 'approved_by', frappe.session.user)
#     return "ok"
@frappe.whitelist()
def update_pf_and_fixed():
    employees = frappe.db.sql("""SELECT name, basic, conveyance_allowance,house_rent_allowance,food_allowance,education_allowance,medical_allowance,
                              special_allowance,attire_allowance,mobile_allowance,pf_amount
                              FROM `tabEmployee` ORDER BY name""", as_dict=True)
    for employee in employees:
        # print(employee)
        # if employee.name =='JMPLTT325':
        pf_amount =employee.basic*0.12
        fixed_earning = employee.basic + employee.conveyance_allowance + employee.house_rent_allowance + employee.food_allowance + employee.education_allowance + employee.medical_allowance + employee.special_allowance + employee.attire_allowance +employee.mobile_allowance
        ctc_amount = employee.basic + employee.conveyance_allowance + employee.house_rent_allowance + employee.food_allowance + employee.education_allowance + employee.medical_allowance + employee.special_allowance + employee.attire_allowance + employee.mobile_allowance+pf_amount
        frappe.db.set_value('Employee', employee.name, 'pf_amount', pf_amount)
        frappe.db.set_value('Employee', employee.name, 'fixed_earning', fixed_earning)
        frappe.db.set_value('Employee', employee.name, 'ctc_amount', ctc_amount)

# @frappe.whitelist()
# def validate_the_holiday_list(name,holiday_date):
#     doc = frappe.get_doc('Holiday List', name)
#     if doc.holidays:
#         holiday_counts = frappe.db.get_all(
#             'Holiday',
#             {'parent': doc.name,'holiday_date':holiday_date},
#             ['holiday_date', 'count(*) as count'],
#             group_by='holiday_date'
#         )
#         for h in holiday_counts:
#             count = h.get('count')
#             if count > 0:
#                 holiday_date = h.get('holiday_date')
#                 holiday_date = frappe.utils.formatdate(holiday_date, 'dd-mm-yyyy')
#                 return f"Duplicate holiday found on {holiday_date}"


@frappe.whitelist()
def update_hd_att():
    app=frappe.db.get_all("Leave Application",{'from_date':('between',('2025-03-21','2025-04-20')),'workflow_state':"Approved",'total_leave_days':0.5},['name','employee','from_date'])
    count=0
    for a in app:
        count+=1
        print(count)
        att_name=frappe.db.get_value("Attendance",{'docstatus':['!=',2],'employee':a.employee,'attendance_date':a.from_date},['name'])
        frappe.db.set_value("Attendance",att_name,'leave_application',a.name)
  
# @frappe.whitelist()
# def create_job_fail():
#     job = frappe.db.exists('Scheduled Job Type', 'cron_failed')
#     if not job:
#         emc = frappe.new_doc("Scheduled Job Type")
#         emc.update({
#             "method": 'johoku.custom.cron_failed_method1',
#             "frequency": 'Cron',
#             "cron_format": '*/5 * * * *'
#         })
#         emc.save(ignore_permissions=True)

# @frappe.whitelist()
# def cron_failed_method1():
#     cutoff_time = datetime.now() - timedelta(minutes=5)
#     failed_jobs = frappe.get_all(
#         "Scheduled Job Log",
#         filters={
#             "status": "Failed",
#             "creation": [">=", cutoff_time],
#             "scheduled_job_type":"mark_attendance.mark_att"
#         },
#         fields=["scheduled_job_type"]
#     )
#     unique_job_types = set()
#     for job in failed_jobs:
#         unique_job_types.add(job['scheduled_job_type'])

#     for job_type in unique_job_types:
#         frappe.sendmail(
#             recipients = ["jeniba.a@groupteampro.com","sivarenisha.m@groupteampro.com"],
#             subject = 'Failed Cron List - JOHOKU',
#             message = 'Dear Sir / Mam <br> Kindly find the below failed Scheduled Job  %s'%(job_type)
#         )  
        



# import frappe
# from frappe.utils import today, getdate, add_days
# @frappe.whitelist()
# def alert_for_probation_new():
#     job = frappe.db.exists('Scheduled Job Type', 'send_probation_alerts_new')
#     if not job:
#         emc = frappe.new_doc("Scheduled Job Type")
#         emc.update({
#             "method": 'johoku.custom.send_probation_alerts_new',
#             "frequency": 'Cron',
#             "cron_format": '0 10 * * *'  
#         })
#         emc.save(ignore_permissions=True)

# def send_probation_alerts_new():
#     today_date = getdate(today())
#     end_date_limit = add_days(today_date, 30)
    
#     employees = frappe.get_all(
#         'Employee',
#         filters={'employment_type': 'Probation','probation_start_date': ['is', 'set'],'probation_end_date': ['between', [today_date, end_date_limit]]},
#         fields=['name', 'employee_name', 'probation_end_date']
#     )
    
#     expired_employees = frappe.get_all(
#         'Employee',
#         filters={'employment_type': 'Probation','probation_start_date': ['is', 'set'],'probation_end_date': ['<', today_date]},
#         fields=['name', 'employee_name', 'probation_end_date']
#     )
    
#     rows = ""
#     for emp in employees:
#         days_remaining = (getdate(emp.probation_end_date) - today_date).days
#         rows += f"""
#             <tr>
#                 <td>{emp.name}</td>
#                 <td>{emp.employee_name}</td>
#                 <td>{emp.probation_end_date}</td>
#                 <td>{days_remaining} days remaining</td>
#                 <td style="color:orange;">Expiring Soon</td>
#             </tr>
#         """
#     for emp in expired_employees:
#         days_expired = (today_date - getdate(emp.probation_end_date)).days
#         rows += f"""
#             <tr>
#                 <td>{emp.name}</td>
#                 <td>{emp.employee_name}</td>
#                 <td>{emp.probation_end_date}</td>
#                 <td>Expired {days_expired} days ago</td>
#                 <td style="color:red;">Expired</td>
#             </tr>
#         """
    
#     if rows:
#         html = f"""
#         <h3>Probation Period Alerts</h3>
#         <table border="1" cellpadding="5" cellspacing="0">
#             <tr>
#                 <th>Employee ID</th>
#                 <th>Employee Name</th>
#                 <th>Probation End Date</th>
#                 <th>Days Remaining / Expired Days</th>
#                 <th>Expiry Status</th>
#             </tr>
#             {rows}
#         </table>
#         """

#         frappe.sendmail(
#             recipients=["hr@johoku.co.in" , "jeniba.a@groupteampro.com" ,"t.kannadhasan@johoku.co.in" , "saranya.v@johoku.co.in"],  
#             subject="Daily Probation Alert Notification",
#             message=html
#         )
        
        
import frappe
import mysql.connector
from openpyxl import Workbook
from frappe.utils.file_manager import save_file
from frappe.utils.background_jobs import enqueue

@frappe.whitelist()
def download_easytimepro_excel(from_date, to_date):
    enqueue(
        create_easytimepro_excel,
        queue="long",
        timeout=9000,
        from_date=from_date,
        to_date=to_date
    )
    return "ok"


import mysql.connector
from openpyxl import Workbook
from frappe.utils.file_manager import save_file

@frappe.whitelist()
def create_easytimepro_excel(from_date, to_date):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Pa55w0rd@",
        database="easytimepro"
    )
    cursor = mydb.cursor(dictionary=True)

    query = """
        SELECT 
            emp_code,
            punch_time,
            punch_state,
            terminal_alias,
            area_alias
            
        FROM iclock_transaction
        WHERE DATE(punch_time) BETWEEN %s AND %s
        ORDER BY punch_time ASC
    """
    cursor.execute(query, (from_date, to_date))
    rows = cursor.fetchall()

    wb = Workbook()
    ws = wb.active
    ws.title = "EasyTimePro Punch Data"

    headers = [
        "Employee Code",
        "Punch Time",
        "Punch State",
        "Terminal Alias",
        "Area Alias"
        # "Serial No",
        # "Device IP",
        # "Verify Mode",
        # "Work Code",
        # "Status",
        # "Upload Time"
    ]
    ws.append(headers)

    for r in rows:
        ws.append([
            r.get("emp_code"),
            str(r.get("punch_time")),
            r.get("punch_state"),
            r.get("terminal_alias"),
            r.get("area_alias")
            # r.get("serial_number"),
            # r.get("device_name"),
            # r.get("verify_mode"),
            # r.get("work_code"),
            # r.get("status"),
            # str(r.get("upload_time")),
        ])

    file_name = f"easytimepro_punches_{from_date}_to_{to_date}.xlsx"
    file_path = f"/tmp/{file_name}"
    wb.save(file_path)

    with open(file_path, "rb") as f:
        saved_file = save_file(
            file_name,
            f.read(),
            "Attendance Settings",
            None,
            is_private=1
        )

    return saved_file



# def create_easytimepro_excel(from_date=None, to_date=None):

#     # MySQL connect
#     mydb = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         passwd="Pa55w0rd@",
#         database="easytimepro"
#     )
#     cursor = mydb.cursor(dictionary=True)

#     # 11 Columns Query
#     query = """
#         SELECT 
#             emp_code,
#             punch_time,
#             punch_state,
#             terminal_alias,
#             area_alias,
#             serial_number,
#             device_ip,
#             verify_mode,
#             work_code,
#             status,
#             upload_time
#         FROM iclock_transaction
#         WHERE DATE(punch_time) BETWEEN %s AND %s
#         ORDER BY punch_time ASC
#     """

#     cursor.execute(query, (from_date, to_date))
#     rows = cursor.fetchall()

#     # Excel create
#     wb = Workbook()
#     ws = wb.active
#     ws.title = "EasyTimePro Punch Data"

#     headers = [
#         "Employee Code",
#         "Punch Time",
#         "Punch State",
#         "Terminal Alias",
#         "Area Alias",
#         "Serial No",
#         "Device IP",
#         "Verify Mode",
#         "Work Code",
#         "Status",
#         "Upload Time"
#     ]
#     ws.append(headers)

#     for r in rows:
#         ws.append([
#             r.get("emp_code"),
#             str(r.get("punch_time")),
#             r.get("punch_state"),
#             r.get("terminal_alias"),
#             r.get("area_alias"),
#             r.get("serial_number"),
#             r.get("device_ip"),
#             r.get("verify_mode"),
#             r.get("work_code"),
#             r.get("status"),
#             str(r.get("upload_time")),
#         ])

#     # Save to file
#     file_name = f"easytimepro_punches_{from_date}_to_{to_date}.xlsx"
#     file_path = f"/tmp/{file_name}"
#     wb.save(file_path)

#     # Save in File List
#     with open(file_path, "rb") as f:
    #     saved_file = save_file(
    #         file_name,
    #         f.read(),
    #         "Attendance Settings",
    #         None,
    #         is_private=1
    #     )

    # return saved_file



# def create_easytimepro_excel(from_date=None, to_date=None):
#     from openpyxl import Workbook
#     from frappe.utils.file_manager import save_file

#     wb = Workbook()
#     ws = wb.active
#     ws.title = "EasyTimePro Punch Data"

#     headers = [
#         "Employee Code",
#         "Punch Time",
#         "Punch State",
#         "Terminal Alias",
#         "Area Alias",
#         "Serial No",
#         "Device IP",
#         "Verify Mode",
#         "Work Code",
#         "Status",
#         "Upload Time"
#     ]
#     ws.append(headers)  # headers only

#     file_name = "test_empty_easytimepro.xlsx"
#     file_path = f"/tmp/{file_name}"
#     wb.save(file_path)

#     # Save in File List
#     with open(file_path, "rb") as f:
#         saved_file = save_file(
#             file_name,
#             f.read(),
#             "Attendance Settings",
#             None,
#             is_private=1
#         )

#     return saved_file

# @frappe.whitelist()
# def create_scheduled_job():
#     job = frappe.db.exists('Scheduled Job Type', 'Birthday Remainder')
#     if not job:
#         emc = frappe.new_doc("Scheduled Job Type")
#         emc.update({
#             "method": 'johoku.custom.send_birthday_reminder_to_hr',
#             "frequency": 'Cron',
#             "cron_format": '0 7 * * *'
#         })
#         emc.save(ignore_permissions=True)
        
# from frappe.utils import nowdate
# @frappe.whitelist()
# def send_birthday_reminder_to_hr():
#     today = nowdate()
#     month = today.split("-")[1]
#     day = today.split("-")[2]

#     employees = frappe.db.sql("""
#         SELECT name, employee_name
#         FROM `tabEmployee`
#         WHERE status = 'Active'
#         AND MONTH(date_of_birth) = %s
#         AND DAY(date_of_birth) = %s
#     """, (month, day), as_dict=True)

#     if not employees:
#         return

#     emp_names = ", ".join([emp["employee_name"] for emp in employees])

#     hr_users = frappe.get_all(
#         "Has Role",
#         filters={"role": ["in", ["HR User"]]},
#         pluck="parent"
#     )

#     if not hr_users:
#         return

#     subject = "Birthday Reminder 🎉"
#     message = f"""
#     Today is {emp_names}'s birthday 🎉<br><br>
#     A friendly reminder for the HR team.
#     """

#     frappe.sendmail(
#         recipients=list(set(hr_users)),
#         subject=subject,
#         message=message
#     )
    
    