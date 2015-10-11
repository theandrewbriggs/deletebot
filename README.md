# Delete All Tweets

The `delete_all.py` script can be run locally or uploaded to and run on Heroku. 

The process takes approximately one hour per 7000 tweets you want to delete. If you have many more than that, I recommend running it on Heroku, as your computer must be awake for the duration of the process while running locally.

If you want to set up an app that regularly deletes your old tweets (rather than manually deleting them from time to time), 

## Setup

- Request your Tweet Archive from Twitter. The request button should be near the bottom of your user settings page. (This can take anywhere from minutes to months. Twitter's kinda weird about archives.)
- Open Terminal.
- Install Git if you haven't from [here](https://git-scm.com) (it should be installed by default on OSX). To find out whether you have git installed, type `git --version` into your Terminal.
- Clone the Github repository to your machine: type `git clone https://github.com/theandrewbriggs/deletebot.git`
- Create a twitter app at [apps.twitter.com](https://apps.twitter.com). Add a name, description, website (it can just be something like "http://example.com"), and agree to the Developer Agreement.
- Create an access token on the "Keys and Access Tokens" tab.
- In a text editor ([Sublime Text](http://www.sublimetext.com/2) is great and sort-of free), copy and paste the consumer key, consumer secret, access token key, and access token secret into the appropriate spots in `credentials.py` file in the Deletebot project folder. (**N.B.** - Do not share these values with anyone or post them publicly anywhere on the internet, lest you want strangers fucking with your account.)
- Download your archive from Twitter. Copy and paste the `data` folder into the Deletebot project folder.
- If you want to keep tweets newer than a certain number of days or a given date, fill out either the `MAX_DAYS` or `MAX_DATE` variables near the top of the `delete_all.py` script.


## Local delete

- Install Pip, follow the directions [here](http://pip.readthedocs.org/en/stable/installing).
- In the Terminal, run `pip install tweepy`.
- From the project folder, type `python delete_all.py` and hit return. The script will output information about the delete process, and you must keep Terminal open and your computer on while this is going on (though you can let it run in the background while you do other stuff). 


## Heroku delete

- Create a free Heroku account at [heroku.com](http://www.heroku.com)
- Install the [Heroku Toolbelt](https://toolbelt.heroku.com).
- In Terminal, type `heroku login` and enter your Heroku account information.
- Again in Terminal, from your Deletebot project directory, type `heroku create` to start a new Heroku instance.
- Commit your local changes by typing
    > `git add .`
    > `git commit -m "Initialize deleter"`
- Type `git push heroku master`. This uploads your repository to Heroku.
- Type `heroku run worker1` to delete all your tweets. The script will output to your terminal, but you can close the terminal and the process will continue to run.


## Heroku app for continuous deleting

Instructions coming soon!