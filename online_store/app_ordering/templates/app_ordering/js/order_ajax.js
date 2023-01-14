// ID полей формы.
var formIds = ["name", "phone", "mail", "delivery-method", "city", "address", "payment-method"]
// ID элементов вывода значений, введенных пользователем.
var outputIds = ["name-output", "phone-output", "mail-output", "delivery-output", "city-output", "address-output", "payment-output"]

$("#step4-link").click(function(e) {
  e.preventDefault();
  for (var i = 0; i < 7; i++) {
    element = document.getElementById(outputIds[i]);
    field_val = document.getElementById(formIds[i]).value;
    if (field_val === "") {
      element.innerHTML = '<span style="color: red;">Обязательно для заполнения!</span>';
    } else if ((formIds[i] === "phone") && (field_val.includes("x"))) {
      element.innerHTML = '<span style="color: red;">Неправильный номер телефона!</span>';
    } else if ((formIds[i] === "delivery-method")) {
      element.innerHTML = document.querySelector('input[name="delivery_method"]:checked').value;
    } else {
      // Присваиваем элементу вывода значение введенное пользователем.
      element.innerHTML = field_val;
    }
  }
});