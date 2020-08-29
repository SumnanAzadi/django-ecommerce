$(document).ready(function () {
  var productForm = $(".form-product-ajax");

  productForm.submit(function (event) {
    event.preventDefault();
    var thisForm = $(this);
    // var actionEndpoint = thisForm.attr("action"); // API Endpoint
    var actionEndpoint = thisForm.attr("data-endpoint");
    var httpMethod = thisForm.attr("method");
    var formData = thisForm.serialize();

    $.ajax({
      url: actionEndpoint,
      method: httpMethod,
      data: formData,
      success: function (data) {
        var submitSpan = thisForm.find(".submit-span");
        if (data.added) {
          submitSpan.html(
            "In cart <button type='submit' class='btn btn-link'>Remove?</button>"
          );
        } else {
          submitSpan.html(
            "<button type='submit'  class='btn btn-success'>Add to cart</button>"
          );
        }
        var navbarCount = $(".navbar-cart-count");
        navbarCount.text(data.cartItemCount);
        var currentPath = window.location.href;
        //It will trigger only if cart is present in the url
        if (currentPath.indexOf("cart") != -1) {
          refreshCart();
        }
      },
      error: function (errorData) {
        $.alert({
          title: "Oops!",
          content: "An error occurred",
          theme: "modern",
        });
      },
    });
  });
  function refreshCart() {
    console.log("In refreshCart ");
    //all functions in carts/templates/carts/home.html
    var cartTable = $(".cart-table");
    var cartBody = cartTable.find(".cart-body");
    var productRows = cartBody.find(".cart-product");
    var currentUrl = window.location.href;

    var refreshCartUrl = "/api/cart/";
    var refreshCartMethod = "GET";
    var data = {};
    $.ajax({
      url: refreshCartUrl,
      method: refreshCartMethod,
      data: data,
      success: function (data) {
        console.log("Success");
        var hiddenCartItemRemoveForm = $(".cart-item-remove-form");
        if (data.products.length > 0) {
          productRows.html(" ");
          i = data.products.length;
          $.each(data.products, function (index, value) {
            console.log(value);
            var newCartItemRemove = hiddenCartItemRemoveForm.clone();
            newCartItemRemove.css("display", "block");
            //newCartItemRemove.removeClass("hidden-class")
            newCartItemRemove.find(".cart-item-product-id").val(value.id);
            cartBody.prepend(
              '<tr><th scope="row">' +
                i +
                "</th><td><a href='" +
                value.url +
                "'>" +
                value.name +
                "</a>" +
                newCartItemRemove.html() +
                "</td><td>" +
                value.price +
                "</td></tr>"
            );
            i--;
          });
          cartBody.find(".cart-subtotal").text(data.subtotal);
          cartBody.find(".cart-total").text(data.total);
        } else {
          console.log("Else loop");
          window.location.href = currentUrl;
        }
      },
      error: function (errorData) {
        console.log("error");
        console.log(errorData);
      },
    });
  }
});
