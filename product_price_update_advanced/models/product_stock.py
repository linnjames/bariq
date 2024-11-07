from odoo import api, fields, models, _


class ProductStock(models.TransientModel):
    _name = 'product.stock'
    _description = 'Product Stock'

    product_id = fields.Many2one('product.product',
                                 string="All Products",
                                 required=True,
                                 help="select the product for changing "
                                      "the sales and cost price")
    quantity = fields.Integer(string="Quantity Available", required=True)

    stock_location_ids = fields.Many2many("stock.quant")

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.quantity = self.product_id.qty_available
            product = self.product_id.id
            print(product)

            stock_details = self.env['stock.quant'].search([('product_id', '=', product),('location_id.usage','=','internal')])
            print(stock_details)

            product_details = stock_details.ids
            print(product_details)
            self.stock_location_ids = [(6, 0, product_details)]
        else:
            self.stock_location_ids = [(5,)]  # Clear the field


    def action_change_product_stock(self):
        stock_quants = self.env['stock.quant'].browse(self.stock_location_ids.ids)
        print(stock_quants)
        stock_quants.action_apply_inventory()
