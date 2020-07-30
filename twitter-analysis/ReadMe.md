## Reqirements

- Python 3.7.3 or higher

## Set Up

1. Install dependencies
```shell
pip install -r requirements.txt
```

 ## Knowledge
 - Twitter API gives us 450 requests per 15 Minutes and gives us a maximum of 100 tweets per request which makes 45000 tweets/15 minutes (https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets).
 -  With the standard/free Twitter API we are able to retrieve the Tweets of the last 7 days. We can not go further in the past (https://developer.twitter.com/en/docs/tweets/search/overview).
 - Tweets have very large identifiers (e.g. 1259491841898094592). The Cosmos DB somehow has difficulties with storing those accurately. Therefore you should work with the "id_str" and convert them to integers if you have to do numeric comparisons on identifiers


