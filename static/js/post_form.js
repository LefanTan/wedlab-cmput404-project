const form = document.querySelector("form");

const authorObj = JSON.parse(document.getElementById("author").textContent);

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
        console.log(JSON.parse(request.responseText));
        //  location.href = "/";
      } else {
        console.error(request.statusText);
      }
    }
  };
  request.open("POST", `../../service/authors/${authorObj.id}/posts`);
  request.send(formData);
};

form.addEventListener("submit", submitHandler);
