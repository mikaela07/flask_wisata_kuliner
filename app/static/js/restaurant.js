// Restaurant related functions

function toggleFavorite(restaurantId) {
  fetch(`/user/favorite/${restaurantId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === "success") {
        const favoriteBtn = document.querySelector(".favorite-btn");
        favoriteBtn.classList.toggle("active");

        // Update icon
        const icon = favoriteBtn.querySelector("i");
        if (icon.classList.contains("bi-heart")) {
          icon.classList.replace("bi-heart", "bi-heart-fill");
        } else {
          icon.classList.replace("bi-heart-fill", "bi-heart");
        }
      }
    })
    .catch((error) => console.error("Error:", error));
}

function submitReview() {
  const form = document.getElementById("reviewForm");
  const formData = new FormData(form);

  fetch(form.action, {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === "success") {
        location.reload();
      } else {
        alert(data.message);
      }
    })
    .catch((error) => console.error("Error:", error));
}
