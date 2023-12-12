// Function to add a new job card
function addJobCard(job, callback) {
    var newCard = `
        <a href="{{ url_for('main_bp.job_details', job_id=job.id) }}" class="job-card" id="job-card-${job.id}">
            <div class="job-card" id="job-card-${job.id}">
                <h3>${job.title}</h3>
                <p>${job.location} - ${job.type}</p>
                <div class="job-description">${job.description}</div>
                <button class="delete-button" data-job-id="${job.id}">Delete</button>
                <a href="/view_job/${job.id}">View Details</a>
            </div>
        </a>
    `;
    var newCardElement = $(newCard);

    // Set HTML content for job description
    newCardElement.find('.job-description').html(job.description);

    // Append the new job card
    $('#new-job-cards').append(newCardElement);

    // Update the careers page with the new job
    $('#careers-page').append(newCardElement);

    // Execute the callback function after adding the job card
    callback();
}

// ... (rest of your code)


// Function to check and update the visibility of the careerStatus message
function updateCareerStatusVisibility() {
    if ($('.third-container2 .job-card').length > 0 || $('.right-div9 .job-card').length > 0) {
        $('.third-container2 .careerStatus, .right-div9 .careerStatus').hide();
    } else {
        $('.third-container2 .careerStatus, .right-div9 .careerStatus').show();
    }
}

// Function to filter jobs based on the search input
function filterJobs() {
    var searchInput = $('#job-search').val().toLowerCase();

    var foundJobs = false;

    $('.job-card').each(function () {
        var jobTitle = $(this).find('.cardTitle9 p').text().toLowerCase();

        if (searchInput === '' || jobTitle.includes(searchInput)) {
            $(this).show();
            foundJobs = true;
        } else {
            $(this).hide();
        }
    });

    // Update the visibility of the careerStatus message
    updateCareerStatusVisibility();

    // Display "Search not found" message if no matching jobs are found
    if (!foundJobs) {
        $('.search-not-found').show();
    } else {
        // Hide the "Search not found" message if there are matching jobs
        $('.search-not-found').hide();
    }
}


// Event handlers
$(document).ready(function () {
    // Check and update the visibility of the careerStatus message on page load
    updateCareerStatusVisibility();

    // Set HTML content for job descriptions
    $('.job-description').html(function (index, oldHtml) {
        return $(this).text(oldHtml);
    });

    // Handle form submission using AJAX
    $(document).on('submit', '#career-form', function (e) {
        e.preventDefault();

        var form = $(this);
        var url = form.attr('action');
        var formData = form.serialize();

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

    // Handle click event for entire job card
    $(document).on('click', '.job-card', function (e) {
        // No need to prevent the default behavior here
        var jobId = $(this).attr('id').replace('job-card-', '');
        var detailsUrl = `/job_details/${jobId}`;

        // Navigate to the job details page directly
        window.location.href = detailsUrl;
    });

    // Handle click event for search button
    $(document).on('click', '#search-button', function () {
        filterJobs();
    });

    // Handle input event for live search
    $(document).on('input', '#job-search', function () {
        filterJobs();
    });

    // Handle keypress event for live search when the Enter key is pressed
    $(document).on('keypress', '#job-search', function (event) {
        if (event.which === 13) {
            event.preventDefault();
            filterJobs();
        }
    });
});
