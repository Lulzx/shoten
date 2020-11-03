import time
import requests
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup

class LibgenSearch:
	
	def search_title(self, query):
		self.search_request = SearchRequest(query, search_type="title")
		return self.search_request.aggregate_request_data()

	def search_author(self, query):
		self.search_request = SearchRequest(query, search_type="author")
		return self.search_request.aggregate_request_data()

	def search_title_filtered(self, query, filters = {	"ID": "",
														"Author": "", 
														"Title": "", 
														"Publisher": "", 
														"Year": "",
														"Pages": "",
														"Language": "",
														"Size": "",
														"Extension": "", 
														"Mirror_1": "",
														"Mirror_2": "",
														"Mirror_3": "",
														"Mirror_4": "",
														"Mirror_5": "",
														"Edit": ""	
														}):
		self.search_request = SearchRequest(query, search_type="title")
		data = self.search_request.aggregate_request_data()
		
		filtered_data = data
		for f in filters:
			filtered_data = [d for d in filtered_data if d[f] in filters.values()]
		return filtered_data

	def search_author_filtered(self, query, filters = {	"ID": "",
														"Author": "", 
														"Title": "", 
														"Publisher": "", 
														"Year": "",
														"Pages": "",
														"Language": "",
														"Size": "",
														"Extension": "", 
														"Mirror_1": "",
														"Mirror_2": "",
														"Mirror_3": "",
														"Mirror_4": "",
														"Mirror_5": "",
														"Edit": ""	
														}):
		self.search_request = SearchRequest(query, search_type="author")
		data = self.search_request.aggregate_request_data()
		
		filtered_data = data
		for f in filters:
			filtered_data = [d for d in filtered_data if d[f] in filters.values()]
		return filtered_data
		
class SearchRequest:

	col_names = ["ID", "Author", "Title", "Publisher", "Year", "Pages", "Language", "Size", "Extension", 
			"Mirror_1", "Mirror_2", "Mirror_3", "Mirror_4", "Mirror_5", "Edit"]

	def __init__(self, query, search_type="title"):
		self.query = query
		self.search_type = search_type

	def strip_i_tag_from_soup(self, soup):
		subheadings = soup.find_all("i")
		for subheading in subheadings:
			subheading.decompose()

	def get_search_page(self):
		query_parsed = "%20".join(self.query.split(" "))
		search_url = ""
		if self.search_type.lower() == 'title':
			search_url = f'http://gen.lib.rus.ec/search.php?req={query_parsed}&column=title'
		elif self.search_type.lower() == 'author':
			search_url = f'http://gen.lib.rus.ec/search.php?req={query_parsed}&column=author'
		search_page = requests.get(search_url)
		return search_page

	def aggregate_request_data(self):
		search_page = self.get_search_page()
		soup = BeautifulSoup(search_page.text, 'lxml')
		self.strip_i_tag_from_soup(soup)
		information_table = soup.find_all('table')[2]
		raw_data = [
			[
				td.a['href'] if td.find('a') and td.find('a').has_attr("title") and td.find('a')["title"] != "" 
				else ''.join(td.stripped_strings)
				for td in row.find_all("td")
			]
			for row in information_table.find_all("tr")[1:] # Skip row 0 as it is the headings row
		]

		output_data = [ dict(zip(self.col_names, row))  for row in raw_data ]
		return output_data


s = LibgenSearch()


app = FastAPI()


@app.get("/")
async def root():
	return {"message": "Hello, World!"}


@app.get("/query/{query}")
async def read_item(query):
	start = time.time()
	title = query.lower()
	filters = {
		"Extension"	: "pdf"
	}
	result = str(s.search_title_filtered(title, filters)).replace("'", '"')
	end = time.time()
	time_elapsed = str(end - start)
	count = str(len(result))
	data = '{"time": ' + time_elapsed + ', "results": ' + result + ', "count": ' + count + '}'
	return Response(content=data, media_type="application/json")
