# -*- coding: utf-8 -*-
#
#    Copyright © 2019; Brasil; By Brenno Campos Garcia; Todos os direitos reservados
#    Copyright © 2019; Brazil; By Brenno Campos Garcia; All rights reserved
#


from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp


class EnterpriseType(models.Model):
    _name = 'enterprise.type'
    _description = 'Tipo de Empresas'

    name = fields.Char(
        string='Descrição do Tipo de Empresa',
    )


class IndustryType(models.Model):
    _name = 'industry.type'
    _description = 'Tipo de Indústrias'

    name = fields.Char(
        string='Descrição do Tipo de Indústria',
    )
    partner_ids = fields.Many2many(
        'res.partner',
        'partner_industry_rel',
        'industry_id',
        'partner_id',
        string='Colaboradores Vinculados',
        ondelete='restrict',
    )


class CompanyMarket(models.Model):
    _name = 'business.market'
    _description = 'Mercados de Atuação'

    name = fields.Char(
        string='Descrição do Tipo de Mercado de Atuação',
    )
    partner_ids = fields.Many2many(
        'res.partner',
        'partner_market_rel',
        'market_id',
        'partner_id',
        string='Colaboradores Vinculados',
        ondelete='restrict',
    )


class ResPartner(models.Model):
    _inherit = 'res.partner'

    fax = fields.Char()
    livechat = fields.Char()
    enterprise_type_id = fields.Many2one(
        'enterprise.type',
        string='Tipo da Empresa',
    )
    annual_income = fields.Float(
        string='Rendimento Anual',
        digits=(6, 2),
    )
    level = fields.Selection(
        [('C', 'Sem Prioridade'),
         ('B', 'Normal'),
         ('A','Prioridade')],
        default='C',
        index=True,
        string="Prioridade",
    )
    market_ids = fields.Many2many(
        'business.market',
        'partner_market_rel',
        'partner_id',
        'market_id',
        string='Mercados de Atuação',
        ondelete='restrict',
    )
    industry_type_ids = fields.Many2many(
        'industry.type',
        'partner_industry_rel',
        'partner_id',
        'industry_id',
        string='Tipo da Indústria',
        ondelete='restrict',
    )
    discount = fields.Float(
        string='Desconto do Fornecedor(%)',
        digits=dp.get_precision('Discount'),
        default=0.0,
        store=True,
    )