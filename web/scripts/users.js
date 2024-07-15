
function card_footer(user_id) {
  const cardfooter = document.createElement('div');
  cardfooter.setAttribute('class', ' row card-footer');

  const left_side = document.createElement('div');
  left_side.setAttribute('class', 'col-9 col-xl-12');

  const container = document.createElement('div');
  container.setAttribute('class', 'row');

  const delete_btn = document.createElement('button');
  delete_btn.setAttribute('class', 'btn btn-danger col-12 col-lx-2 col-md-4 mt-auto ms-md-3 ms-lx-3');
  delete_btn.setAttribute('data-user-id', user_id);

  const edit_btn = document.createElement('a');
  edit_btn.setAttribute('class', 'btn btn-warning col-12 col-md-4 col-lx-2 ');
  edit_btn.setAttribute('data-user-id', user_id);
  edit_btn.setAttribute('href', '/users/edit?id=' + user_id);
  edit_btn.textContent = 'Edit';

  delete_btn.setAttribute('onclick', 'remove_user(event)');
  delete_btn.textContent = 'X';

  container.appendChild(edit_btn);
  container.appendChild(delete_btn);
  left_side.appendChild(container);
  cardfooter.appendChild(left_side);
  return cardfooter;
}


function create_users_list(users) {
  const users_list = document.getElementById("users");
  for (const user of users) {
    const user_element = document.createElement("div");
    user_element.setAttribute(
      "class",
      "col-6 col-md-4 col-lg-3 col-xl-4 ",
    );

    const card = document.createElement("div");
    card.setAttribute("class", "card text-decoration-none");
    const cardheader = document.createElement("div");
    cardheader.setAttribute("class", "card-header");
    const user_text = document.createElement("span");
    user_text.setAttribute("class", "fw-bold");
    user_text.append(user.username);
    cardheader.append(user_text);

    const card_body = document.createElement("div");
    card_body.setAttribute("class", "card-body");
    card_body.append("Reviews: " + user.cant_reviews);
    card.append(cardheader);
    card.append(card_body);
    card.append(card_footer(user.id));
    user_element.appendChild(card);
    users_list.appendChild(user_element);
  }
}

function response(response) {
  console.log(response);
  return response.json();
}

function parse_data(users) {
  create_users_list(users);
}

function request_error(error) {
  console.log(error);
}

fetch("http://localhost:5000/users").then(response).then(parse_data)
  .catch(
    request_error,
  );

function delete_response(data) {
  alert("Review removed successfully")
  window.location.href = "/users";
}
function remove_user(event) {
  event.preventDefault();
  const user_id = event.target.getAttribute('data-user-id');
  fetch(`http://localhost:5000/users/${user_id}`, {
    method: 'DELETE',
  }).then((res) => res.json()).then(delete_response).catch(request_error);
}
