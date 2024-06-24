let query = "http://localhost:5000/games/filter?";
const params = new URLSearchParams(window.location.search);
const game_name = params.get("name");
const category = params.get("category");
const developer = params.get("developer");

query += game_name ? `name=${game_name}&` : "";
query += category ? `category=${category}&` : "";
query += developer ? `developer=${developer}&` : "";

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

function response(response) {
  console.log(response);
  return response.json();
}

function parse_data(games) {
  create_games_list(games);
}

function request_error(error) {
  console.log(error);
}

fetch(query).then(response).then(parse_data).catch(
  request_error,
);
