const params2 = new URLSearchParams(window.location.search);
const game_id2 = params2.get('id');

function card_header(username, id) {
  const cardHeader = document.createElement('div');
  cardHeader.setAttribute('class', ' row card-header');

  const left_side = document.createElement('div');
  left_side.setAttribute('class', 'col-9 col-xl-8');

  const username_txt = document.createElement('h5');
  username_txt.setAttribute('class', 'card-title mt-1');
  username_txt.textContent = username;

  const container = document.createElement('div');
  container.setAttribute('class', 'row');


  const right_side = document.createElement('div');
  right_side.setAttribute('class', 'col-4 col-md-4 col-xl-4');
  const delete_btn = document.createElement('button');
  delete_btn.setAttribute('class', 'btn btn-danger col-12 col-lx-2 col-md-4 mt-auto ms-md-3 ms-lx-3');
  delete_btn.setAttribute('data-review-id', id);

  const edit_btn = document.createElement('a');
  edit_btn.setAttribute('class', 'btn btn-warning col-12 col-md-4 col-lx-2 ');
  edit_btn.setAttribute('data-review-id', id);
  edit_btn.setAttribute('href', '/games/edit?id=' + game_id2 + '&id_review=' + id);
  edit_btn.textContent = 'Edit';

  delete_btn.setAttribute('onclick', 'remove_review(event)');
  delete_btn.textContent = 'X';

  container.appendChild(edit_btn);
  container.appendChild(delete_btn);
  right_side.appendChild(container);
  left_side.appendChild(username_txt)

  cardHeader.appendChild(left_side);
  cardHeader.appendChild(right_side);
  return cardHeader;
}
function card_body(comment) {
  const cardBody = document.createElement('div');
  cardBody.setAttribute('class', 'card-body');

  const comment_txt = document.createElement('p');
  comment_txt.setAttribute('class', 'card-text');
  comment_txt.textContent = comment;
  cardBody.appendChild(comment_txt);

  return cardBody;
}

function stars(score) {
  let starts = ''
  for (let i = 0; i < score; i++) {
    starts += '☆';
  }
  return starts;
}
function card_footer(score) {
  const cardFooter = document.createElement('div');
  cardFooter.setAttribute('class', ' row card-footer');
  const score_txt = document.createElement('p');
  score_txt.setAttribute('class', 'card-text text-warning fw-bold');
  score_txt.textContent = 'Score: ' + stars(score)
  cardFooter.appendChild(score_txt);
  return cardFooter;
}

function load_reviews(reviews) {
  const reviewList = document.getElementById('reviews');
  for (const review of reviews) {

    const review_element = document.createElement('div');
    review_element.setAttribute('class', 'row mt-2 mb-2');
    const card = document.createElement('div');
    card.setAttribute('class', 'card');

    card.appendChild(card_header(review.username, review.review_id));
    card.appendChild(card_body(review.comment));
    card.appendChild(card_footer(review.score));

    review_element.appendChild(card);
    reviewList.appendChild(review_element);
  }
}


function handle_response(response) {
  console.log(response)
  window.location.href = '/games/?id=' + game_id2;
}
function response(response) {
  return response.json();
}

function parse_data(reviews) {
  load_reviews(reviews);
}

function request_error(error) {
  console.log(error);
}


function delete_response(data) {
  alert("Review removed successfully")
  window.location.href = "/games/?id=" + game_id2;
}
function remove_review(event) {
  event.preventDefault();
  const review_id = event.target.getAttribute('data-review-id');
  fetch(`http://localhost:5000/reviews/${review_id}`, {
    method: 'DELETE',
  }).then((res) => res.json()).then(delete_response).catch(request_error);
}
function create_review(event) {
  event.preventDefault();
  const formData = new FormData(event.target);
  const data = {
    username: formData.get('username'),
    comment: formData.get('comment'),
    appid: game_id2,
    score: formData.get('score'),
  };
  fetch(`http://localhost:5000/reviews`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  }).then((res) => res.json()).then(handle_response).catch(request_error);
}
fetch(`http://localhost:5000/games/${game_id2}/reviews`).then(response).then(parse_data).then(parse_data).catch(request_error);
