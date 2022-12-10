$("#remove-button").click(function(e) {
    e.preventDefault();
    var itemPrice = Number(document.getElementById("#add-button").innerHTML);
    var cartPrice = Number(document.getElementById("cart-price").innerHTML);
    if (itemPrice > 0) {
      document.getElementById("item-price").innerHTML = itemPrice - productPrice;
      document.getElementById("cart-price").innerHTML = cartPrice - productPrice;
    };
  });

  $("#add-button").click(function(e) {
    e.preventDefault();
    var itemPrice = Number(document.getElementById("item-price").innerHTML);
    var cartPrice = Number(document.getElementById("cart-price").innerHTML);
    document.getElementById("item-price").innerHTML = itemPrice + productPrice;
    document.getElementById("cart-price").innerHTML = cartPrice + productPrice;
  });