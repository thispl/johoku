# # Copyright (c) 2024, TEAMPRO and contributors
# # For license information, please see license.txt

# import frappe
# from frappe.model.document import Document
# from datetime import datetime
# import openpyxl
# from openpyxl import Workbook
# from openpyxl.styles import Font, Alignment, Border, Side
# from six import BytesIO
# from datetime import datetime
# from datetime import datetime, timedelta
# from frappe.utils import (getdate, cint, add_months, date_diff, add_days, format_date,
#     nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
# import pandas as pd
# from collections import defaultdict
# from openpyxl.styles import GradientFill, PatternFill
# class CheckinWisePlanVsActualReport(Document):
#     pass

# @frappe.whitelist(allow_guest=True)
# def get_data_system(date, shift , department=None): 
#     date_  = datetime.strptime(date, "%Y-%m-%d").strftime('%d-%m-%Y')
#     data = f"""<h2 class='text-center' style="color: black;">Manpower Category wise plan vs Actual Summary</h2>
#             <div style="overflow-x: auto; color: black;">
#             <table class="text-center" style="overflow: hidden; white-space: wrap;">
#             <thead>
#             <tr>
#                 <td colspan="27">
                    
#                 </td>
#             </tr>
#             <tr style="background-color: #ffe5b4; font-weight: 500; color: black;">
#                 <td style="width: 200px;" colspan=1 class="border border-1 border-dark"></td>
#                 <td  colspan=17 class="border border-1 border-dark">
#                     <strong>Plan / Count
#                     </strong>
#                 </td>
#                 <td  colspan=5 class="border border-1 border-dark">
#                     <strong>Date: { date_ }
#                     </strong>
#                 </td>
#                 <td  colspan=3 class="border border-1 border-dark">
#                     <strong>Shift: { shift or "All Shift"}
#                     </strong>
#                 </td>
#             </tr>
#             <tr style="background-color: #ffe5b4; font-weight: 500; color: black;">
#                 <td rowspan=3 class="border border-1 border-dark" style="min-width: 200px;">Employee Category / Department</td>
#                 <td colspan=2 class="border border-1 border-dark" style="min-width: 100px;">Staff</td>
#                 <td colspan=2 class="border border-1 border-dark" style="min-width: 100px;">JOE</td>
#                 <td colspan=2 class="border border-1 border-dark" style="min-width: 100px;">Tech</td>
#                 <td colspan=2 class="border border-1 border-dark" style="min-width: 100px;">Trainee</td>
#                 <td colspan=2 class="border border-1 border-dark" style="min-width: 100px;">NAPS</td>
#                 <td colspan=2 class="border border-1 border-dark" style="min-width: 100px;">Contract(CL)</td>
#                 <td colspan=2 class="border border-1 border-dark" style="min-width: 100px;">New Joining Trainees</td>
#                 <td colspan=2 class="border border-1 border-dark" style="min-width: 100px;">Temporary CL</td>
#                 <td rowspan=3 class="border border-1 border-dark" style="min-width: 100px;">Total Plan</td>
                
#                 <td rowspan=3 class="border border-1 border-dark" style="min-width: 100px;">Cummulative Actual</td>
#                 <td rowspan=3 class="border border-1 border-dark" style="min-width: 100px;">Absent Gap (Plan-Actual)</td>
#                 <td rowspan=3 class="border border-1 border-dark" style="min-width: 100px;">Informed Leave(HRMS request approved)</td>
#                 <td rowspan=3 class="border border-1 border-dark" style="min-width: 100px;"> Un informed Leave(HRMS request not approved)</td>
#                 <td rowspan=3 class="border border-1 border-dark" style="min-width: 100px;">Total Gap</td>
#                 <td rowspan=3 class="border border-1 border-dark" style="min-width: 100px;">Remarks</td>
#                 <td rowspan=3 class="border border-1 border-dark" style="min-width: 100px;">Requested manpower</td>
#                 <td rowspan=3 class="border border-1 border-dark" style="min-width: 100px;">Given manpower</td>
                
#             </tr>
#             <tr style="background-color: #ffe5b4; font-weight: 500; color: black;">
#                 <td rowspan=2 class="border border-1 border-dark" style="min-width: 50px;">Plan</td>
#                 <td rowspan=2 class="border border-1 border-dark" style="min-width: 50px;">Actual</td>
#                 <td rowspan=2 class="border border-1 border-dark" style="min-width: 50px;">Plan</td>
#                 <td rowspan=2 class="border border-1 border-dark" style="min-width: 50px;">Actual</td>
#                 <td rowspan=2 class="border border-1 border-dark" style="min-width: 50px;">Plan</td>
#                 <td rowspan=2 class="border border-1 border-dark" style="min-width: 50px;">Actual</td>
#                 <td rowspan=2 class="border border-1 border-dark" style="min-width: 50px;">Plan</td>
#                 <td rowspan=2 class="border border-1 border-dark" style="min-width: 50px;">Actual</td>
#                 <td rowspan=2 class="border border-1 border-dark" style="min-width: 50px;">Plan</td>
#                 <td rowspan=2 class="border border-1 border-dark" style="min-width: 50px;">Actual</td>
#                 <td rowspan=2 class="border border-1 border-dark" style="min-width: 50px;">Plan</td>
#                 <td rowspan=2 class="border border-1 border-dark" style="min-width: 50px;">Actual</td>
#                 <td rowspan=2 class="border border-1 border-dark" style="min-width: 50px;">Plan</td>
#                 <td rowspan=2 class="border border-1 border-dark" style="min-width: 50px;">Actual</td>
#                 <td rowspan=2 class="border border-1 border-dark" style="min-width: 50px;">Plan</td>
#                 <td rowspan=2 class="border border-1 border-dark" style="min-width: 50px;">Actual</td>
#             </tr>
#         </thead>
#         <tbody>
#             """
#     # departments = frappe.get_all("Department",{"disabled": 0,"name": ["!=", "All Departments"]},["name"], order_by="name asc")
#     if department:
#         departments = [{"name": department}]
#     else:
#         departments = frappe.get_all("Department", {"disabled": 0, "name": ["!=", "All Departments"]}, ["name"], order_by="name asc")
#     if shift in ['1', '2']:
#         shift1 = shift
#         shift = f"shift = '{shift}'"
#         # shift_new =[shift]
#         shift_new = shift1
#     else:
#         shift1 = ['is', 'set'] 
#         shift_new =['1','2','3']
#         shift = "shift IN ('1', '2')"
#     # frappe.errprint(shift)
#     # frappe.errprint(shift)
#     total_planning_staff,total_plan_cl ,total_plan_dt, total_plan_iti,total_plan_naps,total_plan_trainee = 0,0,0,0,0,0
#     total_actual_dt,total_actual_staff,total_actual_naps,total_actual_iti,total_actual_cl, total_actual_trainee =0, 0,0,0,0,0
#     total_cumulative,total_coff,total_absent_gap,total_of_total_gap,total_od,total_permission,actual_leave,plan_leave,total_misspunch = 0,0,0,0,0,0,0,0,0
#     total_plan_total,total_actual_total =0, 0
#     total_plan_access_card,total_actual_access_card = 0,0
#     total_plan_new_joinee,total_actual_new_joinee = 0,0
#     total_cl_access_card_actual =0
#     for dept in departments:
#         category_order = {
#             "Staff": 1,
#             "DT": 2,
#             "ITI": 3,
#             "GT": 4,
#             "TT": 5,
#             "CL (Access Card)": 6,
#             "CL": 7, 
#             "CL(Oneday)": 8,
#             "Executive": 9 ,
#             'Naps': 10,
#             "New CL": 11,
#             "New Staff": 12,
#             "New Trainees": 13
#         }
#         remarks = ""
#         if dept["name"] != "All Departments":
#             emp_category_name = ['Staff','Manager','ITI','TT','Naps','CL','GT','New CL','New Staff','New Trainees','DT']
#             # planed_emp = frappe.db.get_all("Shift Assignment",{'department': dept.name,'start_date': date ,'shift_type':shift,'docstatus': 1,'employee_category': ['in', emp_category_name]},pluck="employee")
#             planed_emp = frappe.db.get_all("Shift Assignment",{'department': dept["name"],'start_date': date,'shift_type':shift1,'docstatus': 1,'employee_category': ['in',['Staff','Manager','ITI','TT','Naps','CL','GT','New CL','New Staff','New Trainees','DT']]},pluck="employee")
#             query = """
#                 SELECT DISTINCT employee
#                 FROM `tabEmployee Checkin`
#                 WHERE DATE(time) = %s
#                 AND log_type = 'IN'
#                 AND shift IN %s
#                 AND department = %s
#                 AND employee_category IN %s
#                 ORDER BY time
#             """
#             params = (date, tuple(shift_new), dept["name"], tuple(emp_category_name))
#             result = frappe.db.sql(query, params, as_dict=True)

#             present_emp = {row["employee"] for row in result}
#             frappe.errprint(result)
#             frappe.errprint(f"Planned Employees: {planed_emp}")
#             frappe.errprint(f"Present Employees: {present_emp}")
#             # for i in planed_emp:
#             #     if i not in present_emp:
#             #         emp_name = frappe.db.get_value("Employee",i,"employee_name")
#             #         if remarks =='':
#             #             remarks+=f"{i} : {emp_name}"
#             #         else:
#             #             remarks+=f", {i} : {emp_name}"

#             emp_list = []

#             for i in planed_emp:
#                 if i not in present_emp:
#                     emp_data = frappe.db.get_value(
#                         "Employee",
#                         i,
#                         ["employee_name", "employee_category"],
#                         as_dict=True
#                     )
#                     if emp_data:
#                         emp_list.append({
#                             "id": i,
#                             "name": emp_data.employee_name,
#                             "category": emp_data.employee_category,
#                             "order": category_order.get(emp_data.employee_category, 99)
#                         })

#             category_groups = defaultdict(list)
#             for emp in emp_list:
#                 category_groups[emp['category']].append(f"{emp['id']} : {emp['name']}")

#             # remarks = "<br>".join([
#             #     f"<span style='color: red;'>{category}</span> - {', '.join(category_groups[category])}"
#             #     for category in sorted(category_groups.keys(), key=lambda x: category_order.get(x, 99))
#             # ])
            
#             # remarks = "<br>".join([
#             #     f"<span style='color: red;'>({len(category_groups[category])}) : {category}</span> : {', '.join(category_groups[category])}"
#             #     for category in sorted(category_groups.keys(), key=lambda x: category_order.get(x, 99))
#             #     ])
            
#             category_colors = {
#                 "Staff": "blue",
#                 "DT": "orange",
#                 "ITI": "green",
#                 "GT": "purple",
#                 "TT": "brown",
#                 "CL (Access Card)": "darkred",
#                 "CL": "red",
#                 "CL(Oneday)": "crimson",
#                 "Executive": "darkblue",
#                 "Naps": "teal",
#                 "New CL": "magenta",
#                 "New Staff": "darkgreen",
#                 "New Trainees": "darkorange"
#             }

#             remarks = "<br>".join([
#                 f"<span style='color:{category_colors.get(category, 'black')};'>"
#                 f"({len(category_groups[category])}) : {category} : "
#                 f"{', '.join(category_groups[category])}"
#                 f"</span>"
#                 for category in sorted(category_groups.keys(), key=lambda x: category_order.get(x, 99))
#             ])

#             frappe.errprint(f"Remarks: {remarks}")            
#             # Get employee categories and prepare row structure
#             employee_categories = frappe.get_all("Employee Category", fields=["name"], order_by='name')
#             total_plan= 0
    
#             plan_staff, actual_staff, plan_cl, plan_dt, plan_gt, plan_iti, plan_naps, actual_cl, actual_dt, actual_new_joinee, actual_access_card = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
#             plan_tt, actual_tt, actual_gt, actual_iti, actual_naps, actual_trainee, plan_trainee, plan_new_joinee, plan_access_card = 0, 0, 0, 0, 0, 0, 0, 0, 0
#             actual_total_permission, actual_total_misspunch, actual_total_coff, actual_total_od, actual_total_absent_gap, actual_total_cumulative = 0, 0, 0, 0, 0, 0
#             actual_total_leave_application, total_leave_application_not_approved, total_gap = 0, 0, 0
#             new_trainee_plan_access_card,new_staff_plan_access_card,new_staff_actual_access_card,new_trainee_actual_access_card =0,0,0,0
#             cl_access_card_actual,cl_access_card_plan =0,0
#             # Loop through employee categories
#             for emp_category in employee_categories:
#                 emp_category_name = emp_category['name']
#                 employee_category = 'employee_category'
#                 actual_field = 'category'
#                 if emp_category_name == "Staff":
#                     plan_staff = frappe.db.count("Shift Assignment", {
#                         'department': dept["name"],
#                         employee_category: emp_category_name,
#                         'start_date': date,
#                         'shift_type':shift1,
#                         'docstatus': 1
#                     })
#                     frappe.errprint(plan_staff)
#                     query = f"""
#                         SELECT DISTINCT employee, COUNT(*) as count
#                         FROM `tabEmployee Checkin`
#                         WHERE DATE(time) = %s 
#                         AND log_type = 'IN' 
#                         AND {shift}
#                         AND department = %s 
#                         AND employee_category = %s
#                         GROUP BY employee
#                         ORDER BY time
#                     """
#                     result = frappe.db.sql(query, (date, dept["name"], emp_category_name), as_dict=True)
#                     actual_staff = len(result)
#                 elif emp_category_name == "DT":
#                     plan_dt = frappe.db.count("Shift Assignment", {
#                         'department': dept["name"],
#                         employee_category: emp_category_name,
#                         'start_date': date,
#                         'shift_type':shift1,
#                         'docstatus': 1
#                     })
#                     query = f"""
#                         SELECT DISTINCT employee, COUNT(*) as count
#                         FROM `tabEmployee Checkin`
#                         WHERE DATE(time) = %s 
#                         AND log_type = 'IN' 
#                         AND {shift} 
#                         AND department = %s 
#                         AND employee_category = %s
#                         GROUP BY employee
#                         ORDER BY time
#                     """
#                     result = frappe.db.sql(query, (date, dept["name"], emp_category_name), as_dict=True)
#                     actual_dt = len(result)
#                 elif emp_category_name == "ITI":
#                     plan_iti = frappe.db.count("Shift Assignment", {
#                         'department': dept["name"],
#                         employee_category: emp_category_name,
#                         'start_date': date,
#                         'shift_type':shift1,
#                         'docstatus': 1
#                     })
#                     query = f"""
#                         SELECT DISTINCT employee, COUNT(*) as count
#                         FROM `tabEmployee Checkin`
#                         WHERE DATE(time) = %s 
#                         AND log_type = 'IN' 
#                         AND {shift} 
#                         AND department = %s 
#                         AND employee_category = %s
#                         GROUP BY employee
#                         ORDER BY time
#                     """
#                     result = frappe.db.sql(query, (date, dept["name"], emp_category_name), as_dict=True)
#                     actual_iti = len(result)
#                 elif emp_category_name == "TT":
#                     plan_tt = frappe.db.count("Shift Assignment", {
#                         'department': dept["name"],
#                         employee_category: emp_category_name,
#                         'start_date': date,
#                         'shift_type':shift1,
#                         'docstatus': 1
#                     })
#                     query = f"""
#                         SELECT DISTINCT employee, COUNT(*) as count
#                         FROM `tabEmployee Checkin`
#                         WHERE DATE(time) = %s 
#                         AND log_type = 'IN' 
#                         AND {shift} 
#                         AND department = %s 
#                         AND employee_category = %s
#                         GROUP BY employee
#                         ORDER BY time
#                     """
#                     result = frappe.db.sql(query, (date, dept["name"], emp_category_name), as_dict=True)
#                     actual_tt = len(result)
#                 elif emp_category_name == "Naps":
#                     plan_naps = frappe.db.count("Shift Assignment", {
#                         'department': dept["name"],
#                         employee_category: emp_category_name,
#                         'start_date': date,
#                         'shift_type':shift1,
#                         'docstatus': 1
#                     })
#                     query = f"""
#                         SELECT DISTINCT employee, COUNT(*) as count
#                         FROM `tabEmployee Checkin`
#                         WHERE DATE(time) = %s 
#                         AND log_type = 'IN' 
#                         AND {shift}
#                         AND department = %s 
#                         AND employee_category = %s
#                         GROUP BY employee
#                         ORDER BY time
#                     """
#                     result = frappe.db.sql(query, (date, dept["name"], emp_category_name), as_dict=True)
#                     actual_naps = len(result)
#                 elif emp_category_name == "CL":
#                     plan_cl = frappe.db.count("Shift Assignment", {
#                         'department': dept["name"],
#                         employee_category: emp_category_name,
#                         'start_date': date,
#                         'shift_type':shift1,
#                         'docstatus': 1
#                     })
#                     query = f"""
#                         SELECT DISTINCT employee, COUNT(*) as count
#                         FROM `tabEmployee Checkin`
#                         WHERE DATE(time) = %s 
#                         AND log_type = 'IN' 
#                         AND {shift}
#                         AND department = %s 
#                         AND employee_category = %s
#                         GROUP BY employee
#                         ORDER BY time
#                     """
#                     result = frappe.db.sql(query, (date, dept["name"], emp_category_name), as_dict=True)
#                     actual_cl = len(result)
                
#                 elif emp_category_name == "GT":
#                     plan_gt = frappe.db.count("Shift Assignment", {
#                         'department': dept["name"],
#                         employee_category: emp_category_name,
#                         'start_date': date,
#                         'shift_type':shift1,
#                         'docstatus': 1
#                     })
#                     query = f"""
#                         SELECT DISTINCT employee, COUNT(*) as count
#                         FROM `tabEmployee Checkin`
#                         WHERE DATE(time) = %s 
#                         AND log_type = 'IN' 
#                         AND {shift} 
#                         AND department = %s 
#                         AND employee_category = %s
#                         GROUP BY employee
#                         ORDER BY time
#                     """
#                     result = frappe.db.sql(query, (date, dept["name"], emp_category_name), as_dict=True)
#                     actual_gt = len(result)
#                 elif emp_category_name == "New Staff":
#                     new_staff_plan_access_card = frappe.db.count("Shift Assignment", {
#                         'department': dept["name"],
#                         employee_category: emp_category_name,
#                         'start_date': date,
#                         'shift_type':shift1,
#                         'docstatus': 1
#                     })
#                     query = f"""
#                         SELECT DISTINCT employee, COUNT(*) as count
#                         FROM `tabEmployee Checkin`
#                         WHERE DATE(time) = %s 
#                         AND log_type = 'IN' 
#                         AND {shift} 
#                         AND department = %s 
#                         AND employee_category = %s
#                         GROUP BY employee
#                         ORDER BY time
#                     """
#                     result = frappe.db.sql(query, (date, dept["name"], emp_category_name), as_dict=True)
#                     new_staff_actual_access_card = len(result)
#                 elif emp_category_name == "New Trainees":
#                     new_trainee_plan_access_card = frappe.db.count("Shift Assignment", {
#                         'department': dept["name"],
#                         employee_category: emp_category_name,
#                         'start_date': date,
#                         'shift_type':shift1,
#                         'docstatus': 1
#                     })
#                     query = f"""
#                         SELECT DISTINCT employee, COUNT(*) as count
#                         FROM `tabEmployee Checkin`
#                         WHERE DATE(time) = %s 
#                         AND log_type = 'IN' 
#                         AND {shift} 
#                         AND department = %s 
#                         AND employee_category = %s
#                         GROUP BY employee
#                         ORDER BY time
#                     """
#                     result = frappe.db.sql(query, (date, dept["name"], emp_category_name), as_dict=True)
#                     new_trainee_actual_access_card = len(result)
#                 elif emp_category_name == "New CL":
#                     plan_access_card = frappe.db.count("Shift Assignment", {
#                         'department': dept["name"],
#                         employee_category: emp_category_name,
#                         'start_date': date,
#                         'shift_type':shift1,
#                         'docstatus': 1
#                     })
#                     query = f"""
#                         SELECT DISTINCT employee, COUNT(*) as count
#                         FROM `tabEmployee Checkin`
#                         WHERE DATE(time) = %s 
#                         AND log_type = 'IN' 
#                         AND {shift} 
#                         AND department = %s 
#                         AND employee_category = %s
#                         GROUP BY employee
#                         ORDER BY time
#                     """
#                     result = frappe.db.sql(query, (date, dept["name"], emp_category_name), as_dict=True)
#                     actual_access_card = len(result)
#                 elif emp_category_name == "CL (Access Card)":
#                     cl_access_card_plan = frappe.db.count("Shift Assignment", {
#                         'department': dept["name"],
#                         employee_category: emp_category_name,
#                         'start_date': date,
#                         'shift_type':shift1,
#                         'docstatus': 1
#                     })
#                     query = f"""
#                         SELECT DISTINCT employee, COUNT(*) as count
#                         FROM `tabEmployee Checkin`
#                         WHERE DATE(time) = %s 
#                         AND log_type = 'IN' 
#                         AND {shift} 
#                         AND department = %s 
#                         AND employee_category = %s
#                         GROUP BY employee
#                         ORDER BY time
#                     """
#                     result = frappe.db.sql(query, (date, dept["name"], emp_category_name), as_dict=True)
#                     cl_access_card_actual = len(result)
#             plan_new_joinee = new_trainee_plan_access_card + new_staff_plan_access_card
#             actual_new_joinee = new_staff_actual_access_card + new_trainee_actual_access_card
#             actual_trainee = actual_gt + actual_tt
#             plan_trainee = plan_gt + plan_tt
#             plan_total = frappe.db.count("Shift Assignment", {
#                 'department': dept["name"],
#                 'start_date': date,
#                 'employee_category': ('not in', ['CL (Access Card)']),
#                 'shift_type':shift1,
#                 'docstatus': 1
#             })
#             query = f"""
#                         SELECT DISTINCT employee, COUNT(*) as count
#                         FROM `tabEmployee Checkin`
#                         WHERE DATE(time) = %s 
#                         AND log_type = 'IN' 
#                         AND employee_category NOT IN ('CL (Access Card)')
#                         AND  {shift}
#                         AND department = %s 
#                         GROUP BY employee
#                         ORDER BY time
#                     """
#             result = frappe.db.sql(query, (date, dept["name"]), as_dict=True)
#             # frappe.errprint(query)
#             actual_total = len(result)
#             actual_total_permission = frappe.db.count("Permission Request", {
#                 'department': dept["name"],
#                 'shift': shift,
#                 'workflow_state': ["=", "Approved"],
#                 'employee_category': ('not in', ['CL (Access Card)']),
#                 'docstatus': 1,
#                 'permission_date': ["between", [date, date]]
#             })
#             actual_total_misspunch = frappe.db.count("Miss Punch Application", {
#                 'department': dept["name"],
#                 'shift': shift,
#                 'workflow_state': ["=", "Approved"],
#                 'employee_category': ('not in', ['CL (Access Card)']),
#                 'docstatus': 1,
#                 'date': ["between", [date, date]]
#             })
#             actual_total_od = frappe.db.sql("""
#                 SELECT COUNT(*)
#                 FROM `tabOn Duty Application`
#                 WHERE workflow_state = "Approved"
#                 AND docstatus = 1
#                 AND category NOT IN ('CL (Access Card)')
#                 AND department = %(department)s
#                 AND %(shift)s
#                 AND (
#                     od_date BETWEEN %(from_date)s AND %(to_date)s
#                     OR to_date BETWEEN %(from_date)s AND %(to_date)s
#                     OR (od_date < %(from_date)s AND to_date > %(to_date)s)
#                 )
#             """, {
#                 "from_date": date,
#                 "to_date": date,
#                 "department": dept["name"],
#                 "shift": shift,
#             })[0][0]
#             approved_leaves  = frappe.db.sql("""
#                 select employee
#                 from `tabLeave Application`
#                 where workflow_state="Approved" and docstatus=1 and department = %(department)s
#                     and (from_date between %(from_date)s and %(to_date)s
#                         or to_date between %(from_date)s and %(to_date)s
#                         or (from_date < %(from_date)s and to_date > %(to_date)s))
#                 """, {
#                     "from_date": date,
#                     "to_date": date,
#                     "department":dept["name"]
#                 },as_dict = True)
#             # frappe.errprint(approved_leaves)
#             for leave in approved_leaves:
#                 shift_count_leaves = frappe.db.count(
#                     'Shift Assignment',
#                     {
#                         'employee': leave['employee'],
#                         'employee_category': ('not in', ['CL (Access Card)']),       
#                         'start_date': date,         
#                         'end_date': date,
#                         'shift_type': shift,              
#                         'docstatus': ('!=', 2)           
#                     }
#                 )
#                 actual_total_leave_application += shift_count_leaves
#             not_approved_leaves = frappe.db.sql("""
#                 select employee
#                 from `tabLeave Application`
#                 where docstatus = 0 and department = %(department)s
#                     and (from_date between %(from_date)s and %(to_date)s
#                         or to_date between %(from_date)s and %(to_date)s
#                         or (from_date < %(from_date)s and to_date > %(to_date)s))
#                 """, {
#                     "from_date": date,
#                     "to_date": date,
#                     "department":dept["name"]
#                 },
#             as_dict = True)
#             # frappe.errprint(not_approved_leaves)
#             for leave in not_approved_leaves:
#                 shift_count_leaves_ = frappe.db.count(
#                     'Shift Assignment',
#                     {
#                         'employee': leave['employee'],       
#                         'start_date': date,         
#                         'end_date': date,
#                         'employee_category': ('not in', ['CL (Access Card)']),
#                         'shift_type': shift,              
#                         'docstatus': ('!=', 2)           
#                     }
#                 )
#                 total_leave_application_not_approved += shift_count_leaves_
#             actual_total_cumulative = actual_total + actual_total_misspunch + actual_total_permission + actual_total_od
#             actual_total_absent_gap = plan_total - actual_total_cumulative
#             total_gap = total_leave_application_not_approved + actual_total_leave_application
#             total_planning_staff += plan_staff 
#             total_actual_staff += actual_staff
#             total_plan_dt += plan_dt
#             total_actual_dt += actual_dt
#             total_plan_iti += plan_iti
#             total_plan_trainee += plan_trainee
#             total_plan_naps +=plan_naps
#             total_plan_cl += plan_cl
#             total_actual_iti += actual_iti
#             total_actual_trainee += actual_trainee
#             total_actual_naps += actual_naps
#             total_actual_cl += actual_cl
#             plan_leave += actual_total_leave_application
#             actual_leave += total_leave_application_not_approved
#             total_of_total_gap +=total_gap
#             total_permission += actual_total_permission
#             total_misspunch += actual_total_misspunch
#             total_od += actual_total_od
#             total_coff += actual_total_coff
#             total_plan_total +=plan_total
#             total_actual_total += actual_total
#             total_cumulative += actual_total_cumulative
#             total_absent_gap += actual_total_absent_gap
#             total_actual_access_card += actual_access_card
#             total_plan_access_card += plan_access_card
#             total_actual_new_joinee +=actual_new_joinee
#             total_plan_new_joinee+=plan_new_joinee
#             total_cl_access_card_actual += cl_access_card_actual
#             data += f"""
#                 <tr>
#                     <td class="border border-1 border-dark text-left pl-3">{dept["name"]}</td>
#                     <td class="border border-1 border-dark">{plan_staff}</td>
#                     <td class="border border-1 border-dark">{actual_staff}</td>
#                     <td class="border border-1 border-dark">{plan_dt}</td>
#                     <td class="border border-1 border-dark">{actual_dt}</td>
#                     <td class="border border-1 border-dark">{plan_iti}</td>
#                     <td class="border border-1 border-dark">{actual_iti}</td>
#                     <td class="border border-1 border-dark">{plan_trainee}</td>
#                     <td class="border border-1 border-dark">{actual_trainee}</td>
#                     <td class="border border-1 border-dark">{plan_naps}</td>
#                     <td class="border border-1 border-dark">{actual_naps}</td>
#                     <td class="border border-1 border-dark">{plan_cl}</td>
#                     <td class="border border-1 border-dark">{actual_cl}</td>
#                     <td class="border border-1 border-dark">{plan_new_joinee}</td>
#                     <td class="border border-1 border-dark">{actual_new_joinee}</td>
#                     <td class="border border-1 border-dark">{plan_access_card}</td>
#                     <td class="border border-1 border-dark">{actual_access_card}</td>
#                     <td class="border border-1 border-dark">{plan_total}</td>
                     
#                     <td class="border border-1 border-dark">{actual_total_cumulative}</td>
#                     <td class="border border-1 border-dark">{actual_total_absent_gap}</td>
#                     <td class="border border-1 border-dark">{actual_total_leave_application}</td>
#                     <td class="border border-1 border-dark">{total_leave_application_not_approved}</td>
#                     <td class="border border-1 border-dark">{total_gap}</td>
#                     <td class="border border-1 border-dark" style="white-space: nowrap; overflow-x: auto; max-width:500px;text-align:left;">{remarks}</td>
#                     <td class="border border-1 border-dark"></td>
#                     <td class="border border-1 border-dark">{cl_access_card_actual}</td>
                    
                    
#                 </tr>
#             """
    
#     data += f"""
#                     <tr style="background-color: #ffe5b4; font-weight: 700; color: black;">
#                         <td class="border border-1 border-dark">Total</td>
#                         <td class="border border-1 border-dark">{total_planning_staff}</td>
#                         <td class="border border-1 border-dark">{total_actual_staff}</td>
#                         <td class="border border-1 border-dark">{total_plan_dt}</td>
#                         <td class="border border-1 border-dark">{total_actual_dt}</td>
#                         <td class="border border-1 border-dark">{total_plan_iti}</td>
#                         <td class="border border-1 border-dark">{total_actual_iti}</td>
#                         <td class="border border-1 border-dark">{total_plan_trainee}</td>
#                         <td class="border border-1 border-dark">{total_actual_trainee}</td>
#                         <td class="border border-1 border-dark">{total_plan_naps}</td>
#                         <td class="border border-1 border-dark">{total_actual_naps}</td>
#                         <td class="border border-1 border-dark">{total_plan_cl}</td>
#                         <td class="border border-1 border-dark">{total_actual_cl}</td>
#                         <td class="border border-1 border-dark">{total_plan_new_joinee}</td>
#                         <td class="border border-1 border-dark">{total_actual_new_joinee}</td>
#                         <td class="border border-1 border-dark">{total_plan_access_card}</td>
#                         <td class="border border-1 border-dark">{total_actual_access_card}</td>
#                         <td class="border border-1 border-dark">{total_plan_total}</td>
#                         <td class="border border-1 border-dark">{total_cumulative}</td>
#                         <td class="border border-1 border-dark">{total_absent_gap}</td>
#                         <td class="border border-1 border-dark">{plan_leave}</td>
#                         <td class="border border-1 border-dark">{actual_leave}</td>
#                         <td class="border border-1 border-dark">{total_of_total_gap}</td>
#                         <td class="border border-1 border-dark"></td>
#                         <td class="border border-1 border-dark"></td>
#                         <td class="border border-1 border-dark">{total_cl_access_card_actual}</td>
                        
#                     </tr>
#                  </tbody></table></div>
#              """
#     return data



# @frappe.whitelist()
# def download():
#     filename = 'EmployeeCheckinWisePlanVsActualReport.xlsx'
#     build_xlsx_response(filename)
# def make_xlsx(sheet_name=None):
#     args = frappe.local.form_dict
#     wb = Workbook()
#     ws = wb.active
#     ws.title = sheet_name if sheet_name else 'Sheet1'
#     # frappe.errprint(args)
#     data = get_data(args)
#     if not data:  # Check if data is empty or None
#         frappe.throw("No data available to generate the report.")
    
#     for row in data:
#         if not isinstance(row, (list, tuple)):
#             row = [row]  # Convert to a list if it's a single item (likely a string)
#         ws.append(row)

#     # Merging cells based on the number of rows in the header
#     ws.merge_cells(start_row=3, start_column=1, end_row=4, end_column=1)
#     ws.merge_cells(start_row=1, start_column=1, end_row=2, end_column=28)
#     ws.merge_cells(start_row=3, start_column=2, end_row=4, end_column=18)
#     ws.merge_cells(start_row=3, start_column=19, end_row=4, end_column=24)
#     ws.merge_cells(start_row=3, start_column=25, end_row=4, end_column=28)
#     ws.merge_cells(start_row=5, start_column=1, end_row=8, end_column=1)
#     ws.merge_cells(start_row=5, start_column=18, end_row=8, end_column=18)
#     ws.merge_cells(start_row=5, start_column=2, end_row=7, end_column=3)
#     ws.merge_cells(start_row=5, start_column=4, end_row=7, end_column=5)
#     ws.merge_cells(start_row=5, start_column=6, end_row=7, end_column=7)
#     ws.merge_cells(start_row=5, start_column=8, end_row=7, end_column=9)
#     ws.merge_cells(start_row=5, start_column=10, end_row=7, end_column=11)
#     ws.merge_cells(start_row=5, start_column=12, end_row=7, end_column=13)
#     ws.merge_cells(start_row=5, start_column=14, end_row=7, end_column=15)
#     ws.merge_cells(start_row=5, start_column=16, end_row=7, end_column=17)
#     ws.merge_cells(start_row=8, start_column=2, end_row=8, end_column=2)
#     ws.merge_cells(start_row=8, start_column=3, end_row=8, end_column=3)
#     ws.merge_cells(start_row=8, start_column=4, end_row=8, end_column=4)
#     ws.merge_cells(start_row=8, start_column=5, end_row=8, end_column=5)
#     ws.merge_cells(start_row=8, start_column=6, end_row=8, end_column=6)
#     ws.merge_cells(start_row=8, start_column=7, end_row=8, end_column=7)
#     ws.merge_cells(start_row=8, start_column=8, end_row=8, end_column=8)
#     ws.merge_cells(start_row=8, start_column=9, end_row=8, end_column=9)
#     ws.merge_cells(start_row=8, start_column=10, end_row =8, end_column=10)
#     ws.merge_cells(start_row=8, start_column=11, end_row =8, end_column=11)
#     ws.merge_cells(start_row=8, start_column=12, end_row =8, end_column=12)
#     ws.merge_cells(start_row=8, start_column=13, end_row =8, end_column=13)
#     ws.merge_cells(start_row=8, start_column=14, end_row =8, end_column=14)
#     ws.merge_cells(start_row=8, start_column=15, end_row =8, end_column=15)
#     ws.merge_cells(start_row=8, start_column=16, end_row =8, end_column=16)
#     ws.merge_cells(start_row=8, start_column=17, end_row =8, end_column=17)
#     # ws.merge_cells(start_row=5, start_column=19, end_row=7, end_column=22)
#     ws.merge_cells(start_row=5, start_column=19, end_row=8, end_column=19)
#     ws.merge_cells(start_row=5, start_column=20, end_row=8, end_column=20)
#     ws.merge_cells(start_row=5, start_column=21, end_row=8, end_column=22)
#     ws.merge_cells(start_row=5, start_column=23, end_row=8, end_column=24)
#     ws.merge_cells(start_row=5, start_column=25, end_row=8, end_column=25)
#     ws.merge_cells(start_row=5, start_column=26, end_row=8, end_column=26)
#     ws.merge_cells(start_row=5, start_column=27, end_row=8, end_column=27)
#     ws.merge_cells(start_row=5, start_column=28, end_row=8, end_column=28)
#     # ws.merge_cells(start_row=7, start_column=19, end_row=8, end_column=19)
#     # ws.merge_cells(start_row=8, start_column=19, end_row=8, end_column=22)
#     for x in range(9,ws.max_row+1):
#         ws.merge_cells(start_row=x, start_column=21, end_row=x, end_column=22)
#         ws.merge_cells(start_row=x, start_column=23, end_row=x, end_column=24)

#     apply_styles(ws)
#     set_column_widths(ws)

#     xlsx_file = BytesIO()
#     wb.save(xlsx_file)
#     xlsx_file.seek(0)
#     return xlsx_file

# def apply_styles(ws):
#     align_center = Alignment(horizontal='center', vertical='center', wrap_text=True)
#     align_right = Alignment(horizontal='right', vertical='top', wrap_text=True)
#     align_left = Alignment(horizontal='left', vertical='top', wrap_text=True)
#     header_font = Font(bold=True, size=14)
#     text_font = Font(bold=True, size=8)
#     text_font_header = Font(bold=True, size=12)
#     text_font_data = Font(bold=False, size=9)
#     border = Border(
#         left=Side(border_style='thin'),
#         right=Side(border_style='thin'),
#         top=Side(border_style='thin'),
#         bottom=Side(border_style='thin')
#     )
#     for rows in ws.iter_rows(min_row=1, max_row=8, min_col=1, max_col = ws.max_column):
#         for cell in rows:
#             cell.fill = PatternFill(fgColor="ffe5b4", fill_type = "solid")
#     for rows in ws.iter_rows(min_row=ws.max_row, max_row=ws.max_row, min_col=1, max_col = ws.max_column):
#         for cell in rows:
#             cell.fill = PatternFill(fgColor="ffe5b4", fill_type = "solid")      
#     for rows in ws.iter_rows(min_row=1, max_row=2, min_col=1, max_col = ws.max_column):
#         for cell in rows:
#             cell.font = header_font
#             cell.alignment = align_center
#             cell.border = border

#     for rows in ws.iter_rows(min_row=3, max_row=4, min_col=2, max_col=18):
#         for cell in rows:
#             cell.font = text_font_header
#             cell.alignment = align_center
#             cell.border = border
#     for rows in ws.iter_rows(min_row=3, max_row=4, min_col=1, max_col=2):
#         for cell in rows:
#             cell.font = text_font_header
#             cell.alignment = align_center
#             cell.border = border
#     for rows in ws.iter_rows(min_row=3, max_row=4, min_col=19, max_col=24):
#         for cell in rows:
#             cell.font = text_font_header
#             cell.alignment = align_center
#             cell.border = border
#     for rows in ws.iter_rows(min_row=3, max_row=4, min_col=25, max_col = ws.max_column):
#         for cell in rows:
#             cell.font = text_font_header
#             cell.alignment = align_center
#             cell.border = border
#     for rows in ws.iter_rows(min_row=5, max_row=7, min_col=1, max_col=2):
#         for cell in rows:
#             cell.font = text_font
#             cell.alignment = align_center
#             cell.border = border
#     for rows in ws.iter_rows(min_row=5, max_row=7, min_col=2, max_col=3):
#         for cell in rows:
#             cell.font = text_font
#             cell.alignment = align_center
#             cell.border = border
#     for rows in ws.iter_rows(min_row=5, max_row=7, min_col=4, max_col=5):
#         for cell in rows:
#             cell.font = text_font
#             cell.alignment = align_center
#             cell.border = border
#     for rows in ws.iter_rows(min_row=5, max_row=7, min_col=6, max_col=7):
#         for cell in rows:
#             cell.font = text_font
#             cell.alignment = align_center
#             cell.border = border
#     for rows in ws.iter_rows(min_row=5, max_row=7, min_col=8, max_col=9):
#         for cell in rows:
#             cell.font = text_font
#             cell.alignment = align_center
#             cell.border = border
#     for rows in ws.iter_rows(min_row=5, max_row=7, min_col=10, max_col=11):
#         for cell in rows:
#             cell.font = text_font
#             cell.alignment = align_center
#             cell.border = border
#     for rows in ws.iter_rows(min_row=5, max_row=7, min_col=12, max_col=13):
#         for cell in rows:
#             cell.font = text_font
#             cell.alignment = align_center
#             cell.border = border
#     for rows in ws.iter_rows(min_row=5, max_row=7, min_col=14, max_col=15):
#         for cell in rows:
#             cell.font = text_font
#             cell.alignment = align_center
#             cell.border = border
#     for rows in ws.iter_rows(min_row=5, max_row=7, min_col=16, max_col=17):
#         for cell in rows:
#             cell.font = text_font
#             cell.alignment = align_center
#             cell.border = border
#     for rows in ws.iter_rows(min_row=5, max_row=7, min_col=18, max_col=18):
#         for cell in rows:
#             cell.font = text_font
#             cell.alignment = align_center
#             cell.border = border
#     for x in range(2,19):
#         for rows in ws.iter_rows(min_row=8, max_row=8, min_col=x, max_col=x):
#             for cell in rows:
#                 cell.font = text_font
#                 cell.alignment = align_center
#                 cell.border = border
    
#     # for rows in ws.iter_rows(min_row=8, max_row=9, min_col=20, max_col=20):
#     #     for cell in rows:
#     #         cell.font = text_font
#     #         cell.alignment = align_center
#     #         cell.border = border
#     for rows in ws.iter_rows(min_row=8, max_row=8, min_col=18, max_col=18):
#         for cell in rows:
#             cell.font = text_font
#             cell.alignment = align_center
#             cell.border = border
#     for rows in ws.iter_rows(min_row=5, max_row=7, min_col=19, max_col=19):
#         for cell in rows:
#             cell.font = text_font
#             cell.alignment = align_center
#             cell.border = border
#     # for rows in ws.iter_rows(min_row=8, max_row=7, min_col=19, max_col=22):
#     #     for cell in rows:
#     #         cell.font = text_font
#     #         cell.alignment = align_center
#     #         cell.border = border
#     # for rows in ws.iter_rows(min_row=8, max_row=9, min_col=21, max_col=21):
#     #     for cell in rows:
#     #         cell.font = text_font
#     #         cell.alignment = align_center
#     #         cell.border = border
#     # for rows in ws.iter_rows(min_row=8, max_row=9, min_col=22, max_col=22):
#     #     for cell in rows:
#     #         cell.font = text_font
#     #         cell.alignment = align_center
#     #         cell.border = border
#     for rows in ws.iter_rows(min_row=5, max_row=7, min_col=20, max_col=20):
#         for cell in rows:
#             cell.font = text_font
#             cell.alignment = align_center
#             cell.border = border
#     for rows in ws.iter_rows(min_row=5, max_row=7, min_col=21, max_col=21):
#         for cell in rows:
#             cell.font = text_font
#             cell.alignment = align_center
#             cell.border = border
#     for rows in ws.iter_rows(min_row=5, max_row=7, min_col=22, max_col=22):
#         for cell in rows:
#             cell.font = text_font
#             cell.alignment = align_center
#             cell.border = border
#     for rows in ws.iter_rows(min_row=5, max_row=7, min_col=23, max_col=25):
#         for cell in rows:
#             cell.font = text_font
#             cell.alignment = align_center
#             cell.border = border
#     for x in range(26,29):
#         for rows in ws.iter_rows(min_row=5, max_row=7, min_col=x, max_col=x):
#             for cell in rows:
#                 cell.font = text_font
#                 cell.alignment = align_center
#                 cell.border = border
#     # for rows in ws.iter_rows(min_row=5, max_row=7, min_col=19, max_col=23):
#     #     for cell in rows:
#     #         cell.font = text_font
#     #         cell.alignment = align_center
#     #         cell.border = border
#     # for rows in ws.iter_rows(min_row=8, max_row=7, min_col=20, max_col=21):
#     #     for cell in rows:
#     #         cell.font = text_font
#     #         cell.alignment = align_center
#     #         cell.border = border
#     # for rows in ws.iter_rows(min_row=8, max_row=9, min_col=19, max_col=19):
#     #     for cell in rows:
#     #         cell.font = text_font
#     #         cell.alignment = align_center
#     #         cell.border = border
#     for rows in ws.iter_rows(min_row=3, max_row=4, min_col=1, max_col=1):
#         for cell in rows:
#             cell.font = text_font
#             cell.alignment = align_center
#             cell.border = border
#     for rows in ws.iter_rows(min_row=8, max_row=8, min_col=1, max_col=1):
#         for cell in rows:
#             cell.font = text_font
#             cell.alignment = align_center
#             cell.border = border
#     for x in range (9,ws.max_row+1):
#         for rows in ws.iter_rows(min_row=x, max_row=x, min_col=23, max_col=24):
#             for cell in rows:
#                 cell.font = text_font_data
#                 cell.alignment = align_right
#                 cell.border = border
#         for rows in ws.iter_rows(min_row=x, max_row=x, min_col=21, max_col=22):
#             for cell in rows:
#                 cell.font = text_font_data
#                 cell.alignment = align_right
#                 cell.border = border
#     for x in range (9,ws.max_row+1):
#         for rows in ws.iter_rows(min_row=x, max_row=x, min_col=1, max_col=1):
#             for cell in rows:
#                 cell.font = text_font
#                 cell.alignment = align_left
#                 cell.border = border
#         for rows in ws.iter_rows(min_row=x, max_row=x, min_col=2, max_col=20):
#             for cell in rows:
#                 cell.font = text_font_data
#                 cell.alignment = align_right
#                 cell.border = border
#         for rows in ws.iter_rows(min_row=x, max_row=x, min_col=25, max_col=27):
#             for cell in rows:
#                 cell.font = text_font_data
#                 cell.alignment = align_right
#                 cell.border = border
#         for rows in ws.iter_rows(min_row=x, max_row=x, min_col=28, max_col = ws.max_column):
#             for cell in rows:
#                 cell.font = text_font_data
#                 cell.alignment = align_left
#                 cell.border = border        
#         for rows in ws.iter_rows(min_row=8, max_row=8, min_col=19, max_col = ws.max_column):
#             for cell in rows:
#                 cell.font = text_font
#                 cell.alignment = align_center
#                 cell.border = border
#         for rows in ws.iter_rows(min_row=x, max_row=x, min_col=27, max_col=27):
#             for cell in rows:
#                 cell.font = text_font_data
#                 cell.alignment = align_left
#                 cell.border = border 
#         for rows in ws.iter_rows(min_row=x, max_row=x, min_col=26, max_col=26):
#             for cell in rows:
#                 cell.font = text_font_data
#                 cell.alignment = align_left
#                 cell.border = border 
                
# def set_column_widths(ws):
#     column_widths = [18, 5] + [5] * 13 + [7] * 2 + [5] * 1 +[6] * 1 + [5] * 4 +[6] * 1 + [4] * 5+ [8] * 7
#     for i, width in enumerate(column_widths, start=1):
#         ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = width
#     ws.column_dimensions[openpyxl.utils.get_column_letter(26)].width = 80
    
# def build_xlsx_response(filename):
#     xlsx_file = make_xlsx(sheet_name=filename)
#     frappe.response['filename'] = filename + '.xlsx'
#     frappe.response['filecontent'] = xlsx_file.getvalue()
#     frappe.response['type'] = 'binary'



# def get_data(args):
#     if args.get('date'):
#         row =[]
#         date =args.get('date')
#         fromdate = datetime.strptime(args.get('date'), '%Y-%m-%d').date()
#         fromdate_ = fromdate.strftime('%d-%m-%Y')
#         if not args.get('shift'):
#             shift_header = 'All Shift'
#         else:
#             shift_header = args.get('shift')
#         data = [
#             ["Employee Checkin Wise Man Power Plan Vs Actual Summary"],
#             [""],
#             ["", "Plan / Actual"] + [""] * 16 + ["Date: " + fromdate_]+ [""] * 5+ ["Shift: " + shift_header],
#             [""],
#             ["Employee category / Department", "Staff", "", "JOE", "", "Tech", "", "Trainee", "", "NAPS", "",
#              "Contract(CL)", "", "New Joining Trainees", "", "Temporary CL","", "Total Plan",
#             "Cummulative Actual","Absent Gap (Plan-Actual)","Informed Leave(HRMS request approved)",""," Un informed Leave(HRMS request not approved)","","Total Gap",
#             "Remarks","Requested manpower","Given manpower",],
#             [""],
#             [""],
#             ["", "Plan", "Actual", "Plan", "Actual", "Plan", "Actual", "Plan", "Actual",
#             "Plan", "Actual", "Plan", "Actual", "Plan", "Actual", "Plan", "Actual",
#             "", "", "", "", "", "", "", "", ""]
#             # ["",]+[""]*17+ ["Actual Present","Permission","Miss Punch","OD"]
#         ]
#         frappe.log_error(
#             title="Plan Vs Actual Debug",
#             message=f"HEADER LENGTH: {len(data[7])}"
#         )
        
#         if args.get('shift') in ['1', '2']:
#             shift1 = args.get('shift')
#             shift = f"shift = '{args.get('shift')}'"
#             shift_new =[args.get('shift')]
#         else:
#             shift1 = ['is', 'set'] 
#             shift = "shift IN ('1', '2')"
#             shift_new =['1','2','3']
#         frappe.errprint(shift)
#         # departments = frappe.get_all('Department', filters={'disabled': 0}, order_by='name asc')
#         # total_planning_staff,total_plan_cl ,total_plan_dt, total_plan_iti,total_plan_naps,total_plan_trainee = 0,0,0,0,0,0
#         # total_actual_dt,total_actual_staff,total_actual_naps,total_actual_iti,total_actual_cl, total_actual_trainee =0, 0,0,0,0,0
#         # total_cumulative,total_coff,total_absent_gap,total_of_total_gap,total_od,total_permission,actual_leave,plan_leave,total_misspunch = 0,0,0,0,0,0,0,0,0
#         # total_plan_total,total_actual_total =0, 0
#         # total_plan_access_card, total_actual_access_card =0,0
#         # total_plan_new_joinee,total_actual_new_joinee = 0,0
#         # total_cl_access_card_actual =0
#         # # total_new_trainee_and_staff_plan_access_card,total_new_trainee_and_staff_actual_access_card = 0,0
        
#         # departments = frappe.get_all("Department",{"disabled": 0,"name": ["!=", "All Departments"]},["name"], order_by="name asc")
#         user = frappe.session.user
#         has_misspunch_role = "Miss Punch" in frappe.get_roles(user)
#         employee = frappe.db.get_value("Employee", {"user_id": user}, "name")

#         selected_dept = args.get("department")
#         if selected_dept:
#             selected_dept = selected_dept.strip()

#         if has_misspunch_role:
#             if selected_dept:
#                 departments = [selected_dept]
#             else:
#                 departments = [d.name for d in frappe.get_all("Department", filters={"disabled": 0,"name": ["!=", "All Departments"]}, order_by="name asc")]
#         else:
#             dept_name = frappe.db.get_value("Employee", employee, "department")
#             if selected_dept:
#                 departments = [selected_dept]
#             else:
#                 departments = [dept_name] if dept_name else []
            
#             # shift = "shift IN ('1', '2')"
#         total_planning_staff,total_plan_cl ,total_plan_dt, total_plan_iti,total_plan_naps,total_plan_trainee = 0,0,0,0,0,0
#         total_actual_dt,total_actual_staff,total_actual_naps,total_actual_iti,total_actual_cl, total_actual_trainee =0, 0,0,0,0,0
#         total_cumulative,total_coff,total_absent_gap,total_of_total_gap,total_od,total_permission,actual_leave,plan_leave,total_misspunch = 0,0,0,0,0,0,0,0,0
#         total_plan_total,total_actual_total =0, 0
#         total_plan_access_card,total_actual_access_card = 0,0
#         total_plan_new_joinee,total_actual_new_joinee = 0,0
#         total_cl_access_card_actual =0
#         for dept in departments:
#             category_order = {
#                 "Staff": 1,
#                 "DT": 2,
#                 "ITI": 3,   
#                 "GT": 4,
#                 "TT": 5,
#                 "CL (Access Card)": 6,
#                 "CL": 7, 
#                 "CL(Oneday)": 8,
#                 "Executive": 9 ,
#                 'Naps': 10,
#                 "New CL": 11,
#                 "New Staff": 12,
#                 "New Trainees": 13
#             }
#             remarks = ""
#             emp_category_name = ['Staff','Manager','ITI','TT','Naps','CL','GT','New CL','New Staff','New Trainees','DT']
#             # planed_emp = frappe.db.get_all("Shift Assignment",{'department': dept.name,'start_date': date ,'shift_type':shift,'docstatus': 1,'employee_category': ['in', emp_category_name]},pluck="employee")
#             planed_emp = frappe.db.get_all("Shift Assignment",{'department': dept,'start_date': date,'shift_type':shift1,'docstatus': 1,'employee_category': ['in',['Staff','Manager','ITI','TT','Naps','CL','GT','New CL','New Staff','New Trainees','DT']]},pluck="employee")
#             query = """
#                 SELECT DISTINCT employee
#                 FROM `tabEmployee Checkin`
#                 WHERE DATE(time) = %s
#                 AND log_type = 'IN'
#                 AND shift IN %s
#                 AND department = %s
#                 AND employee_category IN %s
#                 ORDER BY time
#             """
#             params = (date, tuple(shift_new), dept, tuple(emp_category_name))
#             result = frappe.db.sql(query, params, as_dict=True)
            
#             present_emp = {row["employee"] for row in result}
#             frappe.errprint(result)
#             frappe.errprint(f"Planned Employees: {planed_emp}")
#             frappe.errprint(f"Present Employees: {present_emp}")
#             # for i in planed_emp:
#             #     # frappe.errprint(planed_emp)
#             #     if i not in present_emp:
#             #         # frappe.errprint(present_emp)
#             #         emp_name = frappe.db.get_value("Employee",i,"employee_name")
#             #         if remarks =='':
#             #             remarks+=f"{i} : {emp_name}"
#             #         else:
#             #             remarks+=f", {i} : {emp_name}"
            
            
#             emp_list = []

#             for i in planed_emp:
#                 if i not in present_emp:
#                     emp_data = frappe.db.get_value(
#                         "Employee",
#                         i,
#                         ["employee_name", "employee_category"],
#                         as_dict=True
#                     )
#                     if emp_data:
#                         emp_list.append({
#                             "id": i,
#                             "name": emp_data.employee_name,
#                             "category": emp_data.employee_category,
#                             "order": category_order.get(emp_data.employee_category, 99)
#                         })

#             category_groups = defaultdict(list)
#             for emp in emp_list:
#                 category_groups[emp['category']].append(f"{emp['id']} : {emp['name']}")

#             # remarks = "\n".join([
#             #     f"{category} - {', '.join(category_groups[category])}"
#             #     for category in sorted(category_groups.keys(), key=lambda x: category_order.get(x, 99))
#             # ])
            
#             remarks = "\n".join([
#                 f"({len(category_groups[category])}) : {category} : {', '.join(category_groups[category])}"
#                 for category in sorted(category_groups.keys(), key=lambda x: category_order.get(x, 99))
#             ])
            
                        
#             row = [dept]
#             employee_categories = frappe.get_all("Employee Category", fields=["name"], order_by='name')
#             total_plan= 0
#             plan_staff, actual_staff, plan_cl, plan_dt, plan_gt, plan_iti, plan_naps, actual_cl, actual_dt, actual_new_joinee, actual_access_card = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
#             plan_tt, actual_tt, actual_gt, actual_iti, actual_naps, actual_trainee, plan_trainee, plan_new_joinee, plan_access_card = 0, 0, 0, 0, 0, 0, 0, 0, 0
#             actual_total_permission, actual_total_misspunch, actual_total_coff, actual_total_od, actual_total_absent_gap, actual_total_cumulative = 0, 0, 0, 0, 0, 0
#             actual_total_leave_application, total_leave_application_not_approved, total_gap = 0, 0, 0
#             new_trainee_plan_access_card,new_staff_plan_access_card,new_staff_actual_access_card,new_trainee_actual_access_card =0,0,0,0
#             cl_access_card_actual,cl_access_card_plan =0,0
#             for emp_category in employee_categories:
#                 emp_category_name = emp_category['name']
#                 employee_category = 'employee_category'
#                 if emp_category_name == "Staff":
#                     plan_staff = frappe.db.count("Shift Assignment", {
#                         'department': dept,
#                         employee_category: emp_category_name,
#                         'start_date': date,
#                         'shift_type':shift1,
#                         'docstatus': 1
#                     })
#                     query = f"""
#                         SELECT DISTINCT employee, COUNT(*) as count
#                         FROM `tabEmployee Checkin`
#                         WHERE DATE(time) = %s 
#                         AND log_type = 'IN' 
#                         AND {shift}
#                         AND department = %s 
#                         AND employee_category = %s
#                         GROUP BY employee
#                         ORDER BY time
#                     """
#                     result = frappe.db.sql(query, (date, dept, emp_category_name), as_dict=True)
#                     actual_staff = len(result)
#                 elif emp_category_name == "DT":
#                     plan_dt = frappe.db.count("Shift Assignment", {
#                         'department': dept,
#                         employee_category: emp_category_name,
#                         'start_date': date,
#                         'shift_type':shift1,
#                         'docstatus': 1
#                     })
#                     query = f"""
#                         SELECT DISTINCT employee, COUNT(*) as count
#                         FROM `tabEmployee Checkin`
#                         WHERE DATE(time) = %s 
#                         AND log_type = 'IN' 
#                         AND {shift} 
#                         AND department = %s 
#                         AND employee_category = %s
#                         GROUP BY employee
#                         ORDER BY time
#                     """
#                     result = frappe.db.sql(query, (date, dept, emp_category_name), as_dict=True)
#                     actual_dt = len(result)
#                 elif emp_category_name == "ITI":
#                     plan_iti = frappe.db.count("Shift Assignment", {
#                         'department': dept,
#                         employee_category: emp_category_name,
#                         'start_date': date,
#                         'shift_type':shift1,
#                         'docstatus': 1
#                     })
#                     query = f"""
#                         SELECT DISTINCT employee, COUNT(*) as count
#                         FROM `tabEmployee Checkin`
#                         WHERE DATE(time) = %s 
#                         AND log_type = 'IN' 
#                         AND {shift} 
#                         AND department = %s 
#                         AND employee_category = %s
#                         GROUP BY employee
#                         ORDER BY time
#                     """
#                     result = frappe.db.sql(query, (date, dept, emp_category_name), as_dict=True)
#                     actual_iti = len(result)
#                 elif emp_category_name == "TT":
#                     plan_tt = frappe.db.count("Shift Assignment", {
#                         'department': dept,
#                         employee_category: emp_category_name,
#                         'start_date': date,
#                         'shift_type':shift1,
#                         'docstatus': 1
#                     })
#                     query = f"""
#                         SELECT DISTINCT employee, COUNT(*) as count
#                         FROM `tabEmployee Checkin`
#                         WHERE DATE(time) = %s 
#                         AND log_type = 'IN' 
#                         AND {shift} 
#                         AND department = %s 
#                         AND employee_category = %s
#                         GROUP BY employee
#                         ORDER BY time
#                     """
#                     result = frappe.db.sql(query, (date, dept, emp_category_name), as_dict=True)
#                     actual_tt = len(result)
#                 elif emp_category_name == "Naps":
#                     plan_naps = frappe.db.count("Shift Assignment", {
#                         'department': dept,
#                         employee_category: emp_category_name,
#                         'start_date': date,
#                         'shift_type':shift1,
#                         'docstatus': 1
#                     })
#                     query = f"""
#                         SELECT DISTINCT employee, COUNT(*) as count
#                         FROM `tabEmployee Checkin`
#                         WHERE DATE(time) = %s 
#                         AND log_type = 'IN' 
#                         AND {shift}
#                         AND department = %s 
#                         AND employee_category = %s
#                         GROUP BY employee
#                         ORDER BY time
#                     """
#                     result = frappe.db.sql(query, (date, dept, emp_category_name), as_dict=True)
#                     actual_naps = len(result)
#                 elif emp_category_name == "CL":
#                     plan_cl = frappe.db.count("Shift Assignment", {
#                         'department': dept,
#                         employee_category: emp_category_name,
#                         'start_date': date,
#                         'shift_type':shift1,
#                         'docstatus': 1
#                     })
#                     actual_cl_query = f"""
#                         SELECT DISTINCT employee, COUNT(*) as count
#                         FROM `tabEmployee Checkin`
#                         WHERE DATE(time) = %s 
#                         AND log_type = 'IN' 
#                         AND {shift}
#                         AND department = %s 
#                         AND employee_category = %s
#                         GROUP BY employee
#                         ORDER BY time
#                     """
#                     result = frappe.db.sql(actual_cl_query, (date, dept, emp_category_name), as_dict=True)
#                     actual_cl = len(result)
#                     frappe.errprint(actual_cl)
#                 elif emp_category_name == "GT":
#                     plan_gt = frappe.db.count("Shift Assignment", {
#                         'department': dept,
#                         employee_category: emp_category_name,
#                         'start_date': date,
#                         'shift_type':shift1,
#                         'docstatus': 1
#                     })
#                     query = f"""
#                         SELECT DISTINCT employee, COUNT(*) as count
#                         FROM `tabEmployee Checkin`
#                         WHERE DATE(time) = %s 
#                         AND log_type = 'IN' 
#                         AND {shift} 
#                         AND department = %s 
#                         AND employee_category = %s
#                         GROUP BY employee
#                         ORDER BY time
#                     """
#                     result = frappe.db.sql(query, (date, dept, emp_category_name), as_dict=True)
#                     actual_gt = len(result)
#                 elif emp_category_name == "New Staff":
#                     new_staff_plan_access_card = frappe.db.count("Shift Assignment", {
#                         'department': dept,
#                         employee_category: emp_category_name,
#                         'start_date': date,
#                         'shift_type':shift1,
#                         'docstatus': 1
#                     })
#                     query = f"""
#                         SELECT DISTINCT employee, COUNT(*) as count
#                         FROM `tabEmployee Checkin`
#                         WHERE DATE(time) = %s 
#                         AND log_type = 'IN' 
#                         AND {shift} 
#                         AND department = %s 
#                         AND employee_category = %s
#                         GROUP BY employee
#                         ORDER BY time
#                     """
#                     result = frappe.db.sql(query, (date, dept, emp_category_name), as_dict=True)
#                     new_staff_actual_access_card = len(result)
#                 elif emp_category_name == "New Trainees":
#                     new_trainee_plan_access_card = frappe.db.count("Shift Assignment", {
#                         'department': dept,
#                         employee_category: emp_category_name,
#                         'start_date': date,
#                         'shift_type':shift1,
#                         'docstatus': 1
#                     })
#                     query = f"""
#                         SELECT DISTINCT employee, COUNT(*) as count
#                         FROM `tabEmployee Checkin`
#                         WHERE DATE(time) = %s 
#                         AND log_type = 'IN' 
#                         AND {shift} 
#                         AND department = %s 
#                         AND employee_category = %s
#                         GROUP BY employee
#                         ORDER BY time
#                     """
#                     result = frappe.db.sql(query, (date, dept, emp_category_name), as_dict=True)
#                     new_trainee_actual_access_card = len(result)
#                 elif emp_category_name == "New CL":
#                     plan_access_card = frappe.db.count("Shift Assignment", {
#                         'department': dept,
#                         employee_category: emp_category_name,
#                         'start_date': date,
#                         'shift_type':shift1,
#                         'docstatus': 1
#                     })
#                     query = f"""
#                         SELECT DISTINCT employee, COUNT(*) as count
#                         FROM `tabEmployee Checkin`
#                         WHERE DATE(time) = %s 
#                         AND log_type = 'IN' 
#                         AND {shift} 
#                         AND department = %s 
#                         AND employee_category = %s
#                         GROUP BY employee
#                         ORDER BY time
#                     """
#                     result = frappe.db.sql(query, (date, dept, emp_category_name), as_dict=True)
#                     actual_access_card = len(result)
#                 elif emp_category_name == "CL (Access Card)":
#                     cl_access_card_plan = frappe.db.count("Shift Assignment", {
#                         'department': dept,
#                         employee_category: emp_category_name,
#                         'start_date': date,
#                         'shift_type':shift1,
#                         'docstatus': 1
#                     })
#                     query = f"""
#                         SELECT DISTINCT employee, COUNT(*) as count
#                         FROM `tabEmployee Checkin`
#                         WHERE DATE(time) = %s 
#                         AND log_type = 'IN' 
#                         AND {shift} 
#                         AND department = %s 
#                         AND employee_category = %s
#                         GROUP BY employee
#                         ORDER BY time
#                     """
#                     result = frappe.db.sql(query, (date, dept, emp_category_name), as_dict=True)
#                     cl_access_card_actual = len(result)
#             plan_new_joinee = new_trainee_plan_access_card + new_staff_plan_access_card
#             actual_new_joinee = new_staff_actual_access_card + new_trainee_actual_access_card
#             actual_trainee = actual_gt + actual_tt
#             plan_trainee = plan_gt + plan_tt
#             plan_total = frappe.db.count("Shift Assignment", {
#                 'department': dept,
#                 'start_date': date,
#                 'employee_category': ('not in', ['CL (Access Card)']),
#                 'shift_type':shift1,
#                 'docstatus': 1
#             })
#             query = f"""
#                         SELECT DISTINCT employee, COUNT(*) as count
#                         FROM `tabEmployee Checkin`
#                         WHERE DATE(time) = %s 
#                         AND log_type = 'IN' 
#                         AND employee_category NOT IN ('CL (Access Card)')
#                         AND  {shift}
#                         AND department = %s 
#                         GROUP BY employee
#                         ORDER BY time
#                     """
#             result = frappe.db.sql(query, (date, dept), as_dict=True)
#             # frappe.errprint(query)
#             actual_total = len(result)
#             actual_total_permission = frappe.db.count("Permission Request", {
#                 'department': dept,
#                 'shift': shift,
#                 'workflow_state': ["=", "Approved"],
#                 'employee_category': ('not in', ['CL (Access Card)']),
#                 'docstatus': 1,
#                 'permission_date': ["between", [date, date]]
#             })
#             actual_total_misspunch = frappe.db.count("Miss Punch Application", {
#                 'department': dept,
#                 'shift': shift,
#                 'workflow_state': ["=", "Approved"],
#                 'employee_category': ('not in', ['CL (Access Card)']),
#                 'docstatus': 1,
#                 'date': ["between", [date, date]]
#             })
#             actual_total_od = frappe.db.sql("""
#                 SELECT COUNT(*)
#                 FROM `tabOn Duty Application`
#                 WHERE workflow_state = "Approved"
#                 AND docstatus = 1
#                 AND category NOT IN ('CL (Access Card)')
#                 AND department = %(department)s
#                 AND %(shift)s
#                 AND (
#                     od_date BETWEEN %(from_date)s AND %(to_date)s
#                     OR to_date BETWEEN %(from_date)s AND %(to_date)s
#                     OR (od_date < %(from_date)s AND to_date > %(to_date)s)
#                 )
#             """, {
#                 "from_date": date,
#                 "to_date": date,
#                 "department": dept,
#                 "shift": shift,
#             })[0][0]
#             approved_leaves  = frappe.db.sql("""
#                 select employee
#                 from `tabLeave Application`
#                 where workflow_state="Approved" and docstatus=1 and department = %(department)s
#                     and (from_date between %(from_date)s and %(to_date)s
#                         or to_date between %(from_date)s and %(to_date)s
#                         or (from_date < %(from_date)s and to_date > %(to_date)s))
#                 """, {
#                     "from_date": date,
#                     "to_date": date,
#                     "department":dept
#                 },as_dict = True)
#             for leave in approved_leaves:
#                 shift_count_leaves = frappe.db.count(
#                     'Shift Assignment',
#                     {
#                         'employee': leave['employee'],
#                         'employee_category': ('not in', ['CL (Access Card)']),       
#                         'start_date': date,         
#                         'end_date': date,
#                         'shift_type': shift,              
#                         'docstatus': ('!=', 2)           
#                     }
#                 )
#                 actual_total_leave_application += shift_count_leaves
#             not_approved_leaves = frappe.db.sql("""
#                 select employee
#                 from `tabLeave Application`
#                 where docstatus = 0 and department = %(department)s
#                     and (from_date between %(from_date)s and %(to_date)s
#                         or to_date between %(from_date)s and %(to_date)s
#                         or (from_date < %(from_date)s and to_date > %(to_date)s))
#                 """, {
#                     "from_date": date,
#                     "to_date": date,
#                     "department":dept
#                 },
#             as_dict = True)
#             for leave in not_approved_leaves:
#                 shift_count_leaves_ = frappe.db.count(
#                     'Shift Assignment',
#                     {
#                         'employee': leave['employee'],       
#                         'start_date': date,         
#                         'end_date': date,
#                         'employee_category': ('not in', ['CL (Access Card)']),
#                         'shift_type': shift,              
#                         'docstatus': ('!=', 2)           
#                     }
#                 )
#                 total_leave_application_not_approved += shift_count_leaves_
#             actual_total_cumulative = actual_total + actual_total_misspunch + actual_total_permission + actual_total_od
#             actual_total_absent_gap = plan_total - actual_total_cumulative
#             total_gap = total_leave_application_not_approved + actual_total_leave_application
            
#             row.extend([
#                 plan_staff, actual_staff, 
#                 plan_dt, actual_dt, 
#                 plan_iti, actual_iti, 
#                 plan_trainee, actual_trainee,
#                 plan_naps, actual_naps, 
#                 plan_cl, actual_cl, 
#                 plan_new_joinee, actual_new_joinee, 
#                 plan_access_card, actual_access_card
#             ])
#             total_planning_staff += plan_staff 
#             total_actual_staff += actual_staff
#             total_plan_dt += plan_dt
#             total_actual_dt += actual_dt
#             total_plan_iti += plan_iti
#             total_plan_trainee += plan_trainee
#             total_plan_naps +=plan_naps
#             total_plan_cl += plan_cl
#             total_actual_iti += actual_iti
#             total_actual_trainee += actual_trainee
#             total_actual_naps += actual_naps
#             total_actual_cl += actual_cl
#             plan_leave += actual_total_leave_application
#             actual_leave += total_leave_application_not_approved
#             total_of_total_gap +=total_gap
#             total_permission += actual_total_permission
#             total_misspunch += actual_total_misspunch
#             total_od += actual_total_od
#             total_coff += actual_total_coff
#             total_plan_total +=plan_total
#             total_actual_total += actual_total
#             total_cumulative += actual_total_cumulative
#             total_absent_gap += actual_total_absent_gap
#             total_plan_access_card +=plan_access_card
#             total_actual_access_card +=actual_access_card
#             total_actual_new_joinee +=actual_new_joinee
#             total_plan_new_joinee+=plan_new_joinee
#             total_cl_access_card_actual += cl_access_card_actual
#             row.append(plan_total)                        
#             row.append(actual_total_cumulative)             
#             row.append(actual_total_absent_gap)             
#             row.append(actual_total_leave_application) 
#             row.append("")
#             row.append(total_leave_application_not_approved)
#             row.append("")
#             row.append(total_gap)    
#             row.append(remarks) 
#             row.append("")                                
#             row.append(cl_access_card_actual)              
#             frappe.log_error(
#             title=f"{dept} ROW",
#             message=f"ROW LENGTH: {len(row)}"
#         )
#             data.append(row)
    
#         extra_row = [
#             "Totals", total_planning_staff, total_actual_staff, total_plan_dt, total_actual_dt, total_plan_iti, 
#             total_actual_iti, total_plan_trainee, total_actual_trainee, total_plan_naps, total_actual_naps, 
#             total_plan_cl, total_actual_cl, total_plan_new_joinee, total_actual_new_joinee, total_plan_access_card, total_actual_access_card, 
#             total_plan_total, total_cumulative, total_absent_gap, plan_leave, 
#             actual_leave,  total_of_total_gap,"",total_cl_access_card_actual
#         ]
#         # extra_row = ["Totals", total_planning_staff, total_actual_staff,total_plan_dt, total_actual_dt, total_plan_iti, total_actual_iti, total_plan_trainee, total_actual_trainee, total_plan_naps, total_actual_naps, total_plan_cl, total_actual_cl,
#         # 0,0,0,0,total_permission,total_misspunch,total_od,total_coff,total_plan_total,total_actual_total,total_cumulative,total_absent_gap,plan_leave,"",actual_leave,"",total_of_total_gap]
#         data.append(extra_row)
#         return data
        
    
# Copyright (c) 2024, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side
from six import BytesIO
from datetime import datetime
from datetime import datetime, timedelta
from frappe.utils import (getdate, cint, add_months, date_diff, add_days, format_date,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
import pandas as pd
from collections import defaultdict
from openpyxl.styles import GradientFill, PatternFill

class CheckinWisePlanVsActualReport(Document):
    pass


# ─────────────────────────────────────────────────────────────────────────────
#  SHARED HELPER  – fetch ALL bulk data for a given date + shift in ONE SHOT
# ─────────────────────────────────────────────────────────────────────────────
def _get_bulk_data(date, shift_new, departments):
    """
    Returns three lookup dicts so the caller never issues per-dept / per-category
    queries inside a loop.

    plan_lookup  : { dept: { category: count } }
    actual_lookup: { dept: { category: count } }
    present_emp  : { dept: set(employee) }
    """
    dept_tuple = tuple(departments)
    cat_tuple  = ('Staff','Manager','ITI','TT','Naps','CL','GT',
                  'New CL','New Staff','New Trainees','DT','CL (Access Card)')
    shift_tuple = tuple(shift_new)

    # ── 1. Plan counts (Shift Assignment) ────────────────────────────────────
    plan_rows = frappe.db.sql("""
        SELECT department, employee_category, COUNT(*) AS cnt
        FROM   `tabShift Assignment`
        WHERE  start_date        = %(date)s
          AND  docstatus         = 1
          AND  department        IN %(depts)s
          AND  employee_category IN %(cats)s
          AND  shift_type        IN %(shifts)s
        GROUP  BY department, employee_category
    """, {"date": date, "depts": dept_tuple,
          "cats": cat_tuple, "shifts": shift_tuple}, as_dict=True)

    plan_lookup = defaultdict(lambda: defaultdict(int))
    for r in plan_rows:
        plan_lookup[r.department][r.employee_category] = r.cnt

    # ── plan total (excluding CL Access Card) ────────────────────────────────
    plan_total_rows = frappe.db.sql("""
        SELECT department, COUNT(*) AS cnt
        FROM   `tabShift Assignment`
        WHERE  start_date        = %(date)s
          AND  docstatus         = 1
          AND  department        IN %(depts)s
          AND  employee_category NOT IN ('CL (Access Card)')
          AND  shift_type        IN %(shifts)s
        GROUP  BY department
    """, {"date": date, "depts": dept_tuple, "shifts": shift_tuple}, as_dict=True)

    plan_total_lookup = {r.department: r.cnt for r in plan_total_rows}

    # ── 2. Actual checkin counts ──────────────────────────────────────────────
    actual_rows = frappe.db.sql("""
        SELECT department, employee_category,
               COUNT(DISTINCT employee) AS cnt
        FROM   `tabEmployee Checkin`
        WHERE  DATE(time)        = %(date)s
          AND  log_type          = 'IN'
          AND  shift             IN %(shifts)s
          AND  department        IN %(depts)s
          AND  employee_category IN %(cats)s
        GROUP  BY department, employee_category
    """, {"date": date, "shifts": shift_tuple,
          "depts": dept_tuple, "cats": cat_tuple}, as_dict=True)

    actual_lookup = defaultdict(lambda: defaultdict(int))
    for r in actual_rows:
        actual_lookup[r.department][r.employee_category] = r.cnt

    # ── actual total (excluding CL Access Card) ───────────────────────────────
    actual_total_rows = frappe.db.sql("""
        SELECT department, COUNT(DISTINCT employee) AS cnt
        FROM   `tabEmployee Checkin`
        WHERE  DATE(time)        = %(date)s
          AND  log_type          = 'IN'
          AND  shift             IN %(shifts)s
          AND  department        IN %(depts)s
          AND  employee_category NOT IN ('CL (Access Card)')
        GROUP  BY department
    """, {"date": date, "shifts": shift_tuple, "depts": dept_tuple}, as_dict=True)

    actual_total_lookup = {r.department: r.cnt for r in actual_total_rows}

    # ── 3. Present employees (for remarks) ───────────────────────────────────
    present_rows = frappe.db.sql("""
        SELECT DISTINCT department, employee
        FROM   `tabEmployee Checkin`
        WHERE  DATE(time)        = %(date)s
          AND  log_type          = 'IN'
          AND  shift             IN %(shifts)s
          AND  department        IN %(depts)s
          AND  employee_category IN %(cats)s
    """, {"date": date, "shifts": shift_tuple,
          "depts": dept_tuple, "cats": cat_tuple}, as_dict=True)

    present_emp = defaultdict(set)
    for r in present_rows:
        present_emp[r.department].add(r.employee)

    # ── 4. Planned employees (for remarks) ───────────────────────────────────
    planned_rows = frappe.db.sql("""
        SELECT sa.department, sa.employee, e.employee_name, e.employee_category
        FROM   `tabShift Assignment` sa
        JOIN   `tabEmployee`         e  ON e.name = sa.employee
        WHERE  sa.start_date        = %(date)s
          AND  sa.docstatus         = 1
          AND  sa.department        IN %(depts)s
          AND  sa.employee_category IN %(cats)s
          AND  sa.shift_type        IN %(shifts)s
    """, {"date": date, "depts": dept_tuple,
          "cats": cat_tuple, "shifts": shift_tuple}, as_dict=True)

    planned_emp = defaultdict(list)
    for r in planned_rows:
        planned_emp[r.department].append(r)

    return (plan_lookup, plan_total_lookup,
            actual_lookup, actual_total_lookup,
            present_emp, planned_emp)


def _get_leave_counts(date, departments):
    """
    Returns two dicts  { dept: count }
    approved_leave_lookup     – Approved Leave Applications matched to shift
    not_approved_leave_lookup – Draft Leave Applications matched to shift
    Both use a single batch query instead of a per-employee loop.
    """
    dept_tuple = tuple(departments)

    # ── Approved leaves ───────────────────────────────────────────────────────
    approved_rows = frappe.db.sql("""
        SELECT la.department,
               COUNT(sa.name) AS cnt
        FROM   `tabLeave Application` la
        JOIN   `tabShift Assignment`  sa ON sa.employee = la.employee
        WHERE  la.workflow_state = 'Approved'
          AND  la.docstatus      = 1
          AND  la.department     IN %(depts)s
          AND  sa.start_date     = %(date)s
          AND  sa.end_date       = %(date)s
          AND  sa.docstatus     != 2
          AND  sa.employee_category NOT IN ('CL (Access Card)')
          AND  (
              la.from_date BETWEEN %(date)s AND %(date)s
              OR la.to_date   BETWEEN %(date)s AND %(date)s
              OR (la.from_date < %(date)s AND la.to_date > %(date)s)
          )
        GROUP  BY la.department
    """, {"date": date, "depts": dept_tuple}, as_dict=True)

    approved_leave_lookup = {r.department: r.cnt for r in approved_rows}

    # ── Not-approved (draft) leaves ───────────────────────────────────────────
    not_approved_rows = frappe.db.sql("""
        SELECT la.department,
               COUNT(sa.name) AS cnt
        FROM   `tabLeave Application` la
        JOIN   `tabShift Assignment`  sa ON sa.employee = la.employee
        WHERE  la.docstatus    = 0
          AND  la.department   IN %(depts)s
          AND  sa.start_date   = %(date)s
          AND  sa.end_date     = %(date)s
          AND  sa.docstatus   != 2
          AND  sa.employee_category NOT IN ('CL (Access Card)')
          AND  (
              la.from_date BETWEEN %(date)s AND %(date)s
              OR la.to_date   BETWEEN %(date)s AND %(date)s
              OR (la.from_date < %(date)s AND la.to_date > %(date)s)
          )
        GROUP  BY la.department
    """, {"date": date, "depts": dept_tuple}, as_dict=True)

    not_approved_leave_lookup = {r.department: r.cnt for r in not_approved_rows}

    return approved_leave_lookup, not_approved_leave_lookup


def _get_permission_misspunch_od(date, shift, departments):
    """
    Returns three dicts { dept: count } for Permission, MissPunch, OD.
    All fetched in batch – no per-dept queries.
    """
    dept_tuple = tuple(departments)

    perm_rows = frappe.db.sql("""
        SELECT department, COUNT(*) AS cnt
        FROM   `tabPermission Request`
        WHERE  workflow_state    = 'Approved'
          AND  docstatus         = 1
          AND  department        IN %(depts)s
          AND  shift             = %(shift)s
          AND  employee_category NOT IN ('CL (Access Card)')
          AND  permission_date   BETWEEN %(date)s AND %(date)s
        GROUP  BY department
    """, {"date": date, "shift": shift, "depts": dept_tuple}, as_dict=True)
    perm_lookup = {r.department: r.cnt for r in perm_rows}

    mp_rows = frappe.db.sql("""
        SELECT department, COUNT(*) AS cnt
        FROM   `tabMiss Punch Application`
        WHERE  workflow_state    = 'Approved'
          AND  docstatus         = 1
          AND  department        IN %(depts)s
          AND  shift             = %(shift)s
          AND  employee_category NOT IN ('CL (Access Card)')
          AND  date              BETWEEN %(date)s AND %(date)s
        GROUP  BY department
    """, {"date": date, "shift": shift, "depts": dept_tuple}, as_dict=True)
    mp_lookup = {r.department: r.cnt for r in mp_rows}

    od_rows = frappe.db.sql("""
        SELECT department, COUNT(*) AS cnt
        FROM   `tabOn Duty Application`
        WHERE  workflow_state  = 'Approved'
          AND  docstatus       = 1
          AND  category        NOT IN ('CL (Access Card)')
          AND  department      IN %(depts)s
          AND  (
              od_date BETWEEN %(date)s AND %(date)s
              OR to_date BETWEEN %(date)s AND %(date)s
              OR (od_date < %(date)s AND to_date > %(date)s)
          )
        GROUP  BY department
    """, {"date": date, "depts": dept_tuple}, as_dict=True)
    od_lookup = {r.department: r.cnt for r in od_rows}

    return perm_lookup, mp_lookup, od_lookup


def _build_remarks(dept, planned_emp, present_emp):
    """Build colour-coded remarks string for a single department."""
    category_order = {
        "Staff": 1, "DT": 2, "ITI": 3, "GT": 4, "TT": 5,
        "CL (Access Card)": 6, "CL": 7, "CL(Oneday)": 8,
        "Executive": 9, "Naps": 10, "New CL": 11,
        "New Staff": 12, "New Trainees": 13
    }
    category_colors = {
        "Staff": "blue", "DT": "orange", "ITI": "green",
        "GT": "purple", "TT": "brown", "CL (Access Card)": "darkred",
        "CL": "red", "CL(Oneday)": "crimson", "Executive": "darkblue",
        "Naps": "teal", "New CL": "magenta",
        "New Staff": "darkgreen", "New Trainees": "darkorange"
    }

    dept_present = present_emp.get(dept, set())
    category_groups = defaultdict(list)

    for emp in planned_emp.get(dept, []):
        if emp.employee not in dept_present:
            category_groups[emp.employee_category].append(
                f"{emp.employee} : {emp.employee_name}"
            )

    return "<br>".join([
        f"<span style='color:{category_colors.get(cat, 'black')};'>"
        f"({len(category_groups[cat])}) : {cat} : "
        f"{', '.join(category_groups[cat])}</span>"
        for cat in sorted(category_groups.keys(),
                          key=lambda x: category_order.get(x, 99))
    ])


def _build_remarks_plain(dept, planned_emp, present_emp):
    """Plain-text remarks for Excel (no HTML)."""
    category_order = {
        "Staff": 1, "DT": 2, "ITI": 3, "GT": 4, "TT": 5,
        "CL (Access Card)": 6, "CL": 7, "CL(Oneday)": 8,
        "Executive": 9, "Naps": 10, "New CL": 11,
        "New Staff": 12, "New Trainees": 13
    }
    dept_present = present_emp.get(dept, set())
    category_groups = defaultdict(list)

    for emp in planned_emp.get(dept, []):
        if emp.employee not in dept_present:
            category_groups[emp.employee_category].append(
                f"{emp.employee} : {emp.employee_name}"
            )

    return "\n".join([
        f"({len(category_groups[cat])}) : {cat} : {', '.join(category_groups[cat])}"
        for cat in sorted(category_groups.keys(),
                          key=lambda x: category_order.get(x, 99))
    ])


# ─────────────────────────────────────────────────────────────────────────────
#  HTML REPORT ENDPOINT
# ─────────────────────────────────────────────────────────────────────────────
@frappe.whitelist(allow_guest=True)
def get_data_system(date, shift, department=None):
    date_ = datetime.strptime(date, "%Y-%m-%d").strftime('%d-%m-%Y')

    # ── Build HTML table header (unchanged from original) ────────────────────
    data = f"""<h2 class='text-center' style="color: black;">Manpower Category wise plan vs Actual Summary</h2>
            <div style="overflow-x: auto; color: black;">
            <table class="text-center" style="overflow: hidden; white-space: wrap;">
            <thead>
            <tr>
                <td colspan="27"></td>
            </tr>
            <tr style="background-color: #ffe5b4; font-weight: 500; color: black;">
                <td style="width: 200px;" colspan=1 class="border border-1 border-dark"></td>
                <td colspan=17 class="border border-1 border-dark"><strong>Plan / Count</strong></td>
                <td colspan=5 class="border border-1 border-dark"><strong>Date: {date_}</strong></td>
                <td colspan=3 class="border border-1 border-dark"><strong>Shift: {shift or "All Shift"}</strong></td>
            </tr>
            <tr style="background-color: #ffe5b4; font-weight: 500; color: black;">
                <td rowspan=3 class="border border-1 border-dark" style="min-width: 200px;">Employee Category / Department</td>
                <td colspan=2 class="border border-1 border-dark" style="min-width: 100px;">Staff</td>
                <td colspan=2 class="border border-1 border-dark" style="min-width: 100px;">JOE</td>
                <td colspan=2 class="border border-1 border-dark" style="min-width: 100px;">Tech</td>
                <td colspan=2 class="border border-1 border-dark" style="min-width: 100px;">Trainee</td>
                <td colspan=2 class="border border-1 border-dark" style="min-width: 100px;">NAPS</td>
                <td colspan=2 class="border border-1 border-dark" style="min-width: 100px;">Contract(CL)</td>
                <td colspan=2 class="border border-1 border-dark" style="min-width: 100px;">New Joining Trainees</td>
                <td colspan=2 class="border border-1 border-dark" style="min-width: 100px;">Temporary CL</td>
                <td rowspan=3 class="border border-1 border-dark" style="min-width: 100px;">Total Plan</td>
                <td rowspan=3 class="border border-1 border-dark" style="min-width: 100px;">Cummulative Actual</td>
                <td rowspan=3 class="border border-1 border-dark" style="min-width: 100px;">Absent Gap (Plan-Actual)</td>
                <td rowspan=3 class="border border-1 border-dark" style="min-width: 100px;">Informed Leave(HRMS request approved)</td>
                <td rowspan=3 class="border border-1 border-dark" style="min-width: 100px;">Un informed Leave(HRMS request not approved)</td>
                <td rowspan=3 class="border border-1 border-dark" style="min-width: 100px;">Total Gap</td>
                <td rowspan=3 class="border border-1 border-dark" style="min-width: 100px;">Remarks</td>
                <td rowspan=3 class="border border-1 border-dark" style="min-width: 100px;">Requested manpower</td>
                <td rowspan=3 class="border border-1 border-dark" style="min-width: 100px;">Given manpower</td>
            </tr>
            <tr style="background-color: #ffe5b4; font-weight: 500; color: black;">
                <td rowspan=2 class="border border-1 border-dark" style="min-width: 50px;">Plan</td>
                <td rowspan=2 class="border border-1 border-dark" style="min-width: 50px;">Actual</td>
                <td rowspan=2 class="border border-1 border-dark" style="min-width: 50px;">Plan</td>
                <td rowspan=2 class="border border-1 border-dark" style="min-width: 50px;">Actual</td>
                <td rowspan=2 class="border border-1 border-dark" style="min-width: 50px;">Plan</td>
                <td rowspan=2 class="border border-1 border-dark" style="min-width: 50px;">Actual</td>
                <td rowspan=2 class="border border-1 border-dark" style="min-width: 50px;">Plan</td>
                <td rowspan=2 class="border border-1 border-dark" style="min-width: 50px;">Actual</td>
                <td rowspan=2 class="border border-1 border-dark" style="min-width: 50px;">Plan</td>
                <td rowspan=2 class="border border-1 border-dark" style="min-width: 50px;">Actual</td>
                <td rowspan=2 class="border border-1 border-dark" style="min-width: 50px;">Plan</td>
                <td rowspan=2 class="border border-1 border-dark" style="min-width: 50px;">Actual</td>
                <td rowspan=2 class="border border-1 border-dark" style="min-width: 50px;">Plan</td>
                <td rowspan=2 class="border border-1 border-dark" style="min-width: 50px;">Actual</td>
                <td rowspan=2 class="border border-1 border-dark" style="min-width: 50px;">Plan</td>
                <td rowspan=2 class="border border-1 border-dark" style="min-width: 50px;">Actual</td>
            </tr>
            <tr style="background-color: #ffe5b4; font-weight: 500; color: black;"></tr>
        </thead>
        <tbody>"""

    # ── Determine departments ─────────────────────────────────────────────────
    if department:
        departments = [department]
    else:
        departments = [
            d["name"] for d in frappe.get_all(
                "Department",
                {"disabled": 0, "name": ["!=", "All Departments"]},
                ["name"], order_by="name asc"
            )
        ]

    # ── Shift normalisation ───────────────────────────────────────────────────
    if shift in ['1', '2']:
        shift_new  = [shift]
        shift_single = shift       # for permission / misspunch filters
    else:
        shift_new    = ['1', '2']
        shift_single = None        # will handle below

    # ── Fetch ALL data in bulk (only ~6 queries total) ────────────────────────
    (plan_lookup, plan_total_lookup,
     actual_lookup, actual_total_lookup,
     present_emp, planned_emp) = _get_bulk_data(date, shift_new, departments)

    approved_leave_lookup, not_approved_leave_lookup = _get_leave_counts(date, departments)

    # Permission / MissPunch / OD – these still need the shift string filter
    # We pass shift_single; if None we query for both shifts
    if shift_single:
        perm_lookup, mp_lookup, od_lookup = _get_permission_misspunch_od(
            date, shift_single, departments)
    else:
        perm_lookup1, mp_lookup1, od_lookup1 = _get_permission_misspunch_od(date, '1', departments)
        perm_lookup2, mp_lookup2, od_lookup2 = _get_permission_misspunch_od(date, '2', departments)
        perm_lookup = {d: perm_lookup1.get(d, 0) + perm_lookup2.get(d, 0) for d in departments}
        mp_lookup   = {d: mp_lookup1.get(d, 0)   + mp_lookup2.get(d, 0)   for d in departments}
        od_lookup   = {d: od_lookup1.get(d, 0)   + od_lookup2.get(d, 0)   for d in departments}

    # ── Grand totals ──────────────────────────────────────────────────────────
    totals = defaultdict(int)

    for dept in departments:
        pl  = plan_lookup[dept]
        al  = actual_lookup[dept]

        plan_staff        = pl.get("Staff", 0)
        plan_dt           = pl.get("DT", 0)
        plan_iti          = pl.get("ITI", 0)
        plan_trainee      = pl.get("GT", 0) + pl.get("TT", 0)
        plan_naps         = pl.get("Naps", 0)
        plan_cl           = pl.get("CL", 0)
        plan_new_joinee   = pl.get("New Staff", 0) + pl.get("New Trainees", 0)
        plan_access_card  = pl.get("New CL", 0)
        plan_total        = plan_total_lookup.get(dept, 0)

        actual_staff       = al.get("Staff", 0)
        actual_dt          = al.get("DT", 0)
        actual_iti         = al.get("ITI", 0)
        actual_trainee     = al.get("GT", 0) + al.get("TT", 0)
        actual_naps        = al.get("Naps", 0)
        actual_cl          = al.get("CL", 0)
        actual_new_joinee  = al.get("New Staff", 0) + al.get("New Trainees", 0)
        actual_access_card = al.get("New CL", 0)
        cl_access_card_actual = al.get("CL (Access Card)", 0)
        actual_total       = actual_total_lookup.get(dept, 0)

        actual_total_permission = perm_lookup.get(dept, 0)
        actual_total_misspunch  = mp_lookup.get(dept, 0)
        actual_total_od         = od_lookup.get(dept, 0)

        actual_total_leave_application       = approved_leave_lookup.get(dept, 0)
        total_leave_application_not_approved = not_approved_leave_lookup.get(dept, 0)

        actual_total_cumulative  = actual_total + actual_total_misspunch + actual_total_permission + actual_total_od
        actual_total_absent_gap  = plan_total - actual_total_cumulative
        total_gap                = actual_total_leave_application + total_leave_application_not_approved

        remarks = _build_remarks(dept, planned_emp, present_emp)

        # accumulate grand totals
        totals["staff_plan"]       += plan_staff
        totals["staff_actual"]     += actual_staff
        totals["dt_plan"]          += plan_dt
        totals["dt_actual"]        += actual_dt
        totals["iti_plan"]         += plan_iti
        totals["iti_actual"]       += actual_iti
        totals["trainee_plan"]     += plan_trainee
        totals["trainee_actual"]   += actual_trainee
        totals["naps_plan"]        += plan_naps
        totals["naps_actual"]      += actual_naps
        totals["cl_plan"]          += plan_cl
        totals["cl_actual"]        += actual_cl
        totals["nj_plan"]          += plan_new_joinee
        totals["nj_actual"]        += actual_new_joinee
        totals["ac_plan"]          += plan_access_card
        totals["ac_actual"]        += actual_access_card
        totals["plan_total"]       += plan_total
        totals["cumulative"]       += actual_total_cumulative
        totals["absent_gap"]       += actual_total_absent_gap
        totals["informed_leave"]   += actual_total_leave_application
        totals["uninformed_leave"] += total_leave_application_not_approved
        totals["total_gap"]        += total_gap
        totals["cl_ac_actual"]     += cl_access_card_actual

        data += f"""
            <tr>
                <td class="border border-1 border-dark text-left pl-3">{dept}</td>
                <td class="border border-1 border-dark">{plan_staff}</td>
                <td class="border border-1 border-dark">{actual_staff}</td>
                <td class="border border-1 border-dark">{plan_dt}</td>
                <td class="border border-1 border-dark">{actual_dt}</td>
                <td class="border border-1 border-dark">{plan_iti}</td>
                <td class="border border-1 border-dark">{actual_iti}</td>
                <td class="border border-1 border-dark">{plan_trainee}</td>
                <td class="border border-1 border-dark">{actual_trainee}</td>
                <td class="border border-1 border-dark">{plan_naps}</td>
                <td class="border border-1 border-dark">{actual_naps}</td>
                <td class="border border-1 border-dark">{plan_cl}</td>
                <td class="border border-1 border-dark">{actual_cl}</td>
                <td class="border border-1 border-dark">{plan_new_joinee}</td>
                <td class="border border-1 border-dark">{actual_new_joinee}</td>
                <td class="border border-1 border-dark">{plan_access_card}</td>
                <td class="border border-1 border-dark">{actual_access_card}</td>
                <td class="border border-1 border-dark">{plan_total}</td>
                <td class="border border-1 border-dark">{actual_total_cumulative}</td>
                <td class="border border-1 border-dark">{actual_total_absent_gap}</td>
                <td class="border border-1 border-dark">{actual_total_leave_application}</td>
                <td class="border border-1 border-dark">{total_leave_application_not_approved}</td>
                <td class="border border-1 border-dark">{total_gap}</td>
                <td class="border border-1 border-dark" style="white-space: nowrap; overflow-x: auto; max-width:500px;text-align:left;">{remarks}</td>
                <td class="border border-1 border-dark"></td>
                <td class="border border-1 border-dark">{cl_access_card_actual}</td>
            </tr>"""

    t = totals
    data += f"""
        <tr style="background-color: #ffe5b4; font-weight: 700; color: black;">
            <td class="border border-1 border-dark">Total</td>
            <td class="border border-1 border-dark">{t['staff_plan']}</td>
            <td class="border border-1 border-dark">{t['staff_actual']}</td>
            <td class="border border-1 border-dark">{t['dt_plan']}</td>
            <td class="border border-1 border-dark">{t['dt_actual']}</td>
            <td class="border border-1 border-dark">{t['iti_plan']}</td>
            <td class="border border-1 border-dark">{t['iti_actual']}</td>
            <td class="border border-1 border-dark">{t['trainee_plan']}</td>
            <td class="border border-1 border-dark">{t['trainee_actual']}</td>
            <td class="border border-1 border-dark">{t['naps_plan']}</td>
            <td class="border border-1 border-dark">{t['naps_actual']}</td>
            <td class="border border-1 border-dark">{t['cl_plan']}</td>
            <td class="border border-1 border-dark">{t['cl_actual']}</td>
            <td class="border border-1 border-dark">{t['nj_plan']}</td>
            <td class="border border-1 border-dark">{t['nj_actual']}</td>
            <td class="border border-1 border-dark">{t['ac_plan']}</td>
            <td class="border border-1 border-dark">{t['ac_actual']}</td>
            <td class="border border-1 border-dark">{t['plan_total']}</td>
            <td class="border border-1 border-dark">{t['cumulative']}</td>
            <td class="border border-1 border-dark">{t['absent_gap']}</td>
            <td class="border border-1 border-dark">{t['informed_leave']}</td>
            <td class="border border-1 border-dark">{t['uninformed_leave']}</td>
            <td class="border border-1 border-dark">{t['total_gap']}</td>
            <td class="border border-1 border-dark"></td>
            <td class="border border-1 border-dark"></td>
            <td class="border border-1 border-dark">{t['cl_ac_actual']}</td>
        </tr>
    </tbody></table></div>"""

    return data


# ─────────────────────────────────────────────────────────────────────────────
#  EXCEL DOWNLOAD
# ─────────────────────────────────────────────────────────────────────────────
@frappe.whitelist()
def download():
    filename = 'EmployeeCheckinWisePlanVsActualReport.xlsx'
    build_xlsx_response(filename)


def make_xlsx(sheet_name=None):
    args  = frappe.local.form_dict
    wb    = Workbook()
    ws    = wb.active
    ws.title = sheet_name if sheet_name else 'Sheet1'

    data = get_data(args)
    if not data:
        frappe.throw("No data available to generate the report.")

    for row in data:
        if not isinstance(row, (list, tuple)):
            row = [row]
        ws.append(row)

    # ── Cell merges (unchanged) ───────────────────────────────────────────────
    ws.merge_cells(start_row=3,  start_column=1,  end_row=4,  end_column=1)
    ws.merge_cells(start_row=1,  start_column=1,  end_row=2,  end_column=28)
    ws.merge_cells(start_row=3,  start_column=2,  end_row=4,  end_column=18)
    ws.merge_cells(start_row=3,  start_column=19, end_row=4,  end_column=24)
    ws.merge_cells(start_row=3,  start_column=25, end_row=4,  end_column=28)
    ws.merge_cells(start_row=5,  start_column=1,  end_row=8,  end_column=1)
    ws.merge_cells(start_row=5,  start_column=18, end_row=8,  end_column=18)
    ws.merge_cells(start_row=5,  start_column=2,  end_row=7,  end_column=3)
    ws.merge_cells(start_row=5,  start_column=4,  end_row=7,  end_column=5)
    ws.merge_cells(start_row=5,  start_column=6,  end_row=7,  end_column=7)
    ws.merge_cells(start_row=5,  start_column=8,  end_row=7,  end_column=9)
    ws.merge_cells(start_row=5,  start_column=10, end_row=7,  end_column=11)
    ws.merge_cells(start_row=5,  start_column=12, end_row=7,  end_column=13)
    ws.merge_cells(start_row=5,  start_column=14, end_row=7,  end_column=15)
    ws.merge_cells(start_row=5,  start_column=16, end_row=7,  end_column=17)
    for col in range(2, 18):
        ws.merge_cells(start_row=8, start_column=col, end_row=8, end_column=col)
    ws.merge_cells(start_row=5, start_column=19, end_row=8, end_column=19)
    ws.merge_cells(start_row=5, start_column=20, end_row=8, end_column=20)
    ws.merge_cells(start_row=5, start_column=21, end_row=8, end_column=22)
    ws.merge_cells(start_row=5, start_column=23, end_row=8, end_column=24)
    ws.merge_cells(start_row=5, start_column=25, end_row=8, end_column=25)
    ws.merge_cells(start_row=5, start_column=26, end_row=8, end_column=26)
    ws.merge_cells(start_row=5, start_column=27, end_row=8, end_column=27)
    ws.merge_cells(start_row=5, start_column=28, end_row=8, end_column=28)
    for x in range(9, ws.max_row + 1):
        ws.merge_cells(start_row=x, start_column=21, end_row=x, end_column=22)
        ws.merge_cells(start_row=x, start_column=23, end_row=x, end_column=24)

    apply_styles(ws)
    set_column_widths(ws)

    xlsx_file = BytesIO()
    wb.save(xlsx_file)
    xlsx_file.seek(0)
    return xlsx_file


# ─────────────────────────────────────────────────────────────────────────────
#  get_data  (used by Excel download)  – OPTIMIZED
# ─────────────────────────────────────────────────────────────────────────────
def get_data(args):
    if not args.get('date'):
        return []

    date      = args.get('date')
    fromdate  = datetime.strptime(date, '%Y-%m-%d').date()
    fromdate_ = fromdate.strftime('%d-%m-%Y')
    shift_arg = args.get('shift')
    shift_header = shift_arg if shift_arg else 'All Shift'

    # ── Header rows (unchanged layout) ───────────────────────────────────────
    data = [
        ["Employee Checkin Wise Man Power Plan Vs Actual Summary"],
        [""],
        ["", "Plan / Actual"] + [""] * 16 + ["Date: " + fromdate_] + [""] * 5 + ["Shift: " + shift_header],
        [""],
        ["Employee category / Department",
         "Staff", "", "JOE", "", "Tech", "", "Trainee", "", "NAPS", "",
         "Contract(CL)", "", "New Joining Trainees", "", "Temporary CL", "",
         "Total Plan", "Cummulative Actual", "Absent Gap (Plan-Actual)",
         "Informed Leave(HRMS request approved)", "",
         "Un informed Leave(HRMS request not approved)", "",
         "Total Gap", "Remarks", "Requested manpower", "Given manpower"],
        [""],
        [""],
        ["", "Plan", "Actual", "Plan", "Actual", "Plan", "Actual",
         "Plan", "Actual", "Plan", "Actual", "Plan", "Actual",
         "Plan", "Actual", "Plan", "Actual",
         "", "", "", "", "", "", "", "", ""]
    ]

    # ── Shift normalisation ───────────────────────────────────────────────────
    if shift_arg in ['1', '2']:
        shift_new    = [shift_arg]
        shift_single = shift_arg
    else:
        shift_new    = ['1', '2']
        shift_single = None

    # ── Determine departments (with role check) ───────────────────────────────
    user            = frappe.session.user
    has_misspunch   = "Miss Punch" in frappe.get_roles(user)
    employee        = frappe.db.get_value("Employee", {"user_id": user}, "name")
    selected_dept   = (args.get("department") or "").strip() or None

    if has_misspunch:
        if selected_dept:
            departments = [selected_dept]
        else:
            departments = [d.name for d in frappe.get_all(
                "Department",
                filters={"disabled": 0, "name": ["!=", "All Departments"]},
                order_by="name asc")]
    else:
        dept_name = frappe.db.get_value("Employee", employee, "department")
        departments = [selected_dept or dept_name] if (selected_dept or dept_name) else []

    if not departments:
        return data

    # ── Bulk data fetch (6 queries total regardless of dept count) ────────────
    (plan_lookup, plan_total_lookup,
     actual_lookup, actual_total_lookup,
     present_emp, planned_emp) = _get_bulk_data(date, shift_new, departments)

    approved_leave_lookup, not_approved_leave_lookup = _get_leave_counts(date, departments)

    if shift_single:
        perm_lookup, mp_lookup, od_lookup = _get_permission_misspunch_od(
            date, shift_single, departments)
    else:
        perm_lookup1, mp_lookup1, od_lookup1 = _get_permission_misspunch_od(date, '1', departments)
        perm_lookup2, mp_lookup2, od_lookup2 = _get_permission_misspunch_od(date, '2', departments)
        perm_lookup = {d: perm_lookup1.get(d, 0) + perm_lookup2.get(d, 0) for d in departments}
        mp_lookup   = {d: mp_lookup1.get(d, 0)   + mp_lookup2.get(d, 0)   for d in departments}
        od_lookup   = {d: od_lookup1.get(d, 0)   + od_lookup2.get(d, 0)   for d in departments}

    # ── Grand total accumulators ──────────────────────────────────────────────
    totals = defaultdict(int)

    for dept in departments:
        pl = plan_lookup[dept]
        al = actual_lookup[dept]

        plan_staff        = pl.get("Staff", 0)
        plan_dt           = pl.get("DT", 0)
        plan_iti          = pl.get("ITI", 0)
        plan_trainee      = pl.get("GT", 0) + pl.get("TT", 0)
        plan_naps         = pl.get("Naps", 0)
        plan_cl           = pl.get("CL", 0)
        plan_new_joinee   = pl.get("New Staff", 0) + pl.get("New Trainees", 0)
        plan_access_card  = pl.get("New CL", 0)
        plan_total        = plan_total_lookup.get(dept, 0)

        actual_staff       = al.get("Staff", 0)
        actual_dt          = al.get("DT", 0)
        actual_iti         = al.get("ITI", 0)
        actual_trainee     = al.get("GT", 0) + al.get("TT", 0)
        actual_naps        = al.get("Naps", 0)
        actual_cl          = al.get("CL", 0)
        actual_new_joinee  = al.get("New Staff", 0) + al.get("New Trainees", 0)
        actual_access_card = al.get("New CL", 0)
        cl_access_card_actual = al.get("CL (Access Card)", 0)
        actual_total       = actual_total_lookup.get(dept, 0)

        actual_total_permission = perm_lookup.get(dept, 0)
        actual_total_misspunch  = mp_lookup.get(dept, 0)
        actual_total_od         = od_lookup.get(dept, 0)

        actual_total_leave_application       = approved_leave_lookup.get(dept, 0)
        total_leave_application_not_approved = not_approved_leave_lookup.get(dept, 0)

        actual_total_cumulative = actual_total + actual_total_misspunch + actual_total_permission + actual_total_od
        actual_total_absent_gap = plan_total - actual_total_cumulative
        total_gap               = actual_total_leave_application + total_leave_application_not_approved

        remarks = _build_remarks_plain(dept, planned_emp, present_emp)

        # accumulate
        totals["staff_plan"]       += plan_staff
        totals["staff_actual"]     += actual_staff
        totals["dt_plan"]          += plan_dt
        totals["dt_actual"]        += actual_dt
        totals["iti_plan"]         += plan_iti
        totals["iti_actual"]       += actual_iti
        totals["trainee_plan"]     += plan_trainee
        totals["trainee_actual"]   += actual_trainee
        totals["naps_plan"]        += plan_naps
        totals["naps_actual"]      += actual_naps
        totals["cl_plan"]          += plan_cl
        totals["cl_actual"]        += actual_cl
        totals["nj_plan"]          += plan_new_joinee
        totals["nj_actual"]        += actual_new_joinee
        totals["ac_plan"]          += plan_access_card
        totals["ac_actual"]        += actual_access_card
        totals["plan_total"]       += plan_total
        totals["cumulative"]       += actual_total_cumulative
        totals["absent_gap"]       += actual_total_absent_gap
        totals["informed_leave"]   += actual_total_leave_application
        totals["uninformed_leave"] += total_leave_application_not_approved
        totals["total_gap"]        += total_gap
        totals["cl_ac_actual"]     += cl_access_card_actual

        row = [
            dept,
            plan_staff, actual_staff,
            plan_dt, actual_dt,
            plan_iti, actual_iti,
            plan_trainee, actual_trainee,
            plan_naps, actual_naps,
            plan_cl, actual_cl,
            plan_new_joinee, actual_new_joinee,
            plan_access_card, actual_access_card,
            plan_total,
            actual_total_cumulative,
            actual_total_absent_gap,
            actual_total_leave_application, "",
            total_leave_application_not_approved, "",
            total_gap,
            remarks, "",
            cl_access_card_actual
        ]
        data.append(row)

    t = totals
    extra_row = [
        "Totals",
        t["staff_plan"],    t["staff_actual"],
        t["dt_plan"],       t["dt_actual"],
        t["iti_plan"],      t["iti_actual"],
        t["trainee_plan"],  t["trainee_actual"],
        t["naps_plan"],     t["naps_actual"],
        t["cl_plan"],       t["cl_actual"],
        t["nj_plan"],       t["nj_actual"],
        t["ac_plan"],       t["ac_actual"],
        t["plan_total"],
        t["cumulative"],
        t["absent_gap"],
        t["informed_leave"],
        t["uninformed_leave"],
        t["total_gap"],
        "",
        t["cl_ac_actual"]
    ]
    data.append(extra_row)
    return data


# ─────────────────────────────────────────────────────────────────────────────
#  Styling helpers (unchanged from original)
# ─────────────────────────────────────────────────────────────────────────────
def apply_styles(ws):
    align_center      = Alignment(horizontal='center', vertical='center', wrap_text=True)
    align_right       = Alignment(horizontal='right',  vertical='top',    wrap_text=True)
    align_left        = Alignment(horizontal='left',   vertical='top',    wrap_text=True)
    header_font       = Font(bold=True, size=14)
    text_font         = Font(bold=True, size=8)
    text_font_header  = Font(bold=True, size=12)
    text_font_data    = Font(bold=False, size=9)
    border = Border(
        left=Side(border_style='thin'), right=Side(border_style='thin'),
        top=Side(border_style='thin'),  bottom=Side(border_style='thin')
    )
    peach = PatternFill(fgColor="ffe5b4", fill_type="solid")

    for rows in ws.iter_rows(min_row=1, max_row=8, min_col=1, max_col=ws.max_column):
        for cell in rows:
            cell.fill = peach
    for rows in ws.iter_rows(min_row=ws.max_row, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
        for cell in rows:
            cell.fill = peach

    for rows in ws.iter_rows(min_row=1, max_row=2, min_col=1, max_col=ws.max_column):
        for cell in rows:
            cell.font = header_font; cell.alignment = align_center; cell.border = border

    for col_range in [(2,18),(1,2),(19,24),(25,ws.max_column)]:
        for rows in ws.iter_rows(min_row=3, max_row=4, min_col=col_range[0], max_col=col_range[1]):
            for cell in rows:
                cell.font = text_font_header; cell.alignment = align_center; cell.border = border

    for col_start, col_end in [(1,1),(2,3),(4,5),(6,7),(8,9),(10,11),
                                (12,13),(14,15),(16,17),(18,18),
                                (19,19),(20,20),(21,21),(22,22),(23,25)]:
        for rows in ws.iter_rows(min_row=5, max_row=7, min_col=col_start, max_col=col_end):
            for cell in rows:
                cell.font = text_font; cell.alignment = align_center; cell.border = border

    for x in range(26, 29):
        for rows in ws.iter_rows(min_row=5, max_row=7, min_col=x, max_col=x):
            for cell in rows:
                cell.font = text_font; cell.alignment = align_center; cell.border = border

    for col in range(1, ws.max_column + 1):
        for rows in ws.iter_rows(min_row=8, max_row=8, min_col=col, max_col=col):
            for cell in rows:
                cell.font = text_font; cell.alignment = align_center; cell.border = border

    for x in range(9, ws.max_row + 1):
        for rows in ws.iter_rows(min_row=x, max_row=x, min_col=1, max_col=1):
            for cell in rows:
                cell.font = text_font; cell.alignment = align_left; cell.border = border
        for rows in ws.iter_rows(min_row=x, max_row=x, min_col=2, max_col=20):
            for cell in rows:
                cell.font = text_font_data; cell.alignment = align_right; cell.border = border
        for rows in ws.iter_rows(min_row=x, max_row=x, min_col=21, max_col=24):
            for cell in rows:
                cell.font = text_font_data; cell.alignment = align_right; cell.border = border
        for rows in ws.iter_rows(min_row=x, max_row=x, min_col=25, max_col=25):
            for cell in rows:
                cell.font = text_font_data; cell.alignment = align_right; cell.border = border
        for rows in ws.iter_rows(min_row=x, max_row=x, min_col=26, max_col=ws.max_column):
            for cell in rows:
                cell.font = text_font_data; cell.alignment = align_left; cell.border = border


def set_column_widths(ws):
    column_widths = [18, 5] + [5]*13 + [7]*2 + [5] + [6] + [5]*4 + [6] + [4]*5 + [8]*7
    for i, width in enumerate(column_widths, start=1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = width
    ws.column_dimensions[openpyxl.utils.get_column_letter(26)].width = 80


def build_xlsx_response(filename):
    xlsx_file = make_xlsx(sheet_name=filename)
    frappe.response['filename']    = filename + '.xlsx'
    frappe.response['filecontent'] = xlsx_file.getvalue()
    frappe.response['type']        = 'binary'