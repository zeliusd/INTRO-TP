const params = new URLSearchParams(window.location.search);
const user_id = params.get('id');

function handle_response(response) {
  if (response.message === "User updated successfully") {
    alert(response.message);
    window.location.href = '/users'
  }
  console.log(response);

}
function response(response) {
  console.log(response);
  return response.json();
}

function parse_data(user) {
  if (user.message) {
    window.location.href = '/users'
  }
  const reviews = document.getElementById('reviews');
  const username = document.getElementById('username');
  reviews.innerHTML = "Reviews: " + user.cant_reviews;
  username.value = user.username;

}

function request_error(error) {
  console.log(error);
}

fetch(`http://localhost:5000/users/${user_id}`).then(response).then(parse_data).catch(request_error);

function edit_user(event) {
  event.preventDefault()
  const formData = new FormData(event.target);

  const username = formData.get("username");
  if (username.length === 0) {
    alert("Username can't be empty");
    return;
  }
  fetch(`http://localhost:5000/users/${user_id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username }),
  }).then(response).then(handle_response).catch(request_error);
}


