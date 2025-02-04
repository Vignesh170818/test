jQuery(document).ready(function () {

    $("#generate_deployment_button").click(function (event) {
        $("#preloader").show();
        event.preventDefault();
        asyncDeploymentFunction();
    }
    );

})

async function asyncDeploymentFunction() {

    // Assuming you still want to collect data from a form, or you can define your data directly
    // For direct definition, skip this part and define your `formJSON` directly
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

    const url = window.location.href.replace('\/#', '').replace('#', '') + '/generatedeployment';

    try {
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

            document.getElementById('deployment_strategy_ui').value = jsonResponse.uideployment;
            document.getElementById('deployment_strategy_services').value = jsonResponse.servicesdeployment;
            document.getElementById('deployment_strategy_data').value = jsonResponse.datadeployment;
            
            $("#preloader").fadeOut();
            openTab(event, 'deploymentTab', 'deployment-link');
        } else {
            throw new Error('Network response was not ok.');
        }
    } catch (error) {
        $("#preloader").fadeOut();
        console.error('There has been a problem with your fetch operation:', error);
    }
}