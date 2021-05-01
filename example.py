#Scrape for emails and phones
import sys
import tldextract
from contactscraper.controller import Controller

def call_scrapper(website_name, file_name, max_number_of_results):
    instance = Controller(starting_urls=[website_name],
                        scrape_numbers=False,
                        scrape_emails=True,
                        region="US",
                        max_results=max_number_of_results,
                        website_name=file_name)

    instance.scrape()


def print_output(file_name):
    #Print Results

    import json

    with open(f"{file_name}.json", 'r') as raw_output:
        data = raw_output.read()
        output = json.loads(data)

    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    website_name = sys.argv[1]
    if len(sys.argv) >= 3:
        file_name = sys.argv[2]
    else:
        file_name = "_".join(tldextract.extract(website_name)[1:])
    if len(sys.argv) >= 4:
        max_number_of_results = int(sys.argv[3])
    else:
        max_number_of_results = 20
    try:
        call_scrapper(website_name, file_name, max_number_of_results)
        print_output(file_name)
    except e:
        print(f"unable to fetch, exception ocurred {e}")