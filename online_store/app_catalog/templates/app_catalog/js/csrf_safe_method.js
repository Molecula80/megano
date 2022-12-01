var csrftoken = Cookies.get('csrftoken')

function csrfSafeMethod(method) {
  // Для этих методов токен не будет подставляться в заголовок.
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});
