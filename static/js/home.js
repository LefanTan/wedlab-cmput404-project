const formList = document.getElementsByClassName("post");
console.log("formList", formList)

const authorObj = JSON.parse(document.getElementById("author").textContent);

const submitHandler = (e) => {
  const form = e.currentTarget;
  console.log("form", form)
  const id = form.id;

  e.preventDefault();
  let formData = new FormData(form);

  var request = new XMLHttpRequest();
  request.open("POST", `../../service/authors/${authorObj.id}/posts/${id}/comments`);
  request.onload = function (e) {
    if (request.readyState === 4) {
      if (request.status === 200) {
        location.reload();
        console.log(JSON.parse(request.responseText));
      } else {
        console.log("error: ", request.statusText);
        console.error(request.statusText);
      }
    }
  };
  request.send(formData);
};

for (let form of formList) {
  form.addEventListener("submit", submitHandler);
}