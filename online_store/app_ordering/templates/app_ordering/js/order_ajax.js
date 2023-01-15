// Способы доставки.
var deliveryMethods = "{{ delivery_str }}".split('|');
// Способы оплаты.
var paymentMethods = ["Онлайн картой", "Онлайн со случайного чужого счета"];
// ID всех полей формы кроме способов оплаты и доставки.
var formIds = ["name", "phone", "mail", "city", "address"];
// ID всех элементов вывода значений, введенных пользователем, кроме доставки и оплаты.
var outputIds = ["name-output", "phone-output", "mail-output", "city-output", "address-output"];

$("#step4-link").click(function(e) {
  e.preventDefault();
  deliveryVal = document.querySelector('input[name="delivery_method"]:checked').value;
  document.getElementById("delivery-output").innerHTML = deliveryMethods[deliveryVal - 1];
  paymentVal = document.querySelector('input[name="payment_method"]:checked').value;
  document.getElementById("payment-output").innerHTML = paymentMethods[paymentVal - 1];
  for (var i = 0; i < 5; i++) {
    outputEl = document.getElementById(outputIds[i]);
    inputVal = document.getElementById(formIds[i]).value;
    if (inputVal === "") {
      outputEl.innerHTML = '<span style="color: red;">Обязательно для заполнения!</span>';
    } else if ((formIds[i] === "phone") && (inputVal.includes("x"))) {
      outputEl.innerHTML = '<span style="color: red;">Неправильный номер телефона!</span>';
    } else {
      // Присваиваем элементу вывода значение введенное пользователем.
      outputEl.innerHTML = inputVal;
    }
  }
});