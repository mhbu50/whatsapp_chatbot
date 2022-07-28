# Copyright (c) 2022, Accurate Systems and contributors
# For license information, please see license.txt

import frappe
from frappe.integrations.utils import make_post_request, make_get_request
from frappe.model.document import Document


class ChatbotSettings(Document):
    @frappe.whitelist()
    def genrate(self):
        # res = make_post_request(url="http://localhost:21465/api/" +
        #                         self.session+"/"+self.secret_key+"/generate-token")
        # self.token = res["token"]
        headers = {"Content-Type": "application/json",
                   "Accept": "application/json"}

        res = make_get_request(url=self.host_url+"/qr")
        self.token = res
        self.save()

    @frappe.whitelist()
    def disconnect(self):
        make_get_request(url=self.host_url+"/disconnect")


