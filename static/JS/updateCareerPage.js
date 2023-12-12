// Function to add a new job card
function addJobCard(job, callback) {
    // Use the HTML content stored in the hidden input field
    var jobDescriptionHtml = $('#hidden-description').val();

    var newCard = `
        <a href="{{ url_for('main_bp.job_details', job_id=job.id) }}" class="job-card" id="job-card-${job.id}">
            <div class="job-card" id="job-card-${job.id}">
                <h3>${job.title}</h3>
                <p>${job.location} - ${job.type}</p>
                <div class="job-description">${jobDescriptionHtml}</div>
                <button class="delete-button" data-job-id="${job.id}">Delete</button>
                <a href="/view_job/${job.id}">View Details</a>
            </div>
        </a>
    `;

    var newCardElement = $(newCard);

    // Append the new job card
    $('#new-job-cards').append(newCardElement);

    // Update the careers page with the new job
    $('#careers-page').append(newCardElement);

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

document.addEventListener('DOMContentLoaded', function () {
    const descriptionTextarea = document.getElementById('description-markdown');
    
    // Add an input event listener to update the textarea value with the rendered HTML
    descriptionTextarea.addEventListener('input', function () {
        const markdownText = descriptionTextarea.value;
        const htmlText = marked(markdownText);
        descriptionTextarea.innerHTML = htmlText;
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const quill = new Quill('#quill-editor', {
        theme: 'snow',
        modules: {
            toolbar: [
                ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
                ['blockquote', 'code-block'],
                [{ 'header': 1 }, { 'header': 2 }],               // custom button values
                [{ 'list': 'ordered' }, { 'list': 'bullet' }],
                [{ 'script': 'sub' }, { 'script': 'super' }],    // superscript/subscript
                [{ 'indent': '-1' }, { 'indent': '+1' }],        // outdent/indent
                [{ 'direction': 'rtl' }],                        // text direction
                [{ 'size': ['small', false, 'large', 'huge'] }], // custom dropdown
                [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
                [{ 'color': [] }, { 'background': [] }],         // dropdown with defaults from theme
                [{ 'font': [] }],
                [{ 'align': [] }],
                ['clean'],                                       // remove formatting button
                ['link', 'image', 'video']                       // link, image, video
            ]
        }
    });

    // Listen for changes and update the hidden input
    quill.on('text-change', function () {
        const html = quill.root.innerHTML;
        document.getElementById('hidden-description').value = html;
    });
});