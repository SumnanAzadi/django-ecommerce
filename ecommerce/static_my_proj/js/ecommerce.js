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
});
