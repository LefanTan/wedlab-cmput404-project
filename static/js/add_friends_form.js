const form = document.querySelector("form");

const followObj = JSON.parse(document.getElementById("followrequest").textContent);


const handleSubmit = (e) => {
  e.preventDefault();
  let formData = new FormData(form);

  let xhr = new XMLHttpRequest();
  xhr.open("POST", `../../add_friends`, true);
  xhr.onload = function (e) {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        //console.log(JSON.parse(xhr.responseText));
        history.back();
      } else {
        console.log("error: ", xhr.statusText);
        console.error(xhr.statusText);

        // Send error message to django
        location.href =
          location.href +
          "?error=The username is not exist, try again.";
      }
    }
  };
  xhr.send(formData);
};

form.addEventListener("submit", handleSubmit);
