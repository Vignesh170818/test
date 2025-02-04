var apiUrl = "";

// function openTab(evt, tabName) {
//     // Declare all variables
//     var i, tabcontent, tablinks;
  
//     // Get all elements with class="tabcontent" and hide them
//     tabcontent = document.getElementsByClassName("tabcontent");
//     for (i = 0; i < tabcontent.length; i++) {
//       tabcontent[i].style.display = "none";
//     }
  
//     // Get all elements with class="tablinks" and remove the class "active"
//     tablinks = document.getElementsByClassName("tablinks");
//     for (i = 0; i < tablinks.length; i++) {
//       tablinks[i].className = tablinks[i].className.replace(" active", "");
//     }
  
//     // Show the current tab, and add an "active" class to the button that opened the tab
//     document.getElementById(tabName).style.display = "block";
//     let targetElem = evt.currentTarget || evt.target;
//     targetElem.className += " active";
//     // evt.currentTarget.className += " active";

// }
// Add a new entry to the history stack
window.history.pushState(null, null, window.location.href);

// Replace the current entry without adding a new one
window.history.replaceState(null, null, window.location.href);

//history.replaceState(null, null, window.location.href);
function openTab(evt, tabName, activeTab) {
    // Declare all variables
    var i, tabcontent, tablinks;
  
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("nav-link header-tab");
    for (i = 0; i < tablinks.length; i++) {
      // tablinks[i].className = tablinks[i].className.replace(" disabled", "");
      tablinks[i].classList.remove("active")
    }

    dropdowns = document.getElementsByClassName("dropdown-item header-tab");
    for (i = 0; i < dropdowns.length; i++) {
      // tablinks[i].className = tablinks[i].className.replace(" disabled", "");
      dropdowns[i].classList.remove("active")
    }
  
    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    document.getElementById(activeTab).classList.add("active")
    // let targetElem = evt.currentTarget || evt.target;
    // // targetElem.className += " disabled";
    // targetElem.className = targetElem.className.replace(" dropdown-toggle", "");
  
  }

jQuery(document).ready(function() {
    // Hide the preloader when the page loads.
    $("#preloader").fadeOut();

    // Show the preloader when the form is submitted.
    $("#gen_lite").submit(function(e) {
        $("#preloader").show();
    });

    var timeout = Number($("#session_timeout").val()) * 1000;
    setTimeout(function() {
        alert('Your session is expired. You are logged out.');
        window.location.href = "/core/logout";
    }, timeout);
});


function exportToWordFile(content, filename) {
    var converted = htmlDocx.asBlob(content);
    saveAs(converted, filename);
}

// document.getElementById('submit-button-fundesignimport').addEventListener('click', function () {
//     const content = $("#functionaldesign_html").val();
//     exportToWordFile(content, 'functionaldesign.docx');
// });
