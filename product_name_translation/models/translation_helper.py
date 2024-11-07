# -*- coding: utf-8 -*-
from googletrans import Translator
from odoo import api, models, fields, _



class ProductTemplate(models.Model):
    """ Class to create translation for selected words"""

    _inherit = 'product.template'

    arabic_name = fields.Char(string='Arabic Name')

    @api.onchange('name')
    def translate_to_arabic(self):
        """Translate the product_id value to Arabic and store in arabic_name field"""
        translator = Translator()

        for record in self:
            product_name = record.name

            if not product_name:
                record.arabic_name = 'No name provided'
                continue

            try:
                translated_text = translator.translate(product_name, dest='ar').text
                record.arabic_name = translated_text
            except Exception as e:
                record.arabic_name = 'Translation error'
