var price = {{ product.price }}

$('#remove-button').click(function(e) {
  e.preventDefault();
  document.getElementById("item-price").innerHTML -= '0'
  document.getElementById("cart-price").innerHTML -= '0'
});

$('#add-button').click(function(e) {
  e.preventDefault();
  document.getElementById("item-price").innerHTML += '1000'
  document.getElementById("cart-price").innerHTML += '1000'
});