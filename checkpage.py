from pynma import PyNMA
from pprint import pprint
import hashpage
import os
import urllib2
import hashlib

url = "https://apps.utu.fi/wentti/laitossivut/MATLTS.html"
app_name = "Wentti update"
newhash_event = "Page has changed"
newhash_msg = "Go check the new results!"
nofile_event = "Hashfile missing"
nofile_msg = "Can't find last hash, go and check if the page has changed."
lasthash_file = "lasthash"
p = None

def hashpage(url):
	m = hashlib.sha256()
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	page = response.read()
	m.update(page)
	return m.hexdigest()

def notify(keys, app, event, msg, url):
	global p
	pkey = None
	
	p = PyNMA()
	if os.path.isfile("mydeveloperkey"):
		dkey = open("mydeveloperkey",'r').readline().strip()
		p.developerkey(dkey)

	p.addkey(keys)
	res = p.push(app, event, msg, url, batch_mode=False)
	pprint(res)

def get_apikey(keyfile):
	if os.path.isfile(keyfile):
		return [_f for _f in open(keyfile,'r').read().split("\n") if _f]

def checkhash():
	print "Checking changes for", url
	if os.path.isfile(lasthash_file):
		f = open(lasthash_file, "r")
		newhash = hashpage(url)
		oldhash = f.readline()
		f.close()
		print "Old hash", oldhash
		print "New hash", newhash
		if newhash != oldhash:
			f = open(lasthash_file, "w")
			notify(get_apikey('myapikey'), app_name, newhash_event, newhash_msg, url)
			f.write(newhash)
			f.close()
	else:
		notify(get_apikey('myapikey'), app_name, nofile_event, nofile_msg, url)
		f = open(lasthash_file, "w")
		f.write(hashpage(url))
		f.close()
    
if __name__ == "__main__":
	checkhash()