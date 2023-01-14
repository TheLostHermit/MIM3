// function to get the form with the search information and toggle viewing
function toggle_form(this_button, event_id) {

    DISPLAY_OPTIONS = {
        "none":['none', 'Manage Volunteers'],
        "block":['block', 'Hide Form'],
    }

    const clicked_button = this_button;
    const form_div = document.getElementById(`post-${event_id}-form-div`);

    // if the user is already none then change button and none inputs to that of a non-volunteer
    if (clicked_button.value== DISPLAY_OPTIONS['none'][0]) {

        form_div.style.display = DISPLAY_OPTIONS['block'][0];
        clicked_button.value = DISPLAY_OPTIONS['block'][0];   
        clicked_button.innerHTML = DISPLAY_OPTIONS['block'][1];        
    }

    // and if not vice versa
    else {

        form_div.style.display = DISPLAY_OPTIONS['none'][0];
        clicked_button.value = DISPLAY_OPTIONS['none'][0];
        clicked_button.innerHTML = DISPLAY_OPTIONS['none'][1];
        
    }
}