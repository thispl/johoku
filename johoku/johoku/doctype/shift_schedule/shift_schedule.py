# # Copyright (c) 2022, TEAMPRO and contributors
# # For license information, please see license.txt

# from __future__ import unicode_literals
# from csv import writer
# from inspect import getfile
# from unicodedata import name
# import frappe
# from frappe.utils import cstr, add_days, date_diff, getdate
# from frappe import _
# from frappe.utils.csvutils import UnicodeWriter, read_csv_content
# from frappe.utils.file_manager import get_file, upload
# from frappe.model.document import Document
# from datetime import datetime,timedelta,date,time
# from frappe.utils import cint,today,flt,date_diff,add_days,add_months,date_diff,getdate,formatdate,cint,cstr
# from numpy import unicode_
# from frappe.utils.background_jobs import enqueue
# from frappe.utils import get_first_day, get_last_day, format_datetime,get_url_to_form, format_date

# class ShiftSchedule(Document):
        
#     # def on_submit(self):
#     #     #on submission it will create Shift Assignment 
#     #     if self.attach:
#     #         # self.create_shift_assignment()
#     #         # frappe.errprint("attach")
#     #         frappe.msgprint(
#     #             msg="The Shift Assignment is being created in the background. Please check after few minutes.",
#     #             indicator="green",
#     #         )
#     #         enqueue(self.create_shift_assignment, queue='long', timeout=10000, event='create_shift_assignment'
#     #             )
            
    
    
    


#     # def create_shift_assignment(self):
#     #     #creates shift assignment for each employees in the uploaded file
#     #     frappe.log_error('test')
#     #     filepath = get_file(self.attach)
#     #     pps = read_csv_content(filepath[1])
#     #     dates = self.get_dates(self.from_date,self.to_date)
#     #     shift_assignments = []
#     #     for date in dates:
#     #         # frappe.errprint(date)
#     #         for pp in pps:
#     #             # frappe.errprint(pp[1])
#     #             if pp[2] != 'Shift':
#     #                 if pp[1]:
#     #                     # frappe.errprint(pp[1])
#     #                     if not frappe.db.exists("Shift Assignment",{'employee':pp[0],'start_date':date,'end_date':date,'docstatus':("!=",2)}):
#     #                         doc = frappe.new_doc('Shift Assignment')
#     #                         doc.employee = pp[0]
#     #                         doc.shift_type = pp[2]
#     #                         doc.department = pp[3]
#     #                         doc.employee_type = pp[4]
#     #                         doc.route_no = pp[5]
#     #                         doc.boarding_point = pp[6]
#     #                         doc.start_date = date
#     #                         doc.end_date = date
#     #                         doc.schedule = self.name
#     #                         shift_assignments.append(doc)
                            


#     #     if shift_assignments:
#     #         for doc in shift_assignments:
#     #             doc.insert(ignore_permissions=True)
#     #             doc.submit()

#     #     frappe.db.commit()
    
    
    
#     def on_submit(self):
#         if self.attach:
#             frappe.msgprint(
#                 msg="The Shift Assignment is being created in the background. Please check after few minutes.",
#                 indicator="green",
#             )
#             enqueue(
#                 self.create_shift_assignment,
#                 queue='long',
#                 timeout=10000,
#                 event='create_shift_assignment'
#             )

#     # def create_shift_assignment(self):
#     #     # creates shift assignment for each employee in the uploaded file
#     #     frappe.log_error('Shift Assignment creation started')

#     #     filepath = get_file(self.attach)
#     #     pps = read_csv_content(filepath[1])
#     #     dates = self.get_dates(self.from_date, self.to_date)

#     #     for date in dates:
#     #         for pp in pps:
#     #             if pp[1] and pp[2] != 'Shift':  # employee exists and shift type valid
#     #                 # check if a shift assignment exists
#     #                 existing = frappe.get_all(
#     #                     "Shift Assignment",
#     #                     filters={
#     #                         "employee": pp[0],
#     #                         "start_date": date,
#     #                         "end_date": date
#     #                     },
#     #                     fields=["name", "docstatus"],
#     #                     limit_page_length=1
#     #                 )

#     #                 if existing:
#     #                     # if existing doc is cancelled, allow recreation
#     #                     if existing[0].docstatus != 2:
#     #                         continue  # skip active assignments

#     #                 try:
#     #                     doc = frappe.new_doc('Shift Assignment')
#     #                     doc.employee = pp[0]
#     #                     doc.shift_type = pp[2]
#     #                     doc.department = pp[3]
#     #                     doc.employee_type = pp[4]
#     #                     doc.route_no = pp[5]
#     #                     doc.boarding_point = pp[6]
#     #                     doc.start_date = date
#     #                     doc.end_date = date
#     #                     doc.schedule = self.name
#     #                     doc.insert(ignore_permissions=True)
#     #                     doc.submit()
#     #                     frappe.db.commit()
#     #                 except Exception as e:
#     #                     frappe.log_error(
#     #                         f"Failed to create Shift Assignment for {pp[0]} on {date}: {str(e)}",
#     #                         "Shift Assignment Error"
#     #                     )

#     #     frappe.db.commit()
#     #     frappe.log_error('Shift Assignment creation finished')
        
    
#     def create_shift_assignment(self):
#         frappe.log_error('Shift Assignment creation started')

#         filepath = get_file(self.attach)
#         pps = read_csv_content(filepath[1])
#         dates = self.get_dates(self.from_date, self.to_date)

#         failed_records = []  # collect all failures

#         for date in dates:
#             for pp in pps:
#                 if pp[1] and pp[2] != 'Shift':
#                     existing = frappe.get_all(
#                         "Shift Assignment",
#                         filters={
#                             "employee": pp[0],
#                             "start_date": date,
#                             "end_date": date
#                         },
#                         fields=["name", "docstatus"],
#                         limit_page_length=1
#                     )

#                     if existing:
#                         if existing[0].docstatus != 2:
#                             continue
                    
#                     # try:
#                     #     # validate employee exists first
#                     #     if not frappe.db.exists("Employee", pp[0]):
#                     #         failed_records.append({
#                     #             "employee": pp[0],
#                     #             "employee_name": pp[1],
#                     #             "shift_type": pp[2],
#                     #             "date": date,
#                     #             "error": f"Employee ID '{pp[0]}' does not exist in the system"
#                     #         })
#                     #         frappe.log_error(
#                     #             f"Failed to create Shift Assignment - Employee ID '{pp[0]}' does not exist on {date}",
#                     #             "Shift Assignment Error"
#                     #         )
#                     #         continue  # skip to next record

                    
    
#                     try:
#                         doc = frappe.new_doc('Shift Assignment')
#                         doc.employee = pp[0]
#                         doc.shift_type = pp[2]
#                         doc.department = pp[3]
#                         doc.employee_type = pp[4]
#                         doc.route_no = pp[5]
#                         doc.boarding_point = pp[6]
#                         doc.start_date = date
#                         doc.end_date = date
#                         doc.schedule = self.name
#                         doc.insert(ignore_permissions=True)
#                         doc.submit()
#                         frappe.db.commit()
#                     except Exception as e:
#                         error_msg = f"Failed to create Shift Assignment for {pp[0]} on {date}: {str(e)}"
#                         frappe.log_error(error_msg, "Shift Assignment Error")

#                         # collect failed record details
#                         failed_records.append({
#                             "employee": pp[0],
#                             "employee_name": pp[1],
#                             "shift_type": pp[2],
#                             "date": date,
#                             "error": str(e)
#                         })

#         # send email to HR if any failures occurred
#         if failed_records:
#             self.send_failure_email_to_hr(failed_records)

#         frappe.db.commit()
#         frappe.log_error('Shift Assignment creation finished')


    
#     def on_cancel(self):
#         #delete the Shift Assignment created from this shift schedule
#         frappe.db.sql("""delete from `tabShift Assignment` where schedule=%s """, (self.name))

#     def get_dates(self,from_date,to_date):
#         """get list of dates in between from date and to date"""
#         no_of_days = date_diff(add_days(to_date, 1), from_date)
#         dates = [add_days(from_date, i) for i in range(0, no_of_days)]
#         return dates

#     @frappe.whitelist()
#     def validate(self):
#         if self.attach:
#             filepath = get_file(self.attach)
#             # frappe.errprint(filepath)
#             pps = read_csv_content(filepath[1])
#             shift_data = frappe.db.get_all('Shift Type', ['name'])
#             # frappe.errprint(shift_data)
#             shift_type_list =[]
#             for shift in shift_data:
#                 shift_type_list += shift['name'] 
#             # frappe.errprint(shift_type_list)
#             idx = 0
#             for pp in pps:
#                 idx += 1
#                 if pp[2] == "Shift":
#                     continue
#                 shift_type = pp[2]
                
#                 if shift_type not in shift_type_list:
#                 # if shift_type not in ["1", "2", "3"]:
#                     frappe.throw(
#                         f"Shift is mandatory. Please check the row {idx} in the uploaded file."
#                     )
#         #checks if any other shift assignment is exists against the same department for the same period
#         shift_assignment = frappe.db.sql("""select name from `tabShift Assignment` where department = '%s' and start_date between '%s' and '%s' and docstatus !=2 """ % (self.department, self.from_date, self.to_date), as_dict=True)
#         if shift_assignment:
#                 self.attach = ''
#                 return 'Shift Schedule already submitted for the selected date'
        

#     @frappe.whitelist()
#     def show_summary(self):
#         #shows the shift summary of the uploaded shift assigment file
#         filepath = get_file(self.attach)
#         pps = read_csv_content(filepath[1])
#         data = ''
#         wc1 = wc2 = wc3 = 0

#         for pp in pps:
#             if pp[2] == "1":
#                 wc1 += 1
#             elif pp[2] == "2":
#                 wc2 += 1
#             elif pp[2] == "3":
#                 wc3  += 1
#         data += """
#             <table style="border-collapse: collapse; width: 100%;">
#                 <tr>
#                     <td style= "border: 1px solid black;text-align:center"><b>Shift</b></td>
#                     <td style= "border: 1px solid black;text-align:center"><b>1</b></td>
#                     <td style= "border: 1px solid black;text-align:center"><b>2</b></td>
#                     <td style= "border: 1px solid black;text-align:center"><b>3</b></td>
#                 </tr>
#                 <tr>
#                     <td style="border: 1px solid black;text-align:center"><b>Total</b></td>
#                     <td style="border: 1px solid black;text-align:center">{}</td>
#                     <td style="border: 1px solid black;text-align:center">{}</td>
#                     <td style="border: 1px solid black;text-align:center">{}</td>
#                 </tr>
#             </table>
#         """.format(
#             wc1, wc2, wc3
            
#         )

#         return data
    
   
#     def send_failure_email_to_hr(self, failed_records):
#         shift_schedule_url = get_url_to_form("Shift Schedule", self.name)

#         from_date = formatdate(self.from_date, "dd-MM-yyyy")
#         to_date = formatdate(self.to_date, "dd-MM-yyyy")

#         failed_dates = sorted(set(record['date'] for record in failed_records))
#         dates_list = "".join(f"<li>{formatdate(d, 'dd-MM-yyyy')}</li>" for d in failed_dates)

#         message = f"""
#             <p>Dear HR Team,</p>
#             <p>
#                 Shift Assignments could not be created for some employees
#                 under Shift Schedule <a href="{shift_schedule_url}"><strong>{self.name}</strong></a>.
#             </p>
#             <p><b>From Date:</b> {from_date}</p>
#             <p><b>To Date:</b> {to_date}</p>
            
#             <p>Please review and recreate the failed assignments manually.</p>
#             <p>Regards,<br>System</p>
#         """

#         frappe.sendmail(
#             recipients=['jeniba.a@groupteampro.com','t.kannadhasan@johoku.co.in','hr@johoku.co.in','saranya.v@johoku.co.in'],
#             subject=f"[Action Required] Shift Assignment Creation Failed - {self.name}",
#             message=message,
#             now=True
#         )
    
# @frappe.whitelist()
# def get_template():
#     #use to get the csv file template for Overtime plan (add_header,add_data,get_data,writedata)
#     args = frappe.local.form_dict

#     if getdate(args.from_date) > getdate(args.to_date):
#         frappe.throw(_("To Date should be greater than From Date"))

#     w = UnicodeWriter()
#     w = add_header(w)
#     w = add_data(w, args)

#     frappe.response['result'] = cstr(w.getvalue())
#     frappe.response['type'] = 'csv'
#     frappe.response['doctype'] = "Shift Assignment"

# def add_header(w):
#     w.writerow(['Employee ID','Employee Name','Shift','Department','Employement Type','Route No','Boarding Point'])
#     return w

# def add_data(w, args):
#     data = get_data(args)
#     writedata(w, data)
#     return w

# @frappe.whitelist()
# def get_data(args):
#     if args.department == "All Departments":
#         employees = frappe.db.get_all('Employee',{'status':'Active'},['*'])
#         data = []
#         for emp in employees:
#             row = [
#                 emp.name,emp.employee_name,emp.default_shift or '',emp.department,emp.employee_type or '',emp.route_no or '',emp.boarding_point or ''
#             ]
#             data.append(row)
#     else:
#         employees = frappe.db.get_all('Employee',{'status':'Active','department':args.department},['*'])
#         data = []
#         for emp in employees:
#             row = [
#                 emp.name,emp.employee_name,emp.default_shift or '',emp.department,emp.employee_type or '',emp.route_no or '',emp.boarding_point or ''
#             ]
#             data.append(row)
#     return data

# @frappe.whitelist()
# def writedata(w, data):
#     for row in data:
#         w.writerow(row)


# Copyright (c) 2022, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from csv import writer
from inspect import getfile
from unicodedata import name
import frappe
from frappe.utils import cstr, add_days, date_diff, getdate
from frappe import _
from frappe.utils.csvutils import UnicodeWriter, read_csv_content
from frappe.utils.file_manager import get_file, upload
from frappe.model.document import Document
from datetime import datetime,timedelta,date,time
from frappe.utils import cint,today,flt,date_diff,add_days,add_months,date_diff,getdate,formatdate,cint,cstr
from numpy import unicode_
from frappe.utils.background_jobs import enqueue
from frappe.utils import get_first_day, get_last_day, format_datetime,get_url_to_form, format_date

class ShiftSchedule(Document):

    def on_submit(self):
        if self.attach:
            frappe.msgprint(
                msg="The Shift Assignment is being created in the background. Please check after few minutes.",
                indicator="green",
            )
            enqueue(
                self.create_shift_assignment,
                queue='long',
                timeout=10000,
                event='create_shift_assignment'
            )

    def create_shift_assignment(self):
        
        frappe.log_error('Shift Assignment creation started')

        filepath = get_file(self.attach)
        pps = read_csv_content(filepath[1])
        dates = self.get_dates(self.from_date, self.to_date)

        failed_records = []  

        existing_rows = frappe.get_all(
            "Shift Assignment",
            filters={
                "start_date": ["between", [self.from_date, self.to_date]],
                "end_date": ["between", [self.from_date, self.to_date]],
                "docstatus": ["!=", 2],
            },
            fields=["employee", "start_date", "end_date"],
        )
        existing_set = set(
            (r.employee, str(r.start_date), str(r.end_date)) for r in existing_rows
        )

        insert_count = 0

        for date in dates:
            for pp in pps:
                if pp[1] and pp[2] != 'Shift':
                   
                    if (pp[0], str(date), str(date)) in existing_set:
                        continue

                    try:
                        doc = frappe.new_doc('Shift Assignment')
                        doc.employee = pp[0]
                        doc.shift_type = pp[2]
                        doc.department = pp[3]
                        doc.employee_type = pp[4]
                        doc.route_no = pp[5]
                        doc.boarding_point = pp[6]
                        doc.start_date = date
                        doc.end_date = date
                        doc.schedule = self.name
                        doc.insert(ignore_permissions=True)

                        doc.db_set('docstatus', 1, update_modified=False)

                        existing_set.add((pp[0], str(date), str(date)))

                        insert_count += 1

                        if insert_count % 100 == 0:
                            frappe.db.commit()

                    except Exception as e:
                        error_msg = f"Failed to create Shift Assignment for {pp[0]} on {date}: {str(e)}"
                        frappe.log_error(error_msg, "Shift Assignment Error")

                        # collect failed record details
                        failed_records.append({
                            "employee": pp[0],
                            "employee_name": pp[1],
                            "shift_type": pp[2],
                            "date": date,
                            "error": str(e)
                        })

        frappe.db.commit()

        if failed_records:
            self.send_failure_email_to_hr(failed_records)

        frappe.log_error('Shift Assignment creation finished')

    def on_cancel(self):
        frappe.db.sql("""delete from `tabShift Assignment` where schedule=%s """, (self.name))

    def get_dates(self,from_date,to_date):
        """get list of dates in between from date and to date"""
        no_of_days = date_diff(add_days(to_date, 1), from_date)
        dates = [add_days(from_date, i) for i in range(0, no_of_days)]
        return dates

    @frappe.whitelist()
    def validate(self):
        if self.attach:
            filepath = get_file(self.attach)
            pps = read_csv_content(filepath[1])
            shift_data = frappe.db.get_all('Shift Type', ['name'])
            shift_type_list =[]
            for shift in shift_data:
                shift_type_list += shift['name'] 
            idx = 0
            for pp in pps:
                idx += 1
                if pp[2] == "Shift":
                    continue
                shift_type = pp[2]
                
                if shift_type not in shift_type_list:
                    frappe.throw(
                        f"Shift is mandatory. Please check the row {idx} in the uploaded file."
                    )
        
        shift_assignment = frappe.db.sql("""select name from `tabShift Assignment` where department = '%s' and start_date between '%s' and '%s' and docstatus !=2 """ % (self.department, self.from_date, self.to_date), as_dict=True)
        if shift_assignment:
                self.attach = ''
                return 'Shift Schedule already submitted for the selected date'
        

    @frappe.whitelist()
    def show_summary(self):
        filepath = get_file(self.attach)
        pps = read_csv_content(filepath[1])
        data = ''
        wc1 = wc2 = wc3 = 0

        for pp in pps:
            if pp[2] == "1":
                wc1 += 1
            elif pp[2] == "2":
                wc2 += 1
            elif pp[2] == "3":
                wc3  += 1
        data += """
            <table style="border-collapse: collapse; width: 100%;">
                <tr>
                    <td style= "border: 1px solid black;text-align:center"><b>Shift</b></td>
                    <td style= "border: 1px solid black;text-align:center"><b>1</b></td>
                    <td style= "border: 1px solid black;text-align:center"><b>2</b></td>
                    <td style= "border: 1px solid black;text-align:center"><b>3</b></td>
                </tr>
                <tr>
                    <td style="border: 1px solid black;text-align:center"><b>Total</b></td>
                    <td style="border: 1px solid black;text-align:center">{}</td>
                    <td style="border: 1px solid black;text-align:center">{}</td>
                    <td style="border: 1px solid black;text-align:center">{}</td>
                </tr>
            </table>
        """.format(
            wc1, wc2, wc3
            
        )

        return data
    
   
    def send_failure_email_to_hr(self, failed_records):
        shift_schedule_url = get_url_to_form("Shift Schedule", self.name)

        from_date = formatdate(self.from_date, "dd-MM-yyyy")
        to_date = formatdate(self.to_date, "dd-MM-yyyy")

        failed_dates = sorted(set(record['date'] for record in failed_records))
        dates_list = "".join(f"<li>{formatdate(d, 'dd-MM-yyyy')}</li>" for d in failed_dates)

        message = f"""
            <p>Dear HR Team,</p>
            <p>
                Shift Assignments could not be created for some employees
                under Shift Schedule <a href="{shift_schedule_url}"><strong>{self.name}</strong></a>.
            </p>
            <p><b>From Date:</b> {from_date}</p>
            <p><b>To Date:</b> {to_date}</p>
            
            <p>Please review and recreate the failed assignments manually.</p>
            <p>Regards,<br>System</p>
        """

        frappe.sendmail(
            recipients=['t.kannadhasan@johoku.co.in','hr@johoku.co.in','saranya.v@johoku.co.in'],
            subject=f"[Action Required] Shift Assignment Creation Failed - {self.name}",
            message=message,
            now=True
        )
    
@frappe.whitelist()
def get_template():
    #use to get the csv file template for Overtime plan (add_header,add_data,get_data,writedata)
    args = frappe.local.form_dict

    if getdate(args.from_date) > getdate(args.to_date):
        frappe.throw(_("To Date should be greater than From Date"))

    w = UnicodeWriter()
    w = add_header(w)
    w = add_data(w, args)

    frappe.response['result'] = cstr(w.getvalue())
    frappe.response['type'] = 'csv'
    frappe.response['doctype'] = "Shift Assignment"

def add_header(w):
    w.writerow(['Employee ID','Employee Name','Shift','Department','Employement Type','Route No','Boarding Point'])
    return w

def add_data(w, args):
    data = get_data(args)
    writedata(w, data)
    return w

@frappe.whitelist()
def get_data(args):
    if args.department == "All Departments":
        employees = frappe.db.get_all('Employee',{'status':'Active'},['*'])
        data = []
        for emp in employees:
            row = [
                emp.name,emp.employee_name,emp.default_shift or '',emp.department,emp.employee_type or '',emp.route_no or '',emp.boarding_point or ''
            ]
            data.append(row)
    else:
        employees = frappe.db.get_all('Employee',{'status':'Active','department':args.department},['*'])
        data = []
        for emp in employees:
            row = [
                emp.name,emp.employee_name,emp.default_shift or '',emp.department,emp.employee_type or '',emp.route_no or '',emp.boarding_point or ''
            ]
            data.append(row)
    return data

@frappe.whitelist()
def writedata(w, data):
    for row in data:
        w.writerow(row)