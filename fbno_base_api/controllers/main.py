# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class BaseApi(http.Controller):

    @http.route(['/api/test'], type='json', method=['GET'], auth="user")
    def test_api(self, **kw):
        if kw:
            partner = request.env['res.partner'].sudo().search([])
            partner_data = [{
                "name": rec.name,
            } for rec in partner]
            return partner_data

    @http.route(['/api/product'], type='json', method=['POST'], auth="public")
    def product_create(self):
            product = request.env['product.product'].sudo().create({
                'name': 'flowerpot',
                'default_code': '002',
                'list_price': '150',
            })

            return {
                "success": True,
                "product_id": product.id,
                "name": product.name,
                "default_code": product.default_code,
                "list_price": product.list_price,
            }

    @http.route(['/api/get_product_details'], type='json', method=['GET'], auth="user")
    def get_product_details(self, **kw):
        if kw:
            products = request.env['product.product'].sudo().search([])
            product_data = [{
                "name": rec.name,
                "default_code": rec.default_code,
                "price": rec.list_price,
                "cost": rec.standard_price,
            } for rec in products]
            return product_data

    @http.route(['/api/get_sale_order'], type='json', method=['GET'], auth="user")
    def get_sale_order(self, **kw):
        if kw:
            sales = request.env['sale.order'].sudo().search([])
            sale_order = [{
                "name": rec.name,
                "date": rec.date_order,
                "partner": rec.partner_id,
                "salesperson": rec.user_id,
                "company": rec.company_id,
                "total": rec.amount_total,
            } for rec in sales]
            return sale_order

    @http.route(['/api/get_pricelist'], type='json', method=['GET'], auth="user")
    def get_pricelist(self, **kw):
        if kw:
            pricelist = request.env['product.pricelist'].sudo().search([])
            all_get = [{
                "name": rec.name,
                "company": rec.company_id,
            } for rec in pricelist]
            return all_get
