
from odoo import api, fields, models, _

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    kitchen_order_id = fields.Many2one('kitchen.order',
        string="Kitchen Orders")
    branch_id = fields.Many2one('res.branch')
    company_ids = fields.Many2many('res.company')


class StockLocation(models.Model):
    _inherit = 'stock.location'

    company_ids = fields.Many2many('res.company')
    location_id = fields.Many2one('stock.location', 'From',
        domain="[('usage', '!=', 'view')]", check_company=False, required=False)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    company_ids = fields.Many2many('res.company')

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if not args:
            args = []
        if name:
            domain = [('vat', operator, name)]
            partners = self.search(domain + args, limit=limit, )
            res = partners.name_get()
            if limit:
                limit_rest = limit - len(partners)
            else:
                limit_rest = limit
            if limit_rest or not limit:
                args += [('id', 'not in', partners.ids)]
                res += super().name_search(
                    name, args=args, operator=operator, limit=limit_rest)
            return res
        return super().name_search(
            name, args=args, operator=operator, limit=limit
        )

class ProductProduct(models.Model):
    _inherit = 'product.product'

    company_ids = fields.Many2many('res.company')

class StockRule(models.Model):
    _inherit = 'stock.rule'

    company_ids = fields.Many2many('res.company')

class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    company_ids = fields.Many2many('res.company')


class StockMove(models.Model):
    _inherit = 'stock.move'

    company_ids = fields.Many2many('res.company')
    location_dest_id = fields.Many2one('stock.location', 'To',
        domain="[('usage', '!=', 'view')]", check_company=False, required=True)
    picking_id = fields.Many2one('stock.picking', 'Transfer', index=True, states={'done': [('readonly', True)]}, check_company=False)
    picking_type_id = fields.Many2one('stock.picking.type', 'Operation Type', compute='_compute_picking_type_id', store=True, check_company=False)
    location_id = fields.Many2one('stock.location', 'From',
        domain="[('usage', '!=', 'view')]", check_company=False, required=True)

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    location_id = fields.Many2one('stock.location', 'From',
        domain="[('usage', '!=', 'view')]", check_company=False, required=True)
    location_dest_id = fields.Many2one('stock.location', 'To',
        domain="[('usage', '!=', 'view')]", check_company=False, required=True)
    picking_id = fields.Many2one(
        'stock.picking', 'Transfer', auto_join=True,
        check_company=False,
        index=True,
        help='The stock operation where the packing has been made')

class StockLocaionRoute(models.Model):
    _inherit = 'stock.location.route'

    company_ids = fields.Many2many('res.company')

class StockPackage_level(models.Model):
    _inherit = 'stock.package_level'

    company_ids = fields.Many2many('res.company')

class StockWarehouseOrderpoint(models.Model):
    _inherit = 'stock.warehouse.orderpoint'

    company_ids = fields.Many2many('res.company')


class ProductPackaging(models.Model):
    _inherit = 'product.packaging'

    company_ids = fields.Many2many('res.company')

class StockQuantPackage(models.Model):
    _inherit = 'stock.quant.package'

    company_ids = fields.Many2many('res.company')

class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    company_ids = fields.Many2many('res.company')


class StockValuationLayer(models.Model):
    _inherit = 'stock.valuation.layer'

    company_ids = fields.Many2many('res.company')

class AccountMove(models.Model):
    _inherit = 'account.move'

    company_ids = fields.Many2many('res.company')


class StockStorageCategory(models.Model):
    _inherit = 'stock.storage.category'

    company_ids = fields.Many2many('res.company')

class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'    

    company_ids = fields.Many2many('res.company')

class AccountPaymenterm(models.Model):
    _inherit = 'account.payment.term'

    company_ids = fields.Many2many('res.company')

class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    company_ids = fields.Many2many('res.company')

class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'

    company_ids = fields.Many2many('res.company')

class CrmTeam(models.Model):
    _inherit = 'crm.team'

    company_ids = fields.Many2many('res.company')

class SaleOrderTemplate(models.Model):
    _inherit = 'sale.order.template'

    company_ids = fields.Many2many('res.company')

class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    company_ids = fields.Many2many('res.company')

class AccountAccount(models.Model):
    _inherit = 'account.account'

    company_ids = fields.Many2many('res.company')

class AccountTax(models.Model):
    _inherit = 'account.tax'

    company_ids = fields.Many2many('res.company')

class AccountPaymentMethodLine(models.Model):
    _inherit = 'account.payment.method.line'

    company_ids = fields.Many2many('res.company')

class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    company_ids = fields.Many2many('res.company')

class AccountJournalGroup(models.Model):
    _inherit = 'account.journal.group'

    company_ids = fields.Many2many('res.company')

class IrSequence(models.Model):
    _inherit = 'ir.sequence'

    company_ids = fields.Many2many('res.company')

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    company_ids = fields.Many2many('res.company')

class AccountReconcileModel(models.Model):
    _inherit = 'account.reconcile.model'

    company_ids = fields.Many2many('res.company')

class AccountTaxRepartitionLine(models.Model):
    _inherit = 'account.tax.repartition.line'

    company_ids = fields.Many2many('res.company')


class AccountAnalyticTag(models.Model):
    _inherit = 'account.analytic.tag'

    company_ids = fields.Many2many('res.company')
