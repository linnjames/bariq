
from odoo import  fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    arabic_name = fields.Char(string="Arabic name")
    street_arabic = fields.Char()
    street2_arabic = fields.Char()
    city_arabic = fields.Char()
    mobile_arabic = fields.Char()
    vat_arabic = fields.Char()
