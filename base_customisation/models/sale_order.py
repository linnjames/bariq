from datetime import datetime, timedelta

from odoo import api, models, fields, _, exceptions
from odoo.exceptions import ValidationError
from odoo.tools import float_is_zero, float_compare
from itertools import groupby
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_id = fields.Many2one(
        'res.partner', string='Customer', readonly=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        required=True, change_default=True, index=True, tracking=1,
        domain="[('company_id', '=', company_id)]" )
    branch_id = fields.Many2one('res.branch')
    is_ko_invoice = fields.Boolean(compute="_compute_is_ko_invoice", store=True, default=False)
    inv_date = fields.Date('Inv Date')

    @api.onchange('date_order')
    def _depends_order_date_confirm(self):
        if self.date_order != fields.Datetime.now():
            return {
                'warning': {
                    'message': _("Please confirm your sale order date as " + " " + str(self.date_order))
                }
            }

    def fully_invoiced_button(self):
        for rec in self:
            rec.update({'invoice_status': 'invoiced'})

    @api.onchange('date_order')
    def _onchange_order_date_invoice(self):
        date = str(self.date_order + timedelta(hours=3,minutes=00))
        self.inv_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").date()


    @api.onchange('order_line', 'date_order')
    def _onchange_order_date_line(self):
        for i in self.order_line:
            i.write({'order_date': self.date_order})
        kitchen_data = self.env['kitchen.order'].search([('sale_order_line_ids', '=',self.name)])
        if kitchen_data:
            kitchen_data.update({'date_order': self.date_order})



    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice for a sales order. This method may be
        overridden to implement custom invoice generation (making sure to call super() to establish
        a clean extension chain).
        """
        self.ensure_one()
        journal = self.env['account.move'].with_context(default_move_type='out_invoice')._get_default_journal()
        if not journal:
            raise UserError(_('Please define an accounting sales journal for the company %s (%s).', self.company_id.name, self.company_id.id))

        invoice_vals = {
            'ref': self.client_order_ref or '',
            'move_type': 'out_invoice',
            'narration': self.note,
            'currency_id': self.pricelist_id.currency_id.id,
            'campaign_id': self.campaign_id.id,
            'medium_id': self.medium_id.id,
            'invoice_date': self.inv_date,
            'l10n_sa_delivery_date': self.inv_date,
            'l10n_sa_confirmation_datetime': self.inv_date,
            'source_id': self.source_id.id,
            'user_id': self.user_id.id,
            'invoice_user_id': self.user_id.id,
            'team_id': self.team_id.id,
            'partner_id': self.partner_invoice_id.id,
            'partner_shipping_id': self.partner_shipping_id.id,
            'fiscal_position_id': (self.fiscal_position_id or self.fiscal_position_id.get_fiscal_position(self.partner_invoice_id.id)).id,
            'partner_bank_id': self.company_id.partner_id.bank_ids[:1].id,
            'journal_id': journal.id,  # company comes from the journal
            'invoice_origin': self.name,
            'invoice_payment_term_id': self.payment_term_id.id,
            'payment_reference': self.reference,
            'transaction_ids': [(6, 0, self.transaction_ids.ids)],
            'invoice_line_ids': [],
            'company_id': self.company_id.id,
        }
        return invoice_vals

    @api.onchange('order_line')
    def _check_exist_product_in_line(self):
        for order in self:
            products_in_lines = order.mapped('order_line.product_template_id')
            for product in products_in_lines:
                lines_count = len(order.order_line.filtered(lambda line: line.product_template_id == product))
                if lines_count > 1:
                    raise UserError(_('Product already added, Select one per line'))
        # return True

    def print_pro_forma(self):
        return self.env.ref('base_customisation.action_report_pro_forma_invoice_custom').report_action(self)

    @api.depends('order_line',
        'order_line.is_ko_transfer')
    def _compute_is_ko_invoice(self):
        for order in self:
            if any([line for line in order.order_line.filtered(lambda x: x.is_ko_transfer)]):                
                order.is_ko_invoice = True

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        res.env['kitchen.order.process'].with_context(order_id=res.id).process_kitchen_order()
        res.write({
            'branch_id': res.user_id.branch_id.id
        })
        return res

    def _get_invoiceable_lines(self, final=False):
        """Return the invoiceable lines for order `self`."""
        down_payment_line_ids = []
        invoiceable_line_ids = []
        pending_section = None
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')

        for line in self.order_line:
            if line.display_type == 'line_section':
                # Only invoice the section if one of its lines is invoiceable
                pending_section = line
                continue
            if line.display_type != 'line_note' and float_is_zero(line.qty_to_invoice, precision_digits=precision):
                continue
            if line.qty_to_invoice > 0 or (line.qty_to_invoice < 0 and final) or line.display_type == 'line_note':
                if line.is_downpayment:
                    # Keep down payment lines separately, to put them together
                    # at the end of the invoice, in a specific dedicated section.
                    down_payment_line_ids.append(line.id)
                    continue
                if pending_section:
                    invoiceable_line_ids.append(pending_section.id)
                    pending_section = None
                invoiceable_line_ids.append(line.id)
            pass 
        sol = self.env['sale.order.line'].browse(invoiceable_line_ids + down_payment_line_ids)
        if self._context.get('ko_invoice_policy') == 'only_product':
            return sol.filtered(lambda x: x.is_ko_transfer)
        else:
            return sol

    def _create_invoices(self, grouped=False, final=False, date=None):
        """
        Create the invoice associated to the SO.
        :param grouped: if True, invoices are grouped by SO id. If False, invoices are grouped by
                        (partner_invoice_id, currency)
        :param final: if True, refunds will be generated if necessary
        :returns: list of created invoices
        """
        if not self.env['account.move'].check_access_rights('create', False):
            try:
                self.check_access_rights('write')
                self.check_access_rule('write')
            except AccessError:
                return self.env['account.move']

        # 1) Create invoices.
        invoice_vals_list = []
        invoice_item_sequence = 0 # Incremental sequencing to keep the lines order on the invoice.
        for order in self:
            order = order.with_company(order.company_id)
            current_section_vals = None
            down_payments = order.env['sale.order.line']

            invoice_vals = order._prepare_invoice()
            ctx = self._context
            invoiceable_lines = order.with_context(ctx)._get_invoiceable_lines(final)

            if not any(not line.display_type for line in invoiceable_lines):
                continue

            invoice_line_vals = []
            down_payment_section_added = False
            for line in invoiceable_lines:
                if not down_payment_section_added and line.is_downpayment:
                    # Create a dedicated section for the down payments
                    # (put at the end of the invoiceable_lines)
                    invoice_line_vals.append(
                        (0, 0, order._prepare_down_payment_section_line(
                            sequence=invoice_item_sequence,
                        )),
                    )
                    down_payment_section_added = True
                    invoice_item_sequence += 1
                invoice_line_vals.append(
                    (0, 0, line._prepare_invoice_line(
                        sequence=invoice_item_sequence,
                    )),
                )
                invoice_item_sequence += 1

            invoice_vals['invoice_line_ids'] += invoice_line_vals
            invoice_vals_list.append(invoice_vals)

        if not invoice_vals_list:
            raise self._nothing_to_invoice_error()

        # 2) Manage 'grouped' parameter: group by (partner_id, currency_id).
        if not grouped:
            new_invoice_vals_list = []
            invoice_grouping_keys = self._get_invoice_grouping_keys()
            invoice_vals_list = sorted(
                invoice_vals_list,
                key=lambda x: [
                    x.get(grouping_key) for grouping_key in invoice_grouping_keys
                ]
            )
            for grouping_keys, invoices in groupby(invoice_vals_list, key=lambda x: [x.get(grouping_key) for grouping_key in invoice_grouping_keys]):
                origins = set()
                payment_refs = set()
                refs = set()
                ref_invoice_vals = None
                for invoice_vals in invoices:
                    if not ref_invoice_vals:
                        ref_invoice_vals = invoice_vals
                    else:
                        ref_invoice_vals['invoice_line_ids'] += invoice_vals['invoice_line_ids']
                    origins.add(invoice_vals['invoice_origin'])
                    payment_refs.add(invoice_vals['payment_reference'])
                    refs.add(invoice_vals['ref'])
                ref_invoice_vals.update({
                    'ref': ', '.join(refs)[:2000],
                    'invoice_origin': ', '.join(origins),
                    'payment_reference': len(payment_refs) == 1 and payment_refs.pop() or False,
                })
                new_invoice_vals_list.append(ref_invoice_vals)
            invoice_vals_list = new_invoice_vals_list

        # 3) Create invoices.

        # As part of the invoice creation, we make sure the sequence of multiple SO do not interfere
        # in a single invoice. Example:
        # SO 1:
        # - Section A (sequence: 10)
        # - Product A (sequence: 11)
        # SO 2:
        # - Section B (sequence: 10)
        # - Product B (sequence: 11)
        #
        # If SO 1 & 2 are grouped in the same invoice, the result will be:
        # - Section A (sequence: 10)
        # - Section B (sequence: 10)
        # - Product A (sequence: 11)
        # - Product B (sequence: 11)
        #
        # Resequencing should be safe, however we resequence only if there are less invoices than
        # orders, meaning a grouping might have been done. This could also mean that only a part
        # of the selected SO are invoiceable, but resequencing in this case shouldn't be an issue.
        if len(invoice_vals_list) < len(self):
            SaleOrderLine = self.env['sale.order.line']
            for invoice in invoice_vals_list:
                sequence = 1
                for line in invoice['invoice_line_ids']:
                    line[2]['sequence'] = SaleOrderLine._get_invoice_line_sequence(new=sequence, old=line[2]['sequence'])
                    sequence += 1

        # Manage the creation of invoices in sudo because a salesperson must be able to generate an invoice from a
        # sale order without "billing" access rights. However, he should not be able to create an invoice from scratch.
        moves = self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create(invoice_vals_list)

        # 4) Some moves might actually be refunds: convert them if the total amount is negative
        # We do this after the moves have been created since we need taxes, etc. to know if the total
        # is actually negative or not
        if final:
            moves.sudo().filtered(lambda m: m.amount_total < 0).action_switch_invoice_into_refund_credit_note()
        for move in moves:
            move.message_post_with_view('mail.message_origin_link',
                values={'self': move, 'origin': move.line_ids.mapped('sale_line_ids.order_id')},
                subtype_id=self.env.ref('mail.mt_note').id
            )
        return moves

class SaleOrderLines(models.Model):
    _inherit = 'sale.order.line'

    barcode_scan = fields.Char(
        string='Product Barcode',
        help="Here you can provide the barcode for the product")
    branch_id = fields.Many2one('res.branch', related="order_id.branch_id",
                                store=True)
    is_ko_transfer = fields.Boolean(default=False)
    order_date = fields.Datetime(string="Date")
    # sl_no = fields.Integer(string='Sr#', compute='_compute_serial_number', store=True)

    # @api.depends('sequence', 'order_id')
    # def _compute_serial_number(self):
    #     for order_line in self:
    #         if not order_line.sl_no:
    #             serial_no = 1
    #             for line in order_line.mapped('order_id').order_line:
    #                 line.sl_no = serial_no
    #                 serial_no += 1

    @api.onchange('barcode_scan')
    def _onchange_barcode_scan(self):
        product_rec = self.env['product.product']
        if self.barcode_scan:
            product = product_rec.search([('barcode', '=', self.barcode_scan)])
            self.product_id = product.id



    @api.depends('state', 'product_uom_qty', 'qty_delivered', 'qty_to_invoice', 'qty_invoiced')
    def _compute_invoice_status(self):
        """
        Compute the invoice status of a SO line. Possible statuses:
        - no: if the SO is not in status 'sale' or 'done', we consider that there is nothing to
          invoice. This is also hte default value if the conditions of no other status is met.
        - to invoice: we refer to the quantity to invoice of the line. Refer to method
          `_get_to_invoice_qty()` for more information on how this quantity is calculated.
        - upselling: this is possible only for a product invoiced on ordered quantities for which
          we delivered more than expected. The could arise if, for example, a project took more
          time than expected but we decided not to invoice the extra cost to the client. This
          occurs onyl in state 'sale', so that when a SO is set to done, the upselling opportunity
          is removed from the list.
        - invoiced: the quantity invoiced is larger or equal to the quantity ordered.
        """
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        for line in self:
            if line.state not in ('sale', 'done'):
                line.invoice_status = 'no'
            elif line.is_downpayment and line.untaxed_amount_to_invoice == 0:
                line.invoice_status = 'invoiced'
            # elif not float_is_zero(line.qty_to_invoice, precision_digits=precision):
            #     line.invoice_status = 'to invoice'
            elif line.state == 'sale' and line.product_id.invoice_policy == 'order' and \
                    float_compare(line.qty_delivered, line.product_uom_qty, precision_digits=precision) == 1:
                line.invoice_status = 'upselling'
            elif float_compare(line.qty_invoiced, line.product_uom_qty, precision_digits=precision) >= 0:
                line.invoice_status = 'invoiced'
            else:
                print("\n\n\n")
