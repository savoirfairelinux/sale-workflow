# -*- coding: utf-8 -*-

##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 Savoir-faire Linux (<www.savoirfairelinux.com>).
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
    'name': 'Product Fleet Specification',
    'version': '1.0',
    'category': 'Sale',
    'summary': 'Product Fleet Specification',
    'description': """
Product Fleet Specification
===========================

This module creates a specification tab to the product form that allows
users to add several fleet and catalyser related attributes to products.

Contributors
------------
* Joao Alfredo Gama Batista (joao.gama@savoirfairelinux.com)
""",
    'author': 'Savoir-faire Linux',
    'website': 'www.savoirfairelinux.com',
    'license': 'AGPL-3',
    'depends': ['product', 'fleet'],
    'data': [
        'security/ir.model.access.csv',
        'data/fleet_vehicle_cylinder_data.xml',
        'data/fleet_vehicle_litre_data.xml',
        'view/product_template_view.xml'
    ],
    'test': [],
    'demo': [],
    'auto_install': False,
    'installable': True,
}
