const params = new URLSearchParams(window.location.search);
const game_id = params.get("id");

function load_game(game) {
  const title = document.getElementById("title");
  const developer = document.getElementById("developer");
  const image = document.getElementById("image");
  image.setAttribute("src", game.image);
  console.log(game.image);
  developer.innerHTML = game.developer;
  title.innerHTML = game.name;
}

function response(response) {
  console.log(response);
  return response.json();
}

function parse_data(game) {
  load_game(game);
}

function request_error(error) {
  console.log(error);
}

fetch(`http://localhost:5000/games/${game_id}`).then(response).then(parse_data)
  .catch(
    request_error,
  );
