function confirmRequest() {
    const sum = document.querySelector(".summary")
    sum.style.color = "blue";
}

function rejectRequest() {
    const sum = document.querySelector(".summary")
    sum.style.color = "red";
}

const form = document.querySelector("form");

const authorObj = JSON.parse(document.getElementById("author").textContent);

function clearInbox() {
    let formData = new FormData(form);
    var xhr = new XMLHttpRequest();
    xhr.open("DELETE", `../../service/authors/${authorObj.id}/inbox`, true);
    xhr.onload = function () {
        if (xhr.readyState === 4 && xhr.status === "200") {
            history.back();
        } else {
            console.error(xhr.statusText);
        }
    }
    xhr.setRequestHeader("X-CSRFToken", formData.get("csrfmiddlewaretoken"));
    xhr.send(formData);
}

