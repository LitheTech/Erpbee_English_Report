import frappe
from frappe import _


def execute(filters= None):
	if not filters:
		filters = {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data
	


def get_columns():
	return [
		_("Employee") + ":Data/:120",
		_("Name") + ":Data/:120",
		_("Designation") + ":Data/:120",
		_("Issue Date") + ":Date/:120",
		_("Department") + ":Data/:120",
		_("Loan Principle") + ":Data/:120",
		_("Loan Interest") + ":Data/:120",
		_("Total Loan Amount") + ":Data/:120",
		_("Monthly Amount") + ":Data/:120",
		_("Total Adjustment") + ":Data:120",
		_("Remain Balance") + ":Data:120",
		_("Total Installment") + ":Data:120",
		_("Installment Paid") + ":Data:120",
		_("Last Payment Date") + ":Date:120",		
	]

def get_data(filters):
	conditions, filters = get_conditions(filters)

	result = frappe.db.sql("""
        SELECT 
            ln.applicant, 
            ln.applicant_name, 
            emp.designation, 
            ln.posting_date, 
            emp.department, 
            ln.loan_principle_amount, 
            ln.loan_interest_amount, 
            ln.loan_amount,
            ln.monthly_repayment_amount, 
            (ln.total_amount_paid + ln.loan_opening_amount) AS total_adjustment,
            (ln.loan_amount - (ln.total_amount_paid + ln.loan_opening_amount)) AS remain_balance,
			repayment_periods,
			round(((ln.total_amount_paid + ln.loan_opening_amount)/ln.monthly_repayment_amount),0),
            MAX(rp.payment_date) AS last_repayment_date
        FROM 
            tabLoan ln 
        LEFT JOIN 
            tabEmployee emp ON emp.name = ln.applicant
        right JOIN 
            `tabRepayment Schedule` rp ON rp.parent = ln.name 
		where %s and ln.status='Disbursed'
		
		 GROUP BY 
             ln.applicant, ln.applicant_name, emp.designation, ln.posting_date, emp.department, 
             ln.loan_principle_amount, ln.loan_interest_amount, ln.loan_amount, 
             ln.monthly_repayment_amount, ln.total_amount_paid, ln.loan_opening_amount
        """% conditions, as_list=1)

	return result


    

def get_conditions(filters):
	conditions="" 
	if filters.get("company"): conditions += "ln.company= '%s'" % filters["company"]

	if filters.get("employee"): conditions += " and ln.applicant in %s'" % filters["employee"]

	if filters.get("department"): conditions += " and emp.department= '%s'" % filters["department"]
	if filters.get("designation"): conditions += " and emp.designation='%s'" % filters["designation"]


	
	return conditions, filters

