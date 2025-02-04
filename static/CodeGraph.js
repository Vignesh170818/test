jQuery(document).ready(function() {
    
    $("#codeFileUploadSubmit").click(function (event) {
        var test = document.getElementById("services_code").value;
        //var $fileUpload = $("input[id='services-code']");
        //console.log($fileUpload);
        if (test == "") {
            alert("Service code is empty");
        }
        else {
            $("#preloader").show();
            event.preventDefault();
            uploadCodeFiles();
        }
    }
    );
    $("#graphsourcecodelang").change(function (event) {
        addValidation();
        $("#codeFileUpload").val(null)
        $("#codeiframe").attr("srcdoc", "")
        event.preventDefault();
    }
    );
})

var filelist = []

function addValidation() {
    switch ($("#graphsourcecodelang")[0].value) {
        case 'csharp':
            $("#codeFileUpload").attr("accept", ".cs")
            break;
        case 'python':
            $("#codeFileUpload").attr("accept", ".py")
            break;
        case 'typescript':
            $("#codeFileUpload").attr("accept", ".ts")
            break;
        case 'html':
            $("#codeFileUpload").attr("accept", ".html")
            break;
        case 'css':
            $("#codeFileUpload").attr("accept", ".css")
            break;
        case 'javascript':
            $("#codeFileUpload").attr("accept", ".js")
            break;
        case 'abap':
            $("#codeFileUpload").attr("accept", ".abap")
            break;
        case 'aspnet':
            $("#codeFileUpload").attr("accept", ".aspx ")
            break;
        default:
            $("#codeFileUpload").attr("accept", "")
            break;
    }
}

function generateUniqueString(length) {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let counter = 0;
    while (counter < length) {
        result += characters.charAt(Math.floor(Math.random() * characters.length));
        counter += 1;
    }
    return result;
}

async function readText(files) {
    filelist = []
    for (const file of files) {
        const text = await file.text();
        let obj = {}
        obj.filecontent = text;
        obj.filename = file.name + generateUniqueString(5);
        filelist.push(obj);
    }
}

async function uploadCodeFiles() {
    const form = document.getElementById("gen_lite"); // Make sure you have a form with this ID or collect data differently
    //const serviceCode = document.getElementById("services_code").value;
    document.getElementById('unique_name').value = generateUniqueString(5);
    document.getElementById('codeiframe').srcdoc = '';
    document.getElementById('codegraph').style.display = 'block';
    document.getElementById("errormsg").innerHTML = "";
    //await readText(files);
    const formData = new FormData(form);
    const formObject = {};
    //formData.append('unique_name', uniqueName);

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

    try {
        const url = window.location.href.replace('\/#', '').replace('#', '') + '/getgraph'
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
            document.getElementById('codeiframe').srcdoc = jsonResponse.response;
            
            $("#preloader").fadeOut();
        } else {
            throw new Error('Network response was not ok.');
        }
    } catch (error) {
        $("#preloader").fadeOut();
        console.error('There has been a problem with your fetch operation:', error);
        document.getElementById("errormsg").innerHTML = "There has been a problem in graph generation. Please try again later";
    }
}

