function create_games_list(games) {
  const games_list = document.getElementById("games");
  for (const game of games) {
    const game_element = document.createElement("div");
    game_element.setAttribute(
      "class",
      "col-6 col-md-4 col-lg-3 col-xl-2 ",
    );

    const card = document.createElement("a");
    card.setAttribute("class", "card text-decoration-none");
    card.setAttribute("href", `/games?id=${game.id}`);
    const img = document.createElement("img");
    img.setAttribute("class", "card-img-top");
    img.setAttribute("src", game.image);
    img.setAttribute("width", "100%");

    const card_body = document.createElement("div");
    card_body.setAttribute("class", "card-body");
    card_body.append(game.name);
    card.append(card_body);
    card.append(img);
    game_element.appendChild(card);
    games_list.appendChild(game_element);
  }
}

function carousel(games) {
  for (i = 1; i <= 3; i++) {
    const image = document.getElementById(`image_${i}`);
    image.setAttribute("src", games[i + 55].image);
  }
}

function response(response) {
  console.log(response);
  return response.json();
}

function parse_data(games) {
  create_games_list(games);
  carousel(games);
}

function request_error(error) {
  console.log(error);
}

fetch("http://localhost:5000/games").then(response).then(parse_data).catch(
  request_error,
);
