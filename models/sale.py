# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    percentual_mva = fields.Float(string="% MVA")

    def _prepare_tax_context(self):
        vals = super(SaleOrderLine, self)._prepare_tax_context()
        vals['icms_st_aliquota_mva'] = self.percentual_mva
        return vals
