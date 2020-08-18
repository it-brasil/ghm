
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class PricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    fiscal_classification_id = fields.Many2one(
        'product.fiscal.classification',
        string=u"Classificação Fiscal (NCM)",
    )
    base = fields.Selection(selection_add=[('supplier_cost', 'Baseado no preço do fornecedor')])
