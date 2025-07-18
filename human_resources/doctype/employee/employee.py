def on_submit(self):
		if self.status == "Active":
			allocate_leaves_on_onboarding(self)

	def on_update(self):
		self.set_status()


	def set_status(self):
		if self.status == "Inactive":
			return

		if self.relieving_date:
			if self.relieving_date <= nowdate():
				self.db_set("status", "Inactive")
				self.db_set("user_id", None)

		if self.date_of_joining:
			if self.date_of_joining > nowdate():
				self.db_set("status", "Yet To Join")
				self.db_set("user_id", None)


@frappe.whitelist()
def get_employee_name(name):
	return frappe.db.get_value("Employee", name, "employee_name")


def validate_nssf_no(nssf_no, employee):
	# Check if NSSF No. is unique for active employees
	if nssf_no:
		exists = frappe.db.exists(
			"Employee", {"nssf_no": nssf_no, "docstatus": 0, "name": ["!=", employee]})
		if exists:
			frappe.throw(_("NSSF No. {0} already exists for another employee {1}").format(nssf_no, exists), title=_("Duplicate NSSF No"))


def validate_nhif_no(nhif_no, employee):
	# Check if NHIF No. is unique for active employees
	if nhif_no:
		exists = frappe.db.exists(
			"Employee", {"nhif_no": nhif_no, "docstatus": 0, "name": ["!=", employee]})
		if exists:
			frappe.throw(_("NHIF No. {0} already exists for another employee {1}").format(nhif_no, exists), title=_("Duplicate NHIF No"))



def validate_pin(pin, employee):
	# Check if PIN is unique for active employees
	if pin:
		exists = frappe.db.exists(
			"Employee", {"pin": pin, "docstatus": 0, "name": ["!=", employee]})
		if exists:
			frappe.throw(_("PIN {0} already exists for another employee {1}").format(pin, exists), title=_("Duplicate PIN"))