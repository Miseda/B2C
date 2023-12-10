// Function to add a new job card
function addJobCard(job, callback) {
    var newCard = `
        <div class="job-card" id="job-card-${job.id}">
            <h3>${job.title}</h3>
            <p>${job.location} - ${job.type}</p>
            <p>${job.description}</p>
            <button class="delete-button" data-job-id="${job.id}">Delete</button>
            <a href="/view_job/${job.id}">View Details</a>
        </div>
    `;
    $('#new-job-cards').append(newCard);

    // Update the careers page with the new job
    $('#careers-page').append(newCard);

    // Execute the callback function after adding the job card
    callback();
}

// Function to check and update the visibility of the careerStatus message

function updateCareerStatusVisibility() {
    if ($('.right-div9 .job-card').length > 0) {
        $('.right-div9 .careerStatus').hide();
    } else {
        $('.right-div9 .careerStatus').show();
    }
}



// Handle form submission using AJAX
$(document).on('submit', '#career-form', function (e) {
    e.preventDefault();

    var form = $(this);
    var url = form.attr('action');
    var formData = form.serialize();  // Serialize the form data

    $.ajax({
        type: 'POST',
        url: url,
        data: formData,
        success: function (response) {
            if (response.success) {
                // Add the new job card with a callback to update visibility
                addJobCard(response.job, function () {
                    // Check and update the visibility of the careerStatus message
                    updateCareerStatusVisibility();
                });

                // Clear the form if needed
                form.trigger('reset');
            }
        }
    });
});

// Rest of your JavaScript code...


// Handle click event for delete button using delegation
$(document).on('click', '.delete-button', function (e) {
    e.preventDefault();

    var jobId = $(this).data('job-id');
    var deleteUrl = `/delete_job/${jobId}`;

    // Perform AJAX delete request
    $.ajax({
        type: 'POST',
        url: deleteUrl,
        success: function (response) {
            if (response.success) {
                // Remove the deleted job card from the page
                $('#job-card-' + jobId).remove();

                // Check and update the visibility of the careerStatus message
                updateCareerStatusVisibility();
            }
        }
    });
});

// Check and update the visibility of the careerStatus message on page load
$(document).ready(function () {
    updateCareerStatusVisibility();
});
