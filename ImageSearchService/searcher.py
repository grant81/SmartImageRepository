from functools import lru_cache


class Searcher:
    def __init__(self, dbConnection):
        self.db = dbConnection

    def search_keywords(self, keywords):
        keywords = tuple(keywords)
        return self.__check_keywords(keywords)


    @lru_cache(maxsize=200)
    def __check_keywords(self, keywords):
        result = self.db.search_tags(keywords)
        return result

# if __name__ == '__main__':
#     searcher = Searcher(PostgresImageDBController("imagedb","searchservice","admin","localhost"))
#     out = searcher.search_keywords(('person','cup','spoon'))
