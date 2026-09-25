from . import __version__ as app_version

app_name = "johoku"
app_title = "Johoku"
app_publisher = "TEAMPRO"
app_description = "Customizations for Johoku"
app_email = "erp@groupteampro.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/johoku/css/johoku.css"
# app_include_js = "/assets/johoku/js/johoku.js"

# include js, css files in header of web template
# web_include_css = "/assets/johoku/css/johoku.css"
# web_include_js = "/assets/johoku/js/johoku.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "johoku/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
jinja = {
	# "methods": "johoku.utils.jinja_methods",
	# "filters": "johoku.utils.jinja_filters"
	"methods": ["johoku.utils.payslip_leave_data",
    "johoku.utils.payslip_leave_data_for_gt_and_tt"]
}

# Installation
# ------------

# before_install = "johoku.install.before_install"
# after_install = "johoku.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "johoku.uninstall.before_uninstall"
# after_uninstall = "johoku.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "johoku.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Salary Slip":"johoku.overrides.CustomSalarySlip",
	"Employee Checkin": "johoku.overrides.CustomEmployeeCheckin",
	"Leave Application":"johoku.overrides.CustomLeaveApplication",
	"Compensatory Leave Request": "johoku.overrides.CustomCompensatoryLeaveRequest",
    "Leave Allocation":"johoku.overrides.CustomLeaveAllocation",
	"Employee":"johoku.overrides.CustomEmployee",
 	"Shift Request": "johoku.overrides.CustomShiftRequest"

}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Employee":{
		"validate": "johoku.employee_custom.inactive_employee",
        "after_insert":"johoku.employee_custom.calculate_age"
	},
    "Leave Application" :{
        "after_insert": "johoku.leave_application_custom.validate_leave",
        "validate": "johoku.leave_application_custom.restrict_for_zero_balance",
        "on_update":"johoku.leave_application_custom.update_status"
        
	},
    'Scheduled Job Log':{
       "validate":"johoku.custom.schedule_log_fail" 
	},
    'Compensatory Leave Request':{
        # "after_insert": "johoku.custom.validate_com_off",
        "on_cancel":'johoku.comp_off_custom.compensatory_on_cancel',
	},
    # "Shift Assignment": {
    #     "on_cancel": "johoku.mark_attendance.shift_assignment_cancelled"
    # },
    'Attendance':{
       "validate":"johoku.attendance_custom.submit_att" ,
    #    "on_submit":"johoku.custom.create_coff" ,
    #    'after_insert':"johoku.custom.submit_att_leave" ,
	},
    # "Holiday List":{
	# 	"validate":"johoku.custom.validate_the_holiday_list",
	# },
	# "Overtime Plan": {
	# 	"on_submit": "johoku.johoku.doctype.overtime_plan.overtime_plan.create_overtime_list",
	# },	
}

# Scheduled Tasks
# ---------------

scheduler_events = {
# 	"all": [
# 		"johoku.tasks.all"
# 	],
# 	"daily": [
# 		"johoku.tasks.daily"
# 	],
# 	"hourly": [
# 		"johoku.tasks.hourly"
# 	],
# 	"weekly": [
# 		"johoku.tasks.weekly"
# 	],
# 	"monthly": [
# 		"johoku.tasks.monthly"
# 	],
"cron":{
		"*/7 * * * *" :[
			'johoku.mark_attendance.push_punch'
		],
		"*/11 * * * *" :[
			'johoku.mark_attendance.mark_att'
		],
		"30 00 * * *" :[
			'johoku.mark_attendance.delete_urc_automatically'
		],
        "00 17 20 * *" :[
			'johoku.mark_attendance.mark_late_early_monthly'
		],
        "0 7 * * *": [ 
            "johoku.employee_custom.send_birthday_reminder_to_hr_new1"
        ],
      
        "0 13 * * 2": [  
            "johoku.johoku.doctype.food_count.food_count.auto_create_food_count"
        ]

	}
}

# Testing
# -------

# before_tests = "johoku.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "johoku.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "johoku.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"johoku.auth.validate"
# ]

# Translation
# --------------------------------

# Make link fields search translated document names for these DocTypes
# Recommended only for DocTypes which have limited documents with untranslated names
# For example: Role, Gender, etc.
# translated_search_doctypes = []
