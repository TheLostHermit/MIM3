
// function that toggles the button for opening and closing an event
function toggle_open(event_id) {

    OPEN_OPTIONS = {
        "open": ["true", "This event is open. Click to close"],
        "closed": ["false", "This event is closed. Click to open"]
    }

    const toggle_button = document.getElementById(`toggle-open-event-${event_id}-btn`);

    // getting the CSRFToken for the request
    const csrftoken = document.querySelector(`#event-${event_id}-change-div [name='csrfmiddlewaretoken']`).value;

    // changing the value/appearance of the button and sending the PUT request to the server

    // if the event is currently open
    if (toggle_button.value == OPEN_OPTIONS["open"][0]) {

        new_button_value = "closed";             
        
    }

    else {
        new_button_value = "open";
    }

    toggle_button.value = OPEN_OPTIONS[new_button_value][0];
    toggle_button.innerHTML = OPEN_OPTIONS[new_button_value][1];
    fetch_and_toggle_open(event_id, OPEN_OPTIONS[new_button_value][0], csrftoken);
}

// function that toggles the visibility and validity of the change form
function toggle_change(this_button,event_id) {

    const CHANGE_OPTIONS = {
        "false" : ["none", "Change Event Date or Time"],
        "true" : ["block", "Discard changes to event"]
    };
    
    const form_div = document.getElementById(`event-${event_id}-change-div`);
    const clicked_button = this_button;

    // if the div to change values is currently not being displayed
    if (clicked_button.value === CHANGE_OPTIONS["false"][0]) {

        // display it 
        form_div.style.display = CHANGE_OPTIONS["true"][0];
        clicked_button.value = CHANGE_OPTIONS["true"][0];
        clicked_button.innerHTML = CHANGE_OPTIONS["true"][1];
    }

    //else vice versa (don't display it)
    else if (clicked_button.value === CHANGE_OPTIONS["true"][0]){

        form_div.style.display = CHANGE_OPTIONS["false"][0];
        clicked_button.value = CHANGE_OPTIONS["false"][0];
        clicked_button.innerHTML = CHANGE_OPTIONS["false"][1];
    }
}

// warns the user before they delete an event by displaying a confirmation button
function delete_event_warning(event_id) {
    document.getElementById(`confirm-delete-${event_id}-div`).style.display = "Block"    
}

// hides the warning for the user deleting an event
function cancel_delete_event(event_id) {
    document.getElementById(`confirm-delete-${event_id}-div`).style.display = "None"
}

// deletes the div on the frontend and sends a put request to delete the requested event
function delete_event(event_id) {    

    const post_id = document.getElementById('post-id-input').value;
    const event_change_div = document.getElementById(`event-${event_id}-change-div`)
    const csrftoken = event_change_div.querySelector(`#event-${event_id}-change-div [name='csrfmiddlewaretoken']`).value;

    // deleting the div on the front end
    document.getElementById(`event-${event_id}-div`).remove();

    
    fetch(`${window.location.origin}/Forum/change_event/`, {
        method: "PUT",
        headers: {"X-CSRFToken":csrftoken },
    
        body: JSON.stringify({
            'action': 'delete',
            'target_event': event_id,
            'target_post': post_id

        })
    })
}

function fetch_and_toggle_open(event_id, open, csrftoken) {

    fetch(`${window.location.origin}/Forum/change_event/`, {
        method: "PUT",
        headers: {"X-CSRFToken":csrftoken },
    
        body: JSON.stringify({
            'open':open,
            'action':'toggle_open',
            'target_event':event_id,
        })
    })

}