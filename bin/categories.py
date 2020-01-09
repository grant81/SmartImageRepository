import json
cat_2014 = '../data/annotation/instances_val2014.json'

def main():
    json_file = cat_2014
    if json_file is not None:
        with open(json_file, 'r') as COCO:
            js = json.loads(COCO.read())
            js = js["categories"]
            out = {}
            for category in js:
                out[category["id"]] = category["name"]
            with open('categories.json', 'w') as outfile:
                json.dump(out, outfile)
            print('finish output categories')


if __name__ == "__main__":
    main()