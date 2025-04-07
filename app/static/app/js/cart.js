// function updateUserOrder(productId, action) {
//   console.log("user logged in");
//   var url = "/update_item/";

//   fetch(url, {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//       "X-CSRFToken": csrftoken,
//     },
//     body: JSON.stringify({ productId: productId, action: action }),
//   })
//     .then((response) => {
//       return response.json();
//     })
//     .then((data) => {
//       console.log("data", data);
//       showToast();
//       location.reload();
//     });
// }

function showToast() {
  const toastEl = document.getElementById("toast-add-success");
  const toast = new bootstrap.Toast(toastEl);
  toast.show();
}

let addBtns = document.getElementsByClassName("add-btn");
for (let i = 0; i < addBtns.length; i++) {
  addBtns[i].addEventListener("click", function () {
    var productId = this.dataset.product;
    var action = this.dataset.action;

    fetch("/update_item/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify({ productId: productId, action: action }),
    })
      .then((response) => response.json())
      .then((data) => {
        showToast(); // ✅ Chỉ hiện toast ở đây
      });
  });
}


let updateBtns = document.getElementsByClassName("chg-quantity");
for (let i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener("click", function () {
    var productId = this.dataset.product;
    var action = this.dataset.action;

    fetch("/update_item/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify({ productId: productId, action: action }),
    })
      .then((response) => response.json())
      .then((data) => {
        location.reload(); // ✅ Reload lại giỏ hàng
      });
  });
}
