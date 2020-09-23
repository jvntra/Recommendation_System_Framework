# Recommendation Systems with MovieLens User Rating Data.


Data Science cohort 062220

## Introduction

The global video streaming market size was valued at USD 42.6 billion in 2019 and is projected to grow at a compound annual growth rate (CAGR) of 20.4% from 2020 to 2027 (https://www.grandviewresearch.com/industry-analysis/video-streaming-market).
Innovations in artificial intelligence and Machine Learning are expected to improve video quality and personalized recommendations and aid in market growth.

Recommendation systems AKA recommendation engines are information filtering tools that predict ratings for user-product interactions in big data environments (think netflix, spotify, google etc). The broad purpose of this computational technique is to provide users with personalized recommendations to other products and assist with product engagement while driving conversions. In addition to the latter, movie recommendation systems provide a mechanism to assist data professionals and stakeholders in classifying users with similar interests. This makes them an essential part of websites and e-commerce applications and the marketing of user base demographics. 


## The Data & Context So Far...

Currently, I used the MovieLens small-dataset curated by the Grouplens research lab at the University of Minnesota. The content consists of approximately 100,000 ratings of a corpus of 9,000 movies with 3600 tags submitted by a 600-person user base. The dataset is distributed over four csv files which contain information on ratings, movies, links and tags.


## Recommendation System Evaluation & Testing

Recommendation systems (RS's) are as much an art as they are science. A big part of this is that its tricky to measure how good they are. There is a certain aesthetic quality to the results they give you and its hard to say if your recommendations are good or not especially if you are developing the algorithms offline while only using historical data on user ratings like I am in this project.

### Testing a Recommendation system (caveat)

An RS is an machine learning system. You train your model with prior user behavior to make predictions about what users might like (by issuing predicted ratings to items they havent rated). In general, you can evaluate an RS just like any other machine learning system by:

	1.) Measuring your systems ability to predict how people rated things in the past by using the train-test-split method.
	2.) Prime the system using only training data, where it learns the relationships it needs between items and between users and predicting on unseen data or the test set.

Once trained you can ask it to make predictions about how a new user might rate some item they've never seen before. So you predict the rating a test user would give & compare it to the real answer. Over large groups of users, you can end with a meaningful number that tells you how good your RS is at recommending things, more specifically, recommending things people *already watched and rated*. By using these methods, all we can really do is predict how people rated movies they already saw which is not the point of an RS. *We want to recommend new things to people that they havent interacted with and will find interesting* This is fundamentally impossible offline. For offline methods we have to make due with approaches and evaluations like MAE and RMSE.


### Evaluation & Accuracy Metrics

*MAE:*

the average value of errors (predicted-actual) in rating predictions.

*RMSE:*

The square root of the squared error average.

This metric is particularly useful because it penalizes you more when youre rating prediction is way off from the actual.

#### A note about accuracy
Accuracy isn't really measuring what we want RS's to do. Users in a dynamic real-world situation couldn,t care less about what your system thinks you should've rated some movie they already saw and rated. Rating predictions themselves are really of limited value. Its less important that a RS thinks youll rate up three stars, whats important is what the RS thinks about the best movies for you to see are and thats a very different problem to solve. Overall what matters is what movies or product you put in front of users in a top-N recommender list and how users interact with those products when recommended.

xx include blurb about the netflix prize and how it set a precedent early on to use rmse as an evaluator that was later found to be not useful for online recommendersxx

*Hit Rate:*

You generate top N recommendations for all users in the test set. If one of the recommendations in a users top-N recommendations is something they actually rated, you consider that a hit. You manage to show the users something that they've found interesting enough to consume on their own already, so well consider that a success. 

xx put hit rate formula here xx

Just add all the hits in your top-n recs for every user in the test set and divide by all the users and thats the hit rate.

*Leave-one-out Cross Validation*
Hit Rate is easy enough to understand but measuring it is a bit tricky. We cant use the same train-test or cross validation approaches to measuring accuracy because we arent measuring the accuracy on individual ratings. We are measuring the accuracy of top-n lists for individual users. You could measure hit rate on top-n lists for individual users.

*Average Reciprocal Hit Rate (ARHR)*

A variation on hit rate is is ARHR. It's just like hit rate except it accounts where in the top-n lists your hits appear. So you end up getting more credit for successfully recommending an item in the top slot than in the bottom slot. This is a more user-focused metric since users tend to focus on the beginning of lists. The only difference between ARHR and Hit Rate is that instead of summing up number of hits over , the reciprocal rank of each hit is summed up.So if we successfully predict a recommendation in slot three, that only counts as 1/3. But a hit in slot one of our top n recommendations receives a full weight of 1.0. Whether this makes sense or not depends on how the recommendations are displayed. If a user has to scroll to see the lower items in a top-n lists, then it makes sense to penalize good recommendations that appear too low in the list where the user has to work to find them

xx put in ARHR formula here, adjust placement of table following relevant text. xx

|Rank|Reciprocal Rank|
|----|---------------|
|3|1/3|
|2|1/2|
|1|1|

*Cumulative Hit Rank (cHR)*

Another variation of hit rate is cHR. It means that we throw away hits of predicted ratings below some threshold. The idea is we shouldnt get credit for recommending items to a user that they wouldn't actually enjoy. In the example below, if we had a cutoff of 3 stars we throw away the hits for the second and fourth items in these test results and hour hit rate metric wouldnt count them at all.

|Hit Rank|Predicted Rating|
|--------|----------------|
|4|5.0|
|2|3.0|
|1|5.0|
|0|2.0|

*Rating Hit Rate*

Yet another way to look at hit rate is to break it down by predicted rating score. It can be a good way to get an idea of the distribution of how good your algorithm thinks recommended movies are that actually get a hit. Ideally you want to recommend movies that they actually liked. So breaking down the distribution gives you some sense of how well youre doing in more detail.

|Rating|Hit Rate|
|______|________|
|5.0|0.001|
|4.0|0.004|
|3.0|0.030|
|2.0|0.001|
|1.0|0.0005|

The world of recommender systems would probably look a bit different if Netflix awarded its prize on hit rate instead of rmse. It turns out that small improvements in rmse can lead to large improvements in hit rates, which is what really matters. But it also turns out that you can build RS's with great hit rates but with poor RMSE scores.