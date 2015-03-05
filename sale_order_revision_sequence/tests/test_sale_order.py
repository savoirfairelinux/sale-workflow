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

from openerp.tests import common
from openerp.addons.sale_order_revision_sequence.sale_order import (
    to_letters,
    revision_number_to_letter,
)


class TestSaleOrder(common.TransactionCase):
    def setUp(self):
        super(TestSaleOrder, self).setUp()
        self.sale_order_model = self.registry('sale.order')
        self.res_partner_model = self.registry('res.partner')
        res_partner_id = self.res_partner_model.create(
            self.cr, self.uid,
            {'name': 't_partner'}
        )
        self.res_partner = self.res_partner_model.browse(
            self.cr, self.uid, res_partner_id
        )

    def test_sale_order_sequence(self):
        """Test if the name follow the wanted pattern."""
        sale_order_id = self.sale_order_model.create(
            self.cr, self.uid,
            {'partner_id': self.res_partner.id}
        )
        sale_order = self.sale_order_model.browse(
            self.cr, self.uid, sale_order_id
        )
        ret = self.sale_order_model.create_revision(
            self.cr, self.uid, sale_order.id
        )
        revision = self.sale_order_model.browse(
            self.cr, self.uid, ret['res_id']
        )
        self.assertEqual(revision.name, '{}-{}'.format(sale_order.name, 'A'))


class TestToLetters(common.TransactionCase):
    def test_return(self):
        self.assertEqual(list(to_letters(0)), ['A'])
        self.assertEqual(list(to_letters(1)), ['B'])
        self.assertEqual(list(to_letters(26)), ['A', 'A'])
        self.assertEqual(list(to_letters(27)), ['B', 'A'])
        self.assertEqual(list(to_letters(10218)), ['A', 'C', 'O'])
        self.assertEqual(list(to_letters(266748)), ['O', 'O', 'D', 'O'])


class TestRevisionNumberToLetter(common.TransactionCase):
    def test_return(self):
        # Testing 1 letter sequence.
        for i in xrange(0, 25):
            self.assertEqual(revision_number_to_letter(i), chr(i + 65))

        # Testing multiple letters sequences with randomish number ;)
        self.assertEqual(revision_number_to_letter(26), 'AA')
        self.assertEqual(revision_number_to_letter(27), 'AB')
        self.assertEqual(revision_number_to_letter(51), 'AZ')
        self.assertEqual(revision_number_to_letter(52), 'BA')
        self.assertEqual(revision_number_to_letter(225), 'HR')
        self.assertEqual(revision_number_to_letter(10218), 'OCA')
        self.assertEqual(revision_number_to_letter(13011), 'SFL')
        self.assertEqual(revision_number_to_letter(266748), 'ODOO')

