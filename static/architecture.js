jQuery(document).ready(function () {

    $("#generate_architecture_button").click(function (event) {
        $("#preloader").show();
        event.preventDefault();
        asyncArchFunction();
    }
    );

})

async function asyncArchFunction() {

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
    const url = window.location.href.replace('\/#', '').replace('#', '') + '/generatearchitecture'
    //let fetchURL = '/generatearchitecture';

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
            // console.log(jsonResponse);

            document.getElementById('architecture_ui').value = jsonResponse.uiarch;
            document.getElementById('architecture_services').value = jsonResponse.servicesarch;
            document.getElementById('architecture_data').value = jsonResponse.dataarch;
            
            $("#preloader").fadeOut();
            openTab(event, 'archTab', 'arch-link');
        } else {
            throw new Error('Network response was not ok.');
        }
    } catch (error) {
        $("#preloader").fadeOut();
        console.error('There has been a problem with your fetch operation:', error);
    }
}