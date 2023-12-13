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
  
    // Function to update the visibility of challangeStatus
    function updateChallangeStatusVisibility() {
      if (challengeCards.children.length > 0) {
        // If there are cards, hide the "challangeStatus" element
        challangeStatus.style.display = 'none';
      } else {
        // If no cards, show the "challangeStatus" element
        challangeStatus.style.display = 'block';
      }
    }
  
    // Initial update on page load
    updateChallangeStatusVisibility();
  
    // Add an event listener to handle changes in challengeCards
    var observer = new MutationObserver(updateChallangeStatusVisibility);
    observer.observe(challengeCards, { childList: true });
  
    // Clean up the observer when the page is unloaded
    window.addEventListener('unload', function () {
      observer.disconnect();
    });
  });
  

function deleteContactReport(reportId) {
  // No confirmation, directly delete the contact report
  $.ajax({
    url: '/delete-contact-report/' + reportId,
    type: 'POST',
    data: $('#deleteForm').serialize(),
    success: function (response) {

      // Assuming your job card elements have a data-report-id attribute
      $('.job-card[data-report-id="' + reportId + '"]').remove();
    },
    error: function (error) {
      // Handle error
      alert('Error deleting contact report.');
    }
  });
}

// Add this event listener to handle form submission
$(document).on('submit', '.delete-form', function (e) {
  e.preventDefault(); // Prevent the default form submission
  var reportId = $(this).data('report-id');
  deleteContactReport(reportId);
});


  


