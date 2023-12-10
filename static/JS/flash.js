// flash.js

document.addEventListener("DOMContentLoaded", function() {
    var flashContainer = document.getElementById("flash-container");
  
    if (flashContainer) {
      setTimeout(function() {
        flashContainer.style.display = "none";
      }, 4000); // Adjust the timeout value (in milliseconds) as needed
    }
  });

  
  