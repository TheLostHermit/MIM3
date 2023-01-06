document.addEventListener('DOMContentLoaded', function() {

    // gets the button for toggling the pin and does that
    document.getElementById('toggle-pin-btn').onclick = function () {

        toggle_pin();

    }

    // Gets the button for copying emails and assigns it the email
    document.getElementById('copy-email-btn').onclick = function () {

        var email_field = document.getElementById('organization-email');
        navigator.clipboard.writeText(email_field.value);

        document.getElementById('copy-email-btn').value = "Copied";       
        setTimeout(reset_btn, 3000);
    }
})

// resets the copy button to its original html after the email is copied
function reset_btn() {
    document.getElementById('copy-email-btn').value = "Copy Email";
}

function toggle_pin() {

    var toggle_pin_btn = document.getElementById('toggle-pin-btn');
    const organization_id = document.getElementById('organization-id').value;
    const csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    /* if the organization is pinned and being changed then the action is to unpin 
    and the button's new function is to pin (and vice versa) */
    if (toggle_pin_btn.value === "True") {

        toggle_pin_btn.innerHTML = 'Pin';
        toggle_pin_btn.value = "False";
        action = "unpin" 
    }
    else {
        toggle_pin_btn.innerHTML = "Unpin"
        toggle_pin_btn.value = "True";
        action = "pin" 
    }

    fetch(`${window.location.origin}/Forum/pinned/change_pin`, { 

        method: "PUT",
        headers: {"X-CSRFToken":csrftoken },

        body: JSON.stringify({
            'org_pk': organization_id,
            'action': action
        })
    })

}
