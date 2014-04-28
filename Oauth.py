# OAuth.py
# Perform OAuth Dance


import tweepy

def main():
    #Perform OAuth 3-handshake dance:
    consumer_key = 'qZnzpvBV2uwKiF2e4kR5mg'
    consumer_secret = 'E7ts8X242CfRKWBYMdTdXfwa3qyIHcEf2B76NUbQs'
    
    access_key = '1244598638-biVu1Hk4fiPMUTHO9HvYb09rXq7saMtNaevIt7S'
    access_secret = '75F3W2zKO0MsET6makez1sJVJKh9LpcgRefNQXLZWDg8M'
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    
    api = tweepy.API(auth)

    # Return auth'd api instance for SearchUser()
    return api,auth
    
if __name__=='__main__':
    main()
