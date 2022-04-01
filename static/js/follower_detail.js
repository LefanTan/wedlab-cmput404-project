const form = document.querySelector("form");

const authorObj = JSON.parse(document.getElementById("author").textContent);

const handleSubmit = (e) => {
  e.preventDefault();
  let formData = new FormData(form);

  let xhr = new XMLHttpRequest();
  xhr.open("POST", `../../service/authors/${authorObj.id}`, true);
  xhr.onload = function (e) {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        //console.log(JSON.parse(xhr.responseText));
        history.back();
      } else {
        console.log("error: ", xhr.statusText);
        console.error(xhr.statusText);
        history.back();
      }
    }
  };
  xhr.setRequestHeader("X-CSRFToken", formData.get('csrfmiddlewaretoken'))
  xhr.send(formData)
};

form.addEventListener("submit", handleSubmit);
