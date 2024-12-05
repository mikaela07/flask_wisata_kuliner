// Admin panel functions

function deleteRestaurant(restaurantId) {
  if (confirm("Are you sure you want to delete this restaurant?")) {
    fetch(`/admin/restaurant/${restaurantId}`, {
      method: "DELETE",
    }).then((response) => {
      if (response.ok) {
        location.reload();
      } else {
        alert("Error deleting restaurant");
      }
    });
  }
}

function deleteUser(userId) {
  if (confirm("Are you sure you want to delete this user?")) {
    fetch(`/admin/user/${userId}`, {
      method: "DELETE",
    }).then((response) => {
      if (response.ok) {
        location.reload();
      } else {
        alert("Error deleting user");
      }
    });
  }
}

function editRestaurant(restaurantId) {
  fetch(`/admin/restaurant/${restaurantId}`)
    .then((response) => response.json())
    .then((data) => {
      // Populate modal form
      document.getElementById("editName").value = data.name;
      document.getElementById("editDescription").value = data.description;
      document.getElementById("editAddress").value = data.address;
      document.getElementById("editCategory").value = data.category;

      // Set form action
      document.getElementById(
        "editRestaurantForm"
      ).action = `/admin/restaurant/${restaurantId}/edit`;

      // Show modal
      const modal = new bootstrap.Modal(
        document.getElementById("editRestaurantModal")
      );
      modal.show();
    });
}

// DataTable initialization
document.addEventListener("DOMContentLoaded", function () {
  if (document.getElementById("restaurantsTable")) {
    $("#restaurantsTable").DataTable({
      order: [[0, "asc"]],
      pageLength: 10,
      responsive: true,
    });
  }
  if (document.getElementById("usersTable")) {
    $("#usersTable").DataTable({
      order: [[0, "asc"]],
      pageLength: 10,
      responsive: true,
    });
  }
});
