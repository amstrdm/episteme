import requests

# We use an unofficial RapidAPI here

url = "https://seeking-alpha.p.rapidapi.com/analysis/v2/list"

querystring = {"id":"tsla","size":"5"}

headers = {
	"x-rapidapi-key": "cac0e77b10msha4a2c883a78b7b2p1f7de3jsn0bfbee434940",
	"x-rapidapi-host": "seeking-alpha.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())