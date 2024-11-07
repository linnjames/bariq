
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class KitchenOrderPrint(models.TransientModel):
    _name = "kitchen.order.print"
    _description = "Kitchen Order Print"

    from_date = fields.Datetime('Start Date')
    to_date = fields.Datetime('To Date')
    chef_id = fields.Many2one('kitchen.chef', string='Chef')
    # branch = fields.Many2one('res.branch',string='Branch', default=lambda self: self.env.user.branch_id)
    amt_total = fields.Float('Amount Total')
    qty_total = fields.Float('QTY Total')
    vat_total = fields.Float('VAT Total')
    net_total = fields.Float('Net Total')

    def print_report(self):
        return self.env.ref('base_customisation.action_kitchen_order_print_pdf').report_action(self)



    def get_record(self):
        xx = self.env['kitchen.chef'].search([('name', '=', self.chef_id.name)])
        if xx:
            print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE", xx.product_category)
        sale_order_data = self.env['sale.order.line'].search(
            [('order_date', '>=', str(self.from_date)),
             ('order_date', '<=', str(self.to_date)),
             ('product_id.categ_id', 'in', xx.product_category.ids),
             # ('branch_id.name', '=', self.branch.name),


             ])
        # for rec in sale_order_data:
        #     print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ", rec.name)
        order_data_sales = []
        for i in sale_order_data:
            order_data_sales.append({
                    'category': i.product_id.categ_id.name,
                    'product_id': i.product_id.name,
                    'price': i.price_subtotal,
                    'qty': i.product_uom_qty,
                    'tax': i.price_tax,
                    'subtotal': i.price_total,
                })

        data = {}
        pro_qty_data = []
        for item in order_data_sales:
            data.setdefault(item['product_id'], []).append(item['category'])
        product_name = list(data.keys())
        for z in product_name:
            products = z
            pro_qty_data.append({
                'products': products,

            })
            print("5555555555555555555", products)
        return pro_qty_data
    #
    # def get_record1(self):
    #     sale_order_data = self.env['sale.order'].search(
    #         [('date_order', '>=', self.from_date),
    #          ('date_order', '<=', self.to_date),
    #
    #          ])
    #
    #     order_data_sales = []
    #     same_categ_prdcts = []
    #     for i in sale_order_data.order_line:
    #         order_data_sales.append({
    #             'category': i.product_id.categ_id.name,
    #             'product_id': i.product_id.name,
    #             'price': i.price_subtotal,
    #             'qty': i.product_uom_qty,
    #             'tax': i.price_tax,
    #             'subtotal': i.price_total,
    #         })
    #         print("#######################", i.product_id.name, "=====", i.product_id.categ_id.name)
    #         same_categ_prdcts.append({
    #             'prodcts_name': i.product_id.name,
    #             'category_name': i.product_id.categ_id.name,
    #
    #         })
    #     print("**********************", "=====", same_categ_prdcts)
    #     # prdcts = self.env['product.product'].search([('categ_id.name', '=', i.product_id.categ_id.name)])
    #     # for rec in prdcts:
    #     #     print("QQ", rec.name, "==", rec.categ_id.name)
    #     #     xx = self.env['kitchen.chef'].search([('product_category.name', '=',  rec.categ_id.name)])
    #     #     if xx:
    #     #         print("tt", xx.name)
    #
    #     data = {}
    #     pro_qty_data10 = []
    #     for item in same_categ_prdcts:
    #         data.setdefault(item['prodcts_name'], []).append(item['category_name'])
    #     product_name = list(data.values())
    #     for z in product_name:
    #         products = z
    #         pro_qty_data10.append({
    #             'products': products,
    #
    #         })
    #         print("66666666666666666", products, )
    #         xx = self.env['kitchen.chef'].search([('[product_category.name]', '=', products)])
    #         if xx:
    #             print("tt", xx.name)
    #     return pro_qty_data10



    def product_qty_sorted(self):
        xx = self.env['kitchen.chef'].search([('name', '=', self.chef_id.name)])
        if xx:
            print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE", xx.product_category)
        sale_order_data = self.env['sale.order.line'].search(
            [('order_date', '>=', str(self.from_date)),
             ('order_date', '<=', str(self.to_date)),
             ('product_id.categ_id', 'in', xx.product_category.ids),
             # ('branch_id.name', '=', self.branch.name),

             ])
        for rec in sale_order_data:
            print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ", rec.name)
        order_data_sales = []
        for i in sale_order_data:
            order_data_sales.append({
                'category': i.product_id.categ_id.name,
                'product_id': i.product_id.name,
                'price': i.price_subtotal,
                'qty': i.product_uom_qty,
                'tax': i.price_tax,
                'subtotal': i.price_total,
            })
        data1 = {}
        pro_qty_data1 = []
        for item in order_data_sales:
            data1.setdefault(item['product_id'], []).append(item['qty'])
        product_qty = list(data1.values())
        qty_total = []
        for w in product_qty:
            qty = sum(w)
            qty_total.append(qty)
            self.qty_total = sum(qty_total)
            pro_qty_data1.append({
                'qty': qty,
            })
        return pro_qty_data1

    def product_price_sorted(self):
        xx = self.env['kitchen.chef'].search([('name', '=', self.chef_id.name)])
        if xx:
            print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE", xx.product_category)
        sale_order_data = self.env['sale.order.line'].search(
            [('order_date', '>=', str(self.from_date)),
             ('order_date', '<=', str(self.to_date)),
             ('product_id.categ_id', 'in', xx.product_category.ids),
             # ('branch_id.name', '=', self.branch.name),

             ])
        for rec in sale_order_data:
            print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ", rec.name)
        order_data_sales = []
        for i in sale_order_data:
            order_data_sales.append({
                'category': i.product_id.categ_id.name,
                'product_id': i.product_id.name,
                'price': i.price_subtotal,
                'qty': i.product_uom_qty,
                'tax': i.price_tax,
                'subtotal': i.price_total,
            })
        data2 = {}
        pro_qty_data2 = []
        for item in order_data_sales:
            data2.setdefault(item['product_id'], []).append(item['price'])
        product_price = list(data2.values())
        price_total = []
        for rec in product_price:
            price = sum(rec)
            price_total.append(price)
            self.net_total = sum(price_total)
            pro_qty_data2.append({
                'price': price,
            })
        return pro_qty_data2

    def product_tax_sorted(self):
        xx = self.env['kitchen.chef'].search([('name', '=', self.chef_id.name)])
        if xx:
            print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE", xx.product_category)
        sale_order_data = self.env['sale.order.line'].search(
            [('order_date', '>=', str(self.from_date)),
             ('order_date', '<=', str(self.to_date)),
             ('product_id.categ_id', 'in', xx.product_category.ids),
             # ('branch_id.name', '=', self.branch.name),

             ])
        for rec in sale_order_data:
            print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ", rec.name)
        order_data_sales = []
        for i in sale_order_data:
            order_data_sales.append({
                'category': i.product_id.categ_id.name,
                'product_id': i.product_id.name,
                'price': i.price_subtotal,
                'qty': i.product_uom_qty,
                'tax': i.price_tax,
                'subtotal': i.price_total,
            })

        data3 = {}
        pro_qty_data3 = []
        for item in order_data_sales:
            data3.setdefault(item['product_id'], []).append(item['tax'])
        product_tax = list(data3.values())
        tax_total = []
        for s in product_tax:
            tax = sum(s)
            tax_total.append(tax)
            self.vat_total = sum(tax_total)
            pro_qty_data3.append({
                'tax': tax,
            })
        return pro_qty_data3

    def product_subtotal_sorted(self):
        xx = self.env['kitchen.chef'].search([('name', '=', self.chef_id.name)])
        if xx:
            print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE", xx.product_category)
        sale_order_data = self.env['sale.order.line'].search(
            [('order_date', '>=', str(self.from_date)),
             ('order_date', '<=', str(self.to_date)),
             ('product_id.categ_id', 'in', xx.product_category.ids),
             # ('branch_id.name', '=', self.branch.name),

             ])
        for rec in sale_order_data:
            print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ", rec.name)
        order_data_sales = []
        for i in sale_order_data:
            order_data_sales.append({
                'category': i.product_id.categ_id.name,
                'product_id': i.product_id.name,
                'price': i.price_subtotal,
                'qty': i.product_uom_qty,
                'tax': i.price_tax,
                'subtotal': i.price_total,
            })
        data4 = {}
        pro_qty_data4 = []
        for item in order_data_sales:
            data4.setdefault(item['product_id'], []).append(item['price'])
        product_subtotal = list(data4.values())
        amt_total = []
        for rec in product_subtotal:
            price = sum(rec)
            amt_total.append(price)
            self.amt_total = sum(amt_total)
            pro_qty_data4.append({
                'subtotal': price,
            })
        return pro_qty_data4


    def product_subtotal_sorted_total(self):
        xx = self.env['kitchen.chef'].search([('name', '=', self.chef_id.name)])
        if xx:
            print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE", xx.product_category)
        sale_order_data = self.env['sale.order.line'].search(
            [('order_date', '>=', str(self.from_date)),
             ('order_date', '<=', str(self.to_date)),
             ('product_id.categ_id', 'in', xx.product_category.ids),
             # ('branch_id.name', '=', self.branch.name),

             ])
        for rec in sale_order_data:
            print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ", rec.name)
        order_data_sales = []
        for i in sale_order_data:
            order_data_sales.append({
                'category': i.product_id.categ_id.name,
                'product_id': i.product_id.name,
                'price': i.price_subtotal,
                'qty': i.product_uom_qty,
                'tax': i.price_tax,
                'subtotal': i.price_total,
            })
        data4 = {}
        pro_qty_data4 = []
        for item in order_data_sales:
            data4.setdefault(item['product_id'], []).append(item['subtotal'])
        product_subtotal = list(data4.values())
        amt_total = []
        for rec in product_subtotal:
            subtotal = sum(rec)
            amt_total.append(subtotal)
            self.amt_total = sum(amt_total)
            pro_qty_data4.append({
                'amt_total': sum(amt_total),
            })
        return pro_qty_data4


    # def check_report_excel(self):
    #     data = {
    #         'model': 'kitchen.order.print',
    #         'from_date': self.from_date,
    #         'to_date': self.to_date
    #     }
    #     return self.env.ref('base_customisation.action_kitchen_order_print').report_action(self, data=data, config=False)
#
# class KitchenReportXlsx(models.AbstractModel):
#     _name = 'report.base_customisation.kitchen_print'
#     _inherit = 'report.report_xlsx.abstract'
#
#     def generate_xlsx_report(self, workbook, data, acc_data):
#         from_date = data['from_date']
#         to_date = data['to_date']
#         sheet1 = workbook.add_worksheet("Order Report")
#         data_format = workbook.add_format({
#             'border': 1,
#             'align': 'center',
#             'valign': 'vcenter'})
#         merge_format = workbook.add_format({
#             'bold': 1,
#             'border': 1,
#             'align': 'center',
#             'valign': 'vcenter'})
#         merge_format_header = workbook.add_format({
#             'bold': 1,
#             'border': 1,
#             'align': 'center',
#             'valign': 'vcenter'})
#         sheet1.set_column('D:F', 20)
#         sheet1.set_column('B:B', 20)
#         sheet1.set_column('A:A', 20)
#         sheet1.set_column('C:C', 20)
#         sheet1.set_column('J:J', 20)
#         sheet1.set_column('K:K', 1)
#         sheet1.set_column('L:N', 20)
#         sheet1.set_column('G:G', 20)
#         sheet1.set_default_row(25)
#         data_format.set_font_size(9)
#         merge_format_header.set_font_size(14)
#         merge_format.set_font_size(10)
#         merge_format.set_bg_color('#D3D3D3')
#         # sheet1.merge_range('A1:G1', 'Tax Report : ' + type_tax_use, merge_format_header)
#         sheet1.merge_range('A2:C2', 'From  ' + data['from_date'] + ' To ' + data['to_date'], merge_format)
#         # sheet1.merge_range('D2:G2', 'Date To:' + data['to_date'], merge_format)
#         row = 3
#         col = 0
#         sheet1.write('A3', 'ProductCode', merge_format)
#         sheet1.write('B3', 'Item', merge_format)
#         sheet1.write('C3', 'Qty', merge_format)
#         sheet1.write('D3', 'Net Amount', merge_format)
#         sheet1.write('E3', 'VAT Amount', merge_format)
#         sheet1.write('F3', 'Total Amount', merge_format)
#         # order_data = self.env['kitchen.order'].search(
#         #     [('date_order', '>=', from_date),
#         #      ('date_order', '<=', to_date),
#         #
#         #      ])
#
#         sale_order_data = self.env['sale.order'].search(
#             [('date_order', '>=', from_date),
#              ('date_order', '<=', to_date),
#
#              ])
#         print("$$$$$$$$$$$$$$$$$$$$$$", sale_order_data.order_line)
#         order_data_sales = []
#         for i in sale_order_data.order_line:
#             order_data_sales.append({
#                 'category': i.product_id.categ_id.name,
#                 'product_id': i.product_id.name,
#                 'price': i.price_subtotal,
#                 'qty': i.product_uom_qty,
#                 'tax': i.price_tax,
#                 'subtotal': i.price_total,
#             })
#             xx = self.env['kitchen.chef'].search([('product_category.name', '=', i.product_id.categ_id.name)])
#             if xx:
#                 print("tt", xx.name)
#         print("#######################", order_data_sales)
#         data = {}
#         pro_qty_data = []
#         for item in order_data_sales:
#             data.setdefault(item['product_id'], []).append(item['price'])
#         product_name = list(data.keys())
#         u = 0
#         for z in product_name:
#             u = u + 1
#             print("555555555555555", u)
#             products = z
#             pro_qty_data.append({
#                 'products': products,
#
#             })
#             row += 0
#             sheet1.write(row + 1, 1, products, data_format)
#             row += 1
#
#         data1 = {}
#         pro_qty_data1 = []
#         for item in order_data_sales:
#             data1.setdefault(item['product_id'], []).append(item['qty'])
#         product_qty = list(data1.values())
#         uu = 0
#         for w in product_qty:
#             uu = uu + 1
#             qty = sum(w)
#             pro_qty_data1.append({
#                 'qty': qty,
#             })
#             row += 0
#             r = u - 1
#             sheet1.write(row - r, 2, qty or '-', data_format)
#             row += 1
#             col = 0
#
#
#
#         data2 = {}
#         pro_qty_data2 = []
#         for item in order_data_sales:
#             data2.setdefault(item['product_id'], []).append(item['price'])
#         product_price = list(data2.values())
#         for rec in product_price:
#             price = sum(rec)
#             pro_qty_data2.append({
#                 'price': price,
#             })
#             row += 0
#             rr = uu + 2
#             sheet1.write(row - rr, 3, price or '-', data_format)
#             row += 1
#             col = 0
#
#         data3 = {}
#         pro_qty_data3 = []
#         for item in order_data_sales:
#             data3.setdefault(item['product_id'], []).append(item['tax'])
#         product_tax = list(data3.values())
#         for s in product_tax:
#             tax = sum(s)
#             pro_qty_data3.append({
#                 'tax': tax,
#             })
#             row += 0
#
#             sheet1.write(row - 8, 4, tax or '-', data_format)
#             row += 1
#             col = 0
#
#         data4 = {}
#         pro_qty_data4 = []
#         for item in order_data_sales:
#             data4.setdefault(item['product_id'], []).append(item['subtotal'])
#         product_subtotal = list(data4.values())
#         for rec in product_subtotal:
#             subtotal = sum(rec)
#             pro_qty_data4.append({
#                 'subtotal': subtotal,
#             })
#             row += 0
#
#             sheet1.write(row - 11, 5, subtotal or '-', data_format)
#             row += 1
#             col = 0
#
#         # data5 = {}
#         # pro_qty_data5 = []
#         # for item in order_data_sales:
#         #     data5.setdefault(item['product_id'], []).append(item['category'])
#         # product_categ = list(data5.values())
#         # for rec in product_categ:
#         #     categ = rec
#         #     pro_qty_data4.append({
#         #         'categ': categ,
#         #     })
#         #     row += 0
#         #
#         #     sheet1.write(row - 11, 6, categ or '-', data_format)
#         #     row += 1
#         #     col = 0
#         #
#         # return pro_qty_data5
#         return pro_qty_data4
#         return pro_qty_data3
#         return pro_qty_data2
#         return pro_qty_data1
#         return pro_qty_data
