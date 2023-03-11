import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class RecommendationEngine:
    def __init__(self, ratings_file, movies_file):
        self.ratings_inp = pd.read_csv(ratings_file)
        self.movies = pd.read_csv(movies_file)
        self.ratings = pd.merge(self.movies, self.ratings_inp).drop(['genres', 'timestamp'], axis=1)
        self.user_ratings = pd.pivot_table(self.ratings, index='userId', columns='title', values='rating')
        self.user_ratings = self.user_ratings.dropna(thresh=10, axis=1).fillna(0)
        self.item_similarity = cosine_similarity(self.user_ratings.T)
        self.item_similarity_df = pd.DataFrame(self.item_similarity, index=self.user_ratings.columns,
                                               columns=self.user_ratings.columns)

    def get_similar_movies(self, movie_name, user_rating):
        similar_score = self.item_similarity_df[movie_name] * (user_rating - 2.5)
        similar_score = similar_score.sort_values(ascending=False)
        return similar_score

    def get_movies(self, user_ratings):
        similar_movies = pd.DataFrame()
        movie_names = []
        for movie, rating in user_ratings:
            movie_names.append(movie)
            arr = pd.Series(self.get_similar_movies(movie, rating))
            similar_movies = pd.concat([similar_movies, arr.to_frame().T], ignore_index=True, axis=0)

        recommendations = similar_movies.sum().sort_values(ascending=False).index.tolist()
        for i in range(5):
            while recommendations[i] in movie_names:
                del recommendations[i]

        return recommendations[:5]

    def get_top_movies(self, num_movies=5):
        movies_ratings = pd.merge(self.movies, self.ratings_inp).drop(['timestamp', 'movieId', 'userId'], axis=1)
        ratings_counts = movies_ratings.groupby(['title', 'genres']).count().sort_values(by='rating', ascending=False)
        top_movies = list(ratings_counts.index[:num_movies])

        return top_movies

