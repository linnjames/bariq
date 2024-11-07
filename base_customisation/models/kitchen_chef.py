
from odoo import api, fields, models, _


class KitchenChef(models.Model):
    _name = 'kitchen.chef'
    _description = "Kitchen Chef"

    name = fields.Char(string='Chef Name', required=True, copy=False)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)
    branch_id = fields.Many2one('res.branch', readonly=True)
    product_category = fields.Many2many('product.category', string='Category')

    @api.model
    def create(self,vals):
        res = super(KitchenChef, self).create(vals)
        res.write({
            'branch_id' : res.env.user.branch_id.id
        })
        return res
