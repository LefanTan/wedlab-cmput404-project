const form = document.querySelector("form");

const authorObj = JSON.parse(document.getElementById("author").textContent);

function clearInbox() {
    let formData = new FormData(form);
    var xhr = new XMLHttpRequest();
    xhr.open("DELETE", `../../service/authors/${authorObj.id}/inbox`);
    xhr.onload = function () {
        if (xhr.readyState === 4 && xhr.status === "200") {
            console.log('success delete')
        } else {
            console.log('not delete')
        }
    }
    xhr.setRequestHeader("X-CSRFToken", formData.get("csrfmiddlewaretoken"));
    xhr.send(formData);
}

