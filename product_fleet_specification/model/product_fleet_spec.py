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

from openerp import models, fields


class ProductFleetSpec(models.Model):
    """Product Fleet Specification"""

    _name = 'product.fleet.spec'
    _description = __doc__

    name = fields.Char('Name')
    product_id = fields.Many2one('product.template', string='Product')
    brand_id = fields.Many2one('fleet.vehicle.model.brand', string='Brand')
    model_id = fields.Many2one('fleet.vehicle.model', string='Model')
    year_start = fields.Char('Start Year', size=4)
    year_end = fields.Char('End Year', size=4)
    cylinder_id = fields.Many2one('fleet.vehicle.cylinder', string='Cylinder')
    litre_id = fields.Many2one('fleet.vehicle.litre', string='Litre')
    spec_ids = fields.Many2many(
        'fleet.vehicle.spec',
        string='Vehicle Specification')
    engine_code_id = fields.Many2one(
        'fleet.vehicle.enginecode',
        string='Engine Code')
