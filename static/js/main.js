console.log("Sanity check!");

// Get Stripe publishable key
fetch("../config/")
.then((result) => { return result.json(); })
.then((data) => {
  // Initialize Stripe.js
  const stripe = Stripe(data.publicKey);

  // new
  // Event handler
  var el = document.querySelector("#submitBtn");
  if(el){
    el.addEventListener("click", () => {
    // Get Checkout Session ID
    fetch("../create-checkout-session/")
    .then((result) => { return result.json(); })
    .then((data) => {
      console.log(data);
      // Redirect to Stripe Checkout
      return stripe.redirectToCheckout({sessionId: data.sessionId})
    })
    .then((res) => {
      console.log(res);
    });
  });
}
});

