# -*- coding: utf-8 -*-
from odoo import http

# class Ghm(http.Controller):
#     @http.route('/ghm/ghm/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ghm/ghm/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ghm.listing', {
#             'root': '/ghm/ghm',
#             'objects': http.request.env['ghm.ghm'].search([]),
#         })

#     @http.route('/ghm/ghm/objects/<model("ghm.ghm"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ghm.object', {
#             'object': obj
#         })