document.addEventListener('DOMContentLoaded', function() {

    // Gets the button for copying emails and assigns it the email
    document.getElementById('copy-email-btn').onclick = function () {

        var email_field = document.getElementById('organization-email');
        navigator.clipboard.writeText(email_field.value);

        document.getElementById('copy-email-btn').value = "Copied"       
        setTimeout(reset_btn, 3000)
        

    }
})

function reset_btn() {
    document.getElementById('copy-email-btn').value = "Copy Email"
}