# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import date, time, datetime


class Respartner(models.Model):
	_inherit = 'res.partner'

	custom_credit = fields.Float('Credit')
	allow_credit = fields.Boolean(string='Allow Credit')
	allow_over_limit = fields.Boolean(string='Allow Over limit')
	limit_credit = fields.Float("Credit Limit")

	def update_pos_credit(self):
		jr_entries = self.env['account.move'].sudo().search(
			[('move_type', '=', 'entry'), ('partner_id', '=', self.id), ('journal_id.is_credit', '=', True)])
		jr_entry_amount = []
		for k in jr_entries:
			jr_entry_amount.append(k.amount_total)
		##--Invoice entry or Backend sale--I can also take data from invoice_line ids one2many in respartner,may u ask why i didnt get the
		# daata from accnt move , becoz pos_order_ids is not creating at the time in sytem and it cause issues with cash payment in pos##
		# The below code is future reference
		# inv_entries = self.env['account.move'].search(
		#     [('type', '=', 'out_invoice'), ('partner_id', '=', self.partner_id), ('pos_order_ids', '=', False)])

		inv_entries = self.env['sale.order'].sudo().search([('partner_id', '=', self.id)])
		inv_entries_amount = []
		for inv in inv_entries:
			inv_entries_amount.append(inv.amount_total)
			print("***------------------------", inv.id)
		##--POS sale--##
		if self.pos_order_ids:
			amount = []
			for i in self.pos_order_ids:
				for j in i.payment_ids:
					if j.payment_method_id.is_credit == True:
						amount.append(j.amount)
			self.update({'custom_credit': sum(amount) - sum(jr_entry_amount)})
			print("9999999999999999999999----------------------",sum(jr_entry_amount), sum(amount))



	def action_view_credit_detail(self):
		self.ensure_one()
		self.custom_credit
		print("77")

	def update_partner_credit(self, amount):
		print("888888888888889999999999-----------------", amount)
		self.update({'custom_credit': self.custom_credit + amount})
		# for i in self:
		# 	i.update({'custom_credit': i.custom_credit + amount})


	def pay_partial_payment(self,pos_confg,pos_session_id,partner_id,entered_code,value,partial_journal,pyment_type):
		print("88888888888888-----------------",pos_confg,pos_session_id,partner_id,entered_code,value,partial_journal,pyment_type)
		amount = entered_code
		session = self.env['pos.session'].search([('name','=',pos_session_id)])
		cr_journal_obj = self.env['account.journal'].search([('id', '=', partial_journal)])
		lines = []
		if cr_journal_obj.default_account_id.currency_id.id and session.company_id.currency_id.id:
			if session.company_id.currency_id.id != cr_journal_obj.default_account_id.currency_id.id:
				company_rate = session.company_id.currency_id.rate
				different_rate = cr_journal_obj.default_credit_account_id.currency_id.rate
				amount_diff = company_rate / different_rate
				diff_amount = amount * amount_diff
		if self.property_account_receivable_id:
			partner_line = {'account_id': self.property_account_receivable_id.id,
							'name': '/',
							'date': date.today(),
							'partner_id': partner_id['id'],
							'debit': 0.0,
							'credit': float(amount),
							}
			lines.append(partner_line)
			pos_line = {
				'account_id': cr_journal_obj.default_account_id.id,
				'name': 'POS Credit Payment',
				'date': date.today(),
				'partner_id': partner_id['id'],
				'credit': 0.0,
				'debit': float(amount),
			}
			lines.append(pos_line)
		line_list = [(0, 0, x) for x in lines]
		move_id = self.env['account.move'].create({
			'ref': pos_confg + '-' + session.name,
			'payment_type': pyment_type,
			'partner_id': partner_id['id'],
			'date': date.today(),
			'journal_id': partial_journal,
			'move_type': 'entry',
			'line_ids': line_list
		})
		move_id.action_post()
		# if cr_journal_obj.default_account_id.currency_id.id and session.company_id.currency_id.id:
		# 	if session.company_id.currency_id.id != cr_journal_obj.default_account_id.currency_id.id:
		# 		amount = diff_amount
		return amount

class account_journal(models.Model):
	_inherit = 'account.journal'

	is_credit = fields.Boolean(string='POS Credit Payment Method')


class account_journal(models.Model):
	_inherit = 'pos.payment.method'

	is_credit = fields.Boolean(string='POS Credit Payment Method')


class PosConfig(models.Model):
	_inherit = 'pos.config'

	partial_journal_id = fields.Many2one('account.journal', 'Partial Payment Journal', required=True)
	invoice_auto_check = fields.Boolean(
		help='Check to enable the invoice button')

class AccountMove(models.Model):
	_inherit = 'account.move'

	payment_type = fields.Char(string='Payment type')

	@api.model
	def create(self, vals):
		result = super(AccountMove, self).create(vals)
		if result.move_type in ('out_invoice', 'out_refund', 'entry'):
			result.partner_id.update_pos_credit()
		return result

class PosOrder(models.Model):
	_inherit = 'pos.order'

	# def _generate_pos_order_invoice(self):
	# 	moves = self.env['account.move']
	#
	# 	for order in self:
	# 		# Force company for all SUPERUSER_ID action
	# 		if order.account_move:
	# 			moves += order.account_move
	# 			continue
	#
	# 		if not order.partner_id:
	# 			raise UserError(_('Please provide a partner for the sale.'))
	#
	# 		move_vals = order._prepare_invoice_vals()
	# 		new_move = order._create_invoice(move_vals)
	#
	# 		order.write({'account_move': new_move.id, 'state': 'invoiced'})
	# 		new_move.sudo().with_company(order.company_id)._post()
	# 		moves += new_move
	# 		print("55555555555555--------------------",order)
	# 		order._apply_invoice_payments()