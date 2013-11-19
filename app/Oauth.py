# OAuth.py
# Perform OAuth Dance


import tweepy

def main():
    #Perform OAuth 3-handshake dance:
    consumer_key = 'R5mPVxkjfMJ7JX9f1GTA'
    consumer_secret = 'PLdJKnLlBV1V5aYdJDLXpnVilqgGUkVguObVwPwze0'
    
    access_key = '1858157726-qx0FFQsIa7kb7RAVNM6eb6qBUNV6KvUpyLbmmtA'
    access_secret = 'VwWs2yYlTO3SfATao8m7TZxGuEQIZlXFJoGucrUOI8'
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    
    api = tweepy.API(auth)

    # Return auth'd api instance for SearchUser()
    return api,auth
    
if __name__=='__main__':
    main()
