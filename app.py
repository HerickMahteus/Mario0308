from flask import Flask, render_template, request
from recomendador import Recomendador

app = Flask(__name__)

recomendador = Recomendador()


@app.route("/")
def index():

    filmes = recomendador.movies.sort_values("title")

    return render_template(
        "index.html",
        filmes=filmes.to_dict("records")
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


if __name__ == "__main__":
    app.run(debug=True)