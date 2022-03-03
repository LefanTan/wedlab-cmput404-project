const form = document.querySelector("form");
const postObj = JSON.parse(document.getElementById("post").textContent);


const handleSubmit = (e) => {
    e.preventDefault();
    let formData = new FormData(form);

    let targetName = document.getElementById("targetName").value;
    formData.append("type", "post");
    formData.append("id", postObj.id);

    let request = new XMLHttpRequest();
    request.open("POST", `../../service/authors/${targetName}/inbox`, true);
    request.onload = function(e) {
        if (request.readyState === 4) {
            if (request.status === 200) {
                history.back();
            } else {
                console.log("error: ", request.statusText);
                console.error(request.statusText);

            }
        }
    };
    //request.setRequestHeader("X-CSRFToken", formData.get('csrfmiddlewaretoken'));
    request.send(formData);
};

form.addEventListener("submit", handleSubmit);