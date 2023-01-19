$('button.Amount-update').click(function(e){
  e.preventDefault();
  var productID = $(this).data('id');
  var inputID = 'form-input' + productID;
  var quantity = document.getElementById(inputID).value;
  $.post(
    '{% url "app_cart:cart_update" %}',
    {id: productID, quantity: quantity},
    function(data){
      $('button.Amount-update').data('quantity', quantity);
      location.reload();
      return false;
    }
  );
});