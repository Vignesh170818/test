jQuery(document).ready(function () {

    import('./download.js').then(module => {
        const { downloadWord, downloadText, downloadPDF } = module;

        $('#ecosystem-context-download-word').click(function (event) {
            const content = document.getElementById('ecosystem_context').value;
            if (!content) {
                return;
            }
            downloadWord(content, 'EcosystemContext.doc');
        });
        $('#ecosystem-context-download-txt').click(function (event) {
            const content = document.getElementById('ecosystem_context').value;
            if (!content) {
                return;
            }
            downloadText(content, 'EcosystemContext.txt');
        });
        $('#ecosystem-context-download-pdf').click(function (event) {
            const content = document.getElementById('ecosystem_context').value;
            if (!content) {
                return;
            }
            downloadPDF(content, 'EcosystemContext.pdf');
        });
    });
    $("#industry").change(function (event) {
        $("#preloader").show();
        event.preventDefault();
        industry = document.getElementById('industry').value;
        changeApplicationContext();
    }
    );

});
async function changeApplicationContext() {

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

    try {
        //const url = window.location.href.replace(/\/$/, '')
        url = window.location.href.replace('\/#', '').replace('#', '') + '/changeapplicationcontext'
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
            document.getElementById('ecosystem_context').value = jsonResponse.response;
            $("#preloader").fadeOut();
            openTab(event, 'inputTab', 'input-link');
        } else {
            throw new Error('Network response was not ok.');
        }
    } catch (error) {
        $("#preloader").fadeOut();
        console.error('There has been a problem with your fetch operation:', error);
    }
}

async function demoFromHTML() {
    var doc = new jsPDF();
    var elementHandler = {
        '#ecosys': function (element, renderer) {
            return true;
}
    };
    var source = window.document.getElementsById("ecosystem_context")[0];
    doc.fromHTML(
        source,
        15,
        15,
        {
            'width': 180, 'elementHandlers': elementHandler
        });

    doc.output("dataurlnewwindow");

}
