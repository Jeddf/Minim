# MINIM.li

##### Minimise the web.
A Python crawler and frontend to minimise written content one site at a time.
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

#### To build locally (this will vary wildly depending on your environment)
* $git clone https://github.com/Jeddf/Minim.git
* $cd Minim
* $pip3 install -r requirements.txt
* $python3 minim.py # initiates DB as 'counts.db', crawls for data and saves the complete page in ./builds
