# Recommendation Systems with MovieLens User Rating Data.


Data Science cohort 062220

## Introduction

The global video streaming market size was valued at USD 42.6 billion in 2019 and is projected to grow at a compound annual growth rate (CAGR) of 20.4% from 2020 to 2027 (https://www.grandviewresearch.com/industry-analysis/video-streaming-market).
Innovations in artificial intelligence and Machine Learning are expected to improve video quality and personalized recommendations and aid in market growth.

Recommendation systems AKA recommendation engines are information filtering tools that predict ratings for user-product interactions in big data environments (think netflix, spotify, google etc). The broad purpose of this computational technique is to provide users with personalized recommendations to other products and assist with product engagement while driving conversions. In addition to the latter, movie recommendation systems provide a mechanism to assist data professionals and stakeholders in classifying users with similar interests. This makes them an essential part of websites and e-commerce applications and the marketing of user base demographics. 



## The Data & Context So Far...

Currently, I used the MovieLens small-dataset curated by the Grouplens research lab at the University of Minnesota. The content consists of approximately 100,000 ratings of a corpus of 9,000 movies with 3600 tags submitted by a 600-person user base. The dataset is distributed over four csv files which contain information on ratings, movies, links and tags.

**Ratings**

The ratings dataset is comprised of 100,836 observations which are records of the user id(userId), the id of the movie that was rated by said user (movieId) and the time at which the rating was recorded (timestamp).