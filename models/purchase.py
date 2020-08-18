# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    cp_visivel = fields.Boolean(
        'Deixar os Campos Desconto e Impostos invisível',
        default=False,
    )

    @api.onchange('partner_id')
    def onchange_partner_id_desconto(self):
        for parceiro in self:
            if parceiro.partner_id.discount > 0 and len(parceiro.order_line) > 0:
                for linha in parceiro.order_line:
                    linha.discount = parceiro.partner_id.discount

    @api.onchange('cp_visivel')
    def onchange_cp_visivel(self):
        for compra in self:
            if compra.cp_visivel:
                for linha in compra.order_line:
                    linha.cp_visivel = True
            else:
                for linha in compra.order_line:
                    linha.cp_visivel = False

    @api.multi
    def gera_precocusto(self):
        for compra in self:
            for line in compra.order_line:
                line.product_id.product_tmpl_id.standard_price = line.price_total
                line.product_id.product_tmpl_id.list_price = line.product_id.product_tmpl_id.standard_price * (1 + (
                        (self.env.user.company_id.property_product_pricelist.margem
                         + self.env.user.company_id.property_product_pricelist.frete
                         + self.env.user.company_id.property_product_pricelist.insurance) / 100))

    @api.multi
    def gera_linhas(self):
        for compra in self:
            count = 0
            cal_ids = []
            new_lines = []
            prod_ids = []
            query = """
                        SELECT product_tmpl_id
                        FROM product_supplierinfo
                        WHERE name = (%s)
                        AND fornecedor_padrao = True
                        """ % compra.partner_id.id
            self._cr.execute(query)
            categ_prod = [item[0] for item in self.env.cr.fetchall()]
            if compra.order_line:
                for prods in compra.order_line:
                    cal_ids.append(prods.product_id.id)
            if len(cal_ids) > 1:
                prod_select = self.env['product.product'].search([('product_tmpl_id', 'in', categ_prod),
                                                                  ('id', 'not in', cal_ids)], limit=80)
            else:
                prod_select = self.env['product.product'].search([('product_tmpl_id', 'in', categ_prod)], limit=80)
            for prod in prod_select:
                count += 1
                if len(prod.product_tmpl_id.seller_ids) == 1:
                    new_lines.append((0, 0, {
                        'order_id': compra.id,
                        'product_id': prod.id,
                        'price_unit': prod.product_tmpl_id.seller_ids.price,
                        'product_qty': 1.0,
                        'product_uom_qty': 1,
                        'name': '',
                        'date_planned': fields.Datetime.now(),
                        'product_uom': prod.product_tmpl_id.uom_id.id
                    }))
                    prod_ids.append(prod.id)
                else:
                    for fornecedor in prod.product_tmpl_id.seller_ids:
                        if fornecedor.fornecedor_padrao:
                            new_lines.append((0, 0, {
                                'order_id': compra.id,
                                'product_id': prod.id,
                                'price_unit': fornecedor.price,
                                'product_qty': 1.0,
                                'product_uom_qty': 1,
                                'name': '',
                                'date_planned': fields.Datetime.now(),
                                'product_uom': prod.product_tmpl_id.uom_id.id
                            }))
                            prod_ids.append(prod.id)
                if count >= 80:
                    break
            compra.write({'order_line': new_lines})
            linha = self.env['purchase.order.line'].search([('order_id', '=', compra.id),
                                                            ('product_id', 'in', prod_ids)])
            for ls in linha:
                ls.onchange_product_id()


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    discount = fields.Float(
        string='Desconto do Fornecedor(%)',
        digits=dp.get_precision('Discount'),
        default=0.0,
        store=True,
    )
    cp_visivel = fields.Boolean(
        'Deixar os Campos Desconto e Impostos invisível',
        default=False,
    )

    @api.multi
    @api.onchange('product_id')
    def onchange_partner_id_desconto(self):
        for parceiro in self:
            if parceiro.order_id.partner_id.discount > 0:
                parceiro.discount = parceiro.order_id.partner_id.discount
            for compra in parceiro.order_id:
                if compra.cp_visivel:
                    parceiro.cp_visivel = True
