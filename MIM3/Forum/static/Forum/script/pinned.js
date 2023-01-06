document.addEventListener('DOMContentLoaded', function() {

    // removes an organization from a person's "pinned"
    // document.getElementById('copy-email-btn').onclick = function () {}
})

function unpin(organization_id) {

    // gets the CSRF token to validate the request
    const csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    // runs a fetch command to a URL which removes the organization from the user's 'pinned'
    fetch_and_unpin(organization_id, csrftoken);

    // removes the div with the organization's information from the current feed page
    document.getElementById(`organization-${organization_id}-div`).remove()
    
}

function fetch_and_unpin(organization_id, csrftoken) {

    fetch("pinned/unpin", {
        method: "PUT",
        headers: {"X-CSRFToken":csrftoken },

        body: JSON.stringify({
            'org_pk':organization_id
        })
    })
}