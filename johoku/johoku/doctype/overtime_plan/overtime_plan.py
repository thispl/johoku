from __future__ import unicode_literals
from csv import writer
from email import message
from inspect import getfile
from unicodedata import name
import frappe
from frappe.utils import cstr, add_days, date_diff, getdate
from frappe import _
from frappe.utils.csvutils import UnicodeWriter, read_csv_content
from frappe.utils.file_manager import get_file, upload
from frappe.model.document import Document
from datetime import datetime, timedelta, date, time
from frappe.utils import cint, today, flt, date_diff, add_days, add_months, date_diff, getdate, formatdate, cint, cstr
from numpy import unicode_


class OvertimePlan(Document):
    def validate(self):
        if self.upload:
            self.validate_employees()
    def on_submit(self):
        if self.workflow_state == 'Rejected':
            return
        #will create the Overtime list on submission of this document if the uploaded file is present else throw an error to upload the file 
        if self.upload:
            self.create_overtime_list()
        else:
            frappe.throw(_('Please Attach the File'))    
    def on_cancel(self):
        ot_docs = frappe.db.get_all("Overtime List", {
        'overtime_plan_document': self.name,
        'docstatus': ['in', [0, 1]]
    }, ['name'])

        for ot in ot_docs:
            doc = frappe.get_doc('Overtime List', ot.name)
            if doc.docstatus == 1:
               doc.cancel()
            else:
                doc.delete()

    def create_overtime_list(self):
        #will create the overtime list based on the uploaded file
        filepath = get_file(self.upload)
        pps = read_csv_content(filepath[1])
        dates = self.get_dates(self.ot_from_date,self.ot_to_date)
        for date in dates:
            for pp in pps:
                if pp[0] == 'Employee':
                    pass
                else: 
                    ol = frappe.db.exists("Overtime List",{'employee':pp[0],'ot_from_date':date,'ot_to_date':date,'docstatus':['in',[0,1]]})
                    if not ol:
                        doc = frappe.new_doc('Overtime List')
                        doc.employee = pp[0]
                        doc.ot_from_plan = pp[4]
                        doc.department = pp[2]
                        doc.shift_type = pp[3]
                        doc.ot_from_date = date
                        doc.ot_to_date = date
                        doc.overtime_plan_document = self.name
                        doc.save(ignore_permissions=True)
                        doc.submit()
                        frappe.db.commit()

    def get_dates(self,ot_from_date,ot_to_date):
        """get list of dates in between from date and to date"""
        no_of_days = date_diff(add_days(ot_to_date, 1),ot_from_date)
        dates = [add_days(ot_from_date, i) for i in range(0, no_of_days)]
        return dates

    def validate_employees(self):
        """validate the uploaded csv file for the following conditions
        1)If same employee appears mulitple time
        2)Checks the Employee Name is updated
        3)Checks the Department is updated
        4)Checks the Overtime and Shift Type are updated
        5)Checks if the employee is Active and belongs to the mentioned department
        6)Checks if any other Overtime list is already updated for the department
        """
        err_list = ""
        filepath = get_file(self.upload)
        pps = read_csv_content(filepath[1])
        dates = self.get_dates(self.ot_from_date,self.ot_to_date)
        shift_list = []
        for pp in pps:
            if pp[0].strip() != 'Employee':
                shift_list.append(pp[0])
        for pp in pps:
            if shift_list.count(pp[0]) > 1:
                err_list += '<li> Employee  - <font color="red"> %s</font> appears multiple times in the list. </li>' % pp[0]
        if err_list:
            return err_list
        for pp in pps:
            if pp[0].strip() != 'Employee':
                if pp[0]:
                    emp = (pp[0] or "").strip()
                    name = (pp[1] or "").strip()
                    overtime = (pp[4] or "").strip()
                    dept = (pp[2] or "").strip()
                    shift = (pp[3] or "").strip()

                    if not emp:
                        err_list += '<li>Employee ID should not be Empty.</li>'
                        continue

                    if not name:
                        err_list += f'<li>Employee Name should not be Empty for <b>{emp}</b>.</li>'

                    if not dept:
                        err_list += f'<li>Department Code should not be Empty for <b>{emp}</b>.</li>'

                    if not shift:
                        err_list += f'<li>Shift Type should not be Empty for <b>{emp}</b>.</li>'
                        
                    if not overtime:
                        err_list += f'<li>Overtime should not be Empty for <b>{emp}</b>.</li>'

                    if not frappe.db.exists("Employee", emp):
                        err_list += f'<li><font color="red"><b>{emp}</b></font> Employee not found.</li>'
                    else:
                        emp_doc = frappe.get_doc("Employee", emp)
                        if self.department != emp_doc.department:
                            err_list += f'''
                            <li>
                            <font color="red"><b>{emp}</b></font> does not belong to 
                            <b>{self.department}</b> department.
                            </li>
                            '''
                        else:
                            if overtime:
                                for date in dates:
                                    existing_ot = frappe.db.exists(
                                        "Overtime List",
                                        {
                                            "employee": emp,
                                            "start_date": date,
                                            "docstatus": ["!=", 2]
                                        }
                                    )
                                    if existing_ot:
                                        dept_name = frappe.db.get_value(
                                            "Overtime List",
                                            existing_ot,
                                            "department"
                                        )
                                        err_list += f'''
                                        <li>
                                        {dept_name} department already allocated OT for 
                                        <font color="red"><b>{emp}</b></font> on {date}.
                                        </li>
                                        '''
                            if emp_doc.relieving_date:
                                if getdate(self.ot_to_date) > emp_doc.relieving_date:
                                    err_list += f'''
                                    <li>
                                    <font color="red"><b>{emp}</b></font> was relieved on 
                                    <b>{emp_doc.relieving_date}</b>. 
                                    OT cannot be uploaded after relieving date.
                                    </li>
                                    '''
                else:
                    if not pp[0]:
                        err_list += '<li>Employee should not be Empty.</li>'
        if err_list:
            frappe.throw(f"<ul>{err_list}</ul>")
        
    @frappe.whitelist()
    def check(self):
        #checks if any other Overtime list is exists for the same department for the same period
        overtime_list = frappe.db.sql("""select name from `tabOvertime List` where department = '%s' and ot_from_date between '%s' and '%s' """ % (self.department, self.ot_from_date, self.ot_to_date), as_dict=1)
        if overtime_list:
            self.upload = ''
            return 'Overtime Plan already submitted for the selected date'

    @frappe.whitelist()
    def show_csv_data(self):
        #return the uploaded csv data in HTML View
        filepath = get_file(self.upload)
        pps = read_csv_content(filepath[1])
        data_list = ''
        for pp in pps:
            if pp[0] == 'Employee':
                data_list += "<tr><td style='background-color:#1dbaba; border: 1px solid black'>%s</td><td style='background-color:#1dbaba; border: 1px solid black'>%s</td><td style='background-color:#1dbaba; border: 1px solid black'>%s</td><td style='background-color:#1dbaba; border: 1px solid black'>%s</td><td style='background-color:#1dbaba; border: 1px solid black'>%s</td></tr>" % (pp[0], pp[1], pp[2], pp[3], pp[4])
            else:
                data_list += "<tr><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td></tr>" % (pp[0], pp[1], pp[2], pp[3], pp[4])
        return data_list

@frappe.whitelist()
def get_template():
    #use to get the csv file template for Overtime plan (add_header,add_data,get_data,writedata)
    args = frappe.local.form_dict

    if getdate(args.ot_from_date) > getdate(args.ot_to_date):
        frappe.throw(_(" OT To Date should be greater than From Date"))

    w = UnicodeWriter()
    w = add_header(w)
    w = add_data(w, args)

    frappe.response['result'] = cstr(w.getvalue())
    frappe.response['type'] = 'csv'
    frappe.response['doctype'] = "Overtime Plan"

def add_header(w):
    w.writerow(['Employee', 'Employee Name','Department', 'Shift Type','Overtime Hours'])
    return w

def add_data(w, args):
    data = get_data(args)
    writedata(w, data)
    return w

@frappe.whitelist()
def get_data(args):
    shifts = frappe.get_all('Shift Assignment', {'status': 'Active', 'department': args.department, 'start_date': args.ot_from_date}, ['employee','employee_name','department','shift_type'])
    data = []
    for shift in shifts:
        row = [
            shift.employee, shift.employee_name, shift.department or '', shift.shift_type, ''
        ]
        data.append(row)
    return data

@frappe.whitelist()
def writedata(w, data):
    for row in data:
        w.writerow(row)

@frappe.whitelist()
def check_shift(dept,from_date,to_date):
    #use to check the shift assignment is already exists or not for the department for the period
    data = []
    message = ''
    shift = frappe.db.exists('Shift Assignment',{'start_date':('between',(from_date,to_date)),'department':dept})
    if shift:
        data.append('Shift Assigned')
    else:
        data.append('No Shift Assigned')
    return data
 

@frappe.whitelist()
def get_allowed_departments(doctype, txt, searchfield, start, page_len, filters):
    user = frappe.session.user

    if "HR User" in frappe.get_roles(user):
        data = frappe.db.get_all(
            "Department",
            fields=["name"],
            filters={"name": ["like", f"%{txt}%"]},
            limit_start=start,
            limit_page_length=page_len
        )
    else:
        if "Over Time" in frappe.get_roles(user):
            emp_dept = frappe.db.get_value(
                "Employee",
                {"user_id": user},
                "department"
            )

            perm_depts = frappe.db.get_all(
                "User Permission",
                filters={
                    "user": user,
                    "allow": "Department"
                },
                pluck="for_value"
            )

            departments = set()

            if emp_dept:
                departments.add(emp_dept)

            if perm_depts:
                departments.update(perm_depts)

            if not departments:
                return []

            data = frappe.db.get_all(
                "Department",
                fields=["name"],
                filters={"name": ["in", list(departments)]},
                limit_start=start,
                limit_page_length=page_len
            )


        else:
            departments = frappe.db.get_all(
                "User Permission",
                filters={
                    "user": user,
                    "allow": "Department"
                },
                pluck="for_value"
            )

            if not departments:
                return []

            data = frappe.db.get_all(
                "Department",
                fields=["name"],
                filters={"name": ["in", departments]},
                limit_start=start,
                limit_page_length=page_len
            )

    return [[d.name] for d in data]

