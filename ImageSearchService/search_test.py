import unittest
from searcher import Searcher
from DB_controller import PostgresImageDBController
import mock
class TestSearcher(unittest.TestCase):
    @mock.patch('search_test.PostgresImageDBController')
    def test_search_keywords(self, mock_PostgresImageDBController):
        dbConnection = PostgresImageDBController("imagedb", "test", "test", "localhost")
        searcher = Searcher(dbConnection)
        searcher.search_keywords(('person','cup','spoon'))
        dbConnection.search_tags.assert_called_with(('person','cup','spoon'))

    @mock.patch('search_test.PostgresImageDBController')
    def test_clean_inputs(self,mock_PostgresImageDBController):
        dbConnection = PostgresImageDBController("imagedb", "test", "test", "localhost")
        searcher = Searcher(dbConnection)
        cleaned = searcher._Searcher__clean_input(("horses","persan"))
        self.assertEqual(('horse','person'),cleaned,"keywords should be cleaned")

if __name__ == '__main__':
    unittest.main()