
document.addEventListener("DOMContentLoaded", function () {

    // on load disable the volunteer buttons if the user is not logged in
    if (document.getElementById('user-logged-in').value === "False") {

        form_elements = document.volunteer_form.elements

        for (i=0; i<form_elements.length; i++) {
            form_elements[i].disabled = true
        }

    }
})

function toggle_volunteer(event_id) {

    VOLUNTEER_OPTIONS = {
        "is_volunteer":['volunteered', 'You volunteered for this event. Click to leave.'],
        "not_volunteer":['not_volunteered', 'Volunteer for this event.'],
    }

    clicked_button = document.getElementById(`event-${event_id}-btn`);
    status_field = document.getElementById(`event-${event_id}-status`);

    // if the user is already volunteered then change button and hidden inputs to that of a non-volunteer
    if (status_field.value == VOLUNTEER_OPTIONS['is_volunteer'][0]) {

        status_field.value = VOLUNTEER_OPTIONS['not_volunteer'][0];
        clicked_button.innerHTML = VOLUNTEER_OPTIONS['not_volunteer'][1];        
    }

    // and if not vice versa
    else {

        status_field.value = VOLUNTEER_OPTIONS['is_volunteer'][0];
        clicked_button.innerHTML = VOLUNTEER_OPTIONS['is_volunteer'][1];
        
    }


    
}

/*
    What I need to do:
    When a button is clicked it will perform an onclick function with the parameters
    'requested event id' and 'current status'

    clicking the button will change the current status of both the button text and the hidden input

    When the form is submitted it will send a POST request to the view function responsible for 
    managing the volunteer bids. 

    It will read each bid with the 'name' attribute, and try to perform the prescribed action to it
*/