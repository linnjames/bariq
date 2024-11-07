
from odoo import api, fields, models, _


class KitchenOrder(models.Model):
    _name = 'kitchen.order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Kitchen Order"
    _order = 'date_order desc, id desc'

    name = fields.Char(string='Order Reference', required=True,
        copy=False, readonly=True, tracking=1, index=True, default=lambda self: _('New'))
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
        ], string='Status', copy=False, index=True, tracking=3, default='draft')
    date_order = fields.Datetime(string='Order Date', required=True,
        readonly=True, index=True, copy=False, tracking=2,
        help="Creation date of draft orders")
    sale_order_line_ids = fields.Many2many(
        'sale.order.line', string='SO Line', index=True, tracking=4,
        help="Sale Order Line reference")
    kitchen_qty = fields.Integer(string="Qty")
    product_id = fields.Many2one(
        'product.product', string='Product')
    user_id = fields.Many2one(
        'res.users', string='Salesperson',
        index=True, tracking=2)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True)
    branch_id = fields.Many2one('res.branch', readonly=True)
    is_incomming_stock = fields.Boolean(default=False)
    is_outgoing_stock = fields.Boolean(default=False)

    @api.model
    def create(self, vals):
        # Kitchen Orer Sequence
        if vals.get('name', _('New')) == _('New'):
            seq_date = None
            if 'date_order' in vals:
                seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_order']))
            vals['name'] = self.env['ir.sequence'].next_by_code('kitchen.order', sequence_date=seq_date) or _('New')
        return super(KitchenOrder, self).create(vals)

    def action_process_order(self):
        # Completed Kitchen Order
        self.ensure_one()
        internal_transfer = self.env['stock.picking']
        picking_type_id = self.env['stock.picking.type'].search([(
                'code', '=', 'incoming'),
                ('company_id', '=', self.user_id.company_id.id)
            ], limit=1)
        location_id = self.env['stock.location'].search([(
                'usage', '=', 'supplier'),
                ('company_id', '=', self.user_id.company_id.id)
            ], limit=1)
        location_dest_id = self.env['stock.location'].search([(
                'usage', '=', 'internal'),
                ('company_id', '=', self.user_id.company_id.id)
            ], limit=1)
        it_vals = {
            'partner_id': self.user_id.partner_id.id,
            'picking_type_id': picking_type_id and picking_type_id.id,
            'location_id': location_id and location_id.id,
            'location_dest_id': location_dest_id and location_dest_id.id,
            'kitchen_order_id': self.id,
            'branch_id': self.user_id.branch_id.id,
            'company_id': self.user_id.company_id.id,
            'move_lines': [(0, 0, {
                'name': self.product_id.name,
                'product_id': self.product_id.id,
                'product_uom': self.product_id.uom_id.id,
                'location_id': location_id and location_id.id,
                'location_dest_id': location_dest_id and location_dest_id.id,
                'product_uom_qty': self.kitchen_qty,
                'quantity_done': self.kitchen_qty
            })]
        }
        SP = internal_transfer.create(it_vals)
        SP.action_confirm()
        SP.action_assign()
        SP.action_set_quantities_to_reservation()
        SP.button_validate()
        self.state = 'done'

    def action_order_cancel(self):
        # Cancel Kitchen Order
        self.ensure_one()
        self.state = 'cancel'
