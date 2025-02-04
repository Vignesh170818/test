jQuery(document).ready(function () {

    $("#generate_code_button").click(function (event) {
        $("#preloader").show();
        event.preventDefault();
        asyncCodeFunction('generate');
    }
    );

    $("#generate_unittest_button").click(function (event) {
        $("#preloader").show();
        event.preventDefault();
        asyncCodeFunction('unittest');
    }
    );

})

async function asyncCodeFunction(eventType) {

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

    let url='';
    if (eventType === 'generate') {
        url = window.location.href.replace('\/#', '').replace('#', '') + '/generatecode';
    }
    else if (eventType === 'unittest') {
        url = window.location.href.replace('\/#', '').replace('#', '') + '/generateunittesting';
    }
    else {
        url = window.location.href.replace('\/#', '').replace('#', '') + '/generatecode';
    }

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

            if (eventType === 'generate') {
                //if jsonResponse.uicode is not empty, then set the value of the textarea
                if (jsonResponse.uicode !== '') {
                    document.getElementById('ui_code').value = jsonResponse.uicode;
                }
                if (jsonResponse.servicescode !== '') {
                    document.getElementById('services_code').value = jsonResponse.servicescode;
                }
                if (jsonResponse.datacode !== '') {
                    document.getElementById('data_code').value = jsonResponse.datacode;
                }
            }
            else if (eventType === 'unittest') {
                document.getElementById('ui_unittest').value = jsonResponse.uidesign;
                document.getElementById('services_unittest').value = jsonResponse.servicesdesign;
                document.getElementById('data_unittest').value = jsonResponse.datadesign;
            }
            else {
                if (jsonResponse.uicode !== '') {
                    document.getElementById('ui_code').value = jsonResponse.uicode;
                }
                if (jsonResponse.servicescode !== '') {
                    document.getElementById('services_code').value = jsonResponse.servicescode;
                }
                if (jsonResponse.datacode !== '') {
                    document.getElementById('data_code').value = jsonResponse.datacode;
                }
            }
            $("#preloader").fadeOut();
            openTab(event, 'codeTab', 'code-link');
        } else {
            throw new Error('Network response was not ok.');
        }
    } catch (error) {
        $("#preloader").fadeOut();
        console.error('There has been a problem with your fetch operation:', error);
    }
}