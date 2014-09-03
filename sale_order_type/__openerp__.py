# -*- encoding: utf-8 -*-
# #############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2010 - 2014 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Sale Order Type',
    'version': '1.0',
    'author': 'Savoir-faire Linux',
    'maintainer': 'Savoir-faire Linux',
    'website': 'http://www.savoirfairelinux.com',
    'license': 'AGPL-3',
    'category': 'Sales',
    'summary': 'Sale Order Type',
    'description': """
Sale Order Type
===============
This module is based on the principle of sale_journal. It adds a one2many \
field based on a customizable menu found in the sales configuration tab.

Contributors
------------

*   Mathieu BENOIT (mathieu.benoit@savoirfairelinux.com)
*   William BEVERLY (william.beverly@savoirfairelinux.com)
*   Bruno JOLIVEAU (bruno.joliveau@savoirfairelinux.com)

More informations
-----------------

    Module developped and tested with Odoo version 8.0
    Module is based on sale_journal, developped by Odoo S.A., licence Affero GPL-3, version 8.0.1.0
    For questions, please contact our support services (support@savoirfairelinux.com)
    """,
    'author': 'OpenERP SA',
    'website': 'http://www.openerp.com',
    'images': [],
    'depends': [
        'sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'sale_order_type_view.xml',
    ],
    'external_dependencies': {
        'python': [],
    },
    'demo': [
        'sale_order_type_data_demo.xml',
    ],
    'test': [],
    'installable': True,
}
