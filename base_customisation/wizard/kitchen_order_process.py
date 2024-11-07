

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class KitchenOrderProcess(models.TransientModel):
    _name = "kitchen.order.process"
    _description = "Kitchen Order Process"

    kitchen_order_process_line_ids = fields.One2many(
        'kitchen.order.process.line',
        'kitchen_order_process_id', string="Process Line")

    @api.model
    def default_get(self, fields):
        res = super(KitchenOrderProcess, self).default_get(fields)
        order_lines = self.env['sale.order.line'].search([
            ('id', 'in', self.env[
                'sale.order'
                ].browse(
                    self.env.context.get(
                        'active_ids'
                    )
                ).mapped('order_line').ids)
        ])
        product_val = {}
        for line in order_lines:
            if line.product_id in product_val:
                product_val[line.product_id] += line.product_uom_qty
            else:
                product_val[line.product_id] = line.product_uom_qty
        res['kitchen_order_process_line_ids'] = [(0, 0, {
                'product_id': product_key and product_key.id,
                'product_category_id': product_key.categ_id and product_key.categ_id.id,
                'total_qty': product_val}
                ) for product_key,product_val in product_val.items()]
        return res

    # @api.model
    # def view_init(self, fields):
    #     """ Check some preconditions before the wizard executes. """
    #     sale_orders = self.env['sale.order'].browse(self.env.context.get(
    #                     'active_ids')).mapped('user_id').ids
    #     if len(sale_orders) > 1:
    #         raise UserError(_(
    #             "You can not process Kitchen Order with multiple Salesperson"))
    #     return False

    def process_kitchen_order(self):
        def filtered_order_line(line_group):
            order_line = self.env['sale.order.line'].search([
                ('id', 'in', line_group['__domain'][2][2]),
                ('product_id', '=', line_group['product_id'][0])
                ])
            return [(6, 0, order_line.ids)]
        order_id = self._context.get('order_id')
        sale_orders = self.env['sale.order'].browse(self.env.context.get(
                        'active_ids') or order_id)
        line_groups = self.env['sale.order.line'].read_group(
            [('id', 'in', sale_orders.mapped('order_line').ids)],
            ['id', 'product_id', 'product_uom_qty'], groupby='product_id',
            lazy=False)
        kitchen_vals = [{
                'product_id': line_group['product_id'][0],
                'kitchen_qty': line_group['product_uom_qty'],
                'date_order': sale_orders[0].date_order,
                'user_id': sale_orders[0].user_id.id,
                'branch_id': sale_orders[0].user_id.branch_id.id,
                'company_id': sale_orders[0].user_id.company_id.id,
                'sale_order_line_ids': filtered_order_line(line_group)
            } for line_group in line_groups]
        kitchen_orders = self.env['kitchen.order'].create(kitchen_vals)
        for kitchen_order in kitchen_orders:
            kitchen_order.action_process_order()
            kitchen_orders.is_incomming_stock = True


class KitchenOrderProcessLine(models.TransientModel):
    _name = 'kitchen.order.process.line'
    _description = 'Kitchen Order Process Line'

    kitchen_order_process_id = fields.Many2one(
        'kitchen.order.process', string="Process Order",
        ondelete='cascade', index=True, copy=False)
    product_category_id = fields.Many2one(
        'product.category', string="Category")
    kitchen_chef_id = fields.Many2one('kitchen.chef', string="kitchen Chef")
    product_id = fields.Many2one('product.product', string="Product")
    total_qty = fields.Float(string="Qty")
