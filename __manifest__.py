# -*- coding: utf-8 -*-
{
    'name': "GHM",

    'summary': """
        Personalizações Para a Empresa GHM """,

    'description': """
        Acrescimo de campos no módulo de Clientes, conforme a necessidade da empresa GHM.
    """,

    'author': "Brenno Campos Garcia",
    'website': "https://www.toph.com.br",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'customization',
    'version': '12.0',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'web',
                'br_base',
                'br_account',
                'sale',
                'purchase'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/product_views.xml',
        'views/purchase_views.xml',
        'views/res_company_views.xml',
        'views/sale_views.xml',
        'views/ncm.xml',
        'report/sale_report_templates.xml',
        'report/report_templates.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,

}