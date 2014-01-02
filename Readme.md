Instagram Bot
-------------

A Python Bot to automate different actions on Instagram.

# Log in as a User.

To login to instagram, you'll need a username  and password. It creates a bot which has a logged in session.

```
from instagram_bot import InstgramWebBot

bot = InstgramWebBot()
bot.login(username='lazyme', password='thatsmysecret')

// do something with the 'bot' now.

```

# Create new api clients.

Creating a client requires a logged in bot, with a active developer account.

```
result = bot.create_api_client(app_name='awesomeapp', 
                             description='awesome description', 
                             website_url='http://awesomeness.com', # always put with http 
                             redirect_uri='http://awesomeness.com/callback/')
print result
```


## Installation

```
pip install https://github.com/theskumar/instagram_bot/archive/0.1.0.zip
```

Instgram Bot requires 'Phantomjs' as a dependencies. If you have [node](http://nodejs.org/) installed, you can install it with
```
npm -g install phantomjs
```

## License

MIT
