# Brand Equity Dilution Index (BEDI)
## Description

Many brands leverage brand extensions as a strategy for launching new products. The success or misery of brand extensions can lead to reinforcement or harm to the main brands equity which is referred to as brand equity dilution. In times of big data and social networks businesses have vast amounts of data available to monitor potential harms to their brand equity. Unfortunately brand equity is a phenomenon which is not very tangible as it describes the general public perception of a brand. Luckily, many people give insight about their perceptions and associations towards a particular brand on social media networks such as Twitter in real time. This research utilizes this opportunity and proposes an live index for anticipating brand equity dilution threat based on well established and extensively studied measures. Businesses which make use of brand extension as a strategy for the launch of new products can leverage the index to monitor the threat to brand equity dilution and act accordingly to it, which was before a black box. In particular this paper focuses on three german car manufacturers which are currently trying to make the leap from fuel based cars to electric vehicles which constitutes serious concerns for their brand equity if not managed well.

## Reqirements

- Python 3.7.3 or higher

## Set Up

1. Install dependencies
```shell
pip install -r requirements.txt
```

2. Setup a database and use credentials in config-file

3. Frequently run the data collection script (e.g. via cron job)

4. Frequently run scripts to calculate brand extension success factors

5. Frequently run script to calculate BEDI out of success factors

6. Install Web Gui on any type of Web Server (e.g. Apache2) and configure path to JSON Files with BEDI and successfactor values
