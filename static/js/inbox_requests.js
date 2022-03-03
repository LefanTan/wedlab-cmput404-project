const form = document.querySelector("form");

const requestObj = JSON.parse(document.getElementById("followrequest").textContent);

const handleSubmit = (e) => {
    e.preventDefault();
    let formData = new FormData(form);

    let xhr = new XMLHttpRequest();
      xhr.open("GET", `../../service/${requestObj.id}/getfollowerequest/`, true);
      xhr.onload = function (e) {
          if (xhr.readyState === 4) {
            if (xhr.status === 200) {history.back();} else {console.error(xhr.statusText);}
          }
      }
}