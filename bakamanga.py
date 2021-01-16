import requests

class BakaManga:
    def search(search_str, page=1):
        base_url = 'https://www.mangaupdates.com/series.html?search=%s&output=json&page=%i' % (search_str,page)
        