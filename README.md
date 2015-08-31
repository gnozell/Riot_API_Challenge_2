# Yar Ha Har! - League of Legends API Challenge 2
------
Avast land lubber, here be my entry to the League of Legends API Challenge 2: Bilgewater category!

My submission is a python application that gathers all matches from the list provided by Riot Games and then parses the information to generate an SQL database that is used when serving templates of html files in a Flask web server.

By: Griffin Nozell (NA: DrSunshine)

# Live URL
------

[www.yarhahar.com](http://www.yarhahar.com)

Tested Browsers
* Google Chrome
* Firefox
* Internet Explorer

More details can be found in the "About" page

# Dependencies
------
* [Python 2.7](https://www.python.org/downloads/)
* [Riot Watcher](https://github.com/pseudonym117/Riot-Watcher)
* [Flask](http://flask.pocoo.org/)

# How to run
------
```python flaskapp.wsgi```

Done! You can test it by going to a web browser and going to http://localhost

This will use the provided yarhahar.db database file found in src/FlaskApp/ 

# Remake the yarhahar.db 
------

First make a file called ***api.key*** with your riot api key in it and drop it into the src/ folder.

To collect the information go to src/ and in the command line and type:

```python get_info.py```

This can take a ***LONG***  time with a development key. When get_info.py finishes downloading all the matches we can now parse it to remake the yarhahar.db:

```python parse_info.py```

Once parse_info.py finishes yarhahar.db will be ready to use for the Flask server.
