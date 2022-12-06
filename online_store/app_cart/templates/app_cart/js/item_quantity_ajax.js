var length = {{ cart|length }}
var prices = {{ prices }}


for (var counter = 0; counter < length; counter++) {
  var productPrice = prices[counter];
  var removeButtonId = "#remove-button" + counter;
  var addButtonId = "#add-button" + counter
  var itemPriceId = "item-price" + counter;

  $(removeButtonId).click(function(e) {
    e.preventDefault();
    var itemPrice = Number(document.getElementById(itemPriceId).innerHTML);
    var cartPrice = Number(document.getElementById("cart-price").innerHTML);
    if (itemPrice > 0) {
      document.getElementById(itemPriceId).innerHTML = itemPrice - productPrice;
      document.getElementById("cart-price").innerHTML = cartPrice - productPrice;
    };
  });

  $(addButtonId).click(function(e) {
    e.preventDefault();
    var itemPrice = Number(document.getElementById(itemPriceId).innerHTML);
    var cartPrice = Number(document.getElementById("cart-price").innerHTML);
    document.getElementById(itemPriceId).innerHTML = itemPrice + productPrice;
    document.getElementById("cart-price").innerHTML = cartPrice + productPrice;
  });
}