function validation(e) {
    var product = document.getElementById("product").value;
    console.log(product);
    if (product == ""){
      e.preventDefault();
      alert("Please enter the product");
    }
  }