from django.db import models
from django.db import connection
from django.db.models import Avg, Max, Min, Count
from django.conf import settings

from pycsw.core import util
from geonode.catalogue.models import MetadataCatalogueCache


class SnimarRepository(object):
    __query_target = MetadataCatalogueCache

    def __init__(self, context, repo_filter=None):
        print '=' * 80
        print 'Initializing Snimar Repository handler class on Pycsw'
        print '...'

        self.context = context
        self.filter = repo_filter
        self.fts = False

        self.dbtype = settings.DATABASES['default']['ENGINE'].split('.')[-1]

        # generate core queryables db and obj bindings
        self.queryables = {}

        for tname in self.context.model['typenames']:
            for qname in self.context.model['typenames'][tname]['queryables']:
                self.queryables[qname] = {}

                for qkey, qvalue in \
                self.context.model['typenames'][tname]['queryables'][qname].items():
                    self.queryables[qname][qkey] = qvalue

        # flatten all queryables
        # TODO smarter way of doing this
        self.queryables['_all'] = {}
        for qbl in self.queryables:
            self.queryables['_all'].update(self.queryables[qbl])
        self.queryables['_all'].update(self.context.md_core_model['mappings'])

        print 'Initialization finished.'
        print '=' * 80

    def query_ids(self, ids):
        results = self._get_repo_filter(self.__query_target.objects).filter(identifier__in=ids).all()
        return self.map_cache_to_resources(results)

    def query_domain(self, domain, typenames, domainquerytype='list', count=False):
        return []

    def query_insert(self, direction='max'):
        return []

    def query_source(self, source):
        return []

    def query(self, constraint, sortby=None, typenames=None, maxrecords=10, startposition=0):
        if 'where' in constraint:
            query = self._get_repo_filter(self.__query_target.objects).extra(where=[constraint['where']], params=constraint['values'])
        else:
            query = self._get_repo_filter(self.__query_target.objects)

        total = query.count()

        # apply sorting, limit and offset
        if sortby is not None:
            if 'spatial' in sortby and sortby['spatial']:  # spatial sort
                desc = False
                if sortby['order'] == 'DESC':
                    desc = True
                query = query.all()
                return [str(total), sorted(query, key=lambda x: float(util.get_geometry_area(getattr(x, sortby['propertyname']))), reverse=desc)[startposition:startposition+int(maxrecords)]]
            else:
                if sortby['order'] == 'DESC':
                    pname = '-%s' % sortby['propertyname']
                else:
                    pname = sortby['propertyname']
                return [str(total), \
                query.order_by(pname)[startposition:startposition+int(maxrecords)]]
        else:  # no sort
            results = query.all()[startposition:startposition + int(maxrecords)]
            return [str(total), self.map_cache_to_resources(results)]

    def map_cache_to_resources(self, entries):
        """
        Returns a list of ResourceBase instances
        """
        def entry_to_resource_base(entry):
            return entry.resource

        return map(entry_to_resource_base, entries)

    def _get_repo_filter(self, query):
        return query
