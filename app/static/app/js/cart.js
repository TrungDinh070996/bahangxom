

function updateUserOrder(productId, action) {
  console.log("user logged in");
  var url = "/update_item/";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId: productId, action: action }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log("data", data);
      location.reload();
    });
}

function showToast() {
  const toastEl = document.getElementById('toast-add-success');
  const toast = new bootstrap.Toast(toastEl);
  toast.show();
}

let updateBtns = document.getElementsByClassName("update-cart");

for (let i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener('click', function () {
    var productId = this.dataset.product;
    var action = this.dataset.action;

    fetch('/update_item/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({ productId: productId, action: action }),
    })
    .then(response => response.json())
    .then(data => {
      console.log('Added:', data);
      showToast(); // ✅ GỌI TOAST
    });
  });
}

