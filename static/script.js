/* =====================================================
   CARROSSEL
===================================================== */

function scrollRow(button, direction) {

    const row = button.parentElement;

    const container =
        row.querySelector(".movie-container");

    const amount =
        container.clientWidth * 0.8;

    container.scrollBy({

        left: amount * direction,

        behavior: "smooth"

    });
}


/* =====================================================
   MODAL
===================================================== */

function mostrarDetalhes(title, genres) {

    const modal =
        document.getElementById("movieModal");

    const modalTitle =
        document.getElementById("modalTitle");

    const modalGenres =
        document.getElementById("modalGenres");


    modalTitle.textContent = title;

    modalGenres.textContent =
        "Gêneros: " + genres;


    modal.style.display = "flex";
}


function fecharDetalhes() {

    document.getElementById(
        "movieModal"
    ).style.display = "none";
}


/* =====================================================
   FECHAR MODAL CLICANDO FORA
===================================================== */

window.addEventListener(
    "click",
    function(event) {

        const modal =
            document.getElementById("movieModal");

        if (event.target === modal) {

            fecharDetalhes();

        }

    }
);


/* =====================================================
   PESQUISA DE FILMES
===================================================== */

const searchInput =
    document.getElementById("searchInput");

const searchResults =
    document.getElementById("searchResults");


let timeoutPesquisa;


searchInput.addEventListener(
    "input",
    function() {

        const termo =
            this.value.trim();


        clearTimeout(timeoutPesquisa);


        if (termo.length < 2) {

            searchResults.style.display =
                "none";

            searchResults.innerHTML = "";

            return;

        }


        timeoutPesquisa =
            setTimeout(
                function() {

                    fetch(
                        "/buscar?q=" +
                        encodeURIComponent(termo)
                    )

                    .then(response =>
                        response.json()
                    )

                    .then(filmes => {

                        searchResults.innerHTML =
                            "";


                        if (filmes.length === 0) {

                            searchResults.innerHTML =
                                `<div class="search-result">
                                    Nenhum filme encontrado.
                                </div>`;

                        }


                        filmes.forEach(
                            function(filme) {

                                const item =
                                    document.createElement(
                                        "a"
                                    );


                                item.className =
                                    "search-result";


                                item.href = "#";


                                item.textContent =
                                    filme.title;


                                item.addEventListener(
                                    "click",
                                    function(event) {

                                        event.preventDefault();

                                        selecionarFilme(
                                            filme.movieId
                                        );

                                    }
                                );


                                searchResults.appendChild(
                                    item
                                );

                            }
                        );


                        searchResults.style.display =
                            "block";

                    })

                    .catch(error => {

                        console.error(
                            "Erro na pesquisa:",
                            error
                        );

                    });

                },
                300
            );

    }
);


/* =====================================================
   SELECIONAR FILME DA PESQUISA
===================================================== */

function selecionarFilme(movieId) {

    const form =
        document.createElement("form");

    form.method = "POST";

    form.action = "/recomendar";


    const input =
        document.createElement("input");

    input.type = "hidden";

    input.name = "movie_id";

    input.value = movieId;


    form.appendChild(input);

    document.body.appendChild(form);

    form.submit();
}


/* =====================================================
   ESC
===================================================== */

document.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Escape") {

            fecharDetalhes();

            searchResults.style.display =
                "none";

        }

    }
);


/* =====================================================
   NAVBAR AO ROLAR
===================================================== */

window.addEventListener(
    "scroll",
    function() {

        const navbar =
            document.querySelector(".navbar");


        if (window.scrollY > 50) {

            navbar.style.background =
                "#141414";

        } else {

            navbar.style.background =
                "linear-gradient(to bottom, rgba(0,0,0,0.95), rgba(0,0,0,0.55))";

        }

    }
);