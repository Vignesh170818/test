jQuery(document).ready(function () {
    $('#show_user_request').hide();
    $('#show_status').hide();
    $('#show_download').hide();
    $('#merge_status_button').hide();
    $('#push_to_alm_button').hide();
    $("#generate_user_stories_button").click(function (event) {
        $("#preloader").show();
        event.preventDefault();
        asyncUserStoryFunction('generate');
    }
    );

    $("#get_user_story_details").click(function (event) {
        $("#preloader").show();
        event.preventDefault();
        asyncUserStoryFunction('getData');
    }
    );

    $("#reset_user_story_details").click(function (event) {
        $("#preloader").show();
        event.preventDefault();
        asyncUserStoryFunction('resetUserStory');
    }
    );

    $("#generate_userstories_fromfeature_button").click(function (event) {
        $("#preloader").show();
        event.preventDefault();
        asyncUserStoryFunction('generate');
    }
    );

    $("#expand_user_story_button").click(function (event) {
        $("#preloader").show();
        event.preventDefault();
        asyncUserStoryFunction('expand');
    }
    );

    $("#consolidate_workitems_button").click(function (event) {
        $("#preloader").show();
        event.preventDefault();
        asyncUserStoryFunction('consolidate');
    }
    );

    $("#push_to_alm_button").click(function (event) {
        $("#preloader").show();
        event.preventDefault();
        asyncUserStoryFunction('pushtoalm');
    }
    );

    $("#merge_status_button").click(function (event) {
        $("#preloader").show();
        event.preventDefault();
        asyncUserStoryFunction('checkstatus');
    }
    );

    $("#show_download").click(function (event) {
        $("#preloader").show();
        event.preventDefault();
        asyncUserStoryFunction('downloadjson');
    }
    );
})

async function asyncUserStoryFunction(eventType) {

    // Assuming you still want to collect data from a form, or you can define your data directly
    // For direct definition, skip this part and define your `formJSON` directly
    const form = document.getElementById("gen_lite"); // Make sure you have a form with this ID or collect data differently
    let entity_type = 'userstory'
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
        url = window.location.href.replace('\/#', '').replace('#', '') + '/generateuserstories';
    }
    else if (eventType === 'getData') {
        url = window.location.href.replace('\/#', '').replace('#', '') + '/getentitydata';
    }
    else if (eventType === 'resetUserStory') {
        url = window.location.href.replace('\/#', '').replace('#', '') + '/resetentitydata';
    }
    else if (eventType === 'expand') {
        url = window.location.href.replace('\/#', '').replace('#', '') + '/expanduserstory';
    }
    else if (eventType === 'consolidate') {
        url = window.location.href.replace('\/#', '').replace('#', '') + '/consolidateworkitems';
    }
    else if (eventType === 'pushtoalm') {
        url = window.location.href.replace('\/#', '').replace('#', '') + '/mergeworkitems';
    }
    else if (eventType === 'checkstatus') {
        url = window.location.href.replace('\/#', '').replace('#', '') + '/checkstatus';
    }
    else if (eventType === 'downloadjson') {
        url = window.location.href.replace('\/#', '').replace('#', '') + '/download_tool_queue';
    }
    else {
        url = window.location.href.replace('\/#', '').replace('#', '') + '/generateuserstories';
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
                    document.getElementById('selected_user_story').value = jsonResponse.response.selected_user_story;
                    document.getElementById('user_story_abstract').value = jsonResponse.response.user_story_abstract;
                    document.getElementById('user_story_external_id').readOnly = true;
                    document.getElementById('get_user_story_details').disabled = true;
                }
                else {
                    alert(jsonResponse.response)
                    document.getElementById('selected_user_story').value = ''
                    document.getElementById('user_story_abstract').value = ''
                }
            }
            else if (eventType === 'resetUserStory') {
                if(jsonResponse.responsetype == "success"){
                    document.getElementById('user_story_external_id').value = '';
                    document.getElementById('user_story_external_id').readOnly = false;
                    document.getElementById('get_user_story_details').disabled = false;
                    document.getElementById('user_stories_list').value = '';
                    document.getElementById('selected_user_story').value = '';
                    document.getElementById('user_story_abstract').value = '';
                }
            }
            else if (eventType === 'expand') {
                document.getElementById('user_story_abstract').value = jsonResponse.response;
            }
            else if(eventType === 'consolidate'){
                if(jsonResponse.responsetype == "success"){
                    $('#show_user_request').show().prop('disabled', true);
                    $('#push_to_alm_button').show();
                    $('#show_download').show();
                    $('#show_status').hide();
                    alert(jsonResponse.response)
                    document.getElementById('user_request_id').value = jsonResponse.user_request_id;
                }
                else {
                    alert(jsonResponse.response)
                }
            }
            else if(eventType === 'pushtoalm'){
                $('#show_status').show();
                $('#push_to_alm_button').hide();
                $('#merge_status_button').show();
                $('show_download').hide();
                alert(jsonResponse.response)
            }
            else if(eventType === 'checkstatus'){
                document.getElementById('status_response').value = jsonResponse.response;
            }
            else if (eventType === 'downloadjson') {
                if (jsonResponse.temp_file_path !== '') {
                    const url = 'download_tool_queue_file?file_name_json=' + encodeURIComponent(jsonResponse.temp_file_path);
                    console.log(jsonResponse)
                    console.log(url)
                    document.getElementById("download_json_atag").href = url
                    document.getElementById("download_json_atag").click()
                }
                else {
                    alert(jsonResponse.response)
                }
            }
            else {
                document.getElementById('user_stories_list').value = jsonResponse.response;
            }
            $("#preloader").fadeOut();
            openTab(event, 'userStoriesTab', 'user-story-link');
        } else {
            throw new Error('Network response was not ok.');
        }
    } catch (error) {
        $("#preloader").fadeOut();
        console.error('There has been a problem with your fetch operation:', error);
    }
}