function toggle_pin(this_button) {

    const toggle_pin_btn = this_button;
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
