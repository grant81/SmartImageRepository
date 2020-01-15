import json
from collections import defaultdict
from DB_controller import PostgresImageDBController
import sys

# being used to populate the database using the COCO dataset annotation file,
# start by running python databaseLoadingFromCOCOAnnotation.py [path to annotation file]

postgres = PostgresImageDBController("imagedb", "searchservice", "admin", "localhost", 5432)


def main():
    json_file = sys.argv[1]
    if json_file is not None:
        with open(json_file, 'r') as COCO:
            js = json.loads(COCO.read())
            categories = {}
            for category in js["categories"]:
                categories[category["id"]] = category["name"]
            images = {}
            for image in js["images"]:
                images[image['id']] = image['flickr_url']
            taggedImages = defaultdict(set)
            for annotation in js['annotations']:
                taggedImages[annotation['image_id']].add(categories[annotation['category_id']])

            for image_id in taggedImages:
                url = images[image_id]
                tags = taggedImages[image_id]
                postgres.add_image_with_tags(url, tags)
    print('finished loading database from annotation file %s' % json_file)


if __name__ == "__main__":
    main()
