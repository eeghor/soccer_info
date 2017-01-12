import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import pprint
from collections import namedtuple, defaultdict
import wikipedia

# start from looking up the A-League Wikipedia page
aleague_wiki_url = wikipedia.page("A-League").url

# there's supposed to be a table with the current teams
page = requests.get(aleague_wiki_url)
soup = BeautifulSoup(page.content, 'html.parser')

team_table = soup.find("th", text=re.compile("Current\s*clubs")).parent.parent

for row in team_table.find_all("tr")[2:]:
	print(row.text)

# A-League team names; these will be used to search on Wikipedia so should be complete enough
aleague_teams = ["Sydney FC", "Adelaide United", "Brisbane Roar FC", "Melbourne City FC", "Newcastle Jets", "Central Coast Mariners",
"Melbourne Victory", "Perth Glory", "Wellington Phoenix", "Western Sydney Wanderers"]

team_lst = []
wikis = defaultdict(str)

# Wikipedia page URLs for the A-League teams

print("retrieving Wikipedia urls...")

for team in aleague_teams:
	wikis[team] = wikipedia.page(team).url
	print(wikis[team])

SoccerTeam = namedtuple('SoccerTeam', ["full_name", "nicknames", "short_name", "founded", "home_venue", "hv_capacity", "home_league"], verbose=False)

for t in wikis.keys():

	print("grabbing {} info...".format(t), end="")

	season_line = wikis[t]
	
	#headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
	
	page = requests.get(season_line)
	
	if page.status_code == 200:
		print("ok")
	else:
		print("error!")
		print("status code {}".format(page.status_code))
	
	# create a soup object
	soup = BeautifulSoup(page.content, 'html.parser')
	
	# find the infobox table
	info_table = soup.find("table", class_ = re.compile("infobox"))
	
	# find the top row
	top_row = info_table.find("th", {"scope": "row"}).parent
	
	# get the full name
	full_name = re.sub("\[\w*\]","",top_row.find("td").text) # remove all []
	
	# get the nickname
	nickname_row = top_row.next_sibling.next_sibling
	nick_name = nickname_row.find("td", {"class": "nickname"}).text
	
	# get the short name
	short_name_row = nickname_row.next_sibling.next_sibling
	short_name = short_name_row.find("td").text
	
	# get when founded
	founded_row = short_name_row.next_sibling.next_sibling
	founded = founded_row.find("td").text.split(";")[0].strip()  # only take wha's before ;
	
	# get home venue
	home_venue_row = founded_row.next_sibling.next_sibling
	home_venue = home_venue_row.find("td").text
	
	# get venue capacity
	capacity_row = home_venue_row.next_sibling.next_sibling
	venue_capacity = capacity_row.find("td").text
	
	# get home league
	home_league_row = capacity_row.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
	home_league = home_league_row.find("a").text
	
	
	team_lst.append(SoccerTeam(full_name=full_name, nicknames=nick_name, 
						short_name=short_name, founded=founded, 
						home_venue=home_venue, hv_capacity=venue_capacity, home_league=home_league))
print(team_lst)








