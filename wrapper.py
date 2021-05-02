import sys
import example
import subprocess
import tldextract
from os import path
from time import time
file_name = sys.argv[1]
max_results = sys.argv[2]
start = time()
rows = []
with open(file_name, encoding='utf-8') as raw_output:
    data = raw_output.read()
    rows = data.split('\n')

procs = []
for row in rows:
    if ',' in row and ':' in row:
        cols = row.split(',')
        website_name = cols[1]
        file_name = "_".join(tldextract.extract(website_name)[1:])
        print(f"-------Scraping started: {website_name}------------")
        # example.call_scrapper(website_name, file_name)
        proc = subprocess.Popen(["python", "example.py", website_name, path.join('output', file_name), max_results])
        procs.append(proc)

for proc in procs:
    proc.communicate()

end = time()
print ('Finished in %.3F' % (end - start))
