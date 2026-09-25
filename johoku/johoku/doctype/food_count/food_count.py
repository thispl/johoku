# Copyright (c) 2026, TEAMPRO and contributors
# For license information, please see license.txt
from frappe.model.document import Document
import frappe
from frappe.utils import getdate, now_datetime, add_days
from frappe.utils import getdate, formatdate

class FoodCount(Document):
    def validate(self):
        
        if getattr(self, "flags", None) and self.flags.get("ignore_food_validation"):
            return
        
        food_date = getdate(self.date)
        existing = frappe.db.exists(  "Food Count",  { "date": food_date, "employee": self.employee,  "name": ["!=", self.name] })
        if existing:
            formatted_date = formatdate(food_date, "dd-MM-yyyy")
            frappe.throw(f"Already record exists for date {formatted_date}")
			
        current_dt = now_datetime()
        today = getdate(current_dt)
        food_date = getdate(self.date)

        if food_date < today:
            frappe.throw("You cannot apply for past dates")

        today_weekday = current_dt.weekday()
        food_weekday = food_date.weekday()

        # if food_weekday == 2:

        #     # Must apply only on Tuesday
        #     if today_weekday != 1:
        #         frappe.throw("For Wednesday food, apply only on Tuesday")

        #     # Must apply before 12 PM
        #     if current_dt.hour >= 12:
        #         frappe.throw("For Wednesday food, apply before 12:00 PM")

        if food_weekday == 2:

            # Previous Thursday
            allowed_from = add_days(food_date, -6)
            # Previous Tuesday
            allowed_till = add_days(food_date, -1)


            # Date validation
            if today < allowed_from or today > allowed_till:
                frappe.throw(
                    "For Wednesday food, application is allowed only "
                    "from previous Thursday to Tuesday 12 PM"
                )

            # Tuesday 12 PM validation
            if today == allowed_till and current_dt.hour >= 12:
                frappe.throw(
                    "For Wednesday food, apply before Tuesday 12:00 PM"
                )
        
        else:
            pass

# @frappe.whitelist()
# def auto_create_food_count():
#     current_dt = now_datetime()

#     if current_dt.weekday() != 1 or current_dt.hour < 13:
#         return

#     today = getdate(current_dt)
#     coming_wed = add_days(today, 1)
#     prev_wed = add_days(coming_wed, -7)

#     employees = frappe.get_all("Employee", filters={"status": "Active"}, pluck="name")

#     for emp in employees:
#         exists = frappe.db.exists("Food Count", {
#             "employee": emp,
#             "date": coming_wed
#         })

#         if exists:
#             continue

#         last_entry = frappe.get_all(
#             "Food Count",
#             filters={
#                 "employee": emp,
#                 "date": prev_wed
#             },
#             fields=["food_type"],
#             limit=1
#         )

#         if not last_entry:
#             continue

#         doc = frappe.new_doc("Food Count")
#         doc.employee = emp
#         doc.date = coming_wed
#         doc.food_type = last_entry[0].food_type

#         doc.insert(ignore_permissions=True)

#     frappe.db.commit()

@frappe.whitelist()
def auto_create_food_count():

    current_dt = now_datetime()

    if current_dt.weekday() != 1 or current_dt.hour < 13:
        return

    today = getdate(current_dt)

    coming_day = add_days(today, 1)

    prev_day = add_days(coming_day, -7)

    employees = frappe.get_all(
        "Employee",
        filters={"status": "Active"},
        pluck="name",
    )

    for emp in employees:

        if frappe.db.exists("Food Count", {"employee": emp, "date": coming_day}):
            continue
        last_entry = frappe.get_all(
            "Food Count",
            filters={"employee": emp, "date": prev_day},
            fields=["food_type"],
            limit=1,
        )
        if not last_entry:
            continue
        doc = frappe.new_doc("Food Count")
        doc.employee = emp
        doc.date = coming_day
        doc.food_type = last_entry[0].food_type

        doc.flags.ignore_food_validation = True

        doc.insert(ignore_permissions=True)

    frappe.db.commit()
    
@frappe.whitelist()
def create_scheduled_job_food_count():
    job = frappe.db.exists('Scheduled Job Type', 'Wednesday Food Count')
    if not job:
        emc = frappe.new_doc("Scheduled Job Type")
        emc.update({
            "method": 'johoku.johoku.doctype.food_count.food_count.auto_create_food_count',
            "frequency": 'Cron',
            "cron_format": '0 13 * * 2'
        })
        emc.save(ignore_permissions=True)
    
# import frappe
# from frappe.utils import getdate, now_datetime, add_days

# def test_auto_create_food_count():
#     current_dt = now_datetime()

#     # if current_dt.weekday() != 1 or current_dt.hour < 13:
#     #     return

#     today = getdate(current_dt)

#     # So next day = Wednesday
#     coming_wed = add_days(today, 1)

#     # Previous week Wednesday
#     prev_wed = add_days(coming_wed, -7)

#     employees = frappe.get_all(
#         "Employee",
#         filters={"status": "Active"},
#         pluck="name"
#     )

#     for emp in employees:

#         # Already exists check
#         exists = frappe.db.exists("Food Count", {
#             "employee": emp,
#             "date": coming_wed
#         })

#         if exists:
#             continue

#         # Get last week data
#         last_entry = frappe.get_all(
#             "Food Count",
#             filters={
#                 "employee": emp,
#                 "date": prev_wed
#             },
#             fields=["food_type"],
#             limit=1
#         )

#         if not last_entry:
#             continue

#         # Create new doc
#         doc = frappe.new_doc("Food Count")
#         doc.employee = emp
#         doc.date = coming_wed
#         doc.food_type = last_entry[0].food_type

#         doc.insert(ignore_permissions=True)

#     frappe.db.commit()

#     frappe.msgprint("Test Auto Food Count Created Successfully")