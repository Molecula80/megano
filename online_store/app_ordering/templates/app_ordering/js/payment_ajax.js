$("#generate-number").click(function(e) {
  e.preventDefault();
  // Первые четыре цифры.
  var oneFour = generateDigits(4);
  // С пятой по седьмую цифры.
  var fiveSeven = generateDigits(3);
  // Последняя цифра.
  var lastDigit = (Math.floor(Math.random() * 4) + 1) * 2;
  var fiveEight = [fiveSeven, lastDigit].join("");
  document.getElementById("numero1").value = [oneFour, fiveEight].join(" ");
});


function generateDigits(count) {
  var digits = "";
  for (var i = 0; i < count; i++) {
    var digit = Math.floor(Math.random() * 10);
    digits = [digits, digit].join("");
  }
  return digits;
}
