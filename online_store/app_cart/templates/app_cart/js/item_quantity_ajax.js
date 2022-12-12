$('button.Amount-remove').click(function(e){
  e.preventDefault();
  $.post(
    '{% url "app_cart:cart_update" %}',
    {action: $(this).data('action'), id: $(this).data('id')},
    function(data){
      $('button.Amount-remove').data('action', 'remove');
    }
  );
});

$('button.Amount-add').click(function(e){
  e.preventDefault();
  $.post(
    '{% url "app_cart:cart_update" %}',
    {action: $(this).data('action'), id: $(this).data('id')},
    function(data){
      $('button.Amount-add').data('action', 'add');
    }
  );
});