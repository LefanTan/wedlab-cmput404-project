const PostFormList = document.getElementsByClassName("post");
// console.log("PostFormList", PostFormList)
const CommentFormList = document.getElementsByClassName("comment");
// console.log("CommentFormList", CommentFormList)

const authorObj = JSON.parse(document.getElementById("author").textContent);

const submitHandler = (e) => {
  const form = e.currentTarget;
  const id = form.id;

  e.preventDefault();
  let form_data = new FormData(form);

  var request = new XMLHttpRequest();
  request.open("POST", `../../service/authors/${authorObj.id}/posts/${id}/comments`);
  request.onload = function (e) {
    if (request.readyState === 4) {
      if (request.status === 200) {
        location.reload();
        // console.log(JSON.parse(request.responseText));
      } else {
        console.log("error: ", request.statusText);
        console.error(request.statusText);
      }
    }
  };
  request.send(form_data);
};

for (let form of PostFormList) {
  form.addEventListener("submit", submitHandler);
}


const LikePostButtonHandler = (e) => {
  var target = e.target;
  var post_form = target.closest("form")

  e.preventDefault();
  let form_data = new FormData(post_form);
  const post_id = post_form.id;

  var request = new XMLHttpRequest();
  request.open("POST", `../../service/authors/${authorObj.id}/posts/${post_id}/likes`, true);
  request.onload = function (e) {
    if (request.readyState === 4) {
      if (request.status === 200) {
        location.reload();
      } else {
        console.log("error: ", request.statusText);
        console.error(request.statusText);
      }
    }
  };
  request.setRequestHeader("X-CSRFToken", form_data.get('csrfmiddlewaretoken'));
  request.send();
  //e.disabled = true;
};


const like_post_button = document.querySelectorAll('#like_post_button');
// console.log(like_post_button)

for (let element of like_post_button){
  element.addEventListener('mousedown', LikePostButtonHandler)
}


const LikeCommentButtonHandler = (e) => {
  var target = e.target;
  var comment_form = target.closest("form")
  var mid_parent1 = comment_form.parentElement;
  var mid_parent2 = mid_parent1.parentElement;
  var mid_parent3 = mid_parent2.parentElement;
  var mid_parent4 = mid_parent3.parentElement;
  var post_form = mid_parent4.closest("form");

  e.preventDefault();
  let form_data = new FormData(comment_form);
  const comment_id = comment_form.id;
  const post_id = post_form.id;

  var request = new XMLHttpRequest();
  request.open("POST", `../../service/authors/${authorObj.id}/posts/${post_id}/comments/${comment_id}/likes`, true);
  request.onload = function (e) {
    if (request.readyState === 4) {
      if (request.status === 200) {
        location.reload();
      } else {
        console.log("error: ", request.statusText);
        console.error(request.statusText);
      }
    }
  };
  request.setRequestHeader("X-CSRFToken", form_data.get('csrfmiddlewaretoken'));
  request.send();
};

const like_comment_button = document.querySelectorAll('#like_comment_button');
// console.log("like_comment_button", like_comment_button)

for (let element of like_comment_button){
  element.addEventListener('mousedown', LikeCommentButtonHandler)
}