#Scrape for emails and phones
import sys
import tldextract
website_name = sys.argv[1]

from contactscraper.controller import Controller
file_name = "_".join(tldextract.extract(website_name)[1:])
instance = Controller(starting_urls=[website_name],
                       scrape_numbers=False,
                       scrape_emails=True,
                       region="US",
                       max_results=50,
                       website_name=file_name)

instance.scrape()






#Print Results

import json

with open(f"{file_name}.json", 'r') as raw_output:
    data = raw_output.read()
    output = json.loads(data)

print(json.dumps(output, indent=2))

