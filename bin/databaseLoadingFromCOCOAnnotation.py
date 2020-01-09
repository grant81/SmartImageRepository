import json
from collections import defaultdict
from postgres.datalayer.DB_controller import PostgresImageDBController

postgres = PostgresImageDBController("imagedb","searchservice","admin","localhost")
cat_2014 = '../data/annotation/instances_val2014.json'

def main():
    json_file = cat_2014
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
                postgres.add_image_with_tags(url,tags)
    print('finished loading database from annotation file %s' % json_file)


if __name__ == "__main__":
    main()