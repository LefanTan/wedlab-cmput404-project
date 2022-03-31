// function confirmRequest() {
//     const sum = document.querySelector(".summary")
//     sum.style.color = "blue";
// }
//
// function rejectRequest() {
//     const sum = document.querySelector(".summary")
//     sum.style.color = "red";
// }
const form = document.querySelector("form");
const clearAction = document.getElementById("delete");

const authorObj = JSON.parse(document.getElementById("author").textContent);
const nameObj = JSON.parse(document.getElementById("name").textContent);

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

  request.open("DELETE", `../../service/authors/${authorObj.id}/inbox/`, true);

  request.setRequestHeader("X-CSRFToken", formData.get("csrfmiddlewaretoken"));
  request.send(formData);
};

clearAction?.addEventListener("click", deleteHandler);