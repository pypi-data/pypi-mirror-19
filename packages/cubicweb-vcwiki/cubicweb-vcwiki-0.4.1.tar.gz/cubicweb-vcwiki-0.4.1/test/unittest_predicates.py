# -*- coding: utf-8 -*-
# copyright 2013 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

"""cubicweb-vcwiki predicates' tests"""

from logilab.common.registry import NoSelectableObject

from cubes.vcwiki.hooks import RefreshVCWikiRepoService
from utils import VCWikiTC


class PredicateTC(VCWikiTC):

    def setUp(self):
        super(PredicateTC, self).setUp()
        with self.admin_access.repo_cnx() as cnx:
            self.clients_eid = cnx.create_entity('CWGroup', name=u'clients').eid
            self.create_user(cnx, 'toto', groups=('users', 'clients'))
            cnx.commit()
    
    def test_refresh_selection_no_permission(self):
        with self.new_access('toto').repo_cnx() as cnx:
            with self.assertRaises(NoSelectableObject):
                cnx.vreg['services'].select(
                    'refresh_repository', cnx, eids=[self.repoeid])

    def test_refresh_selection_with_permission(self):
        with self.admin_access.repo_cnx() as cnx:
            perm = cnx.create_entity('CWPermission', name=u'write',
                              label=u'write perm',
                              require_group=self.clients_eid,
                              reverse_require_permission=self.repoeid,
                              )
            cnx.commit()
        with self.new_access('toto').repo_cnx() as cnx:
            self.assertIsInstance(
                cnx.vreg['services'].select(
                    'refresh_repository', cnx, eids=[self.repoeid]),
                RefreshVCWikiRepoService,
                )

            
if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
