from odoo import models, fields, api


class CompanyToArabic(models.Model):
    _inherit = 'res.company'

    company_arabic = fields.Char(string="Arabic Name")
    street_arabic = fields.Char()
    street2_arabic = fields.Char()
    city_arabic = fields.Char()
    mobile_arabic = fields.Char()
    vat_arabic = fields.Char()
    cr_arabic = fields.Char()
