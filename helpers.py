import random
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
import tweepy

# import 
from twitter_secrets import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET, BEARER_TOKEN


def scrape_dict(url):
    """Scrape player names and twitter handles into a dictionary."""

    # Use GET method to pull raw html from url
    html_content = requests.get(url).text

    # Initialize soup object to parse html
    soup = BeautifulSoup(html_content, "html.parser")

    # Get text-only list of players and twitter handles.
    raw_text = soup.find("div", { "id": "div_players" }).get_text()

    # Clean data and turn into list for processing. Chose to replace new lines with " - " to match site's style and make split work in one step
    text_list = raw_text.strip().replace("\n", " - ").rsplit(" - ")

    # Turn clean list into dictionary
    twitter_handles = {text_list[i]: text_list[i + 1] for i in range(0, len(text_list), 2)}

    # Remove deactivated accounts from dictionary (updated as found).
    deactivated_accts = ["Emilio Pagan"]
    for item in deactivated_accts:
        twitter_handles.pop(item)

    return twitter_handles


def scrape_active_player_birthdays(url):
    """Visit Baseball Reference and compile active players with birthdays on current date into a list."""

    # Use pandas to access table at url and turn into DataFrame
    table = pd.read_html(url, attrs={"id": "birthday_stats"})
    df = table[0]

    # Get list of players still active in current year
    current_year = datetime.now().year
    birthday_players = df["Name"][df["To"] == current_year].tolist()

    return birthday_players


def compose_tweet(player_list):
    """Compose tweet for later use by twitter API."""

    # List of birthday greetings to pull from.
    birthday_messages = ["Happy Birthday to ", "Hope you have a great birthday, ", "Wishing a fantastic birthday to ",
                         "Big HBD to ", "Wishing a happy birthday to ", "Completing another trip around the sun today: ", 
                         "Best birthday wishes to ", "Feliz cumpleaños to ", "Feliz cumple to ", "Let's raise a birthday toast to ",
                         "Today we're celebrating the birthday of ", "Wishing a joy-filled birthday to ", "Wishing a wonderful birthday to ",
                         "May all your wishes come true! Happy Birthday to ", "Wishing a very happy birthday to ",
                         "Enjoy the cake and presents! Happy Birthday ", "Let there be cake! Happy Birthday to ",
                         "Wishing an excellent birthday to ", "Happiest of birthdays to ", "Tonight the drinks are on someone else! HBD to ",
                         "Today's the birthday of ", "Born on this day: ", "Be blessed on your birthday, ", "Treat yourself! Happy birthday "
                         ]

    # Add '&' before last element in list.
    if len(player_list) > 1:
        player_list[-1] = "& " + player_list[-1]

    # Handle different amounts of birthday players.
    if len(player_list) > 2:
        tweet = random.choice(birthday_messages) + ", ".join(player_list) + "!"
    elif len(player_list) < 1:
        tweet = "There are no active MLB players with birthdays today."
    else:
        tweet = random.choice(birthday_messages) + " ".join(player_list) + "!"

    return tweet


def post_twitter(tweet):
    """Use Twitter API to post composed tweet."""

    # Bring in necessary API keys
    consumer_key = CONSUMER_KEY
    consumer_secret = CONSUMER_SECRET
    access_token = ACCESS_TOKEN
    access_secret = ACCESS_SECRET

    # Authenticate for access to Twitter API
    client = tweepy.Client(consumer_key=consumer_key, consumer_secret=consumer_secret, 
                           access_token=access_token, access_token_secret=access_secret
                          )

    # Post tweet
    response = client.create_tweet(text=tweet)

    # Confirm response
    print(f"https://twitter.com/MLBBirthdayBot/status/{response.data['id']}")

    return

def confirm_active_acct(account_name):
    """Check to see if Twitter account name is a valid user."""

    # Bring in necessary API key
    bearer_token = BEARER_TOKEN

    # Authenticate for access to Twitter API
    client = tweepy.Client(bearer_token)

    # Remove "@" from twitter handle for testing
    username = account_name.replace("@","")

    # Access Twitter user info via API
    response = client.get_user(username=username)

    # If data field of response is not null, return True
    try:
        response[0]["data"]
        return True
    except:
        return False