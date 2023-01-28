// Способы оплаты.
var paymentMethods = ["Онлайн картой", "Онлайн со случайного чужого счета"];
// ID всех полей формы кроме способов оплаты и доставки.
var formIds = ["name", "phone", "mail", "city", "address"];
// ID всех элементов вывода значений, введенных пользователем, кроме доставки и оплаты.
var outputIds = ["name-output", "phone-output", "mail-output", "city-output", "address-output"];

$("#step4-link").click(function(e) {
  e.preventDefault();
  var errors = false;
  var paymentVal = document.querySelector('input[name="payment_method"]:checked').value;
  document.getElementById("payment-output").innerHTML = paymentMethods[paymentVal - 1];
  for (var i = 0; i < 5; i++) {
    var outputEl = document.getElementById(outputIds[i]);
    var inputVal = document.getElementById(formIds[i]).value;
    if (inputVal === "") {
      outputEl.innerHTML = '<span style="color: red;">Обязательно для заполнения!</span>';
      errors = true;
    } else if ((formIds[i] === "phone") && (inputVal.includes("x"))) {
      outputEl.innerHTML = '<span style="color: red;">Недопустимый номер телефона!</span>';
      errors = true;
    } else {
      // Присваиваем элементу вывода значение введенное пользователем.
      outputEl.innerHTML = inputVal;
    }
  }
  if (errors === true) {
    document.getElementById("order-error").innerHTML = 'Форма содержит ошибки. Проверьте коректность введенных данных.';
  } else {
    document.getElementById("order-error").innerHTML = '';
  }
  var deliveryVal = document.querySelector('input[name="delivery_method"]:checked').value;
  $.post(
    '{% url "app_ordering:get_delivery_method" %}',
    {delivery_val: deliveryVal},
    function (response) {
      document.getElementById("delivery-output").innerHTML = response.delivery_method;
      if (response.delivery_price > 0) {
        document.getElementById("delivery-price").innerHTML = [response.delivery_price, "$"].join("");
      } else {
        document.getElementById("delivery-price").innerHTML = 'бесплатно';
      }
      document.getElementById("order-price").innerHTML = [response.order_price, "$"].join("");
    }
  );
});