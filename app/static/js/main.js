// Global JavaScript functions

// Flash message auto-dismiss
document.addEventListener("DOMContentLoaded", function () {
  // Auto dismiss flash messages after 3 seconds
  setTimeout(function () {
    let alerts = document.querySelectorAll(".alert");
    alerts.forEach(function (alert) {
      let bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    });
  }, 3000);
});

// Rating stars functionality
function initRatingStars() {
  const ratingInputs = document.querySelectorAll(".rating input");
  ratingInputs.forEach((input) => {
    input.addEventListener("change", function () {
      const rating = this.value;
      const stars = this.parentElement.querySelectorAll("label");
      stars.forEach((star) => {
        star.style.color = "#ddd";
      });
      for (let i = 0; i < rating; i++) {
        stars[4 - i].style.color = "#ffc107";
      }
    });
  });
}

// Image preview before upload
function previewImage(input) {
  if (input.files && input.files[0]) {
    const reader = new FileReader();
    reader.onload = function (e) {
      document.getElementById("imagePreview").src = e.target.result;
      document.getElementById("imagePreview").style.display = "block";
    };
    reader.readAsDataURL(input.files[0]);
  }
}
