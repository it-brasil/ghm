from odoo import fields, models


class ProductFiscalClassification(models.Model):
    _inherit = 'product.fiscal.classification'
    
    imposto_ii = fields.Float(string="% II")
    imposto_ipi = fields.Float(string="% IPI")
    imposto_pis = fields.Float(string="% PIS")
    imposto_cofins = fields.Float(string="% COFINS")
    imposto_icms = fields.Float(string="% ICMS")
    
    margem_lucro = fields.Float(string="% Margem")