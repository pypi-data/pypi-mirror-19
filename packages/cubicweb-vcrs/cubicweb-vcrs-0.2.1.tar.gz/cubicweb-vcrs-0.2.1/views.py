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
"""cubicweb-vcrs views/forms/actions/components for web ui"""

from collections import defaultdict

from cubicweb.predicates import nonempty_rset
from cubicweb.view import StartupView
from cubicweb.utils import JSString
from cubicweb.web import httpcache
from cubicweb.web.views import startup

from cubes.jqplot import views as jqplot

class IndexView(startup.IndexView):
    http_cache_manager = httpcache.NoHTTPCacheManager

    def call(self):
        self.w(u'<h1>%s</h1>' % u'Évolution des stocks')
        self.wview('vcrs.evolution.source')
        self.w(u'<h1>%s</h1>' % u'État des stocks')
        self.wview('vcrs.current.source')
        self.w(u'<p>%s</p>' % u'Les patches en attente de validation sont ceux dans l\'état "attente de relecture" ou "relu".')
        self.w(u'<h1>%s</h1>' % u'Top 10 patches en cours')
        rset = self._cw.execute(
             'Any RSU,S,RSIP ORDERBY RSIP DESC LIMIT 10 WHERE '
             'RS from_import DI, RS url RSU, RS nb_in_progress RSIP '
             'WITH DI,S BEING (Any MAX(X),S GROUPBY S WHERE X cw_import_of S, EXISTS(RS from_import X))')
        self.wview('table', rset)
        self.w(u'<h1>%s</h1>' % u'Top 10 patches en attente de validation')
        rset = self._cw.execute(
             'Any RSU,S,RSV ORDERBY RSV DESC LIMIT 10 WHERE '
             'RS from_import DI, RS url RSU, RS nb_validating RSV '
             'WITH DI,S BEING (Any MAX(X),S GROUPBY S WHERE X cw_import_of S, EXISTS(RS from_import X))')
        self.wview('table', rset)
        self.w(u'<h2>%s</h2>' % u'Date des derniers imports')
        rset = self._cw.execute('Any S,XST,XS WHERE X status XS, X start_timestamp XST, X identity SX '
                                'WITH S,SX BEING (Any S, MAX(X) GROUPBY S WHERE X cw_import_of S)')
        self.wview('table', rset)


class CurrentPerSourceStats(StartupView):
    """Display a bar graph using latest stats per source"""
    __regid__ = 'vcrs.current.source'

    def call(self):
        req = self._cw
        rset = req.execute(
            'Any S,SUM(RSIP),SUM(RSV) GROUPBY S WHERE '
            'RS identity X, RS url RSU, RS cw_source S, '
            'RS nb_in_progress RSIP, RS nb_validating RSV '
            'WITH X BEING (Any MAX(X) GROUPBY U WHERE X is RepositoryStats, X url U)')
        series = []
        series_options = []
        for source_eid, nbip, nbval in rset:
            series_options.append({'label': req.entity_from_eid(source_eid).name,
                                   'renderer': 'bar',
                                   })
            series.append([('in-progress', nbip), ('validating', nbval)])
        self.wview('jqplot.default', series=series,
                   width=400, series_options=series_options,
                   axes={'xaxis': {'renderer': 'category'}},
                   highlighter={'tooltipAxes': 'y'})


class EvolutionPerSourceStats(StartupView):
    """Display a bar graph using latest stats per source"""
    __regid__ = 'vcrs.evolution.source'

    def call(self):
        req = self._cw
        rset = req.execute(
            'Any S,RSCD,SUM(RSIP),SUM(RSV) GROUPBY S,RSCD ORDERBY RSCD WHERE '
            'RS url RSU, RS creation_date RSCD, RS cw_source S, '
            'RS nb_in_progress RSIP, RS nb_validating RSV')
        req.add_js('cubes.jqplot.ext.js')
        all_source_series = {}
        series_options = []
        for source_eid, date, nbip, nbval in rset:
            source_series = all_source_series.setdefault(source_eid, {'in-progress': [],
                                                                      'validating': []})
            source_series['in-progress'].append( (date, nbip) )
            source_series['validating'].append( (date, nbval) )
        series = []
        for source_eid, source_series in all_source_series.iteritems():
            source = req.entity_from_eid(source_eid).name
            series_options.append({'label': '%s %s' % (source, 'in-progress')})
            series.append(source_series['in-progress'])
            series_options.append({'label': '%s %s' % (source, 'validating')})
            series.append(source_series['validating'])
        self.wview('jqplot.default', series=series,
                   series_options=series_options,
                   axes={'xaxis': {'renderer': 'date',
                                   'tickOptions': {'angle': -30,
                                                   },
                                   },
                         },
                   )



def registration_callback(vreg):
    vreg.register_all(globals().values(), __name__, (IndexView,))
    vreg.register_and_replace(IndexView, startup.IndexView)
