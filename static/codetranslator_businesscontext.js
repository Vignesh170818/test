function validateInput(industry, ecosystemContext, scopeVision) {
    let isValid = true;
    let errorMessage = "";

    // Check if any of the fields are empty
    if (!industry.trim()) {
        isValid = false;
        errorMessage += "Industry field cannot be empty.\n";
    }
    if (!ecosystemContext.trim()) {
        isValid = false;
        errorMessage += "Ecosystem context field cannot be empty.\n";
    }
    if (!scopeVision.trim()) {
        isValid = false;
        errorMessage += "Scope vision field cannot be empty.\n";
    }

    if (!isValid) {
        alert(errorMessage);
    }

    return isValid;
}

jQuery(document).ready(function() {
    
    $("#get_business_context_button").click(function(event) {
        $("#preloader").show();
        event.preventDefault();
        fetchBusinessContext();
    }
    );
})

async function fetchBusinessContext() {
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
        const response = await fetch('/getbusinesscontext', {
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
            document.getElementById('businesscontext').value = jsonResponse.popovercontent;
            document.getElementById('selectedbusinesscontext').value = jsonResponse.businesscontext;
            
            $("#preloader").fadeOut();
            openTab(event, 'bpmMapTab', 'bpm-map-link');
        } else {
            throw new Error('Network response was not ok.');
        }
    } catch (error) {
        $("#preloader").fadeOut();
        console.error('There has been a problem with your fetch operation:', error);
    }
}
