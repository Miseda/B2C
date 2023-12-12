function performAction(action, actionUrl) {
    // Make an AJAX request to the specified action URL
    $.ajax({
      type: 'POST',
      url: actionUrl,
      data: { 'action': action },
      success: function(response) {
        // Handle success, e.g., remove the rejected/deleted request from the UI
        if (action === 'reject') {
          // Update the status field if necessary
          // ...
        }

        // Remove the request item from the UI
        $('.action-form').closest('.request-item').remove();
      },
      error: function(error) {
        // Handle error, e.g., display an error message
        console.log('Error:', error);
      }
    });
  }


  window.addEventListener("scroll", function() {
    var navbar = document.getElementById("myNavbar");
  
    // Set the scroll threshold, you can adjust this value
    var scrollThreshold = 50;
  
    if (window.scrollY > scrollThreshold) {
      navbar.style.background = "black";
    } else {
      navbar.style.background = "linear-gradient(90deg, #2E8ADF 36.99%, #6A79D0 90.8%)";
    }
  });

  document.addEventListener('DOMContentLoaded', function () {
    // Get the element with class "challangeStatus"
    var challangeStatus = document.querySelector('.challangeStatus');

    // Get the element with class "challengeCards"
    var challengeCards = document.querySelector('.challengeCards');

    // Check if there are child elements (cards) inside the "challengeCards" element
    if (challengeCards.children.length > 0) {
        // If there are cards, hide the "challangeStatus" element
        challangeStatus.style.display = 'none';
    } else {
        // If no cards, show the "challangeStatus" element
        challangeStatus.style.display = 'block';
    }
});
  


