jQuery(document).ready(function () {

    $("#generate_functional_design_button").click(async function (event) {
        $("#preloader").show();
        event.preventDefault();
        await asyncDesignFunction('functional');
        checkAndDisableButton('functional');
        
    }
    );

    $(document).ready(function() {
        // Function to check if all specified textareas with a specific id are empty
        
    
        // Check and disable the button on document load
        checkAndDisableButton('functional');
        checkAndDisableButton('highlevel');
        checkAndDisableButton('lowlevel');
    
    });
    

    $("#generate_high_level_design_button").click(async function (event) {
        $("#preloader").show();
        event.preventDefault();
        await asyncDesignFunction('highlevel');
        checkAndDisableButton('highlevel');
    }
    );

    $("#generate_detailed_design_button").click(async function (event) {
        $("#preloader").show();
        event.preventDefault();
        await asyncDesignFunction('lowlevel');
        checkAndDisableButton('lowlevel');
    }
    );
    $("#fdd_download").click(async function (event) {
        $("#preloader").show();
        event.preventDefault();
        await DownloadDesignFunction('functional');
    }
    );
    $("#hld_download").click(async function (event) {
        $("#preloader").show();
        event.preventDefault();
        await DownloadDesignFunction('highlevel');
    }
    );
    $("#dld_download").click(async function (event) {
        $("#preloader").show();
        event.preventDefault();
        await DownloadDesignFunction('lowlevel');
    }
    );

})

function checkAndDisableButton(event) {
    let isEmpty = false;
    
    if (event === 'functional') {

        isEmpty = $(`#ui_functional_design`).val().trim() === '' &&
                  $(`#services_functional_design`).val().trim() === '' &&
                  $(`#data_functional_design`).val().trim() === '';

        if (isEmpty) {$('#fdd_download').prop('disabled', true);} 
        else {$('#fdd_download').prop('disabled', false);}
    } 
    else if (event === 'highlevel') {
        isEmpty = $(`#ui_high_level_design`).val().trim() === '' &&
                  $(`#services_high_level_design`).val().trim() === '' &&
                  $(`#data_high_level_design`).val().trim() === '';

        if (isEmpty) {$('#hld_download').prop('disabled', true);} 
        else {$('#hld_download').prop('disabled', false);}
    } 
    else if (event === 'lowlevel') {
        isEmpty = $(`#ui_detailed_design`).val().trim() === '' &&
                  $(`#services_detailed_design`).val().trim() === '' &&
                  $(`#data_detailed_design`).val().trim() === '';
        if (isEmpty) {$('#dld_download').prop('disabled', true);} 
        else {$('#dld_download').prop('disabled', false);}
    }

    
    
}


async function asyncDesignFunction(eventType) {

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
    
    let url ='';
    if (eventType === 'functional') {
         url = window.location.href.replace('\/#', '') + '/generatefunctionaldesign';
         console.log("Generate Func Design URL IS", url)
    }
    else if (eventType === 'highlevel') {
         url = window.location.href.replace('\/#', '') + '/generatehighleveldesign';
    }
    else if (eventType === 'lowlevel') {
         url = window.location.href.replace('\/#', '') + '/generatedetaileddesign';
    }
    else {
         url = window.location.href.replace('\/#', '') + '/generatefunctionaldesign';
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

            if (eventType === 'functional') {
                // if jsonResponse.uidesign is not empty, then set the value of the textarea
                if (jsonResponse.uidesign != '') {
                    document.getElementById('ui_functional_design').value = jsonResponse.uidesign;
                }
                if (jsonResponse.servicesdesign != '') {
                    document.getElementById('services_functional_design').value = jsonResponse.servicesdesign;
                }
                if (jsonResponse.datadesign != '') {
                    document.getElementById('data_functional_design').value = jsonResponse.datadesign;
                }
            }
            else if (eventType === 'highlevel') {
                if (jsonResponse.uidesign != '') {
                    document.getElementById('ui_high_level_design').value = jsonResponse.uidesign;
                }
                if (jsonResponse.servicesdesign != '') {
                    document.getElementById('services_high_level_design').value = jsonResponse.servicesdesign;
                }
                if (jsonResponse.datadesign != '') {
                    document.getElementById('data_high_level_design').value = jsonResponse.datadesign;
                }
            }
            else if (eventType === 'lowlevel') {
                if (jsonResponse.uidesign != '') {
                    document.getElementById('ui_detailed_design').value = jsonResponse.uidesign;
                }
                if (jsonResponse.servicesdesign != '') {
                    document.getElementById('services_detailed_design').value = jsonResponse.servicesdesign;
                }
                if (jsonResponse.datadesign != '') {
                    document.getElementById('data_detailed_design').value = jsonResponse.datadesign;
                }
            }
            else {
                if (jsonResponse.uidesign != '') {
                    document.getElementById('ui_functional_design').value = jsonResponse.uidesign;
                }
                if (jsonResponse.servicesdesign != '') {
                    document.getElementById('services_functional_design').value = jsonResponse.servicesdesign;
                }
                if (jsonResponse.datadesign != '') {
                    document.getElementById('data_functional_design').value = jsonResponse.datadesign;
                }
            }
            $("#preloader").fadeOut();
            openTab(event, 'functionalDesignTab', 'fd-link');
        } else {
            throw new Error('Network response was not ok.');
        }
    } catch (error) {
        $("#preloader").fadeOut();
        console.error('There has been a problem with your fetch operation:', error);
    }
}


async function DownloadDesignFunction(eventType) {
 
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
   
    let url ='';
    if (eventType === 'functional') {
         url = window.location.href.replace('\/#', '') + '/download_fdd';
         console.log("Generate Func Design URL IS", url)
    }
    else if (eventType === 'highlevel') {
         url = window.location.href.replace('\/#', '') + '/download_hld';
         console.log("Generate High Level Design URL IS", url)
    }
    else if (eventType === 'lowlevel') {
        url = window.location.href.replace('\/#', '') + '/download_dld';
        console.log("Generate High Level Design URL IS", url)
    }
    else {
         url = window.location.href.replace('\/#', '') + '/download_fdd';
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
 
            if (eventType === 'functional') {
                // if jsonResponse.uidesign is not empty, then set the value of the textarea
                if (jsonResponse.filepath != '') {
                    document.getElementById('download_fdd_filename').value = jsonResponse.filepath;
                    const url = 'download_file_fdd?file_name_fdd=' + encodeURIComponent(jsonResponse.filepath);
                    console.log(jsonResponse)
                    console.log(url)
                    document.getElementById("download_fdd_atag").href = url
                    document.getElementById("download_fdd_atag").click()
                }
            }
            else if (eventType === 'highlevel') {
                if (jsonResponse.uidesign != '') {
                    document.getElementById('download_hld_filename').value = jsonResponse.filepath;
                    const url = 'download_file_hld?file_name_hld=' + encodeURIComponent(jsonResponse.filepath);
                    console.log(jsonResponse)
                    console.log(url)
                    document.getElementById("download_hld_atag").href = url
                    document.getElementById("download_hld_atag").click()
                }
            }
            else if (eventType === 'lowlevel') {
                if (jsonResponse.uidesign != '') {
                    document.getElementById('download_dld_filename').value = jsonResponse.filepath;
                    const url = 'download_file_dld?file_name_dld=' + encodeURIComponent(jsonResponse.filepath);
                    console.log(jsonResponse)
                    console.log(url)
                    document.getElementById("download_dld_atag").href = url
                    document.getElementById("download_dld_atag").click()
                }
                
            }
            else {
                if (jsonResponse.uidesign != '') {
                    document.getElementById('ui_functional_design').value = jsonResponse.uidesign;
                }
                if (jsonResponse.servicesdesign != '') {
                    document.getElementById('services_functional_design').value = jsonResponse.servicesdesign;
                }
                if (jsonResponse.datadesign != '') {
                    document.getElementById('data_functional_design').value = jsonResponse.datadesign;
                }
            }
            $("#preloader").fadeOut();
            openTab(event, 'functionalDesignTab', 'fd-link');
        } else {
            throw new Error('Network response was not ok.');
        }
    } catch (error) {
        $("#preloader").fadeOut();
        console.error('There has been a problem with your fetch operation:', error);
    }
}
