document.addEventListener('DOMContentLoaded', function() {

    document.getElementById('copied-email-div').style.display = "none"

    // Gets the button for copying emails and assigns it the email
    document.getElementById('copy-email-btn').onclick = function () {

        var email_field = document.getElementById('profile-email');
        navigator.clipboard.writeText(email_field.value);

        var success_div = document.getElementById('copied-email-div');
        success_div.style.display = "block"        
        setTimeout(hide, 3000)
        

    }
})

function hide() {
    document.getElementById('copied-email-div').style.display = "none"
}