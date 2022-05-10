# Main code for twitter bot
from helpers import scrape_dict, scrape_active_player_birthdays, compose_tweet, post_twitter, confirm_active_acct

def main():

    # Get all known Twitter handles for MLB players from BREF.
    twitter_handles = scrape_dict("https://www.baseball-reference.com/friv/baseball-player-twitter-accounts.shtml")

    # Get names of active players with birthdays on current date from BREF.
    birthday_players = scrape_active_player_birthdays("https://www.baseball-reference.com/friv/birthdays.cgi")
    birthday_twitter_handles = {}

    # If player has known and active Twitter account, replace player's name with their twitter handle
    for key, value in twitter_handles.items():
        if key in birthday_players:
            birthday_twitter_handles[key] = value

    for player in birthday_players:
        if player in birthday_twitter_handles.keys():
            if confirm_active_acct(birthday_twitter_handles[player]) == True:
                birthday_players[birthday_players.index(player)] = birthday_twitter_handles[player]

    # Create string for use in Twitter API.
    tweet = compose_tweet(birthday_players)

    print(tweet)                                # Debug

    # Use Twitter API to post tweet.
    post_twitter(tweet)

if __name__ == "__main__":
    main()