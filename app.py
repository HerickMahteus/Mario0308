from flask import Flask, render_template, request, jsonify
from recomendador import Recomendador

app = Flask(__name__)

recomendador = Recomendador()


@app.route("/")
def index():

    filmes = recomendador.movies.copy()

    destaque = filmes.sample(1).iloc[0].to_dict()

    avaliacoes = recomendador.ratings

    popularidade = (
        avaliacoes
        .groupby("movieId")
        .size()
        .reset_index(name="quantidade_avaliacoes")
    )

    populares = filmes.merge(
        popularidade,
        on="movieId",
        how="left"
    )

    populares["quantidade_avaliacoes"] = (
        populares["quantidade_avaliacoes"]
        .fillna(0)
    )

    populares = populares.sort_values(
        "quantidade_avaliacoes",
        ascending=False
    ).head(20)

    generos = [
        "Action",
        "Adventure",
        "Animation",
        "Comedy",
        "Crime",
        "Drama",
        "Fantasy",
        "Horror",
        "Romance",
        "Sci-Fi",
        "Thriller"
    ]

    filmes_por_genero = {}

    for genero in generos:

        filtrados = filmes[
            filmes["genres"].str.contains(
                genero,
                case=False,
                na=False
            )
        ].head(20)

        filmes_por_genero[genero] = (
            filtrados.to_dict("records")
        )

    recomendacoes = []

    try:

        filme_base = filmes.sample(1).iloc[0]

        recomendacoes = recomendador.recomendar(
            int(filme_base["movieId"]),
            20
        ).to_dict("records")

    except Exception:
        pass

    return render_template(
        "index.html",
        destaque=destaque,
        populares=populares.to_dict("records"),
        filmes_por_genero=filmes_por_genero,
        recomendacoes=recomendacoes
    )


@app.route("/recomendar", methods=["POST"])
def recomendar():

    movie_id = int(request.form["movie_id"])

    filme_selecionado = recomendador.movies[
        recomendador.movies["movieId"] == movie_id
    ]

    recomendacoes = recomendador.recomendar(
        movie_id,
        10
    )

    return render_template(
        "recomendacoes.html",
        filme=filme_selecionado.iloc[0].to_dict(),
        recomendacoes=recomendacoes.to_dict("records")
    )


@app.route("/buscar")
def buscar():

    termo = request.args.get("q", "").strip()

    if not termo:
        return jsonify([])

    filmes = recomendador.movies[
        recomendador.movies["title"]
        .str.contains(
            termo,
            case=False,
            na=False
        )
    ].head(10)

    return jsonify(
        filmes.to_dict("records")
    )


if __name__ == "__main__":
    app.run(debug=True)