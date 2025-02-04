jQuery(document).ready(function () {

    import('./download.js').then(module => {
        const { downloadWord, downloadText, downloadPDF } = module;
        $("#test-plan-download-word").click(function (event) {
            var content = document.getElementById('test_plan').value;
            if (!content) {
                return;
            }
            downloadWord(content, 'TestPlan.doc');
        });
        $("#test-case-download-word").click(function (event) {
            var content = document.getElementById('test_cases').value;
            if (!content) {
                return;
            }
            downloadWord(content, 'TestCases.doc');
        });
        $("#test-scripts-download-word").click(function (event) {
            var content = document.getElementById('test_scripts').value;
            if (!content) {
                return;
            }
            downloadWord(content, 'TestScripts.doc');
        });
        $("#test-scripts-tool-download-word").click(function (event) {
            var content = document.getElementById('tool_test_script').value;
            if (!content) {
                return;
            }
            downloadWord(content, 'TestScriptsForTool.doc');
        });

        $("#test-plan-download-txt").click(function (event) {
            var content = document.getElementById('test_plan').value;
            if (!content) {
                return;
            }
            downloadText(content, 'TestPlan.txt');
        });
        $("#test-case-download-txt").click(function (event) {
            var content = document.getElementById('test_cases').value;
            if (!content) {
                return;
            }
            downloadText(content, 'TestCases.txt');
        });
        $("#test-scripts-download-txt").click(function (event) {
            var content = document.getElementById('test_scripts').value;
            if (!content) {
                return;
            }
            downloadText(content, 'TestScripts.txt');
        });

        $("#test-scripts-tool-download-txt").click(function (event) {
            var content = document.getElementById('tool_test_script').value;
            if (!content) {
                return;
            }
            downloadText(content, 'TestScriptsForTool.txt');
        });

        $("#test-plan-download-pdf").click(function (event) {
            var content = document.getElementById('test_plan').value;
            if (!content) {
                return;
            }
            downloadPDF(content, 'TestPlan.pdf');
        });
        $("#test-case-download-pdf").click(function (event) {
            var content = document.getElementById('test_cases').value;
            if (!content) {
                return;
            }
            downloadPDF(content, 'TestCases.pdf');
        });
        $("#test-scripts-download-pdf").click(function (event) {
            var content = document.getElementById('test_scripts').value;
            if (!content) {
                return;
            }
            downloadPDF(content, 'TestScripts.pdf');
        });

        $("#test-scripts-tool-download-pdf").click(function (event) {
            var content = document.getElementById('tool_test_script').value;
            if (!content) {
                return;
            }
            downloadPDF(content, 'TestScriptsForTool.pdf');
        });
    });

    $("#generate_test_plan_button").click(function (event) {
        $("#preloader").show();
        event.preventDefault();
        asyncTestFunction('testplan');
    }
    );

    $("#generate_test_cases_button").click(function (event) {
        $("#preloader").show();
        event.preventDefault();
        asyncTestFunction('testcase');
    }
    );

    $("#generate_test_scripts_button").click(function (event) {
        $("#preloader").show();
        event.preventDefault();
        asyncTestFunction('testscript');
    }
    );

    $("#generate_tool_test_scripts_button").click(function (event) {
        $("#preloader").show();
        event.preventDefault();
        asyncTestFunction('tooltestscript');
    }
    );

})

async function asyncTestFunction(eventType) {

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

    let url = '';

    if (eventType === 'testplan') {
        url = window.location.href.replace('\/#', '').replace('#', '') + '/generatetestplan';
    }
    else if (eventType === 'testcase') {
        url = window.location.href.replace('\/#', '').replace('#', '') + '/generatetestcases';
    }
    else if (eventType === 'testscript') {
        url = window.location.href.replace('\/#', '').replace('#', '') + '/generatetestscripts';
    }
    else if (eventType === 'tooltestscript') {
        url = window.location.href.replace('\/#', '').replace('#', '') + '/generatetooltestscripts';
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

            if (eventType === 'testplan') {
                document.getElementById('test_plan').value = jsonResponse.response;
            }
            else if (eventType === 'testcase') {
                document.getElementById('test_cases').value = jsonResponse.response;
            }
            else if (eventType === 'testscript') {
                document.getElementById('test_scripts').value = jsonResponse.response;
            }
            else if (eventType === 'tooltestscript') {
                document.getElementById('tool_test_script').value = jsonResponse.response;
            }
            $("#preloader").fadeOut();
            openTab(event, 'systemTestingTab', 'st-link');
        } else {
            throw new Error('Network response was not ok.');
        }
    } catch (error) {
        $("#preloader").fadeOut();
        console.error('There has been a problem with your fetch operation:', error);
    }
}

