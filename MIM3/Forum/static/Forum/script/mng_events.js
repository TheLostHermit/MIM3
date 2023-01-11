/*
    1) onclick of "change_event" btn makes the hidden input 
    value "valid" and clicking it again makes it invalid (etc.)

    It also hides and shows the event change div

    2) clicking the "make changes" button finds the p for date and p
    for time and changes it to the inputted values, while also hiding the 
    div/making the new form's input invalid (sort of like clicking the 
    change event button)

    Make changes button sends a PUT request to the server with the 
    CSRF token, new date, new time, action ("change") and current event ID


*/

// function that toggles the visibility and validity of the change form
function toggle_change(event_id) {

    const CHANGE_VALUES = {
        "false" : ["none", "Change Event Date or Time", "invalid"],
        "true" : ["block", "Discard changes to event", "valid"]
    }

    const form_div = document.getElementById(`event-${event_id}-change-div`);
    const clicked_button = document.getElementById(`toggle-change-${event_id}-btn`);
    const validation_input = document.getElementById(`event-${event_id}-validity-input`);

    // if the div to change values is currently not being displayed
    if (clicked_button.value === CHANGE_VALUES["false"][0]) {

        // display it and change the form validity
        validation_input.value = CHANGE_VALUES["true"][2];
        form_div.style.display = CHANGE_VALUES["true"][0];
        clicked_button.value = CHANGE_VALUES["true"][0];
        clicked_button.innerHTML = CHANGE_VALUES["true"][1];
    }

    //else vice versa
    else if (clicked_button.value === CHANGE_VALUES["true"][0]){
        // display it and change the form validity
        validation_input.value = CHANGE_VALUES["false"][2];
        form_div.style.display = CHANGE_VALUES["false"][0];
        clicked_button.value = CHANGE_VALUES["false"][0];
        clicked_button.innerHTML = CHANGE_VALUES["false"][1];
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

// function to change a specific event from the list
function change_event(event_id) {

    // checks if the form can actually be inputted before doing anything
    const event_validity = document.getElementById(`event-${event_id}-validity-input`);

    if (event_validity.value == "valid") {

        // gets the toggle change button, new date from form, new time from form and makes the put request
        const toggle_button = document.getElementById(`toggle-change-${event_id}-btn`);

        // form must be accessed from child nodes because generating an unknown number of uniquely prefixed forms in context is being avoided
        const new_year = document.querySelector(`#event-${event_id}-change-div #id_date_year`).value;
        const new_month = document.querySelector(`#event-${event_id}-change-div #id_date_month`).value;
        const new_day = document.querySelector(`#event-${event_id}-change-div #id_date_day`).value;
        const new_time = document.querySelector(`#event-${event_id}-change-div #id_time`).value;
        const csrftoken = document.querySelector(`#event-${event_id}-change-div [name='csrfmiddlewaretoken']`).value;

        console.log(new_time, new_year, new_month, new_day);

        fetch_change_event(event_id, new_year, new_month, new_day, new_time, csrftoken);
        toggle_button.click();        
    }      
}

// function that makes the PUT request to the server to change the event 
// NB: Because this is a once use simple function it's left as is but if it were to be used often 
// it would take a dict input to function similarly to kwargs
function fetch_change_event(event_id, new_year, new_month, new_day, new_time, csrftoken) {

    // change the on screen inner html to reflect the change in input
    const date_p = document.getElementById(`event-${event_id}-date`);
    const time_p = document.getElementById(`event-${event_id}-time`);

    fetch(`${window.location.origin}/Forum/change_event/`, {
        method: "PUT",
        headers: {"X-CSRFToken":csrftoken },
    
        body: JSON.stringify({
            'new_year': new_year,
            'new_month': new_month,
            'new_day': new_day,
            'new_time':new_time,
            'action':'change',
            'target_event':event_id,
        })
    })

    location.reload()
}
