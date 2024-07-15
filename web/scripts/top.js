
function card_header(game) {
  const card_header = document.createElement("div");
  card_header.setAttribute("class", "card-header");
  card_header.append(game.name);
  return card_header;
}
function image_col(image) {
  const image_col = document.createElement("div");
  image_col.setAttribute("class", "col-2");
  const img = document.createElement("img");
  img.setAttribute("class", "card-img-top");
  img.setAttribute("src", image);
  img.setAttribute("width", "100%");
  image_col.appendChild(img);
  return image_col;
}

function information(game) {
  const information_col = document.createElement("div");
  information_col.setAttribute("class", "col-8");

  const developer = document.createElement("p");
  developer.append("Developer: " + game.developer);
  information_col.appendChild(developer);
  if (game.price == 0) game.price = "Free";
  else game.price = game.price + "$";
  const price = document.createElement("p");
  price.append("Price: " + game.price);
  information_col.appendChild(price);

  return information_col;
}

function score_col(game) {
  const score_col = document.createElement("div");
  score_col.setAttribute("class", "col-2");
  const score = document.createElement("p");
  score.setAttribute("class", "text-center text-warning fw-bold");
  score.append("Average Stars: " + game.average_score);
  score_col.appendChild(score);
  return score_col;
}

function cardbody(game) {
  const card_body = document.createElement("div");
  card_body.setAttribute("class", "card-body row");
  card_body.append(image_col(game.image));
  card_body.append(information(game));
  card_body.append(score_col(game));
  return card_body;
}
function create_top_list(games) {
  const games_list = document.getElementById("games");
  for (const game of games) {
    const game_element = document.createElement("div");
    game_element.setAttribute(
      "class",
      "col-12",
    );

    const card = document.createElement("a");
    card.setAttribute("class", "card text-decoration-none")
    card.setAttribute("href", `/games?id=${game.id}`);

    card.append(card_header(game));
    card.append(cardbody(game));
    game_element.appendChild(card);
    games_list.appendChild(game_element);
  }
}

function response(response) {
  console.log(response);
  return response.json();
}

function parse_data(games) {
  create_top_list(games);
}

function request_error(error) {
  console.log(error);
  window.location.href = "/";
}

fetch("http://localhost:5000/games/top-rated").then(response).then(parse_data)
  .catch(
    request_error,
  );
