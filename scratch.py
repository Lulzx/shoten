from libgen_api import LibgenSearch
s = LibgenSearch()

#fetch the value from http call "title"
title = "da vinci"
filters = {
"Extension"	: "pdf"
}
print(  s.search_title_filtered(title, filters))
