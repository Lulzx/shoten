from libgen_api import LibgenSearch
s = LibgenSearch()
title = "da vinci"
filters = {
"Extension"	: "pdf"
}
print(  s.search_title_filtered(title, filters))