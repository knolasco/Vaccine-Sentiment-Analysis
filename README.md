# Introduction

The purpose of this project is to analyze the sentiment for the Covid-19 Vaccine. The sentiment is found by analyzing tweets that mention "Vaccine". The tweets that are gathered range from 12/14/2020 to 12/22/2020. To visualize the sentiment, I created a dashboard using Dash.

# Description of Files
### Twitter Project: Gather Data

This file was created using google colab. Using tweepy's api, I gathered 8,696 tweets. Using textblob, I assigned a subjectivity and polarity score to each tweet. 

### Twitter Vaccine

This is a csv file that contains the tweets that I gathered and analyzed for this project. The columns include Dates, Tweets, Tweets without StopWords, Subjectivity score, Polarity score, and a Label (Positive, Negative, or Neutral).

### Sentiment_Dash

This is a .py file that creates the Dashboard using dash.

### Dashboard

This file contains a link that leads to the Dashboard that was created from Sentiment_Dash.
