import unittest
from searcher import Searcher
from DB_controller import PostgresImageDBController
import mock
import redis


# TODO:fix tests
class TestSearcher(unittest.TestCase):
    @mock.patch('search_test.PostgresImageDBController')
    @mock.patch('search_test.redis')
    def test_search_keywords(self, mock_PostgresImageDBController, mock_redis):
        dbConnection = PostgresImageDBController("imagedb", "test", "test", "localhost")
        redisConn = redis.StrictRedis()
        searcher = Searcher(dbConnection, redisConn)
        searcher.search_keywords(('person','cup','spoon'))
        dbConnection.search_tags.assert_called_with(('person','cup','spoon'))

    @mock.patch('search_test.PostgresImageDBController')
    def test_clean_inputs(self,mock_PostgresImageDBController):
        dbConnection = PostgresImageDBController("imagedb", "test", "test", "localhost")
        redisConn = redis.StrictRedis()
        searcher = Searcher(dbConnection, redisConn)
        cleaned = searcher._Searcher__clean_input(("horses","persan"))
        self.assertEqual(['horse', 'person'], cleaned, "keywords should be cleaned")

if __name__ == '__main__':
    unittest.main()