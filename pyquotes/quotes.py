import requests
import random
from bs4 import BeautifulSoup

class Quoter:
	def __init__(self):
		self._website = "https://www.quoteload.com"

	def get_quotes(self, author=None, category=None):
		author = '' if author is None else author
		category = '' if category is None else category
		author = author.replace(' ', '-').lower()
		category = category.lower()

		# select quotes by author
		response = requests.get(self._website + '/quotes/authors/' + author).text
		soup_obj = BeautifulSoup(response, 'lxml')

		quotes = []
		for card in soup_obj.find_all("div", class_="card-body text-center"):
			quote = card.p.find("a", class_="href-noshow").text
			tag = card.p.find("a", class_="category-tag").text
			quotes.append((quote, author.lower(), tag.lower()))

		# select quotes by category
		response = requests.get(self._website + "/quotes/categories/" + category).text
		soup_obj = BeautifulSoup(response, "lxml")

		for card in soup_obj.find_all("div", class_="card-body text-center"):
			quote = card.p.find("a", class_="href-noshow").text
			tag = card.p.find("a", class_="category-tag").text
			person = card.p.find("a", class_="quote-author").text
			quotes.append((quote, person.lower(), tag.lower()))

		def filter_record(record):
			allowed = True if not author else record[1] == author
			allowed = allowed if not category else record[2] == category
			return allowed

		filtered_quotes = list(filter(filter_record, quotes))
		return random.choice(filtered_quotes)	


obj = Quoter()
print(obj.get_quotes(category='Age'))
