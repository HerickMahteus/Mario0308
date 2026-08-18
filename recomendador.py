import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Recomendador:

    def __init__(self):
        self.movies = pd.read_csv("data/movies.csv")

        self.movies["genres"] = self.movies["genres"].fillna("")

        self.vectorizer = TfidfVectorizer(
            analyzer="word",
            token_pattern=r"(?u)\b[\w-]+\b"
        )

        self.matriz_generos = self.vectorizer.fit_transform(
            self.movies["genres"]
        )

        self.similaridade = cosine_similarity(
            self.matriz_generos,
            self.matriz_generos
        )

    def recomendar(self, movie_id, quantidade=10):

        indices = self.movies[
            self.movies["movieId"] == movie_id
        ].index

        if len(indices) == 0:
            return pd.DataFrame()

        indice = indices[0]

        similaridades = list(
            enumerate(self.similaridade[indice])
        )

        similaridades = sorted(
            similaridades,
            key=lambda x: x[1],
            reverse=True
        )

        similares = similaridades[1:quantidade + 1]

        indices_filmes = [x[0] for x in similares]

        recomendacoes = self.movies.iloc[
            indices_filmes
        ].copy()

        recomendacoes["similaridade"] = [
            x[1] for x in similares
        ]

        return recomendacoes