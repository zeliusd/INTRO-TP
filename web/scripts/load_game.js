const params = new URLSearchParams(window.location.search);
const game_id = params.get("id");

function load_game(game) {
  const web_title = document.getElementById("web-title");
  const title = document.getElementById("title");
  const developer = document.getElementById("developer");
  const image = document.getElementById("image");
  const about = document.getElementById("about");
  const price = document.getElementById("price");
  image.setAttribute("src", game.image);
  developer.innerHTML = game.developer;
  if (game.price === 0) price.innerHTML = "Price: Free"
  else price.innerHTML = "Price: " + game.price + "$";
  title.innerHTML = game.name;
  about.innerHTML = game.about;
  web_title.innerHTML = game.name;
}

function response(response) {
  if (response.status == 404) {
    window.location.href = "/";
  }
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
