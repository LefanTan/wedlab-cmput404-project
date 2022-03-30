const form = document.querySelector("form");
const deleteButton = document.getElementById("delete");

const authorObj = JSON.parse(document.getElementById("author").textContent);
const postObj = JSON.parse(document.getElementById("post").textContent);
const nameObj = JSON.parse(document.getElementById("name").textContent);
console.log(nameObj);
if (!!window.performance && window.PerformanceNavigationTiming.type == 2) {
  window.location.reload();
}

const submitHandler = (e) => {
  e.preventDefault();
  let formData = new FormData(form);

  const categoriesButton = form.querySelectorAll("[data-value]");
  for (let button of categoriesButton) {
    formData.append("categories", button.getAttribute("data-value"));
  }

  let type = formData.get("markdown") === "on" ? "text/markdown" : "text/plain";
  formData.append("contentType", type);

  var request = new XMLHttpRequest();
  request.onload = function (e) {
    if (request.readyState === 4) {
      if (request.status === 200) {
        // console.log(JSON.parse(request.responseText));

        history.back();
      } else {
        console.error(request.statusText);
      }
    }
  };

  request.open(
    "POST",
    `../../service/authors/${authorObj.id}/posts${
      nameObj === "home_post_edit" ? "/" + postObj.id : ""
    }/`
  );
  request.send(formData);
};

const deleteHandler = (e) => {
  let formData = new FormData(form);

  var request = new XMLHttpRequest();
  request.onload = function (e) {
    if (request.readyState === 4) {
      if (request.status === 200) {
        //console.log(JSON.parse(request.responseText));
        history.back();
      } else {
        console.error(request.statusText);
      }
    }
  };

  request.open(
    "DELETE",
    `../../service/authors/${authorObj.id}/posts/${postObj.id}`
  );

  request.setRequestHeader("X-CSRFToken", formData.get("csrfmiddlewaretoken"));
  request.send(formData);
};

deleteButton?.addEventListener("click", deleteHandler);
form.addEventListener("submit", submitHandler);
