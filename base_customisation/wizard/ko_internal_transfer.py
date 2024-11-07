

from odoo import api, models, _
from odoo.exceptions import UserError


class KOInternalTransfer(models.TransientModel):
    _name = "ko.internal.transfer"
    _description = "Kitchen Order Internal Transfer"

    @api.model
    def view_init(self, fields):
        """ Check some preconditions before the wizard executes. """
        kitchen_orders = self.env['kitchen.order'].browse(self.env.context.get(
                        'active_ids'))
        # if len(kitchen_orders.mapped('user_id').ids) > 1:
        #     raise UserError(_(
        #         "You can not process Internal Transfer with multiple \
        #         Salesperson"))
        if any(kitchen_order.state != 'done' for kitchen_order in kitchen_orders):
            raise UserError(_(
                "You can not process Internal Transfer on Draft State"))
        return False

    def process_ko_internal_transfer(self):
        internal_transfer = self.env['stock.picking']
        kitchen_orders = self.env['kitchen.order'].browse(self.env.context.get(
                        'active_ids'))
        picking_type_id = self.env['stock.picking.type'].search([(
                'code', '=', 'outgoing'),
                ('company_id', '=', kitchen_orders[0] and kitchen_orders[0].user_id.company_id.id)
            ], limit=1)
        location_id = self.env['stock.location'].search([(
                'usage', '=', 'internal'),
                ('company_id', '=', kitchen_orders[0] and kitchen_orders[0].user_id.company_id.id)
            ], limit=1)
        location_dest_id = self.env['stock.location'].search([(
                'usage', '=', 'customer'),
                ('company_id', '=', kitchen_orders[0] and kitchen_orders[0].user_id.company_id.id)
            ], limit=1)
        it_vals = {
            'partner_id': kitchen_orders[0] and kitchen_orders[0].user_id\
            and kitchen_orders[0].user_id.partner_id.id,
            'picking_type_id': picking_type_id and picking_type_id.id,
            'location_id': location_id and location_id.id,
            'location_dest_id': location_dest_id and location_dest_id.id,
            'kitchen_order_id': kitchen_orders[0].id,
            'branch_id': kitchen_orders[0].user_id.branch_id.id,
            'company_id': kitchen_orders[0].user_id.company_id.id,
            'move_lines': [(0, 0, {
                'name': kitchen_order.product_id.name,
                'product_id': kitchen_order.product_id.id,
                'product_uom': kitchen_order.product_id.uom_id.id,
                'location_id': location_id and location_id.id,
                'location_dest_id': location_dest_id and location_dest_id.id,
                'product_uom_qty': kitchen_order.kitchen_qty,
                'quantity_done': kitchen_order.kitchen_qty
            }) for kitchen_order in kitchen_orders]
        }
        SP = internal_transfer.create(it_vals)
        SP.action_confirm()
        SP.action_assign()
        SP.action_set_quantities_to_reservation()
        SP.button_validate()
        for ko_sol in kitchen_orders.sale_order_line_ids:
            ko_sol.order_id.write({'state': 'done',
                'invoice_status': 'to invoice'})
            ko_sol.write({
                'qty_delivered': ko_sol.product_uom_qty,
                'is_ko_transfer': True})
        if kitchen_orders:
            kitchen_orders.write({
                'is_outgoing_stock': True,
                'is_incomming_stock': False
            })
