const form = document.querySelector("form");

const authorObj = JSON.parse(document.getElementById("author").textContent);
const followObj = JSON.parse(document.getElementById("follow").textContent);


console.log(nameObj);
if (!!window.performance && window.PerformanceNavigationTiming.type === 2) {
  window.location.reload();
}

const submitHandler = (e) => {
  e.preventDefault();
  let formData = new FormData(form);

  const categoriesButton = form.querySelectorAll("[data-value]");
  for (let button of categoriesButton) {
    formData.append("categories", button.getAttribute("data-value"));
  }

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
    }`
  );
  request.send(formData);
};

deleteButton?.addEventListener("click", deleteHandler);
form.addEventListener("submit", submitHandler);
