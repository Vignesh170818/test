jQuery(document).ready(function () {

    $("#generate_feature_button").click(function (event) {
        $("#preloader").show();
        event.preventDefault();
        asyncFeatureFunction('generate');
    }
    );

    $("#get_feature_details").click(function (event) {
        $("#preloader").show();
        event.preventDefault();
        asyncFeatureFunction('getData');
    }
    );

    $("#reset_feature_details").click(function (event) {
        $("#preloader").show();
        event.preventDefault();
        asyncFeatureFunction('resetFeature');
    }
    );

    $("#generate_feature_fromepic_button").click(function (event) {
        $("#preloader").show();
        event.preventDefault();
        asyncFeatureFunction('generate');
    }
    );

    $("#expand_feature_button").click(function (event) {
        $("#preloader").show();
        event.preventDefault();
        asyncFeatureFunction('expand');
    }
    );

})

async function asyncFeatureFunction(eventType) {

    // Assuming you still want to collect data from a form, or you can define your data directly
    // For direct definition, skip this part and define your `formJSON` directly
    const form = document.getElementById("gen_lite"); // Make sure you have a form with this ID or collect data differently
    let entity_type = 'feature'
    document.getElementById('entity_type').value=entity_type;
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

    let url = '';

    if (eventType === 'generate') {
        url = window.location.href.replace('\/#', '') + '/generatefeature';
    }
    else if (eventType === 'getData') {
        url = window.location.href.replace('\/#', '') + '/getentitydata';
    }
    else if (eventType === 'resetFeature') {
        url = window.location.href.replace('\/#', '') + '/resetentitydata';
    }
    else if (eventType === 'expand') {
        url = window.location.href.replace('\/#', '') + '/expandfeature';
    }
    else {
        url = window.location.href.replace('\/#', '') + '/generatefeature';
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
            if (eventType === 'getData') {
                if(jsonResponse.responsetype == "success"){
                    document.getElementById('selected_feature').value = jsonResponse.response.selected_feature;
                    document.getElementById('feature_user_story').value = jsonResponse.response.feature_user_story;
                    document.getElementById('feature_external_id').readOnly = true;
                    document.getElementById('get_feature_details').disabled = true;
                }
                else {
                    alert(jsonResponse.response)
                    document.getElementById('selected_feature').value = ''
                    document.getElementById('feature_user_story').value = ''
                }
            }
            else if (eventType === 'resetFeature') {
                if(jsonResponse.responsetype == "success"){
                    document.getElementById('feature_external_id').value = '';
                    document.getElementById('feature_external_id').readOnly = false;
                    document.getElementById('get_feature_details').disabled = false;
                    document.getElementById('features_list').value = '';
                    document.getElementById('selected_feature').value = '';
                    document.getElementById('feature_user_story').value = '';
                    document.getElementById('user_story_external_id').value = '';
                    document.getElementById('user_story_external_id').readOnly = false;
                    document.getElementById('get_user_story_details').disabled = false;
                    document.getElementById('user_stories_list').value = '';
                    document.getElementById('selected_user_story').value = '';
                    document.getElementById('user_story_abstract').value = '';
                }
            }
            else if (eventType === 'expand') {
                document.getElementById('feature_user_story').value = jsonResponse.response;
            }
            else {
                document.getElementById('features_list').value = jsonResponse.response;
            }
            $("#preloader").fadeOut();
            openTab(event, 'featuresTab', 'feature-link');
        } else {
            throw new Error('Network response was not ok.');
        }
    } catch (error) {
        $("#preloader").fadeOut();
        console.error('There has been a problem with your fetch operation:', error);
    }
}