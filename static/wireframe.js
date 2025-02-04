jQuery(document).ready(function() {
    
    $("#generate_fd_from_image_button").click(function(event) {
        $("#preloader").show();
        event.preventDefault();
        generateFDFromImage();
    }
    );
})

async function generateFDFromImage() {
    // Assuming you have form fields with these IDs

    var fileInput = document.getElementById('wireframe_image');
    var file = fileInput.files[0];
    var llm_platform_options = document.getElementById('llm_platform_options').value;
    
    if (file) {
        const allowedExtensions = ['.jpg', '.jpeg', '.png'];
        const extension = file.name.split('.').pop().toLowerCase();
        if (!allowedExtensions.includes('.' + extension)) {
            alert('Invalid file format. Please select a file with one of the following extensions: ' + allowedExtensions.join(', '));
            $("#preloader").fadeOut();
            return;
        }
        
        const maxFileSizeInBytes = 5 * 1024 * 1024; // 5MB
        if (file.size > maxFileSizeInBytes) {
            alert('File size exceeds the maximum limit of 5MB.');
            $("#preloader").fadeOut();
            return;
        }

        var formData = new FormData();
        formData.append('wireframe_image', file);
        formData.append('llm_platform_options', llm_platform_options);
    } else {
        alert('Please select a file to upload.');
        $("#preloader").fadeOut();
        return;
    }
    let url='';
    url = window.location.href.replace('\/#', '') + '/uploadwireframe';
    try {
        const response = await fetch(url, {
            method: 'POST', // or 'PUT'
            body: formData, // data can be `string` or {object}!
        });

        if (response.ok) {
            const jsonResponse = await response.json();
            document.getElementById('ui_functional_design').value = jsonResponse.response;
            
            $("#preloader").fadeOut();
            // openTab(event, 'inputTab', 'input-link');
        } else {
            throw new Error('Network response was not ok.');
        }
    } catch (error) {
        $("#preloader").fadeOut();
        console.error('There has been a problem with your fetch operation:', error);
    }
}
