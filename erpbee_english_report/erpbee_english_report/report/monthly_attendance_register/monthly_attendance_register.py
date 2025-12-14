from calendar import monthrange
import frappe
from frappe import _, msgprint
from frappe.utils import cint, cstr, getdate

status_map = {
    "Absent": "A",
    "Half Day": "HD",
    "Holiday": "H",
    "Weekly Off": "WO",
    "On Leave": "OL",
    "Present": "P",
    "Work From Home": "WFH",
}

day_abbr = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def execute(filters=None):
    if not filters:
        filters = {}

    conditions, filters = get_conditions(filters)
    columns, days = get_columns(filters)

    frappe.flags.report_columns = columns

    att_map = get_attendance_list(conditions, filters)
    if not att_map:
        return columns, []

    employees = get_employees(filters.company, filters.get("employee"))

    data = []

    # Get leave types for summarized view
    leave_types = []
    if filters.summarized_view:
        leave_types = frappe.get_all("Leave Type", pluck="name")
        columns.extend([{"label": lt, "fieldtype": "Float", "width": 120, "precision": 2} for lt in leave_types])

    current_department = None

    for emp in employees:
        if emp.department != current_department:
            current_department = emp.department or _("No Department")
            dept_row = [f"<b>{current_department}</b>"]
            dept_row += [""] * (len(columns) - 1)
            data.append(dept_row)

        record = build_employee_row(emp, att_map, filters, conditions, leave_types)
        if record:
            data.append(record)

    return columns, data


def get_employees(company, employee=None):
    return frappe.db.sql(
        f"""
        SELECT
            name,
            employee_name,
            department
        FROM `tabEmployee`
        WHERE company = %(company)s
        {"AND name = %(employee)s" if employee else ""}
        ORDER BY department, name
        """,
        {"company": company, "employee": employee},
        as_dict=True,
    )


def build_employee_row(emp, att_map, filters, conditions, leave_types=[]):
    if emp.name not in att_map:
        return None

    row = ["", emp.name, emp.employee_name]

    total_p = total_late = total_a = total_l = total_h = total_um = 0.0
    emp_status_map = []

    for day in range(filters["total_days_in_month"]):
        status = att_map[emp.name].get(day + 1)

        abbr = status_map.get(status, "")
        if status == "On Leave" and att_map[emp.name].get(day + 1):
            leave_type = frappe.db.get_value(
                "Attendance",
                {"employee": emp.name, "attendance_date": f"{filters.year}-{filters.month}-{day + 1}"},
                "leave_type",
            )
            abbr = leave_type if leave_type else "OL"

        emp_status_map.append(abbr)

        if filters.summarized_view:
            if status in ("Present", "Work From Home"):
                total_p += 1
            elif status == "Absent":
                total_a += 1
            elif status == "On Leave":
                total_l += 1
            elif status == "Half Day":
                total_p += 0.5
                total_l += 0.5
            elif status in ("Holiday", "Weekly Off"):
                total_h += 1
            elif not status:
                total_um += 1

    if not filters.summarized_view:
        row.extend(emp_status_map)
    else:
        row.extend([total_p, total_late, total_l, total_a, total_h, total_um])

        # Add leave type counts
        if leave_types:
            filters.update({"employee": emp.name})
            leave_details = frappe.db.sql(
                f"""SELECT leave_type, COUNT(*) AS count
                    FROM `tabAttendance`
                    WHERE employee=%(employee)s
                    AND leave_type IS NOT NULL
                    AND MONTH(attendance_date)=%(month)s
                    AND YEAR(attendance_date)=%(year)s
                    GROUP BY leave_type""",
                filters,
                as_dict=True,
            )

            leaves_map = {d.leave_type: d.count for d in leave_details}
            for lt in leave_types:
                row.append(leaves_map.get(lt, 0.0))

    if len(row) < len(frappe.flags.report_columns):
        row += [""] * (len(frappe.flags.report_columns) - len(row))

    return row


def get_columns(filters):
    columns = [
        _("Department") + ":Data:150",
        _("Employee") + ":Link/Employee:120",
        _("Employee Name") + ":Data:150",
    ]

    days = []
    for day in range(filters["total_days_in_month"]):
        date = f"{filters.year}-{filters.month}-{day + 1}"
        day_name = day_abbr[getdate(date).weekday()]
        days.append(cstr(day + 1) + " " + day_name + "::65")

    if not filters.summarized_view:
        columns.extend(days)
    else:
        columns.extend([
            _("Total Present") + ":Float:120",
            _("Total Late") + ":Float:120",
            _("Total Leaves") + ":Float:120",
            _("Total Absent") + ":Float:120",
            _("Total Holidays") + ":Float:120",
            _("Unmarked Days") + ":Float:120",
        ])

    return columns, days


def get_attendance_list(conditions, filters):
    attendance_list = frappe.db.sql(
        f"""
        SELECT employee, DAY(attendance_date) AS day, status
        FROM `tabAttendance`
        WHERE docstatus = 1 {conditions}
        ORDER BY employee, attendance_date
        """,
        filters,
        as_dict=True,
    )

    att_map = {}
    for d in attendance_list:
        att_map.setdefault(d.employee, {})[d.day] = d.status

    return att_map


def get_conditions(filters):
    if not (filters.get("month") and filters.get("year")):
        frappe.throw(_("Please select month and year"))

    filters["total_days_in_month"] = monthrange(
        cint(filters.year), cint(filters.month)
    )[1]

    conditions = " AND MONTH(attendance_date) = %(month)s AND YEAR(attendance_date) = %(year)s"

    if filters.get("company"):
        conditions += " AND company = %(company)s"
    if filters.get("employee"):
        conditions += " AND employee = %(employee)s"

    return conditions, filters


@frappe.whitelist()
def get_attendance_years():
    years = frappe.db.sql_list(
        "SELECT DISTINCT YEAR(attendance_date) FROM tabAttendance ORDER BY YEAR(attendance_date) DESC"
    )
    return "\n".join(str(y) for y in years) or str(getdate().year)
