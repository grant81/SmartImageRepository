import pg8000
from sqls import *
import logging

log = logging.getLogger(__name__)


class PostgresImageDBController:
    def __init__(self, database, user, password, host, port=5432):
        self.__dbClient = pg8000.connect(database=database, user=user, password=password, host=host, port=port)

    def add_image_with_tags(self, image_url, tags):
        image_id = self.__insert_image(image_url)
        for tag in tags:
            self.__insert_tag(image_id, tag)

    def __insert_image(self, url):
        cursor = self.__dbClient.cursor()
        cursor.execute(INSERT_IMAGE % url)
        results = cursor.fetchall()
        self.__dbClient.commit()
        log.info("imageurl: %s with id: %d added to the DB" % (url, results[0][0]))
        return results[0][0]

    def __insert_tag(self, image_id, tag):
        cursor = self.__dbClient.cursor()
        cursor.execute(INSERT_IMAGE_TAG % (image_id, tag))
        self.__dbClient.commit()
        log.info("image with id: %d added tag: %s" % (image_id, tag))

    def search_tags(self, tags):
        tag_query = ''
        for i in range(len(tags)):
            if i != 0:
                tag_query += ' AND '
            tag_query += HAVING_ITEM % tags[i]
        cursor = self.__dbClient.cursor()
        cursor.execute(SELECT_IMAGE_URL_MULTIPLE_TAG % tag_query)
        results = cursor.fetchall()
        self.__dbClient.commit()
        out = [result[0] for result in results]
        return out


# if __name__ == '__main__':
#     postgres = PostgresImageDBController("imagedb", "searchservice", "admin", "localhost")
#     postgres.search_tags(('person', 'cup', 'spoon'))
