# Author: Jean-Paul (JP) Ventura

from surprise import AlgoBase
from surprise import PredictionImpossible
from MovieLens import MovieLens
import math
import numpy as np
import heapq

# Create contentKNN class using surprise libs AlgoBase class that contains fit, test, SVD, KNNBasic and other functions
# that can be inherited in other classes)

class ContentKNNAlgorithm(AlgoBase):

    def __init__(self, k=40, sim_options={}):
        AlgoBase.__init__(self)
        self.k = k

    def fit(self, trainset):
        AlgoBase.fit(self, trainset)

        '''
        Compute a 2d-array that is a lookup of the content based similarity score between any two movies.
        '''

        # Load up genre vectors for every movie
        ml = MovieLens()
        genres = ml.getGenres()
        years = ml.getYears()
        mes = ml.getMiseEnScene()
        
        print("Computing content-based similarity matrix...")
            
        # Compute genre distance for every movie combination as an empty 2x2 matrix.
        self.similarities = np.zeros((self.trainset.n_items, self.trainset.n_items))
        
        #  Apply algorithm to year and genre data.
        for thisRating in range(self.trainset.n_items):
            
            # Print progress of computation between movies in the training set.
            if (thisRating % 100 == 0):
                print(thisRating, " of ", self.trainset.n_items)
            for otherRating in range(thisRating+1, self.trainset.n_items):
                
                #Create raw item and raw user ids since that what the surprise predict function works with.
                thisMovieID = int(self.trainset.to_raw_iid(thisRating))
                otherMovieID = int(self.trainset.to_raw_iid(otherRating))
                
                #compute genre and year cosine similarity scores for every possible pair of movies.
                genreSimilarity = self.computeGenreSimilarity(thisMovieID, otherMovieID, genres)
                yearSimilarity = self.computeYearSimilarity(thisMovieID, otherMovieID, years)
                
                
                # Here I compute the genre-year similarities by multiplying them both together to generate a combined 
                # content based similarity score and enter the results into the lookup matrix for movie-to-movie genre-year 
                # similarity. I take advantage of matrix symmetry because the score of movie A and B is the same as B and 
                # A.
                
                self.similarities[thisRating, otherRating] = genreSimilarity * yearSimilarity
                self.similarities[otherRating, thisRating] = self.similarities[thisRating, otherRating]
                
        print("...done.")
                
        return self
    
    
    
    def computeGenreSimilarity(self, movie1, movie2, genres):
        '''
        This function computes genre-based similarity scores.
        '''
        
        genres1 = genres[movie1]
        genres2 = genres[movie2]
        sumxx, sumxy, sumyy = 0, 0, 0
        for i in range(len(genres1)):
            x = genres1[i]
            y = genres2[i]
            sumxx += x * x
            sumyy += y * y
            sumxy += x * y
        
        return sumxy/math.sqrt(sumxx*sumyy)
    
    
    
    def computeYearSimilarity(self, movie1, movie2, years):
        '''
        This function computes year based similarity using an exponential decay function to give more weight to movies
        released around the same time.
        '''
        
        diff = abs(years[movie1] - years[movie2])
        sim = math.exp(-diff / 10.0)
        return sim

    
  
    def estimate(self, u, i):
        '''
        Function that selects the K-nearest movies that a user has rated to the one a prediction is being made for based on 
        their genres and release years. A weighted average is then computed based on similarity scores and user ratings.
        
        '''
        
        if not (self.trainset.knows_user(u) and self.trainset.knows_item(i)):
            raise PredictionImpossible('User and/or item is unkown.')
        
        # Build up similarity scores between this item and everything the user rated
        neighbors = []
        for rating in self.trainset.ur[u]:
            genreSimilarity = self.similarities[i,rating[0]]
            neighbors.append( (genreSimilarity, rating[1]) )
        
        # Extract the top-K most-similar ratings
        k_neighbors = heapq.nlargest(self.k, neighbors, key=lambda t: t[0])
        
        # Compute average sim score of K neighbors weighted by user ratings
        simTotal = weightedSum = 0
        for (simScore, rating) in k_neighbors:
            if (simScore > 0):
                simTotal += simScore
                weightedSum += simScore * rating
            
        if (simTotal == 0):
            raise PredictionImpossible('No neighbors')

        predictedRating = weightedSum / simTotal

        return predictedRating
    