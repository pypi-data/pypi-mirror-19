from __future__ import print_function

import time
import unittest
import httplib

from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections

from cubicweb.devtools import testlib
from cubicweb.cwconfig import CubicWebConfiguration
from cubicweb.predicates import is_instance

from cubes.elasticsearch.search_helpers import compose_search

from cubes.elasticsearch.es import CUSTOM_ATTRIBUTES
from cubes.elasticsearch.entities import IFullTextIndexSerializable

CUSTOM_ATTRIBUTES['Blog'] = ('title',)


class BlogFTIAdapter(IFullTextIndexSerializable):
    __select__ = (IFullTextIndexSerializable.__select__ &
                  is_instance('BlogEntry'))

    def update_parent_info(self, data, entity):
        data['parent'] = entity.entry_of[0].eid


class ParentsSearchTC(testlib.CubicWebTC):

    @classmethod
    def setUpClass(cls):
        try:
            httplib.HTTPConnection('localhost:9200').request('GET', '/')
        except:
            raise unittest.SkipTest('No ElasticSearch on localhost, skipping test')
        super(ParentsSearchTC, cls).setUpClass()

    def setup_database(self):
        super(ParentsSearchTC, self).setup_database()
        self.orig_config_for = CubicWebConfiguration.config_for
        config_for = lambda appid: self.config  # noqa
        CubicWebConfiguration.config_for = staticmethod(config_for)
        self.config['elasticsearch-locations'] = 'http://localhost:9200'
        # TODO unique ID to avoid collision
        self.config['index-name'] = 'unittest_index_name'
        # remove default connection if there's one
        try:
            connections.remove_connection('default')
        except KeyError:
            pass

    def test_parent_search(self):
        # self.vid_validators['esearch'] = lambda: None
        with self.admin_access.cnx() as cnx:
            with self.temporary_appobjects(BlogFTIAdapter):
                indexer = cnx.vreg['es'].select('indexer', cnx)
                indexer.get_connection()
                indexer.create_index(custom_settings={
                    'mappings': {
                        'BlogEntry': {'_parent': {"type": "Blog"}},
                    }
                })
                test_structure = {
                    u'A': [u'Paris ceci', u'Nantes', u'Toulouse'],
                    u'B': [u'Paris cela'],
                    u'C': [u'Paris autre', u'Paris plage'],
                }
                for fa_title, facomp_contents in test_structure.items():
                    blog = cnx.create_entity('Blog',
                                             title=fa_title)
                    for facomp_content in facomp_contents:
                        cnx.create_entity('BlogEntry',
                                          entry_of=blog,
                                          title=facomp_content,
                                          content=facomp_content)
                cnx.commit()
            time.sleep(2)  # TODO find a way to have synchronous operations in unittests
            for query, number_of_results, first_result in (("Paris", 3, "C"),
                                                           ("Nantes", 1, "A")):
                search = compose_search(Search(index=self.config['index-name'],
                                               doc_type='Blog'),
                                        query,
                                        parents_for="BlogEntry",
                                        fields=['_all'],
                                        fuzzy=True)
                self.assertEquals(len(search.execute()), number_of_results)
                self.assertEquals(search.execute().to_dict()['hits']['hits'][0]['_source']['title'],
                                  first_result)

    def tearDown(self):
        with self.admin_access.cnx() as cnx:
            indexer = cnx.vreg['es'].select('indexer', cnx)
            es = indexer.get_connection()
            es.indices.delete(self.config['index-name'])
        super(ParentsSearchTC, self).tearDown()

if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
