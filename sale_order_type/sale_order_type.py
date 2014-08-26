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

from openerp.osv import fields, orm


class sale_order_type(orm.Model):
    _name = 'sale.order.type'
    _description = 'Sale Order Types'
    _columns = {
        'name': fields.char('Sale Order Type', required=True),
        'active': fields.boolean('Active',
                                 help=("If the active field is set to False, it"
                                        " will allow you to hide the sale order"
                                        " type type without removing it.")),
        'note': fields.text('Note'),
    }
    _defaults = {
        'active': True,
    }


#==============================================
# sale order type inherit
#==============================================

class sale(orm.Model):
    _inherit = "sale.order"
    _columns = {
        'sale_order_type_id': fields.many2one('sale.order.type',
                                              'Sale Order Types',
                                              help=("The name of the sale order"
                                                    "you specified in the "
                                                    "configuration table."))
    }
