$('button.Amount-remove').click(function(e){
  e.preventDefault();
  $.get(
    '{% url "app_cart:cart_update" %}',
    {action: $(this).data('action'), id: $(this).data('id')},
    function(data){
      $('button.Amount-remove').data('action', 'remove');
      var itemPrice = $(this).data('item_price');
      var cartPrice = {{ cart.get_total_price }};
      document.getElementById("item-price").innerHTML = itemPrice;
      document.getElementById("cart-price").innerHTML = cartPrice;
    }
  );
});

$('button.Amount-add').click(function(e){
  e.preventDefault();
  $.get(
    '{% url "app_cart:cart_update" %}',
    {action: $(this).data('action'), id: $(this).data('id')},
    function(data){
      $('button.Amount-add').data('action', 'add');
      var item_price = $(this).data('item_price');
      var cart_price = {{ cart.get_total_price }};
      document.getElementById("item-price").innerHTML = itemPrice;
      document.getElementById("cart-price").innerHTML = cartPrice;
    }
  );
});