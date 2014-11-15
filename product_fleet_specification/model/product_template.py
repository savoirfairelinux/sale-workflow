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

from openerp import models, fields, api


class product_template(models.Model):

    _inherit = 'product.template'

    product_fleet_spec_ids = fields.One2many(
        'product.fleet.spec',
        'product_id'
    )
    engine_code = fields.Char(string='Engine Code', size=154)

    a_t = fields.Boolean('A/T')
    m_t = fields.Boolean('M/T')

    y_pipe = fields.Boolean('Y-pipe')

    direct_fit_radiator_side_precat_left_side = fields.Boolean(
        'Direct fit radiator side precat LEFT side')
    direct_fit_radiator_side_precat_right_side = fields.Boolean(
        'Direct fit radiator side precat RIGHT side')

    dohc = fields.Boolean('DOHC')
    shoc = fields.Boolean('SHOC')

    converter_wmanifold = fields.Boolean('Converter W/Manifold')

    super_duty = fields.Boolean('Super Duty')
    b2x4 = fields.Boolean('2X4')
    b4x4 = fields.Boolean('4X4')

    awd = fields.Boolean('AWD')
    fwd = fields.Boolean('FWD')

    b2doors = fields.Boolean('2 doors')
    b4doors = fields.Boolean('4 doors')

    emission_federal = fields.Boolean('Emission Federal')
    emission_californien = fields.Boolean('Emission Californien')

    exc_calif = fields.Boolean('EXC CALIF')

    catalyser2 = fields.Boolean('Catalyser (2)')
    catalyser3 = fields.Boolean('Catalyser (3)')
    catalyser4 = fields.Boolean('Catalyser (4)')

    w_02 = fields.Boolean('W/02')
    w_out = fields.Boolean('W/OUT')

    semi_direct_fit = fields.Boolean('Semi direct fit')
