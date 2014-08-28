# -*- encoding: utf-8 -*-
#
# OpenERP, Open Source Management Solution
# This module copyright (C) 2013 Savoir-faire Linux
# (<http://www.savoirfairelinux.com>).
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

import logging

_logger = logging.getLogger(__name__)
logging.basicConfig()
# _logger.setLevel(logging.DEBUG)

from openerp.osv import fields, orm


class sale_order_specification_social(orm.Model):
    """ Add the notion of revision to sale.order """
    _inherit = 'sale.order'

    _columns = {
        'phone_number': fields.char('Phone Number', size=64),
        'welcome_notes': fields.text('Other')
    }
