class NBAAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api-nba-v1.p.rapidapi.com"
        self.headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
        }