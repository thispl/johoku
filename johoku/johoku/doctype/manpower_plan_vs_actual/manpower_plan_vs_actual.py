# Copyright (c) 2024, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime

class ManpowerPlanvsActual(Document):
    pass

@frappe.whitelist(allow_guest=True)
def get_data_system(date, shift):
    # frappe.errprint(shift)
    # frappe.errprint(date)
    date_  = datetime.strptime(date, "%Y-%m-%d").strftime('%d-%m-%Y')
    data = f"""<h2 class='text-center' style="color: black;">Manpower Category wise plan vs Actual Summary</h2>
            <div style="overflow-x: auto; color: black;">
            <table class="text-center" style="overflow: hidden; white-space: wrap;">
        <tr>
            <td colspan="31">
                
            </td>
        </tr>
        <tr style="background-color: #ffe5b4; font-weight: 500; color: black;">
            <td style="width: 200px;" colspan=1 class="border border-1 border-dark"></td>
            <td  colspan=17 class="border border-1 border-dark">
                <strong>Plan / Count
                </strong>
            </td>
            <td  colspan=9 class="border border-1 border-dark">
                <strong>Date: { date_ }
                </strong>
            </td>
            <td  colspan=4 class="border border-1 border-dark">
                <strong>Shift: { shift or "All Shift"}
                </strong>
            </td>
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
            <td colspan=4 class="border border-1 border-dark" style="min-width: 100px;">Total Actual</td>
            <td rowspan=3 class="border border-1 border-dark" style="min-width: 100px;">Cummulative Actual</td>
            <td rowspan=3 class="border border-1 border-dark" style="min-width: 100px;">Absent Gap (Plan-Actual)</td>
            <td rowspan=3 class="border border-1 border-dark" style="min-width: 100px;">Informed Leave(HRMS request approved)</td>
            <td rowspan=3 class="border border-1 border-dark" style="min-width: 100px;"> Un informed Leave(HRMS request not approved)</td>
            <td rowspan=3 class="border border-1 border-dark" style="min-width: 100px;">Total Gap</td>
            <td rowspan=3 class="border border-1 border-dark" style="min-width: 100px;">Requested manpower</td>
            <td rowspan=3 class="border border-1 border-dark" style="min-width: 100px;">Given manpower</td>
            <td rowspan=3 class="border border-1 border-dark" style="min-width: 100px;">Remarks</td>
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
            <td colspan=4 class="border border-1 border-dark" style="min-width: 50px;">Present</td>
        </tr>
        <tr style="background-color: #ffe5b4; font-weight: 500; color: black;">
            
            <td class="border border-1 border-dark" style="min-width: 100px;">Actual Present</td>
            <td class="border border-1 border-dark" style="min-width: 100px;">Permission</td>
            <td class="border border-1 border-dark" style="min-width: 100px;">Misspunch</td>
            <td class="border border-1 border-dark" style="min-width: 100px;">OD</td>
        </tr>
    
        """
    departments = frappe.get_all("Department",{"disabled": 0,"name": ["!=", "All Departments"]},["name"], order_by="name asc")
    if shift == '1' or shift == '2':
        shift = shift
    else:
        shift = ['is', 'set'] 
    # frappe.errprint(shift)
    # frappe.errprint(date)
    total_planning_staff,total_plan_cl ,total_plan_dt, total_plan_iti,total_plan_naps,total_plan_trainee = 0,0,0,0,0,0
    total_actual_dt,total_actual_staff,total_actual_naps,total_actual_iti,total_actual_cl, total_actual_trainee =0, 0,0,0,0,0
    total_cumulative,total_coff,total_absent_gap,total_of_total_gap,total_od,total_permission,actual_leave,plan_leave,total_misspunch = 0,0,0,0,0,0,0,0,0
    total_plan_total,total_actual_total =0, 0
    total_plan_access_card, total_actual_access_card =0,0
    total_plan_new_joinee,total_actual_new_joinee = 0,0
    total_cl_access_card_actual =0
    for dept in departments:
        remarks = ""
        if dept.name != "All Departments":
            conditions = {
                'department': dept.name,
                'shift': shift,
                'attendance_date': ["between", [date, date]],
                'docstatus':['!=',2] 
            }
            
            planed_emp = frappe.db.get_all("Shift Assignment",{'department': dept.name,'start_date': date,'shift_type':shift,'docstatus': 1,'employee_category': ['in',['Staff','Manager','ITI','TT','Naps','CL','GT','New CL','New Staff','New Trainees']]},pluck="employee")
            frappe.errprint(f"Planned Employees: {planed_emp}")
            present_emp = frappe.db.get_all("Attendance",{**conditions, 'category': ['in',['Staff','Manager','ITI','TT','Naps','CL','GT','New CL','New Staff','New Trainees']]},pluck="employee" )
            for i in planed_emp:
                if i not in present_emp:
                    emp_name = frappe.db.get_value("Employee",i,"employee_name")
                    if remarks =='':
                        remarks+=f"{i} : {emp_name}"
                    else:
                        remarks+=f", {i} : {emp_name}"
            # Get employee categories and prepare row structure
            employee_categories = frappe.get_all("Employee Category", fields=["name"], order_by='name')
            total_plan= 0
    
            plan_staff, actual_staff, plan_cl, plan_dt, plan_gt, plan_iti, plan_naps, actual_cl, actual_dt, actual_new_joinee, actual_access_card = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            plan_tt, actual_tt, actual_gt, actual_iti, actual_naps, actual_trainee, plan_trainee, plan_new_joinee, plan_access_card = 0, 0, 0, 0, 0, 0, 0, 0, 0
            actual_total_permission, actual_total_misspunch, actual_total_coff, actual_total_od, actual_total_absent_gap, actual_total_cumulative = 0, 0, 0, 0, 0, 0
            actual_total_leave_application, total_leave_application_not_approved, total_gap = 0, 0, 0
            new_trainee_plan_access_card,new_staff_plan_access_card,new_staff_actual_access_card,new_trainee_actual_access_card =0,0,0,0
            cl_access_card_actual,cl_access_card_plan =0,0
            # Loop through employee categories
            for emp_category in employee_categories:
                emp_category_name = emp_category['name']
                plan_field = 'employee_category'
                actual_field = 'category'
                

                if emp_category_name == "Staff":
                    plan_staff = frappe.db.count("Shift Assignment", {
                        'department': dept.name,
                        plan_field: emp_category_name,
                        'start_date': date,
                        'shift_type':shift,
                        'docstatus': 1
                    })
                    actual_staff = frappe.db.count("Attendance", {**conditions, actual_field: emp_category_name})
                    
                elif emp_category_name == "Manager":
                    plan_dt = frappe.db.count("Shift Assignment", {
                        'department': dept.name,
                        plan_field: emp_category_name,
                        'start_date': date,
                        'shift_type':shift,
                        'docstatus': 1
                    })
                    actual_dt = frappe.db.count("Attendance", {**conditions, actual_field: emp_category_name})
                
                elif emp_category_name == "ITI":
                    plan_iti = frappe.db.count("Shift Assignment", {
                        'department': dept.name,
                        plan_field: emp_category_name,
                        'start_date': date,
                        'shift_type':shift,
                        'docstatus': 1
                    })
                    actual_iti = frappe.db.count("Attendance", {**conditions, actual_field: emp_category_name})
                    
                elif emp_category_name == "TT":
                    plan_tt = frappe.db.count("Shift Assignment", {
                        'department': dept.name,
                        plan_field: emp_category_name,
                        'start_date': date,
                        'shift_type':shift,
                        'docstatus': 1
                    })
                    actual_tt = frappe.db.count("Attendance", {**conditions, actual_field: emp_category_name})
                    
                elif emp_category_name == "Naps":
                    plan_naps = frappe.db.count("Shift Assignment", {
                        'department': dept.name,
                        plan_field: emp_category_name,
                        'start_date': date,
                        'shift_type':shift,
                        'docstatus': 1
                    })
                    actual_naps = frappe.db.count("Attendance", {**conditions, actual_field: emp_category_name})
                    
                elif emp_category_name == "CL":
                    plan_cl = frappe.db.count("Shift Assignment", {
                        'department': dept.name,
                        plan_field: emp_category_name,
                        'start_date': date,
                        'shift_type':shift,
                        'docstatus': 1
                    })
                    actual_cl = frappe.db.count("Attendance", {**conditions, actual_field: emp_category_name})
                    
                elif emp_category_name == "GT":
                    plan_gt = frappe.db.count("Shift Assignment", {
                        'department': dept.name,
                        plan_field: emp_category_name,
                        'start_date': date,
                        'shift_type':shift,
                        'docstatus': 1
                    })
                    actual_gt = frappe.db.count("Attendance", {**conditions, actual_field: emp_category_name})
                    
                elif emp_category_name == "New CL":
                    plan_access_card = frappe.db.count("Shift Assignment", {
                        'department': dept.name,
                        plan_field: emp_category_name,
                        'start_date': date,
                        'shift_type':shift,
                        'docstatus': 1
                    })
                    actual_access_card = frappe.db.count("Attendance", {**conditions, actual_field: emp_category_name})
                    
                elif emp_category_name == "New Staff":
                    new_staff_plan_access_card = frappe.db.count("Shift Assignment", {
                        'department': dept.name,
                        plan_field: emp_category_name,
                        'start_date': date,
                        'shift_type':shift,
                        'docstatus': 1
                    })
                    new_staff_actual_access_card = frappe.db.count("Attendance", {**conditions, actual_field: emp_category_name})
                    
                elif emp_category_name == "New Trainees":
                    new_trainee_plan_access_card = frappe.db.count("Shift Assignment", {
                        'department': dept.name,
                        plan_field: emp_category_name,
                        'start_date': date,
                        'shift_type':shift,
                        'docstatus': 1
                    })
                    new_trainee_actual_access_card = frappe.db.count("Attendance", {**conditions, actual_field: emp_category_name})
                    
                elif emp_category_name == "CL (Access Card)":
                    cl_access_card_plan = frappe.db.count("Shift Assignment", {
                        'department': dept.name,
                        plan_field: emp_category_name,
                        'start_date': date,
                        'shift_type':shift,
                        'docstatus': 1
                    })
                    cl_access_card_actual = frappe.db.count("Attendance", {**conditions, actual_field: emp_category_name})
                    
                plan_new_joinee = new_trainee_plan_access_card + new_staff_plan_access_card
                actual_new_joinee = new_staff_actual_access_card + new_trainee_actual_access_card
            actual_trainee = actual_gt + actual_tt
            plan_trainee = plan_gt + plan_tt
            plan_total = frappe.db.count("Shift Assignment", {
                'department': dept.name,
                'start_date': date,
                'shift_type':shift,
                'employee_category': ('not in', ['CL (Access Card)']),
                'docstatus': 1
            })
            actual_total = frappe.db.count("Attendance", {
                'department': dept.name,
                'shift': shift,
                'category': ('not in', ['CL (Access Card)']),
                'attendance_date': ["between", [date, date]],
                'docstatus':['!=',2] 
            })
            
            actual_total_permission = frappe.db.count("Attendance", {
                'department': dept.name,
                'shift': shift,
                'permission': ["!=", ""],
                'category': ('not in', ['CL (Access Card)']),
                'attendance_date': ["between", [date, date]],
                'docstatus':['!=',2] 
            })
            actual_total_misspunch = frappe.db.count("Attendance", {
                'department': dept.name,
                'shift': shift,
                'category': ('not in', ['CL (Access Card)']),
                'miss_punch': ["!=", ""],
                'attendance_date': ["between", [date, date]],
                'docstatus':['!=',2] 
            })
            
            actual_total_od = frappe.db.count("Attendance", {
                'department': dept.name,
                'shift': shift,
                'category': ('not in', ['CL (Access Card)']),
                'on_duty_application': ["!=", ""],
                'attendance_date': ["between", [date, date]],
                'docstatus':['!=',2] 
            })
            approved_leaves = frappe.db.get_all(
                "Attendance",
                {
                    'department': dept.name,
                    'leave_application': ["!=", ""],  
                    'attendance_date': date ,
                    'category': ('not in', ['CL (Access Card)']),
                    'docstatus':['!=',2]     
                },
                ['employee']  
            )
            for leave in approved_leaves:
                shift_count_leaves = frappe.db.count(
                    'Shift Assignment',
                    {
                        'employee': leave.employee,       
                        'start_date': date,         
                        'end_date': date,
                        'shift_type': shift, 
                        'employee_category': ('not in', ['CL (Access Card)']),             
                        'docstatus': ('!=', 2)           
                    }
                )
                
                actual_total_leave_application += shift_count_leaves

            
            not_approved_leaves = frappe.db.sql("""
                select employee
                from `tabLeave Application`
                where docstatus = 0 and department = %(department)s
                    and (from_date between %(from_date)s and %(to_date)s
                        or to_date between %(from_date)s and %(to_date)s
                        or (from_date < %(from_date)s and to_date > %(to_date)s))
                """, {
                    "from_date": date,
                    "to_date": date,
                    "department":dept.name
                },
            as_dict = True)
            for leave in not_approved_leaves:
                shift_count_leaves_ = frappe.db.count(
                    'Shift Assignment',
                    {
                        'employee': leave['employee'],       
                        'start_date': date,         
                        'end_date': date,
                        'shift_type': shift, 
                        'employee_category': ('not in', ['CL (Access Card)']),             
                        'docstatus': ('!=', 2)           
                    }
                )
                
                total_leave_application_not_approved += shift_count_leaves_
            actual_total_cumulative = actual_total + actual_total_misspunch + actual_total_permission + actual_total_od
            actual_total_absent_gap = plan_total - actual_total_cumulative
            total_gap = total_leave_application_not_approved + actual_total_leave_application
            total_planning_staff += plan_staff 
            total_actual_staff += actual_staff
            total_plan_dt += plan_dt
            total_actual_dt += actual_dt
            total_plan_iti += plan_iti
            total_plan_trainee += plan_trainee
            total_plan_naps +=plan_naps
            total_plan_cl += plan_cl
            total_actual_iti += actual_iti
            total_actual_trainee += actual_trainee
            total_actual_naps += actual_naps
            total_actual_cl += actual_cl
            plan_leave += actual_total_leave_application
            actual_leave += total_leave_application_not_approved
            total_of_total_gap +=total_gap
            total_permission += actual_total_permission
            total_misspunch += actual_total_misspunch
            total_od += actual_total_od
            total_coff += actual_total_coff
            total_plan_total +=plan_total
            total_actual_total += actual_total
            total_cumulative += actual_total_cumulative
            total_absent_gap += actual_total_absent_gap
            total_actual_access_card +=actual_access_card
            total_plan_access_card += plan_access_card
            total_actual_new_joinee +=actual_new_joinee
            total_plan_new_joinee+=plan_new_joinee
            total_cl_access_card_actual += cl_access_card_actual
            data += f"""
                <tr>
                    <td class="border border-1 border-dark text-left pl-3">{dept.name}</td>
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
                     <td class="border border-1 border-dark">{actual_total}</td>
                    <td class="border border-1 border-dark">{actual_total_permission}</td>
                    <td class="border border-1 border-dark">{actual_total_misspunch}</td>
                      <td class="border border-1 border-dark">{actual_total_od}</td>
                    <td class="border border-1 border-dark">{actual_total_cumulative}</td>
                    <td class="border border-1 border-dark">{actual_total_absent_gap}</td>
                    <td class="border border-1 border-dark">{actual_total_leave_application}</td>
                    <td class="border border-1 border-dark">{total_leave_application_not_approved}</td>
                    <td class="border border-1 border-dark">{total_gap}</td>
                    <td class="border border-1 border-dark"></td>
                    <td class="border border-1 border-dark">{cl_access_card_actual}</td>
                    <td class="border border-1 border-dark" style="white-space: nowrap; overflow-x: auto; max-width:500px;text-align:left;">{remarks}</td>
                    
                </tr>
            """
    
    data += f"""
                    <tr style="font-weight: 700;">
                        <td class="border border-1 border-dark">Total</td>
                        <td class="border border-1 border-dark">{total_planning_staff}</td>
                        <td class="border border-1 border-dark">{total_actual_staff}</td>
                        <td class="border border-1 border-dark">{total_plan_dt}</td>
                        <td class="border border-1 border-dark">{total_actual_dt}</td>
                        <td class="border border-1 border-dark">{total_plan_iti}</td>
                        <td class="border border-1 border-dark">{total_actual_iti}</td>
                        <td class="border border-1 border-dark">{total_plan_trainee}</td>
                        <td class="border border-1 border-dark">{total_actual_trainee}</td>
                        <td class="border border-1 border-dark">{total_plan_naps}</td>
                        <td class="border border-1 border-dark">{total_actual_naps}</td>
                        <td class="border border-1 border-dark">{total_plan_cl}</td>
                        <td class="border border-1 border-dark">{total_actual_cl}</td>
                        <td class="border border-1 border-dark">{total_plan_new_joinee}</td>
                        <td class="border border-1 border-dark">{total_actual_new_joinee}</td>
                        <td class="border border-1 border-dark">{total_plan_access_card}</td>
                        <td class="border border-1 border-dark">{total_actual_access_card}</td>
                        <td class="border border-1 border-dark">{total_plan_total}</td>
                        <td class="border border-1 border-dark">{total_actual_total}</td>
                        <td class="border border-1 border-dark">{total_permission}</td>
                        <td class="border border-1 border-dark">{total_misspunch}</td>
                        <td class="border border-1 border-dark">{total_od}</td>
                        <td class="border border-1 border-dark">{total_cumulative}</td>
                        <td class="border border-1 border-dark">{total_absent_gap}</td>
                        <td class="border border-1 border-dark">{plan_leave}</td>
                        <td class="border border-1 border-dark">{actual_leave}</td>
                        <td class="border border-1 border-dark">{total_of_total_gap}</td>
                        <td class="border border-1 border-dark"></td>
                        <td class="border border-1 border-dark">{total_cl_access_card_actual}</td>
                        <td class="border border-1 border-dark"></td>
                        
                    </tr>
                 </table></div>
             """
    return data

