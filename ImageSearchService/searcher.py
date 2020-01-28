import logging
from spellchecker import SpellChecker
from nltk.stem import WordNetLemmatizer
import nltk

nltk.download('wordnet')


class Searcher:
    def __init__(self, dbConnection, redis_client):
        self.db = dbConnection
        self.spell_checker = SpellChecker()
        self.lemmatizer = WordNetLemmatizer()
        self.redis_client = redis_client

    def search_keywords(self, keywords):
        keywords = self.__clean_input(keywords)
        logging.info("searching for tags: {}".format(keywords))
        return self.__check_keywords(keywords)

    def __clean_input(self, keywords):
        keywords = [self.spell_checker.correction(keyword.lower()) for keyword in keywords]
        keywords = [self.lemmatizer.lemmatize(keyword) for keyword in keywords]
        keywords.sort()
        return keywords

    def __check_keywords(self, keywords):
        redis_key = str(keywords)
        result = self.redis_client.lrange(redis_key, 0, -1)
        if result:
            return result
        result = self.db.search_tags(keywords)
        self.redis_client.rpush(redis_key, *result)
        return result

# if __name__ == '__main__':
#     searcher = Searcher(PostgresImageDBController("imagedb","searchservice","admin","localhost"))
#     out = searcher.search_keywords(('person','cup','spoon'))
#
