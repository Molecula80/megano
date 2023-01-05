popup_opened = false;

$('.login-button').click(function(e) {
  e.preventDefault();
  if (popup_opened === false) {
    popup_opened = true;
    $('#login-popup').show();
  } else {
    popup_opened = false;
    $('#login-popup').hide();
  }
});