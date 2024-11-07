from odoo import api, models, fields, _, exceptions




class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_id = fields.Many2one(
        'product.product', string='Product',
        domain="['|', ('detailed_type', '!=', consu),('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        change_default=True, ondelete='restrict', check_company=True)  # Unrequired company