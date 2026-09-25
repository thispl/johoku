from datetime import datetime, timedelta
import frappe

def execute(filters=None):
    """Main report function."""
    if not filters:
        frappe.throw("Filters are required.")
    
    # Validate date range
    start_date = filters.get("start_date")
    end_date = filters.get("end_date")
    if not start_date or not end_date:
        frappe.throw("Both Start Date and End Date are required.")
    if datetime.strptime(start_date, "%Y-%m-%d") > datetime.strptime(end_date, "%Y-%m-%d"):
        frappe.throw("Start Date cannot be after End Date.")

    # Generate date labels
    day_abbr = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
    days = []
    current_date = start_date_obj
    while current_date <= end_date_obj:
        day_name = day_abbr[current_date.weekday()]
        days.append(f"{current_date.day} {day_name}")
        current_date += timedelta(days=1)

    # Fetch data and chart
    data, chart_data = get_data_and_chart(filters, days, start_date_obj, end_date_obj)

    return ["Department", "Present"], data, chart_data


def get_attendance_count(shift, date, department=None):
    """Fetch attendance count for a specific date, shift, and department."""
    conditions = {"shift": shift, "attendance_date": date}
    if department:
        conditions["department"] = department
    return frappe.db.count("Attendance", conditions)


def get_data_and_chart(filters, days, start_date_obj, end_date_obj):
    """Fetch data for the report and generate chart data."""
    shift = filters.get("shift")
    department = filters.get("department")

    data = []
    chart_data = {
        "labels": days,  # X-axis labels (dates or day names)
        "datasets": [{"name": "Present", "values": []}]
    }

    # Get departments
    departments = (
        [frappe.get_doc("Department", department)]
        if department
        else frappe.get_all("Department", filters={"disabled": 0}, order_by="name asc")
    )

    # Fetch attendance for each department
    for dept in departments:
        dept_name = dept.name if isinstance(dept, frappe._dict) else dept.get("name")
        row = [dept_name]
        total_present_count = 0

        current_date = start_date_obj
        while current_date <= end_date_obj:
            date_str = current_date.strftime("%Y-%m-%d")
            present_count = get_attendance_count(shift, date_str, dept_name)
            total_present_count += present_count
            current_date += timedelta(days=1)

        row.append(total_present_count)
        data.append(row)
        chart_data["datasets"][0]["values"].append(total_present_count)

    return data, chart_data


@frappe.whitelist()
def get_chart_data(filters):
    """API to fetch chart data."""
    filters = frappe.parse_json(filters)
    start_date = filters.get("start_date")
    end_date = filters.get("end_date")
    shift = filters.get("shift")
    department = filters.get("department")

    # Generate date labels
    day_abbr = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
    days = []
    current_date = start_date_obj
    while current_date <= end_date_obj:
        day_name = day_abbr[current_date.weekday()]
        days.append(f"{current_date.day} {day_name}")
        current_date += timedelta(days=1)

    _, chart_data = get_data_and_chart(filters, days, start_date_obj, end_date_obj)
    return {"chart": chart_data}
