jQuery(document).ready(function() {
    
    $("#generateartifact").click(function(event) {
        $("#preloader").show();
        event.preventDefault();
        fetchDesignArtifact();
    }
    );
})

async function fetchDesignArtifact() {
    // Assuming you have form fields with these IDs

    const form = document.getElementById("gen_lite"); // Make sure you have a form with this ID or collect data differently
    const formData = new FormData(form);
    const formObject = {};
    
    formData.forEach((value, key) => {
        // Check if the property exists
        if (formObject.hasOwnProperty(key)) {
            // If it's not already an array, make it an array and append the new value
            if (!Array.isArray(formObject[key])) {
                formObject[key] = [formObject[key], value];
            } else {
                // It's already an array, so we just push the new value
                formObject[key].push(value);
            }
        } else {
            // Property doesn't exist, so we can just set it normally
            formObject[key] = value;
        }
    });

    const formJSON = JSON.stringify(formObject);
    console.log(formJSON);

    try {
        const response = await fetch('/getdesignartifact', {
            method: 'POST', // or 'PUT'
            headers: {
                'Content-Type': 'application/json',
                // Include CSRF token if needed
            },
            body: formJSON, // data can be `string` or {object}!
        });

        if (response.ok) {
            const jsonResponse = await response.json();
            // Now you can use jsonResponse to update your UI accordingly
            // console.log(jsonResponse);
            // For example, updating some div's content:
            document.getElementById('artifact_output').value = jsonResponse.response;
            //append to overall_design_output element
            document.getElementById('overall_design_output').append(jsonResponse.response);
            
            $("#preloader").fadeOut();
            openTab(event, 'generateDesignTab', 'generate-design-link');
        } else {
            throw new Error('Network response was not ok.');
        }
    } catch (error) {
        $("#preloader").fadeOut();
        console.error('There has been a problem with your fetch operation:', error);
    }
}
