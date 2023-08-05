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

"""cubicweb-vcwiki specific hooks and operations"""

from cubicweb.server import Service
from cubicweb.predicates import objectify_predicate, match_user_groups
from cubes.vcsfile.hooks import RefreshRepoService



@objectify_predicate
def has_write_perm_on_vcwiki_repos(cls, req, rset=None, eids=None, **kwargs):
    """check all given eids in kwargs refer to a Repository of a VCWiki the
    current user can write to
    """
    if not eids:
        return 0
    for repo_eid in eids:
        rset_repo = req.execute('Any R WHERE R is Repository, R eid %(eid)s, '
                                'EXISTS(W content_repo R)',
                                 {'eid': repo_eid})
        if not rset_repo:
            return 0
        repo = rset_repo.one()
        if not req.user.has_permission('write', contexteid=repo.eid):
            return 0
    return 1


class RefreshVCWikiRepoService(RefreshRepoService):
    __select__ = (Service.__select__ & has_write_perm_on_vcwiki_repos()
                  & ~match_user_groups('managers'))
