function validation(e) {
    var product = document.getElementById("product").value;
    console.log(product);
    if (product == ""){
      e.preventDefault();
      alert("Please enter the product");
    }
}

$("#SearchProductShopee").click(function () {
  $("#CoverScreenShopee").show();
  setTimeout(function() {
      window.location.href = '/shopee/';
  }, 600000);
});

$("#cancel-shopee").click(function () {
  $("#cancel-text-shopee").show();
});

$("#SearchProductTokopedia").click(function () {
  $("#CoverScreenTokopedia").show();
  setTimeout(function() {
      window.location.href = '/tokopedia/';
  }, 600000);
});

$("#cancel-tokopedia").click(function () {
  $("#cancel-text-tokopedia").show();
});