jQuery(document).ready(function () {

    $("#generate_epic_button").click(function (event) {
        $("#preloader").show();
        event.preventDefault();
        asyncEpicFunction('generate');
    }
    );

    $("#generate_epic_button1").click(function (event) {
        $("#preloader").show();
        event.preventDefault();
        asyncEpicFunction('generate');
    }
    );

    $("#get_epic_details").click(function (event) {
        $("#preloader").show();
        event.preventDefault();
        asyncEpicFunction('getData');
    }
    );

    $("#reset_epic_details").click(function (event) {
        $("#preloader").show();
        event.preventDefault();
        asyncEpicFunction('resetEpic');
    }
    );

    $("#gen_epic_review_button").click(function (event) {
        $("#preloader").show();
        event.preventDefault();
        asyncEpicFunction('review');
    }
    );

    $("#apply_epic_review_button").click(function (event) {
        $("#preloader").show();
        event.preventDefault();
        asyncEpicFunction('apply');
    }
    );

})

async function asyncEpicFunction(eventType) {

    // Assuming you still want to collect data from a form, or you can define your data directly
    // For direct definition, skip this part and define your `formJSON` directly
    let llmModel = document.getElementById('llm_platform_options').value;
    let entity_type = 'epic'
    document.getElementById('selected_llmmodel').value = llmModel;
    document.getElementById('entity_type').value=entity_type;
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
    
    let url = '';

    if (eventType === 'generate') {
         url = window.location.href.replace('\/#', '') + '/generateepic';
        
    }
    else if (eventType === 'getData') {
        url = window.location.href.replace('\/#', '') + '/getentitydata';
    }
    else if (eventType === 'resetEpic') {
        url = window.location.href.replace('\/#', '') + '/resetentitydata';
    }
    else if (eventType === 'apply') {
        url = window.location.href.replace('\/#', '') + '/applyepicreview';
    }
    else if (eventType === 'review') {
        url = window.location.href.replace('\/#', '') + '/reviewepic';
    }
    else {
        url = window.location.href.replace('\/#', '') + '/generateepic';
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
                    document.getElementById('epic_user_story').value = jsonResponse.response.epic_user_story;
                    document.getElementById('epic_external_id').readOnly = true;
                    document.getElementById('get_epic_details').disabled = true;
                }
                else {
                    alert(jsonResponse.response)
                    document.getElementById('epic_user_story').value = ''
                }
            }
            else if (eventType === 'resetEpic') {
                if(jsonResponse.responsetype == "success"){
                    document.getElementById('epic_external_id').value = '';
                    document.getElementById('epic_external_id').readOnly = false;
                    document.getElementById('get_epic_details').disabled = false;
                    document.getElementById('epic_user_story').value = ''
                    document.getElementById('epic_review_comments').value = ''
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
            else if (eventType === 'review') {
                document.getElementById('epic_review_comments').value = jsonResponse.response;
            }
            else {
                document.getElementById('epic_user_story').value = jsonResponse.response;
            }
            $("#preloader").fadeOut();
            openTab(event, 'epicTab', 'epic-link');
        } else {
            throw new Error('Network response was not ok.');
        }
    } catch (error) {
        $("#preloader").fadeOut();
        console.error('There has been a problem with your fetch operation:', error);
    }
}