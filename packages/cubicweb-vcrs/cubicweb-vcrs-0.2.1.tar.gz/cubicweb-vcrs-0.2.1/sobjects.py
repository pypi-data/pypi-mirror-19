# copyright 2013-2014 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of CubicWeb.
#
# CubicWeb is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# CubicWeb is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with CubicWeb.  If not, see <http://www.gnu.org/licenses/>.
"""datafeed parser to retreive statistical review information from a `vcreview`
based forge.
"""
import json
from datetime import datetime

from cubicweb.server.sources import datafeed


class VCReviewStatsParser(datafeed.DataFeedParser):
    """given the URL of a vcreview based forge, generate RepositoryStats
    entities for repositories stored there.
    """
    __regid__ = 'vcreview.stats'


    def process(self, url, raise_on_error=False):
        """IDataFeedParser main entry point"""
        rql = ('Any RU, PSN, COUNT(P) GROUPBY RU,PSN WHERE '
               'P in_state PS, PS name PSN, '
               'EXISTS(P patch_revision RE, RE from_repository R), '
               'R source_url RU, R cw_source S, S name "system"')
        if '?' in url:
            url += '&rql=%s&vid=jsonexport' % self._cw.url_quote(rql)
        else:
            url += '?rql=%s&vid=jsonexport' % self._cw.url_quote(rql)
        self.warning('fetching %s', url)
        try:
            stream = datafeed._OPENER.open(url, timeout=self.source.http_timeout)
            stream= stream.read()
            repo_infos = {}
            for repo_uri, patch_state, count in json.loads(stream):
                repo_infos.setdefault(repo_uri, {})[patch_state] = count
        except Exception as ex:
            if raise_on_error:
                raise
            self.import_log.record_error(unicode(ex))
            return True
        cd = datetime.utcnow() # we want all repository stats to have the same creation date
        unique_string = cd.strftime('%Y-%m-%d.%H:%M:%S')
        for repo_url, repo_info in repo_infos.iteritems():
            # we want to create a unique object for those statistics, generate a
            # unique URI
            repo_info['url'] = repo_url
            repo_info['creation_date'] = cd
            unique_uri = repo_url + unique_string
            self.extid2entity(unique_uri, 'RepositoryStats', info=repo_info,
                              from_import=self.import_log)

    def before_entity_copy(self, entity, sourceparams):
        """IDataFeedParser callback"""
        info = sourceparams['info']
        entity.cw_edited.update({
                'creation_date': info['creation_date'],
                'url': info['url'],
                'nb_in_progress': info.get('in-progress', 0),
                'nb_validating': info.get('pending-review', 0) + info.get('reviewed', 0),
                'nb_closed': info.get('applied', 0),
                'nb_rejected': info.get('rejected', 0) + info.get('deprecated', 0),
                'nb_other': info.get('folded', 0),
                'from_import': sourceparams['from_import'].eid,
                })
