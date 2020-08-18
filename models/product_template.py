# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.addons import decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    order_code_ghm = fields.Text('Cod de Compra')
    name_english_ghm = fields.Char('Nome em Inglês')
    name_french_ghm = fields.Text('Nome em Francês')
    name_spanish_ghm = fields.Text('Nome em Espanhol')
    name_portuguese_ghm = fields.Text('Nome em Português')
    typical_delivery_time_ghm = fields.Text('Tempo de Entrega Típico')
    discount_group_ghm = fields.Text('Grupo de Desconto')
    price_structure_group_ghm = fields.Text('Grupo de Estrutura de Preço')
    release_for_processing_ghm = fields.Text('Liberação para Processamento')
    goods_n_ghm = fields.Text('Número do Recebimento')
    gtin_ghm = fields.Text('GTIN')
    max_qty_for_delivery_time = fields.Text(
        'Quantidade Máxima para o Tempo de Entrega')
    last_production_ghm = fields.Text('Última Produção')
    article_category = fields.Text('Categoria do Artigo')
    partner_id = fields.Many2one(
        'res.partner',
        string='Fornecedor Principal',
    )
    desc_german_ghm = fields.Text('Descrição em Alemão')
    desc_english_ghm = fields.Text('Descrição em Inglês')
    desc_french_ghm = fields.Text('Descrição em Francês')
    desc_spanish_ghm = fields.Text('Descrição em Espanhol')
    desc_portuguese_ghm = fields.Text('Descrição em Português')

    def _compute_cost_supplier(self):
        for item in self:
            supplier = item.seller_ids.filtered(lambda x: x.fornecedor_padrao)
            if supplier:
                price = supplier.price * \
                    (1 - (supplier.supplier_discount / 100))
                local_price = supplier.currency_id._convert(
                    price, item.currency_id, item.company_id,
                    fields.Date.today()
                )
                if supplier.currency_id.rate:
                    item.currency_conversion = 1 / supplier.currency_id.rate

                ncm = item.fiscal_classification_id

                ii = local_price * (ncm.imposto_ii / 100)
                ipi = (local_price + ii) * (ncm.imposto_ipi / 100)
                pis = local_price * (ncm.imposto_pis / 100)
                cofins = local_price * (ncm.imposto_cofins / 100)
                
                divisor = 1 - (ncm.imposto_icms / 100)
                icms = (local_price + ii + ipi + pis + cofins) / divisor * (ncm.imposto_icms / 100)

                final_price = local_price + ii + ipi + pis + cofins + icms
                
                item.cost_based_supplier = final_price
                item.margin_based_cost = final_price * (ncm.margem_lucro / 100)

    margin_based_cost = fields.Monetary(string="Margem", compute=_compute_cost_supplier)
    cost_based_supplier = fields.Monetary(
        string="Custo de compra", compute=_compute_cost_supplier)
    currency_conversion = fields.Float("Conversão Usada", compute=_compute_cost_supplier)

    def name_get(self):
        products = []
        for produto in self:
            if produto.name_portuguese_ghm and produto.name_portuguese_ghm != 'A tradução está faltando':
                products += [
                    (produto.id, '%s%s' % (produto.default_code and
                                           '[%s] ' % produto.default_code or
                                           '', produto.name_portuguese_ghm))]
            elif produto.name_english_ghm and produto.name_english_ghm != 'TRANSLATION IS MISSING':
                products += [
                    (produto.id, '%s%s' % (produto.default_code and
                                           '[%s] ' % produto.default_code or
                                           '', produto.name_english_ghm))]
            elif produto.name_spanish_ghm and produto.name_spanish_ghm != 'Una traducción no se encuentra':
                products += [
                    (produto.id, '%s%s' % (produto.default_code and
                                           '[%s] ' % produto.default_code or
                                           '', produto.name_spanish_ghm))]
            else:
                products += [
                    (produto.id, '%s%s' % (produto.default_code and
                                           '[%s] ' % produto.default_code or
                                           '', produto.name))]
        return products


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def price_compute(self, price_type, uom=False, currency=False, company=False):
        if price_type != 'supplier_cost':
            return super(ProductProduct, self).price_compute(
                price_type, uom=uom, currency=currency, company=company)
        prices = dict.fromkeys(self.ids, 0.0)
        for product in self:
            prices[product.id] = product.cost_based_supplier + product.margin_based_cost
        return prices

    def name_get(self):
        products = []
        for produto in self:
            if produto.product_tmpl_id.name_portuguese_ghm and \
                    produto.product_tmpl_id.name_portuguese_ghm != 'A tradução está faltando':
                products += [
                    (produto.id, '%s%s' % (produto.product_tmpl_id.default_code and
                                           '[%s] ' % produto.product_tmpl_id.default_code or
                                           '', produto.product_tmpl_id.name_portuguese_ghm))]
            elif produto.product_tmpl_id.name_english_ghm and \
                    produto.product_tmpl_id.name_english_ghm != 'TRANSLATION IS MISSING':
                products += [
                    (produto.id, '%s%s' % (produto.product_tmpl_id.default_code and
                                           '[%s] ' % produto.product_tmpl_id.default_code or
                                           '', produto.product_tmpl_id.name_english_ghm))]
            elif produto.product_tmpl_id.name_spanish_ghm and \
                    produto.product_tmpl_id.name_spanish_ghm != 'Una traducción no se encuentra':
                products += [
                    (produto.id, '%s%s' % (produto.product_tmpl_id.default_code and
                                           '[%s] ' % produto.product_tmpl_id.default_code or
                                           '', produto.product_tmpl_id.name_spanish_ghm))]
            else:
                products += [
                    (produto.id, '%s%s' % (produto.product_tmpl_id.default_code and
                                           '[%s] ' % produto.product_tmpl_id.default_code or
                                           '', produto.product_tmpl_id.name))]
        return products


class SupplierInfo(models.Model):
    _inherit = "product.supplierinfo"

    fornecedor_padrao = fields.Boolean(
        'Fornecedor Padrão',
        default=False,
    )

    supplier_discount = fields.Float("% Desconto Fornecedor")

    @api.constrains('default_selected_student')
    def _change_fornecedor_padrao(self):
        if self.default_selected_student:
            padraos = self.env['product.supplierinfo'].search(
                [('id', '!=', self.id)])
            for padrao in padraos:
                padrao.fornecedor_padrao = False


class ProductTemplateGeraFornecedor(models.TransientModel):
    _name = "product.template.gerafornecedor"
    _description = "Gera Fornecedor"

    @api.model
    def _get_ids(self):
        gerapreco_obj = self.env['product.template']
        product = gerapreco_obj.browse(self._context.get('active_ids'))[0]
        return 0

    @api.multi
    def gera_fornecedor(self):
        produtos = self.env['product.template'].browse(
            self._context.get('active_ids', []))

        for prod in produtos:
            if prod.standard_price > 0 and prod.partner_id:
                for x in prod.seller_ids:
                    if x.fornecedor_padrao:
                        x.fornecedor_padrao = False
                self.env['product.supplierinfo'].create({
                    'product_tmpl_id': prod.id,
                    'price': (prod.standard_price / 10000) / prod.partner_id.property_purchase_currency_id.rate,
                    'name': prod.partner_id.id,
                    'fornecedor_padrao': True,
                    'min_qty': 1,
                    'currency_id': self.env.user.company_id.currency_id.id,
                    'delay': 1,
                })
        return True


class ProductTemplateGeraPreco(models.TransientModel):
    _name = "product.template.gerapreco"
    _description = "Gera Preço Venda"

    @api.model
    def _get_ids(self):
        gerapreco_obj = self.env['product.template']
        product = gerapreco_obj.browse(self._context.get('active_ids'))[0]
        return 0

    @api.multi
    def gera_preco(self):
        gera_preco = self.env['product.template'].browse(
            self._context.get('active_ids', []))
        user_pricelist_margem = self.env.user.company_id.property_product_pricelist.margem
        user_pricelist_frete = self.env.user.company_id.property_product_pricelist.frete
        user_pricelist_insurance = self.env.user.company_id.property_product_pricelist.insurance

        # Gera Preço de Venda
        for line in gera_preco:
            if line.standard_price:
                line.list_price = line.standard_price * \
                    (1+((user_pricelist_margem+user_pricelist_frete +
                         user_pricelist_insurance)/100))

        return 1
