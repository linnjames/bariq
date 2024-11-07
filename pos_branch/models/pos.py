# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.http import Controller, route, request, Response

class res_users(models.Model):
	_inherit = 'res.users'

	branch_id = fields.Many2one('res.branch', 'Current Branch')
	branch_ids = fields.Many2many('res.branch', id1='user_id', id2='branch_id',string='Allowed Branches')

	is_branch_user = fields.Boolean("Is branch user",compute="_compute_branch_user")

	def _compute_branch_user(self):
		for user in self:
			
			b_usr = user.has_group('pos_branch.group_branch_user')
			b_mngr = user.has_group('pos_branch.group_branch_user_manager')
			non_user_group = self.env.ref('pos_branch.group_no_branch_user')
			if not b_usr and not b_mngr :
				non_user_group.write({
					'users': [(4, user.id)]
				})
			else:
				non_user_group.write({
					'users': [(3, user.id)]
				})
			user.is_branch_user = False


class res_branch(models.Model):
	_name = 'res.branch'
	_description = "Res Branch"
	_rec_name = 'name'

	name = fields.Char('Name', required=True)
	arabic_name = fields.Char(string='Arabic Name')
	address = fields.Text('Address', size=252)
	telephone_no = fields.Char("Telephone No")
	company_id =  fields.Many2one('res.company', 'Company', required=True)
