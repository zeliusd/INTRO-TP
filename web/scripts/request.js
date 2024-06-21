function create_games_list(games) {
  const games_list = document.getElementById("games");
  for (const game of games) {
    const game_element = document.createElement("li");
    game_element.innerText = game.name;
    games_list.appendChild(game_element);
  }
}
function response(response) {
  console.log(response);
  return response.json();
}

function parse_data(games) {
  console.log(games);
  create_games_list(games);
}

function request_error(error) {
  console.log(error);
}

fetch("http://localhost:5000/games").then(response).then(parse_data).catch(
  request_error,
);
