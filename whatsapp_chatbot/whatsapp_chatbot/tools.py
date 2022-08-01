import frappe 
import json
import requests as req
from frappe import _
from frappe.integrations.utils import make_post_request, make_get_request
from frappe.utils.pdf import get_pdf
from frappe.utils.user import get_users_with_role

from frappe.model.workflow import  get_workflow_name
from frappe.workflow.doctype.workflow_action.workflow_action import get_next_possible_transitions,get_doc_workflow_state,filter_allowed_users,get_confirm_workflow_action_url#,get_users_next_action_data

@frappe.whitelist()
def download_pdf(doctype, name, format=None, doc=None, no_letterhead=0):
	html = frappe.get_print(doctype, name, format, doc=doc, no_letterhead=no_letterhead)
	return get_pdf(html)

# def get_users_next_action_data(transitions, doc):
# 	user_data_map = []
# 	for transition in transitions:
# 		users = get_users_with_role(transition.allowed)
# 		filtered_users = filter_allowed_users(users, doc, transition)
# 		for fu in filtered_users:
# 			user = frappe._dict({'possible_actions': [],'email': frappe.db.get_value('User', fu, 'email')})
# 			user_data_map.append(user)

# 			# user_data_map.get('possible_actions').append(frappe._dict({
# 			# 	'action_name': transition.action,
# 			# 	'action_link': get_confirm_workflow_action_url(doc,transition.action,  user)
# 			# }))
# 	return user_data_map

def get_users_next_action_data(transitions, doc):
	user_data_map = {}
	for transition in transitions:
		users = get_users_with_role(transition.allowed)
		filtered_users = filter_allowed_users(users, doc, transition)
		for user in filtered_users:
			if not user_data_map.get(user):
				user_data_map[user] = frappe._dict({
					'possible_actions': [],
					'email': frappe.db.get_value('User', user, 'email'),
				})

			user_data_map[user].get('possible_actions').append(frappe._dict({
				'action_name': transition.action,
				'action_link': get_confirm_workflow_action_url(doc,transition.action,  user)
			}))
	return user_data_map


def send_whatsapp(doc, state):
	
	workflow = get_workflow_name(doc.get('doctype'))
	if not workflow: return
	print("doc = {}".format(frappe.as_json(doc)))
	print("doc.get('doctype') ={} name = {}".format(doc.get('doctype'),doc.get('name')))
	next_possible_transitions = get_next_possible_transitions(workflow, get_doc_workflow_state(doc), doc)
	if not next_possible_transitions: return
	user_data_map = get_users_next_action_data(next_possible_transitions, doc)
	if not user_data_map: return
	print("\nuser_data_map = {}\n".format(user_data_map))
	user_list = []
	for user in user_data_map:	
		user_doc = frappe.get_doc("User",user)
		user_data_map[user]["first_name"] = user_doc.first_name
		user_data_map[user]["mobile_no"] = user_doc.mobile_no
		user_data_map[user]["doctype"] = doc.get('doctype')
		user_data_map[user]["docname"] = doc.get('name')
		user_list.append(user_data_map)
	# print("user_data_map = {}".format(frappe.as_json(user_data_map)))
	url_host = frappe.db.get_single_value('Chatbot Settings','host_url')
	headers = {"Content-Type": "application/json; charset=UTF-8" }
	data = json.dumps(user_list)
	req.post(url_host + "/send-workflow", data, headers=headers)

	


	

	





