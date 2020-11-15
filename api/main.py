from base64 import b64encode
from re import sub
from time import time

import fastapi.middleware.cors
import requests
from audiobooker.scrappers.librivox import Librivox
from bs4 import BeautifulSoup as bs
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from requests_cache import install_cache

install_cache('book_cache')


class searchResult(BaseModel):
    time: str
    results: list
    count: str


class bookInfo(BaseModel):
    time: str
    title: str
    subtitle: str
    description: str
    year: str
    author: str
    image: str
    direct_url: str


class audiobookInfo(BaseModel):
    time: str
    title: str
    description: str
    authors: str
    url: str
    streams: list


col_names = ["ID", "Author", "Title", "Publisher", "Year", "Pages", "Language", "Size", "Extension",
             "Mirror_1", "Mirror_2", "Mirror_3", "Mirror_4", "Mirror_5", "Edit"]


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


def search(query, search_type="title", page=0):
    start = time()
    query = query.lower()
    query_parsed = "%20".join(query.split(" "))
    search_url = f"http://gen.lib.rus.ec/search.php?req={query_parsed}&column={search_type.lower()}&page={page}"
    search_page = requests.get(search_url)
    soup = bs(search_page.text, 'lxml')
    subheadings = soup.find_all("i")
    for subheading in subheadings:
        subheading.decompose()
    try:
        information_table = soup.find_all('table')[2]
    except IndexError:
        return ['0', [], '0']
    count = soup.find_all('font')[2].string.split('|')[0].split(' ')[0]
    raw_data = [
        [
            td.a['href'] if td.find('a') and td.find('a').has_attr("title") and td.find('a')["title"] != ""
            else ''.join(td.stripped_strings)
            for td in row.find_all("td")
        ]
        for row in information_table.find_all("tr")[1:]
    ]
    cols = ["id", "author", "title",
            "publisher", "year", "size", "extension", "download"]
    result = [dict(zip(cols, sanitize(row))) for row in raw_data]
    if not result:
        count = '0'
    end = time()
    time_elapsed = str(end - start)
    response = [time_elapsed, result, count]
    return response


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
        data = requests.get(url).json()
        if data['totalItems'] != 0:
            query = data['items'][0]['volumeInfo']['title']
            result = search(query, option, page)
    time_elapsed = str(result[0])
    count = str(result[2])
    result = result[1]
    data = dict(time=time_elapsed, results=result, count=count)
    data = jsonable_encoder(searchResult(**data))
    return JSONResponse(content=data)


@app.get("/book/{code}")
async def book_info(code):
    start = time()
    base_url = "http://library.lol"
    link = base_url + "/main/" + code
    markup = requests.get(link).text
    regex = '<[^<]+?>'
    soup = bs(markup, "lxml")
    try:
        image = base_url + soup.find("img")['src']
        response = requests.get(image).content
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
    end = time()
    time_elapsed = str(end - start)
    data = dict(time=time_elapsed, title=title, subtitle=subtitle, description=description, year=year, author=author,
                image=encoded_image_data, direct_url=direct_url)
    data = jsonable_encoder(bookInfo(**data))
    return JSONResponse(content=data)


@app.get("/vox/{query}")
async def read_item(query):
    start = time()
    book = Librivox.search_audiobooks(title=query)[0]
    end = time()
    time_elapsed = str(end - start)
    data = dict(time=time_elapsed, title=str(book.title), description=str(book.description),
                authors=str(book.authors[0]).split(',')[0], url=str(book.url), streams=book.streams)
    data = jsonable_encoder(audiobookInfo(**data))
    return JSONResponse(content=data)
