# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    percentual_mva = fields.Float(string="% MVA")

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id',
                 'icms_st_aliquota_mva', 'incluir_ipi_base',
                 'icms_aliquota_reducao_base', 'icms_st_aliquota_reducao_base',
                 'ipi_reducao_bc', 'icms_st_aliquota_deducao', 'percentual_mva')
    def _compute_amount(self):
        return super(SaleOrderLine, self)._compute_amount()

    def _prepare_tax_context(self):
        vals = super(SaleOrderLine, self)._prepare_tax_context()
        vals['icms_st_aliquota_mva'] = self.percentual_mva
        return vals
