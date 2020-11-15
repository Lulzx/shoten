import time
from base64 import b64encode
from dataclasses import asdict
from re import sub
from typing import List
from urllib.parse import urlencode

import fastapi.middleware.cors
import httpx
from audiobooker.scrappers.librivox import Librivox
from bs4 import BeautifulSoup as bs
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from pydantic import AnyUrl, BaseModel
from pydantic.dataclasses import dataclass


@dataclass
class LibGen:
    req: str
    column: str
    page: int


@dataclass
class GoogleBooks:
    q: str


@dataclass
class Result:
    id: int
    author: str
    title: str
    publisher: str
    year: str
    size: str
    extension: str
    download: AnyUrl


@dataclass
class SearchResult:
    time_elapsed: float
    results: list[Result]
    count: int


class BookInfo(BaseModel):
    time_elapsed: float
    title: str
    subtitle: str
    description: str
    year: str
    author: str
    image: str
    direct_url: AnyUrl


class AudiobookInfo(BaseModel):
    time_elapsed: float
    title: str
    description: str
    authors: str
    url: str
    streams: List[str]


def sanitize(row):
    indices = 5, 6
    row = [i for j, i in enumerate(row[:10]) if j not in indices]
    row = [p.replace("'", "'").replace('"', '"') for p in row]
    size = row[-3].split(" ")
    val = size[0]
    ext = size[1]
    if ext == "Kb":
        val = float(val) / 1024
        ext = "Mb"
    size = "{:.2f} {}".format(round(float(val), 2), ext).replace(".00", "")
    row[-3] = size
    return row


async def search(query: str = "", search_type: str = "title", page: int = 0):
    start = time.time()
    params = LibGen(req=query, column=search_type, page=page)
    query_string = urlencode(asdict(params), doseq=True)
    search_url = f"http://gen.lib.rus.ec/search.php?{query_string}"
    async with httpx.AsyncClient() as client:
        search_page = await client.get(search_url)
    soup = bs(search_page.text, "lxml")
    subheadings = soup.find_all("i")
    for subheading in subheadings:
        subheading.decompose()
    try:
        information_table = soup.find_all("table")[2]
        count = soup.find_all("font")[2].string.split("|")[0].split(" ")[0]
        raw_data = [
            [
                td.a["href"]
                if td.find("a")
                and td.find("a").has_attr("title")
                and td.find("a")["title"] != ""
                else "".join(td.stripped_strings)
                for td in row.find_all("td")
            ]
            for row in information_table.find_all("tr")[1:]
        ]
        cols = [
            "id",
            "author",
            "title",
            "publisher",
            "year",
            "size",
            "extension",
            "download",
        ]
        result = [dict(zip(cols, sanitize(row))) for row in raw_data]
    except:
        count = 0
        result = []
    end = time.time()
    time_elapsed = end - start
    response = dict(time_elapsed=time_elapsed, results=result, count=count)
    return response


app = FastAPI()

app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@cache()
async def get_cache():
    return True


@app.get("/")
@cache(expire=99)
async def root():
    return {"message": "Hello, World!"}


@app.get("/query/{search_type}/{query}/{page}", response_model=SearchResult)
@cache(expire=99)
async def book_search(search_type: str, query: str, page: int):
    result = await search(query, search_type, page)
    if not result["results"] and search_type == "title":
        params = GoogleBooks(q=query)
        query_string = urlencode(asdict(params), doseq=True)
        url = f"https://www.googleapis.com/books/v1/volumes?{query_string}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        data = response.json()
        if data["totalItems"] != 0:
            query = data["items"][0]["volumeInfo"]["title"]
            result = await search(query, search_type, page)
    return result


@app.get("/book/{code}", response_model=BookInfo)
@cache(expire=99)
async def book_info(code: str):
    start = time.time()
    regex: str = "<[^<]+?>"
    base_url = "http://library.lol"
    link = base_url + "/main/" + code
    client = httpx.AsyncClient()
    response = await client.get(link)
    markup = response.text
    soup = bs(markup, "lxml")
    try:
        image = base_url + soup.find("img")["src"]
        response = await client.get(image)
        encoded_image_data = "data:image/png;base64," + b64encode(
            response.content
        ).decode("utf-8")
        await client.aclose()
    except:
        encoded_image_data = "NO_IMAGE"
    try:
        direct_url = soup.select_one("a[href*=cloudflare]")["href"]
    except TypeError:
        direct_url = soup.select_one("a[href*=main]")["href"]
    heading = soup.find("h1").text.split(":")
    title = heading[0]
    subtitle = ""
    if len(heading) > 1:
        subtitle = heading[1].strip()
    try:
        author_prefix = "Author"
        author = str(soup.select_one("p:contains({})".format(author_prefix)))[14:]
        author = sub(regex, "", author)
    except:
        author = ""
    try:
        year = sub(
            regex,
            "",
            str(soup.select_one("p:contains(Publisher)"))
            .split(",")[1]
            .removeprefix(" Year: "),
        )
    except IndexError:
        year = ""
    try:
        description_prefix = "Description"
        description = (
            str(soup.select_one("div:contains({})".format(description_prefix)))
            .removeprefix("<div>" + description_prefix + ":<br/>")
            .removesuffix("</div>")
        )
        description = description.replace("<br />", "")
        description = sub(regex, "", description)
        description = " ".join(description.split())
        description = description.replace("'", "'").replace('"', "")
        description = description.replace("\n", "")
    except:
        description = ""
    end = time.time()
    time_elapsed = end - start
    result = dict(
        time_elapsed=time_elapsed,
        title=title,
        subtitle=subtitle,
        description=description,
        year=year,
        author=author,
        image=encoded_image_data,
        direct_url=direct_url,
    )
    return result


@app.get("/vox/{query}", response_model=AudiobookInfo)
@cache(expire=99)
async def audiobook_search(query: str):
    start = time.time()
    book = Librivox.search_audiobooks(title=query)[0]
    authors = str(book.authors[0]).split(",")[0]
    end = time.time()
    time_elapsed = end - start
    result = dict(
        time_elapsed=time_elapsed,
        title=book.title,
        description=book.description,
        authors=authors,
        url=book.url,
        streams=book.streams,
    )
    return result


@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
