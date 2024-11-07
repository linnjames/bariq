# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools import format_amount


class ProductBom(models.Model):
    _inherit = 'product.template'

    expiry_date = fields.Date(string='Manufacture date')
    mf_date = fields.Date(string='Expiry date')
    product_weight = fields.Float(string='Weight')
    product_weight_unit = fields.Many2one("uom.uom", string='Weight Unit')
    report_qty = fields.Integer(string='QTY')
    price_with_tax = fields.Float(string='MRP')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id)

    # @api.depends('price_with_tax','taxes_id', 'list_price',)
    # def profit_percentage_calc(self):
    #     for record in self:
    #         currency = record.currency_id
    #         res = record.taxes_id.compute_all(self.price_with_tax)
    #         joined = []
    #         included = res['total_included']
    #         self.price_with_tax = included + self.price_with_tax

    # @api.depends('taxes_id', 'list_price', 'price_with_tax')
    # def _compute_tax_string(self):
    #     for record in self:
    #         currency = record.currency_id
    #         res = record.taxes_id.compute_all(record.list_price)
    #         joined = []
    #         included = res['total_included']
    #         self.price_with_tax = included + self.price_with_tax
    #         if currency.compare_amounts(included, record.list_price):
    #             joined.append(_('%s Incl. Taxes', format_amount(self.env, included, currency)))
    #         excluded = res['total_excluded']
    #         if currency.compare_amounts(excluded, record.list_price):
    #             joined.append(_('%s Excl. Taxes', format_amount(self.env, excluded, currency)))
    #         if joined:
    #             record.tax_string = f"(= {', '.join(joined)})"
    #         else:
    #             record.tax_string = " "

    def report_quantity(self):
        qty_value = []
        qty_value.append({'qty': self.report_qty})
        return qty_value

    # def product_bom_name(self):
    #     bom_dat = self.env['mrp.bom'].search(
    #         [('product_tmpl_id.name', '=', self.name)])
    #     for rec in bom_dat:
    #         bom_data = []
    #         for i in rec.bom_line_ids:
    #             bom_data.append({'products': i.product_arabic_name})
    #         return bom_data

    def action_product_label(self):
        return {
            'name': _("Choose Labels Layout"),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'product.label.layout.custom',
            'view_id': self.env.ref('fbno_product_label.product_label_layout_form_custom').id,
            'target': 'new'
        }

    # def print_label75x50(self):
    #     return self.env.ref('fbno_product_label.report_product_template_label_dymo_custom').report_action(self)

    def print_label38x28(self):
        return self.env.ref('fbno_product_label.report_product_template_label_dymo_custom_38x28').report_action(self)

    def print_labellabel60x40(self):
        return self.env.ref('fbno_product_label.action_report_product_label_common_custom').report_action(self)

    def print_labellabel80x50(self):
        return self.env.ref('fbno_product_label.report_product_template_label_dymo_custom_80x50').report_action(self)



# class MrpBom(models.Model):
#     _inherit = 'mrp.bom.line'
#
#     product_id = fields.Many2one('product.product', 'Component', required=True, check_company=True, domain="[('detailed_type', '=', 'consu')]")
#     product_arabic_name = fields.Char(string='Arabic Name', related="product_id.product_arabic")


class ResPartner(models.Model):
    _inherit = 'res.partner'

    company_id = fields.Many2one('res.company', 'Company', index=True, default=lambda self: self.env.user.company_id)