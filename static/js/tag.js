const tagContainersArray = Array.from(
  document.getElementsByClassName("tag-container")
);

for (let tagContainer of tagContainersArray) {
  const input = tagContainer.querySelector('input[type="text"]');
  const tags = tagContainer.getElementsByClassName("tags-container")[0];

  const deleteItemHandler = (e) => {
    console.log(e.currentTarget);
    e.currentTarget.parentNode.removeChild(e.currentTarget);
  };

  const keyUpHandler = (e) => {
    if (e.key === "Enter" || e.keyCode === 13) {
      e.preventDefault();
      if (e.currentTarget.value === "") return;

      const newButton = document.createElement("button");
      newButton.addEventListener("click", deleteItemHandler);
      newButton.classList.add("tag");
      newButton.type = "button";
      newButton.setAttribute("data-value", e.currentTarget.value);

      const cancelIcon = document.createElement("i");
      cancelIcon.className = "fa-solid fa-x";

      newButton.appendChild(cancelIcon);
      newButton.appendChild(document.createTextNode(e.currentTarget.value));
      tags.appendChild(newButton);

      input.value = "";
    }
  };

  input.addEventListener("keydown", keyUpHandler);
}
