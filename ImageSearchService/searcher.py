from functools import lru_cache
import logging
from spellchecker import SpellChecker
from nltk.stem import WordNetLemmatizer
import nltk

nltk.download('wordnet')


class Searcher:
    def __init__(self, dbConnection):
        self.db = dbConnection
        self.spell_checker = SpellChecker()
        self.lemmatizer = WordNetLemmatizer()

    def search_keywords(self, keywords):
        keywords = self.__clean_input(keywords)
        logging.info("searching for tags: {}".format(keywords))
        return self.__check_keywords(keywords)

    def __clean_input(self, keywords):
        keywords = [self.spell_checker.correction(keyword.lower()) for keyword in keywords]
        keywords = tuple(self.lemmatizer.lemmatize(keyword) for keyword in keywords)
        return keywords

    @lru_cache(maxsize=200)
    def __check_keywords(self, keywords):
        result = self.db.search_tags(keywords)
        return result

# if __name__ == '__main__':
#     searcher = Searcher(PostgresImageDBController("imagedb","searchservice","admin","localhost"))
#     out = searcher.search_keywords(('person','cup','spoon'))
#
