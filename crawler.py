"""
Some lingo used in the files:
- page: a requests.models.Response object
- soup: a bs4.BeautifulSoup object, the result of BeautifulSoup(page.content, 'html.parser')
"""

import urlparse

import requests
from bs4 import BeautifulSoup

import scanner
from library import BASE_URL, TARGET_URL, make_vul_dict, make_timestamped_dir, generate_json

ALL_RESULTS_OBJ = []

def aggregate_results():
	# Returns the nice JSON for submission
	aggregate = {}
	output = []
	# Aggregate the results_obj first
	for (vuln_class, results_obj) in ALL_RESULTS_OBJ:
		if vuln_class not in aggregate:
			aggregate[vuln_class] = []
		aggregate[vuln_class].extend(results_obj)
	# Make the final output
	for vuln_class, results_lst in aggregate.items():
		output.append(make_vul_dict(vuln_class, results_lst))
	# Write it to disk
	dirname = make_timestamped_dir('json')
	for dct in output:
		generate_json(dirname, dct)
	return output

def pass_to_scanner(link, soup):
	# Final implementation is to pass URL to scanner once a link is found. 
	# scanner.can returns a list of (vuln_class, result_obj)
	try:
		return scanner.scan(link, soup)
	except:
		return []

def create_full_link(href, url):
	return urlparse.urljoin(url, href)

def crawler(init_url):
	# FILO queue
	all_links = [init_url,]
	seen_links = {init_url}
	while all_links:
		url = all_links.pop()
		page = requests.get(url)
		soup = BeautifulSoup(page.content, 'html.parser')
		# Scan the current URL for vulnerabilities
		ALL_RESULTS_OBJ.extend(pass_to_scanner(url, soup))
		# Find more links from the current URL
		for a_element in soup.find_all('a', href=True):
			link = create_full_link(a_element['href'], url)
			if BASE_URL not in link:
				# Discard any links that are not in the scanning scope
				continue	
			if link and link not in seen_links:
				seen_links.add(link)
				if link not in all_links:
					all_links.append(link)

if __name__ == "__main__":
	crawler(TARGET_URL)
	print(aggregate_results())