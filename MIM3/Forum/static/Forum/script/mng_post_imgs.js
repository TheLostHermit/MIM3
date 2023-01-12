function delete_image(post_img_id) {

    // gets the CSRF token to validate the request
    const csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    // gets the ID of the post to use the post image url
    const post_id = document.getElementById('post-id-input').value;
    // runs a fetch command to a URL which removes the organization from the user's 'pinned'
    fetch_and_delete(post_img_id, post_id, csrftoken);

    // removes the div with the organization's information from the current feed page
    document.getElementById(`img-${post_img_id}-div`).remove();
    
}

function toggle_icon(this_button, image_id) {

    // gets the CSRF token to validate the request
    const csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    // gets the ID of the post to use the post image url
    const post_id = document.getElementById('post-id-input').value;

    // options for the icon button responsible for toggling icon status
    const ICON_OPTIONS = {
        "true": ["true", "This image is an icon. Click to remove icon status"],
        "false": ["false", "Make this image an icon"]
    }

    // (button in question)
    clicked_button = this_button;
    console.log(clicked_button.value)

    // if the image is currently an icon, make that false and vice versa
    if (clicked_button.value == ICON_OPTIONS["true"][0]) {

        clicked_button.innerHTML = ICON_OPTIONS["false"][1];
        clicked_button.value = ICON_OPTIONS["false"][0];
        fetch_and_toggle_icon(image_id, "false", post_id, csrftoken);

    }

    else if (clicked_button.value == ICON_OPTIONS["false"][0]) {

        clicked_button.innerHTML = ICON_OPTIONS["true"][1];
        clicked_button.value = ICON_OPTIONS["true"][0];
        fetch_and_toggle_icon(image_id, "true", post_id, csrftoken);
    }
}

// functions responsible for fetches to the server

function fetch_and_delete(post_img_id, post_id, csrftoken) {

    fetch(`${window.location.origin}/Forum/change_imgs/${post_id}`, {
        method: "PUT",
        headers: {"X-CSRFToken":csrftoken },

        body: JSON.stringify({
            'img_pk':post_img_id,
            'delete':"delete",
        })
    })
}

function fetch_and_toggle_icon(image_id, icon_status, post_id, csrftoken) {

    fetch(`${window.location.origin}/Forum/change_imgs/${post_id}`, {
    method: "PUT",
    headers: {"X-CSRFToken":csrftoken },

    body: JSON.stringify({
        'img_pk':image_id,
        'icon_status':icon_status
    })
})
}