import requests
class MALAnime:
    def __init__(self, token, api_version=1):
        self.token = token
        self.api_version = api_version
        self.ranking_types = ['all','airing','upcoming','tv','ova','movie','special','bypopularity','favorite']
        self.season_names = ['winter','spring','summer','fall']
    def get_anime_list(self, query, limit=100, offset=0):
        base_url = 'https://api.myanimelist.net/v%i/anime?q=%s&limit=%i' %(self.api_version, query, min(100, limit))
        if(offset>0):
            base_url = base_url + '&offset%i' % offset
        response = requests.get(base_url, headers = {
        'Authorization': 'Bearer %s' %self.token['access_token']
        })
        response.raise_for_status()
        print(response.json())
        response.close()
    
    def get_anime_ranking(self, ranking='all', limit=100, offset=0):
        base_url = 'https://api.myanimelist.net/v%i/anime/ranking?q=%s&limit=%i' %(self.api_version, ranking, min(500, limit))
        if(offset>0):
            base_url = base_url + '&offset%i' % offset
        response = requests.get(base_url, headers = {
        'Authorization': 'Bearer %s' %self.token['access_token']
        })
        response.raise_for_status()
        print(response.json())
        response.close()

    def get_anime_details(self, anime_id):
        base_url = 'https://api.myanimelist.net/v%i/anime/%i' %(self.api_version, anime_id)
        response = requests.get(base_url, headers = {
        'Authorization': 'Bearer %s' %self.token['access_token']
        })
        response.raise_for_status()
        print(response.json())
        response.close()
