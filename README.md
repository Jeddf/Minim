# MINIM
Live at https://minim.jedd.pw
###### WHAT words are most common? 
###### WHICH articles do they mainly appear in?! 
###### HOW many of the articles are they in?!?!
###### WHY is the BBC mostly writing "Mr"?!?!?!

#### Pulls from:
* BBC NEWS UK (http://feeds.bbci.co.uk/news/rss.xml?edition=uk)
* BBC NEWS US (http://feeds.bbci.co.uk/news/rss.xml?edition=us)
* VICE (http://vice.com/rss)
* VOX (http://vox.com/rss/index.xml)
* YOUR-FAVE-ONLINE-TEXT-OUTLET (http://www.asourceyouwroteaniftycrawlingscriptforandsubmittedapullrequestwith.heckyes)

#### To crawl for wordz (this will vary wildly depending on your environment)
* $git clone https://github.com/Jeddf/Minim.git
* $cd Minim/minimCrawler
* $pip3 install -r requirements.txt
* $python3 crawl.py --host <mysqlhost> --user <mysqluser> --password <mysqlpassword> --db <mysqldb>
#### ...and build index.html
* $cd ..
* $pip3 install -r requirements.txt
* $python3 Minim.py --host <mysqlhost> --user <mysqluser> --password <mysqlpassword> --db <mysqldb>

