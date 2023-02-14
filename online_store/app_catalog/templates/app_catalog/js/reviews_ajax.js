var num_pages = {{ num_pages }}
var page = 1;
var empty_page = false;
var block_request = false;

$('#lazy_more').click(function(e) {
  e.preventDefault();
  if (empty_page === false && block_request === false) {
    block_request = true;
    page += 1;
    $('#pre_loader').show();
    $.get('?page=' + page, function(data) {
      $('#pre_loader').hide();
      if (data === '') {
        empty_page = true;
      } else {
        block_request = false;
        $('#comments').append(data);
        if (page === num_pages) {
          $('#lazy_more').hide();
        }
      }
    });
  }
});
