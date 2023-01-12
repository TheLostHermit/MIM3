
// Button to copy emails in the displayed list to the clipboard (reset function resets the button message)
function copy_emails(this_button, emails) {

    navigator.clipboard.writeText(emails);
    const current_button = this_button;
    current_button.innerHTML = "Copied";
    setTimeout(function () {
        reset_email_btn(current_button.id)
    }, 3000);
}

function reset_email_btn(button_id) {
    document.getElementById(button_id).innerHTML = "Copy Emails for this List"
}

// utility function to troubleshoot radio values
function display_radio_value() {
    var ele = document.querySelectorAll('input[type="radio"]');

    for (i=0; i< ele.length; i++) {

        if (ele[i].checked) {
            console.log(ele[i])

        }        
    }
}