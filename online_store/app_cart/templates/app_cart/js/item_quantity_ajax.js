$('button.Amount-remove').click(function(e){
  e.preventDefault();
  var quantity = document.getElementById("form-input").value
  $.post(
    '{% url "app_cart:cart_update" %}',
    {action: $(this).data('action'), id: $(this).data('id'), quantity: quantity},
    function(data){
      $('button.Amount-remove').data('action', 'remove');
      $('button.Amount-remove').data('quantity', quantity);
      location.reload();
      return false;
    }
  );
});

$('button.Amount-add').click(function(e){
  e.preventDefault();
  var quantity = document.getElementById("form-input").value
  $.post(
    '{% url "app_cart:cart_update" %}',
    {action: $(this).data('action'), id: $(this).data('id'), quantity: quantity},
    function(data){
      $('button.Amount-add').data('action', 'add');
      $('button.Amount-remove').data('quantity', quantity);
      location.reload();
      return false;
    }
  );
});