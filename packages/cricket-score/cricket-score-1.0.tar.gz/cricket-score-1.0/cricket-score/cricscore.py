#!usr/bin/python

from bs4 import BeautifulSoup
import urllib2
import re

sc=[]
def scorecard(bat , ball):
	tup=[]
	#batting  I innings
	p=bat.findAll("tr")
	for x in p:
		k=x.findAll("th")
		#print k
		for xx in k:
			#appending for a complete list 
			tup.append(xx.get_text().strip())
		sc.append(tup)
		tup=[]
		k=x.findAll("td")[0:len(k)-1]
		for xx in k:
			tup.append(xx.get_text().strip())
		sc.append(tup)
		tup=[]
	sc.append([])
	#bowling  I innings
	#for heading part
	p=ball.find("tr")
	k=p.findAll("th")
	for xx in k:
		tup.append(xx.get_text().strip())
	
	#for  complete details
	sc.append(tup)
	tup=[]
	p=ball.findAll("tr")[1::2]
	for x in p:
		k=x.findAll("td")
		for xx in k:
			tup.append(xx.get_text().strip())
		sc.append(tup)
		tup=[]



def full_sc(url1):
	
	print "*** Full scorecard ***"
	
	content1 = urllib2.urlopen(url1).read()
	soup = BeautifulSoup(content1)
	bat_inn = soup.findAll("table", "batting-table innings")
	bowl_inn = soup.findAll("table", "bowling-table")
	
	for i in range(len(bat_inn)):
		scorecard(bat_inn[i], bowl_inn[i])
	#for print fromat
		sc.append(["*********************"])
	## printing the final scorecard
	for i in sc:
		print "\t".join(i)


def main():
	#url for the webpage for live matches
	url = "http://www.espncricinfo.com/ci/engine/match/index.html?view=live"
	content = urllib2.urlopen(url).read()
	soup = BeautifulSoup(content,"lxml")
	match_sec = soup.findAll("section", "default-match-block")

	#team to be searched 
	team = raw_input("Enter the name of team ")
	
	#flag for successful search
	flag=0
	for i in match_sec:
		In1= i.find("div", "innings-info-1")
		In2= i.find("div", "innings-info-2")
		status= i.find("div", "match-status")
		p = In1.find(text=re.compile(team , re.I ))
		q = In2.find(text=re.compile(team, re.I ) )
		if(p != None or q != None):
			print In1.get_text() , In2.get_text(), status.get_text()
			flag=1

			#for full scorecard
			fsc=raw_input("Do you want full score card? [Y/N]:  ")
			fsc=fsc.lower()
			if(fsc=='y'):
			
				#function for full scorecard display
				p =  i.find("div", "match-articles")
			
				#since the scorecard link tag is first tag in this div
				q = p.find("a")
				fs_link =  q['href']
				fs_link="http://www.espncricinfo.com" + fs_link + "?view=scorecard;wrappertype=none"
				full_sc(fs_link)		
			break	
		
	if(flag == 0):
		print "No Match for" , team



if __name__ == "__main__": main()
