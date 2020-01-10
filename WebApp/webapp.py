import streamlit as st
import requests
import logging


def send_search_request(tags):
    url = "http://localhost:8889/search"
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
    url = 'http://localhost:8888/search'
    files = {'file': ("file", image, 'multipart/form-data', {'Expires': '0'})}
    with requests.Session() as s:
        r = s.post(url, files=files)
        print(r)
        return r.json()


def run():
    title = st.empty()
    image_display = st.empty()
    keywords = st.sidebar.text_input('Search by comma separated keywords')
    image_to_search = st.sidebar.file_uploader("Search by image", type=["png", 'jpg', 'jpeg'])
    image_to_save = st.sidebar.file_uploader("Upload by image",type=["png", 'jpg', 'jpeg'])
    if keywords:
        image_to_search = None
        keywords = keywords.split(',')
        results = send_search_request(keywords)
        results = results['urls']
        if results:
            title.title("showing results for keyword: {}".format(keywords))
            image_display.image(results)
        else:
            title.title("¯\_(ツ)_/¯")
            st.header('no result found for keyword: {}'.format(keywords))

    if image_to_search:
        results = send_search_image_request(image_to_search)
        results = results['urls']
        if results:
            title.title("showing results for uploaded image")
            image_display.image(results)
        else:
            title.title("¯\_(ツ)_/¯")
            st.header('no result found for the upload image')


if __name__ == '__main__':
    run()
