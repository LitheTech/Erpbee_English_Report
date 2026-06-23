# Copyright (c) 2025, LTL and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	if not filters:
		filters = {}
	
	columns = get_columns()
	data = get_data(filters)
	return columns, data

# -----------------------
# COLUMNS
# -----------------------
def get_columns():
	return [
		_("Name") + ":Data/Employee:120",
		_("Employee Name") + ":Data/Employee:120",
		_("Designation") + ":Data/Employee:120",
		_("E-TIN") + ":Data/Employee:120",

		_("Posting Date") + ":Data:120",
		_("Income Year") + ":Data:120",
		_("Assessment Year") + ":Data:120",

		_("Basic") + ":Currency:120",
		_("Medical") + ":Currency:120",
		_("House Rent") + ":Currency:120",
		_("Conveyance") + ":Currency:120",
		_("Festival Bonus") + ":Currency:120",

		_("Earn Leave") + ":Currency:120",
		_("PF") + ":Currency:120",
		_("Gross") + ":Currency:120",
	]

# -----------------------
# DATA
# -----------------------
def get_data(filters):
	conditions = get_conditions(filters)

	result = frappe.db.sql("""
		SELECT 
			employee,
			employee_name,
			designation,
			tin_no,
						
			posting_date,
			income_year,
			assessment_year,

			total_basic,
			total_medical,
			total_hrent,
			total_conveyance,
			festival_bonus,
			earn_leave_allowance,
			total_pf,
			gross_income

		FROM `tabEmployee Income Summary`

		
		WHERE %s
	""" % conditions, as_list=1)

	return result

# -----------------------
# CONDITIONS
# -----------------------
def get_conditions(filters):
	conditions = "1=1 "
	
	#changes done here
	if filters.get("employee"): conditions += "and employee= '%s'" % filters["employee"]
	if filters.get("income_year"): conditions += " and  income_year= '%s'" % filters["income_year"]


	

	#changes done ended here
	# if filters.get("month") and filters.get("year"):

	# 	start_final_date =  filters.get("year")+"-" + str(int(filters.get("month"))).zfill(2) +"-"+  "01"		
	# 	end_final_date = filters.get("year") +"-" + str(int(filters.get("month"))).zfill(2) + "-" + str(total_number_of_days)
	
	# 	conditions += "and `tabSalary Slip`.start_date >= '%s' and `tabSalary Slip`.end_date <=  '%s'" % (start_final_date, end_final_date)
	return conditions
