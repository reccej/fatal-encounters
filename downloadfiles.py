import csv
import subprocess
from urllib.parse import urlparse
from os import path

FILE='fatalencounters.csv'
IMAGEDIR='images'

with open(FILE) as fin, open('tried.dat', 'w') as fout:
  reader = csv.DictReader(fin)
  for row in reader:
    uid = row['Unique ID']
    url = row['URL of image of deceased']
    if url != '':
      parsed = urlparse(url)
      outfile = path.join(IMAGEDIR,uid+path.splitext(parsed.path)[1])
      if not path.exists(outfile):
        subprocess.run(['wget','-O',outfile,'--tries','3','--timeout','10','--waitretry','0',url])
        fout.write(outfile + ',' + url + '\n')
