popup_opened = false;

$(document).ready(function(){
  $('#login-popup').hide();
});

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

$('#register-button').click(function(e) {
  e.preventDefault();
  $('#register-popup').hide();
});