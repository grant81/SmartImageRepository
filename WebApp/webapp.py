import streamlit as st
import requests
import logging
from PIL import Image
import uuid
import os
import json

STORAGE_PATH = "ImageStore"
COMPONENT_ID_STORAGE = 'componentKeys.json'
SEARCH_SERVICE_HOST = os.environ['SEARCH_SERVICE_HOST']
TAG_SERVICE_HOST = os.environ['TAG_SERVICE_HOST']


def send_search_request(tags):
    url = "http://%s:8889/search" % SEARCH_SERVICE_HOST
    headers = {
        'Content-Type': "application/json",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "localhost:8889",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }
    data = {'tags': tags}
    response = requests.request("GET", url, json=data, headers=headers)
    if response.status_code > 300:
        logging.error("failed to get a response from search engine")
        return []
    return response.json()


def send_search_image_request(image):
    url = 'http://%s:8888/search' % TAG_SERVICE_HOST
    files = {'file': ("file", image, 'multipart/form-data', {'Expires': '0'})}
    with requests.Session() as s:
        r = s.post(url, files=files)
        return r.json()


def send_save_image_request(image, path):
    url = 'http://%s:8888/save' % TAG_SERVICE_HOST
    files = {'file': ("file", image, 'multipart/form-data', {'Expires': '0'}), 'url': (None, path)}
    with requests.Session() as s:
        r = s.post(url, files=files)
        return r.json()


def save_image(image_bytes, url):
    img = Image.open(image_bytes).convert("RGB")
    img.save(url, "JPEG")
    return url


def update_image_selector_id(ids, selector_name):
    ids[selector_name] = str(uuid.uuid1())
    with open(COMPONENT_ID_STORAGE, 'w') as f:
        json.dump(ids, f)


def handle_keyword_search(search_bar, title, image_display):
    search_query = search_bar.text_input('Search by comma separated keywords')
    if search_query:
        search_query = search_query.split(',')
        results = send_search_request(search_query)
        results = results['urls']
        if results:
            title.title("showing results for keyword: {}".format(search_query))
            image_display.image(results)
        else:
            title.title("¯\_(ツ)_/¯")
            st.header('no result found for keyword: {}'.format(search_query))


def handle_image_search(search_bar, title, image_display, ids):
    image_to_search = search_bar.file_uploader("Search by image", type=["png", 'jpg', 'jpeg'], key=ids["search_image"])
    if image_to_search:
        results = send_search_image_request(image_to_search)
        results = results['urls']
        if results:
            title.title("showing results for uploaded image")
            image_display.image(results)
        else:
            title.title("¯\_(ツ)_/¯")
            st.header('no result found for the upload image')
        ids["search_image"] = str(uuid.uuid1())
        update_image_selector_id(ids, "search_image")


def handle_image_save(search_bar, title, ids):
    image_to_save = search_bar.file_uploader("Upload by image", type=["png", 'jpg', 'jpeg'], key=ids["save_image"])
    if image_to_save:
        url = os.path.join(STORAGE_PATH, str(uuid.uuid1()) + ".jpg")
        result = send_save_image_request(image_to_save, url)
        save_image(image_to_save, url)
        title.title("Image Saved")
        st.header("with Tags:{}".format(result['tags']))
        st.header("at {}".format(url))
        update_image_selector_id(ids, "save_image")


def run():
    title = st.empty()
    image_display = st.empty()
    search_bar = st.sidebar.empty()
    selection = st.sidebar.radio("Choice Action", ('Keyword', 'Image Search', 'Save Image'))
    with open(COMPONENT_ID_STORAGE, 'r') as f:
        ids = json.loads(f.read())
    if selection == 'Keyword':
        handle_keyword_search(search_bar, title, image_display)
    elif selection == 'Image Search':
        handle_image_search(search_bar, title, image_display, ids)
    else:
        handle_image_save(search_bar, title, ids)


if __name__ == '__main__':
    run()
