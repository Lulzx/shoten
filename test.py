from audiobooker.scrappers.librivox import Librivox

book = Librivox.search_audiobooks(title="Art of War")[0]

print(book.title)
print(book.description)
print(book.authors)
print(book.url)
print(book.streams)