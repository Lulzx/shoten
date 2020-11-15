from base64 import b64encode
from json import dumps
from re import sub
from time import time

import fastapi.middleware.cors
from audiobooker.scrappers.librivox import Librivox
from bs4 import BeautifulSoup as bs
from fastapi import FastAPI, Response
from requests import get
from requests_cache import install_cache

install_cache('book_cache')


def search(query, search_type="title", page=0):
    query = query.lower()
    start = time()
    search_request = SearchRequest(query, search_type, page)
    result = search_request.aggregate_request_data()
    end = time()
    time_elapsed = str(end - start)
    return [time_elapsed] + result


def strip_i_tag_from_soup(soup):
    subheadings = soup.find_all("i")
    for subheading in subheadings:
        subheading.decompose()


class SearchRequest:
    col_names = ["ID", "Author", "Title", "Publisher", "Year", "Pages", "Language", "Size", "Extension",
                 "Mirror_1", "Mirror_2", "Mirror_3", "Mirror_4", "Mirror_5", "Edit"]

    def __init__(self, query, search_type="title", page=0):
        self.query = query
        self.search_type = search_type
        self.page = page

    def get_search_page(self):
        query_parsed = "%20".join(self.query.split(" "))
        page = self.page
        search_url = "http://gen.lib.rus.ec/search.php?req={}&column={}&page={}".format(
            query_parsed, self.search_type.lower(), page)
        search_page = get(search_url)
        return search_page

    def aggregate_request_data(self):
        search_page = self.get_search_page()
        soup = bs(search_page.text, 'lxml')
        strip_i_tag_from_soup(soup)
        information_table = soup.find_all('table')[2]
        count = soup.find_all('font')[2].string.split('|')[0].split(' ')[0]
        raw_data = [
            [
                td.a['href'] if td.find('a') and td.find('a').has_attr("title") and td.find('a')["title"] != ""
                else ''.join(td.stripped_strings)
                for td in row.find_all("td")
            ]
            # Skip row 0 as it is the headings row
            for row in information_table.find_all("tr")[1:]
        ]
        cols = ["id", "author", "title",
                "publisher", "year", "size", "extension", "download"]
        result = [dict(zip(cols, self.sanitize(row))) for row in raw_data]
        if not result:
            count = '0'
        return [result, count]

    @staticmethod
    def sanitize(row):
        indices = 5, 6
        row = [i for j, i in enumerate(row[:10]) if j not in indices]
        row = [p.replace("'", "\'").replace('"', '\"') for p in row]
        size = row[-3].split(' ')
        val = size[0]
        ext = size[1]
        if ext == "Kb":
            val = float(val) / 1024
            ext = "Mb"
        size = "{:.2f} {}".format(round(float(val), 2), ext).replace(".00", "")
        row[-3] = size
        return row


def prepare(result):
    return dumps(result)


app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.get("/query/{option}/{query}/{page}")
async def read_item(option, query, page):
    result = search(query, option, page)
    if not result[1] and option == "title":
        url = "https://www.googleapis.com/books/v1/volumes?q=" + query
        data = get(url).json()
        if data['totalItems'] != 0:
            query = data['items'][0]['volumeInfo']['title']
            result = search(query, option, page)
    time_elapsed = str(result[0])
    count = str(result[2])
    result = result[1]
    data = prepare(dict(time=time_elapsed, results=result, count=count))
    return Response(content=data, media_type="application/json")


# noinspection PyBroadException
@app.get("/book/{code}")
async def book_info(code):
    base_url = "http://library.lol"
    link = base_url + "/main/" + code
    markup = get(link).text
    regex = '<[^<]+?>'
    soup = bs(markup, "lxml")
    try:
        image = base_url + soup.find("img")['src']
        response = get(image).content
        encoded_image_data = "data:image/png;base64," + \
                             b64encode(response).decode('utf-8')
    except:
        encoded_image_data = "NO_IMAGE"
    try:
        direct_url = soup.select_one("a[href*=cloudflare]")["href"]
    except TypeError:
        direct_url = soup.select_one("a[href*=main]")["href"]
    heading = soup.find("h1").text.split(":")
    title = heading[0]
    subtitle = " "
    if len(heading) > 1:
        subtitle = heading[1].strip()
    try:
        author_prefix = "Author"
        author = str(soup.select_one('p:contains({})'.format(
            author_prefix)))[14:]
        author = sub(regex, '', author)
    except:
        author = " "
    try:
        year = sub(regex, '', str(soup.select_one('p:contains(Publisher)')).split(",")[
            1].removeprefix(" Year: "))
    except IndexError:
        year = " "
    try:
        description_prefix = "Description"
        description = str(soup.select_one('div:contains({})'.format(
            description_prefix))).removeprefix("<div>" + description_prefix + ":<br/>").removesuffix("</div>")
        description = description.replace("<br />", "")
        description = sub(regex, '', description)
        description = ' '.join(description.split())
        description = description.replace("'", "\'").replace('"', '')
        description = description.replace('\n', '')
    except:
        description = " "
    data = prepare(dict(title=title, subtitle=subtitle, description=description, year=year, author=author,
                        image=encoded_image_data, direct_url=direct_url))
    return Response(content=data, media_type="application/json")


@app.get("/vox/{query}")
async def read_item(query):
    book = Librivox.search_audiobooks(title=query)[0]
    data = prepare(dict(title=str(book.title), description=str(book.description),
                        authors=str(book.authors[0]).split(',')[0], url=str(book.url), streams=book.streams))
    return Response(content=data, media_type="application/json")
