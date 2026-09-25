import frappe
import requests
from frappe.model.document import Document

class MarkAttendance(Document):
	pass


@frappe.whitelist()
def fetch_geolocation_details(lat, lon):
	"""
	Fetch geolocation details (address, district, state, pincode)
	using latitude and longitude from OpenStreetMap Nominatim API.
	"""
	try:
		lat = float(lat)
		lon = float(lon)

		url = f"https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={lat}&lon={lon}"
		headers = {"User-Agent": "JohokuApp/1.0 (admin@johoku.com)"}
		response = requests.get(url, headers=headers, timeout=10)

		if response.status_code == 200:
			data = response.json()
			address = data.get("address", {})
			return {
				"display_name": data.get("display_name", ""),
				"state_district": address.get("state_district", ""),
				"state": address.get("state", ""),
				"postcode": address.get("postcode", "")
			}
		else:
			frappe.throw(f"Error fetching geolocation data: HTTP {response.status_code}")

	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Fetch Geolocation Error")
		frappe.throw(f"Unable to fetch location details: {str(e)}")


@frappe.whitelist()
def mark_checkin_in(employee, in_time):
	try:
		if not frappe.db.exists('Employee', {'name': employee, 'status': 'Active'}):
			frappe.throw(f"Employee {employee} does not exist or is not active.")

		if frappe.db.exists('Employee Checkin', {'employee': employee, 'time': in_time}):
			return "Check-in already exists."

		ec = frappe.new_doc('Employee Checkin')
		ec.employee = employee.upper()
		ec.time = in_time
		ec.device_id = "Johoku IN"
		ec.log_type = 'IN'
		ec.marked_for_mobile = 1
		ec.save(ignore_permissions=True)
		frappe.db.commit()

		return "Check-in marked successfully."

	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Mark Check-in Error")
		frappe.throw(f"An error occurred while marking check-in: {str(e)}")


@frappe.whitelist()
def mark_checkin_out(employee, out_time):
	try:
		if not frappe.db.exists('Employee', {'name': employee, 'status': 'Active'}):
			frappe.throw(f"Employee {employee} does not exist or is not active.")

		if frappe.db.exists('Employee Checkin', {'employee': employee, 'time': out_time}):
			return "Check-out already exists."

		ec = frappe.new_doc('Employee Checkin')
		ec.employee = employee.upper()
		ec.time = out_time
		ec.device_id = "Johoku OUT"
		ec.log_type = 'OUT'
		ec.marked_for_mobile = 1
		ec.save(ignore_permissions=True)
		frappe.db.commit()

		return "Check-out marked successfully."

	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Mark Check-out Error")
		frappe.throw(f"An error occurred while marking check-out: {str(e)}")
