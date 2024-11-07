
from odoo import models, api, fields, _
from num2words import num2words

from odoo.exceptions import UserError


def currency_to_text(sum, currency, language):
    pass


class AccountMove(models.Model):
    _inherit = 'account.move'

    partner_id = fields.Many2one('res.partner', readonly=True, tracking=True,
                                 states={'draft': [('readonly', False)]},
                                 check_company=True,
                                 string='Partner', change_default=True, domain="[('company_id', '=', company_id)]")

    def action_clear(self):
        for rec in self:
            rec.write({'invoice_line_ids': [(5, 0, 0)],
                       })

    def get_vat_amt(self, tax_ids, subtotal_amt):
        vat_amt = 0
        tax = tax_ids[0]
        if tax.amount_type == 'percent':
            vat_amt = (subtotal_amt * tax.amount) / 100
        elif tax.amount_type == 'fixed':
            vat_amt = tax.amount
        return vat_amt

    @api.model
    def numtoword_s(self, amount_total):
        return (num2words(amount_total, lang='en_IN')).title() + " Halala only"

    def _post(self, soft=True):
        res = super()._post(soft)
        for record in self:
            if record.country_code == 'SA' and record.move_type in ('out_invoice', 'out_refund'):
                if not record.l10n_sa_show_delivery_date:
                    raise UserError(_('Delivery Date cannot be empty'))

                self.write({
                    'l10n_sa_confirmation_datetime': fields.Datetime.now()
                })
                if record.l10n_sa_show_delivery_date:
                    self.write({
                        'l10n_sa_confirmation_datetime': self.l10n_sa_delivery_date
                    })
        return res


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    # sl_no = fields.Integer(string='Sr#', compute='_compute_serial_number', store=True)
    #
    # @api.depends('sequence', 'move_id', 'product_id')
    # def _compute_serial_number(self):
    #     for invoice_line_ids in self:
    #         if not invoice_line_ids.sl_no:
    #             serial_no = 1
    #             for line in invoice_line_ids.mapped('move_id').invoice_line_ids:
    #                 line.sl_no = serial_no
    #                 serial_no += 1

    def _get_computed_uom(self):
        self.ensure_one()
        if self.product_id:
            return self.product_id.uom_po_id
        return False