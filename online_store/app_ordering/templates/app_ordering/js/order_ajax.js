// ID полей формы.
var formIds = ["name", "phone", "mail", "delivery-method", "city", "address", "payment-method"]
// ID элементов вывода значений, введенных пользователем.
var outputIds = ["name-output", "phone-output", "mail-output", "delivery-output", "city-output", "address-output", "payment-output"]

$('#step4-link').click(function(e){
  alert("Шаг-4");
  e.preventDefault();
  for (var i = 0; i < 7; i++) {
    element = document.getElementById(outputIds[i])
    field_val = document.getElementById(formIds[i])).value;
    if (field_val !== "") {
      // Присваиваем элементу вывода значение введенное пользователем.
      document.getElementById(outputIds[i]).innerHTML = field_val;
    } else {
      document.getElementById(outputIds[i]).innerHTML = '<span style="color: red;">Обязательно для заполнения</span>';
    }
  }
});