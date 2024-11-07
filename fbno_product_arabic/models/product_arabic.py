# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductToArabic(models.Model):
    _inherit = 'product.template'

    product_arabic = fields.Char()
    product_custom_id = fields.Char(string='Product ID')

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if not args:
            args = []
        if name:
            domain = [('product_custom_id', '=', name)]
            products = self.search(domain + args, limit=limit, )
            res = products.name_get()
            if limit:
                limit_rest = limit - len(products)
            else:
                limit_rest = limit
            if limit_rest or not limit:
                args += [('id', 'not in', products.ids)]
                res += super().name_search(
                    name, args=args, operator=operator, limit=limit_rest)
            return res
        return super().name_search(
            name, args=args, operator=operator, limit=limit
        )


class ProductProductArabic(models.Model):
    _inherit = 'product.product'

    product_arabic = fields.Char("Arabic Name", related="product_tmpl_id.product_arabic")
    product_custom_id = fields.Char("Arabic Name", related="product_tmpl_id.product_custom_id")

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if not args:
            args = []
        if name:
            domain = [('product_custom_id', '=', name)]
            products = self.search(domain + args, limit=limit, )
            res = products.name_get()
            if limit:
                limit_rest = limit - len(products)
            else:
                limit_rest = limit
            if limit_rest or not limit:
                args += [('id', 'not in', products.ids)]
                res += super().name_search(
                    name, args=args, operator=operator, limit=limit_rest)
            return res
        return super().name_search(
            name, args=args, operator=operator, limit=limit
        )

class ProductCategory(models.Model):
    _inherit = 'product.category'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)