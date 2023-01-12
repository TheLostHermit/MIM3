
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