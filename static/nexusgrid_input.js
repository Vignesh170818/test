jQuery(document).ready(function() {
    
    $("#generate_summary_button").click(function(event) {
        $("#preloader").show();
        event.preventDefault();
        generateSummmaryFunction();
    }
    );
})

async function generateSummmaryFunction() {
    // Assuming you have form fields with these IDs

    const form = document.getElementById("gen_lite"); // Make sure you have a form with this ID or collect data differently
    var fileInput = document.getElementById('inputdocument');
    var file = fileInput.files[0];
    var llm_platform_options = document.getElementById('llm_platform_options').value;
    var informationoption = document.getElementById('informationoption').value;
    if (file) {
        var formData = new FormData();
        formData.append('document', file);
        formData.append('llm_platform_options', llm_platform_options);
        formData.append('informationoption', informationoption);
    } else {
        alert('Please select a file to upload.');
    }

    try {
        const response = await fetch('/generatesummary', {
            method: 'POST', // or 'PUT'
            body: formData, // data can be `string` or {object}!
        });

        if (response.ok) {
            const jsonResponse = await response.json();
            document.getElementById('document_summary').value = jsonResponse.response;
            
            $("#preloader").fadeOut();
            openTab(event, 'inputTab', 'input-link');
        } else {
            throw new Error('Network response was not ok.');
        }
    } catch (error) {
        $("#preloader").fadeOut();
        console.error('There has been a problem with your fetch operation:', error);
    }
}
