# -*- coding: utf-8 -*-


from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ProductLabelLayoutCustom(models.TransientModel):
    _name = 'product.label.layout.custom'

    print_format = fields.Selection([
        # ('label75x50', 'Label 75x50'),
        ('label38x28', 'Label 38x28'),
        # ('label60x40', 'Label 60x40'),
        ('label80x50', 'Label 80x50')
        ], string="Format", default='label38x28')
    custom_quantity = fields.Integer('Quantity', default=1)
    height = fields.Integer(string="height")
    width = fields.Integer(string="Width")
    custom_page_size = fields.Boolean("Custom Page size")

    @api.onchange('custom_quantity')
    def report_qty(self):
        act_ids = self._context.get('active_ids')
        records = self.env["product.template"].search([('id', 'in', act_ids)])
        records.write({'report_qty': self.custom_quantity})

    def process(self):
        if self.print_format == 'label75x50':
            paperformat = self.env['report.paperformat'].search([('name', '=', 'Dymo Label Sheet 75 x 50')])
            paperformat.update({
                'page_height': self.height or 75,
                'page_width': self.width or 50,
            })
        if self.print_format == 'label38x28':
            paperformat = self.env['report.paperformat'].search([('name', '=', 'Dymo Label Sheet 38 x 28')])
            paperformat.update({
                'page_height': self.height or 38,
                'page_width': self.width or 28,
            })
        if self.print_format == 'label60x40':
            paperformat = self.env['report.paperformat'].search([('name', '=', 'Dymo Label 60 x 40')])
            paperformat.update({
                'page_height': self.height or 60,
                'page_width': self.width or 40,
            })
        if self.print_format == 'label80x50':
            paperformat = self.env['report.paperformat'].search([('name', '=', 'Dymo Label Sheet 80 x 50')])
            paperformat.update({
                'page_height': self.height or 80,
                'page_width': self.width or 50,
            })
        if self.print_format == 'label75x50':
            return self.env['product.template'].print_label75x50()
        if self.print_format == 'label38x28':
            return self.env['product.template'].print_label38x28()
        if self.print_format == 'label60x40':
            return self.env['product.template'].print_labellabel60x40()
        if self.print_format == 'label80x50':
            return self.env['product.template'].print_labellabel80x50()

