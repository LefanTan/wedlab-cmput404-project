const form = document.querySelector("form");
const authorObj = JSON.parse(document.getElementById("author").textContent);
const currAuthor = JSON.parse(document.getElementById("current").textContent);
const button = document.querySelector('input');
const paragraph = document.querySelector('p');

function follow() {
    let formData = new FormData(form);
    let xhr = new XMLHttpRequest();
    xhr.open("PUT", `../../service/authors/${currAuthor.id}/followers/${authorObj.id}`);
    xhr.onload = function (e) {
      if (xhr.readyState === 4) {
        if (xhr.status === 200) {
          //console.log(JSON.parse(xhr.responseText));
          history.back();
        } else {
          console.log("error: ", xhr.statusText);
          console.error(xhr.statusText);
        }
      }
    };
    xhr.setRequestHeader("X-CSRFToken", formData.get("csrfmiddlewaretoken"));
    xhr.send(formData);
}

function unfollow() {
    let formData = new FormData(form);
    let xhr = new XMLHttpRequest();
    xhr.open("DELETE", `../../service/authors/${currAuthor.id}/followers/${authorObj.id}`);
    xhr.onload = function (e) {
      if (xhr.readyState === 4) {
        if (xhr.status === 200) {
          //console.log(JSON.parse(xhr.responseText));
          history.back();
        } else {
          console.log("error: ", xhr.statusText);
          console.error(xhr.statusText);
          // history.back();
        }
      }
    };
    xhr.setRequestHeader("X-CSRFToken", formData.get("csrfmiddlewaretoken"));
    xhr.send(formData);
}
