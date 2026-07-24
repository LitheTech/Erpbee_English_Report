from datetime import datetime, timedelta
import frappe
from frappe.utils import flt
from frappe import _
from frappe.utils import add_days, cstr, date_diff, get_first_day, get_last_day, getdate

def execute(filters = None):
	columns = get_columns()
	data = get_data(filters)

	return columns, data

def get_data(filters):
	from_date = get_first_day(filters["month"] + "-" + filters["year"])
	to_date = get_last_day(filters["month"] + "-" + filters["year"])
	conditions, filters = get_conditions(from_date,to_date,filters)
	result = frappe.db.sql("""SELECT 
						ss.employee,
						ss.employee_name,
						ss.department,
						ss.designation,
						ss.total_loan_repayment
						 FROM `tabSalary Slip`ss where %s and ss.total_loan_repayment>0""" 
	% conditions, as_list=1)

	return result


def get_columns():
	columns = [
		_("Employee") + "::200",
		_("Employee Name") + "::200",
		_("Department") + "::200",
		_("Designation") + "::200",
		_("Amount") + "::200",
		# _("End Date") + "::80",

	]


	return columns



# def get_salary_slip(from_date,to_date,filters,department):
# 	conditions, filters = get_conditions(from_date,to_date,filters,department)
	

# 	filters.update({"from_date": filters.get("from_date"), "to_date": filters.get("to_date")})
# 	conditions, filters = get_conditions(from_date,to_date,filters,department)
	

# 	salary_slips = frappe.db.sql("""select ss.*,e.status,e.relieving_date,e.lunch_rate,e.travel_rate,e.night_rate from `tabSalary Slip` as ss inner join tabEmployee as e on ss.employee=e.name WHERE %s ORDER BY ss.department,employee
# 	""" 
# 	%conditions, filters, as_dict=1)


# 	return salary_slips or []









def get_conditions(from_date,to_date,filters):
	conditions="1=1 " 
	# doc_status = {"Draft": 0, "Submitted": 1, "Cancelled": 2}
	# if filters.get("docstatus"):
	# 	conditions += "ss.docstatus = {0}".format(doc_status[filters.get("docstatus")])

	# if department: conditions += " and ss.department= '%s'" % department

	if from_date: conditions += " and ss.start_date>= '%s'" % from_date
	if to_date: conditions += " and ss.end_date<= '%s'" % to_date
	if filters.get("employee"): conditions += " and ss.employee= '%s'" % filters["employee"]
	if filters.get("company"): conditions += " and ss.company= '%s'" % filters["company"]
	if filters.get("department"): conditions += " and ss.department= '%s'" % filters["department"]
	if filters.get("designation"): conditions += " and ss.designation='%s'" % filters["designation"]
	# if filters.get("shift"): conditions += " and att.shift='%s'" % filters["shift"]
	if filters.get("section"): conditions += " and ss.section='%s'" % filters["section"]
	if filters.get("floor"): conditions += " and ss.floor='%s'" % filters["floor"]
	if filters.get("facility_or_line"): conditions += " and ss.facility_or_line='%s'" % filters["facility_or_line"]
	if filters.get("group_name"): conditions += " and ss.group='%s'" % filters["group_name"]
	if filters.get("grade"): conditions += " and ss.grade='%s'" % filters["grade"]
	if filters.get("mode_of_payment"): conditions += " and ss.mode_of_payment='%s'" % filters["mode_of_payment"]
	if filters.get("bank"): conditions += " and ss.bank_name='%s'" % filters["bank"]
	if filters.get("employee_type"):
		if (filters["employee_type"]=="New Join"):
			conditions += " and ss.date_of_joining between ss.start_date and ss.end_date"
		if (filters["employee_type"]=="Active"):
			conditions += " and e.status='Active' "
		if (filters["employee_type"]=="Left"):
			conditions += " and e.status='Left' and e.relieving_date between ss.start_date and ss.end_date"


	return conditions, filters

