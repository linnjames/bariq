# -*- coding: utf-8 -*-
import base64
import codecs
from odoo import http
from odoo.http import request

class VATReportXLSXDownload(http.Controller):

    @http.route(
        ["/web/binary/download_xlsx_report/<int:file>"],
        type='http',
        auth="public",
        website=True,
        sitemap=False)
    def download_proxy_detail_excel(self, file=None, **post):
        if file:
            file_id = request.env['od.vat.report.download'].browse([file])
            if file_id:
                binary_data = file_id.excel_file
                if binary_data:
                    content_base64 = codecs.decode(binary_data, 'base64')
                    headers = [
                        ('Content-Type', 'application/vnd.ms-excel'),
                        ('Content-Disposition', f'attachment; filename={file_id.file_name};')
                    ]
                    return request.make_response(content_base64, headers)
        return False
