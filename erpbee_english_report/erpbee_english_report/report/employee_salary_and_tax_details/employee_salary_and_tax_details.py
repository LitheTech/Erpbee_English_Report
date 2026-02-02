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

def get_columns():
	return [
		_("Name") + ":Data/Employee:120",
		_("Employee Name") + ":Data/Employee:120",
		_("Designation") + ":Data/Employee:120",
		_("E-TIN") + ":Data/Employee:120",
		_("Basic") + ":Data/:120",
		_("Medical") + ":Data/:120",
		_("Hourse rent") + ":Data/:120",
				_("Gross") + ":Data/:120",


	]

def get_data(filters):
	conditions, filters = get_conditions(filters)
	result = frappe.db.sql("""SELECT emp.name, emp.employee_name ,emp.designation,null,
						SUM(CASE WHEN sd.salary_component = 'Basic' THEN sd.amount ELSE 0 END) AS basic,
						SUM(CASE WHEN sd.salary_component = 'Hrent' THEN sd.amount ELSE 0 END) AS house_rent,
						SUM(CASE WHEN sd.salary_component = 'Medical' THEN sd.amount ELSE 0 END) AS medical
						FROM tabEmployee as emp 
						INNER JOIN `tabSalary Slip` as ss 
						ON emp.name = ss.employee
						INNER JOIN `tabSalary Detail` sd
    					ON ss.name = sd.parent
						where %s
						GROUP BY emp.name
						""" 
	% conditions, as_list=1)


	return result

def get_conditions(filters):
	conditions = ""
	
	#changes done here
	if filters.get("employee"): conditions += " emp.name= '%s'" % filters["employee"]
	if filters.get("employee"): conditions += " and  ss.employee= '%s'" % filters["employee"]


	

	#changes done ended here
	# if filters.get("month") and filters.get("year"):

	# 	start_final_date =  filters.get("year")+"-" + str(int(filters.get("month"))).zfill(2) +"-"+  "01"		
	# 	end_final_date = filters.get("year") +"-" + str(int(filters.get("month"))).zfill(2) + "-" + str(total_number_of_days)
	
	# 	conditions += "and `tabSalary Slip`.start_date >= '%s' and `tabSalary Slip`.end_date <=  '%s'" % (start_final_date, end_final_date)
	return conditions,filters
