## Reqirements

- Python 3.7.3 or higher

## Set Up

1. Install dependencies
```shell
pip install -r requirements.txt
```
2. Set values in config.py

3. Mark config.py as unchanged to prevent from accidetially pushing secret config to the remote repository
```shell
git update-index --assume-unchanged config.py
```
 ## Knowledge
 - Twitter API gives us 450 requests per 15 Minutes and gives us a maximum of 100 tweets per request which makes 45000 tweets/15 minutes (https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets).


