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
        industry = document.getElementById('industry').value;
        ecosystemContext = document.getElementById('ecosystem_context').value;
        scopeVision = document.getElementById('scope_vision').value;

        if (validateInput(industry, ecosystemContext, scopeVision)) {
            fetchBusinessContext();
        } else {
            $("#preloader").fadeOut();
        }
    }
    );
})

async function fetchBusinessContext() {
    // Assuming you have form fields with these IDs
    industry = document.getElementById('industry').value;
    ecosystemContext = document.getElementById('ecosystem_context').value;
    scopeVision = document.getElementById('scope_vision').value;
    selected_llmmodel = document.getElementById('selected_llmmodel').value;

    industry = industry.trim();
    ecosystemContext = ecosystemContext.trim();
    scopeVision = scopeVision.trim();

    industry = DOMPurify.sanitize(industry);
    ecosystemContext = DOMPurify.sanitize(ecosystemContext);
    scopeVision = DOMPurify.sanitize(scopeVision);

    let llmModel = document.getElementById('llm_platform_options').value;
    document.getElementById('selected_llmmodel').value = llmModel;
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
    // console.log(formJSON);

    try {
        const url = window.location.href.replace('\/#', '').replace('#', '') + '/getbusinesscontext'
        const response = await fetch(url, {
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
            document.getElementById('displaycontent').innerHTML = jsonResponse.popovercontent;
            document.getElementById('business_process_mapping').value = jsonResponse.businesscontext;
            document.getElementById('process_flow_mapping').value = jsonResponse.process_flow_mapping;
            $("#preloader").fadeOut();
            openTab(event, 'businessContextTab', 'business-context-link');
        } else {
            throw new Error('Network response was not ok.');
        }
    } catch (error) {
        $("#preloader").fadeOut();
        console.error('There has been a problem with your fetch operation:', error);
    }
}
