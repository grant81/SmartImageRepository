#TODO:handeling duplicate url
INSERT_IMAGE = "INSERT INTO image_info (image_url) VALUES ('%s') RETURNING image_id;"
INSERT_IMAGE_TAG = "INSERT INTO image_tag (image_id, tag) VALUES ('%d','%s');"
SELECT_IMAGE_URL_MULTIPLE_TAG = "SELECT ii.image_url from image_info ii join image_tag it on ii.image_id = it.image_id " \
                               "group by ii.image_url HAVING %s limit 100;"
HAVING_ITEM = "SUM(CASE WHEN it.tag = '%s' THEN 1 ELSE 0 END) > 0"