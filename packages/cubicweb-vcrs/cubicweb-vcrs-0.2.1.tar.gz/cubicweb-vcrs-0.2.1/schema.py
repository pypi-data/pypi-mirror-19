# copyright 2013-2014 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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
"""cubicweb-vcrs schema"""
from yams.buildobjs import EntityType, RelationDefinition, String, Int

_ = unicode

class RepositoryStats(EntityType):
    __permissions__ = {
        'read':   ('managers', 'users', 'guests',),
        'add':    (),
        'update': (),
        'delete': ('managers',),
    }
    url = String(indexed=True, required=True)
    nb_in_progress = Int(description=_('number of patches in the "in-progress" state'))
    nb_validating = Int(description=_('number of patches in the "pending-review" or "reviewed" state'))
    nb_closed = Int(description=_('number of patches in the "applied" state'))
    nb_rejected = Int(description=_('number of patches in the "rejected" or "deprecated" state'))
    nb_other = Int(description=_('number of patches in the "folded" or "outdated" state'))

class from_import(RelationDefinition):
    __permissions__ = {
        'read':   ('managers', 'users', 'guests',),
        'add':    (),
        'delete': (),
        }
    subject = 'RepositoryStats'
    object = 'CWDataImport'
    inlined = True
    cardinality = '?*'

# XXX project stats: nb open tickets (aka backlog size) / nb in-progress tickets

# this is necessary to let anon access to stats
from cubicweb.schemas import base as cubicweb
cubicweb.CWDataImport.__permissions__ = cubicweb.CWDataImport.__permissions__.copy()
cubicweb.CWDataImport.__permissions__['read'] += ('guests',)
cubicweb.cw_import_of.__permissions__ = cubicweb.cw_import_of.__permissions__.copy()
cubicweb.cw_import_of.__permissions__['read'] += ('guests',)
