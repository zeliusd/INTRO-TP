
const params2 = new URLSearchParams(window.location.search);
const game_id2 = params2.get('id');
const review_id = params2.get('id_review');



function handle_response(response) {
  window.location.href = `/games/?id=${game_id2}`
}
function response(response) {
  return response.json();
}



function parse_data(reviews) {
  if (reviews.appid != game_id2)
    window.location.href = '/games/?id=' + game_id2;
  const comment = document.getElementById('comment');
  const score = document.getElementById('score');
  comment.value = reviews.comment;
  score.value = reviews.score;

}

function request_error(error) {
  console.log(error);
  window.location.href = '/games/?id=' + game_id2;
}

fetch(`http://localhost:5000/reviews/${review_id}`).then(response).then(parse_data).catch(request_error);


function edit_review(event) {
  event.preventDefault()
  const formData = new FormData(event.target);

  const comment = formData.get("comment");
  const score = formData.get("score");

  fetch(`http://localhost:5000/reviews/${review_id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ comment, score }),
  }).then(response).then(handle_response).catch(request_error);
}


