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
#update the employee checkin from Unregistered employee checkin by clicking process checkin in attendance settings
def get_urc_to_ec(from_date, to_date):
    print("HI")
    urc = frappe.db.sql("""select biometric_pin,biometric_time,log_type,locationdevice_id,name from `tabUnregistered Employee Checkin` where date(biometric_time) between '%s' and '%s'"""%(from_date,to_date),as_dict=True)
    for uc in urc:
        pin = uc.biometric_pin
        time = uc.biometric_time
        dev = uc.locationdevice_id
        typ = uc.log_type
        nam = uc.name
        if time != "":
            if frappe.db.exists('Employee',{'name':pin}):
                if frappe.db.exists('Employee Checkin',{'name':pin,"time":time}):
                    print("HI")
                else:
                    print("HII")
                    ec = frappe.new_doc('Employee Checkin')
                    ec.biometric_pin = pin
                    ec.employee = frappe.db.get_value('Employee',{'name':pin},['employee_number'])
                    ec.time = time
                    ec.device_id = dev
                    ec.log_type = typ
                    ec.save(ignore_permissions=True)
                    frappe.db.commit()
                    print("Created")
                    attendance = frappe.db.sql(""" delete from `tabUnregistered Employee Checkin` where name = '%s' """%(nam))
                    print("Deleted")       
            else:				
                print("hello")	
    return "ok"



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

