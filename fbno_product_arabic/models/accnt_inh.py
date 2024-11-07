
from odoo import api, models, fields, _
from odoo.tools import float_compare, float_round


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    product_arabic_name = fields.Char(string='Arabic name', related="product_id.product_arabic")


