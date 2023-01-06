document.addEventListener('DOMContentLoaded', function() {

    is_a_project = document.getElementById('resubmit_project');

    if ( is_a_project.value == "True") {project = true} else {project = false}
    var checkBox = document.getElementById('id_is_project');
    checkBox.checked = project;

    if (project) {document.getElementById('event-container').style.display = "block"}
    else {document.getElementById('event-container').style.display = "none"}

    // assigns onclick functions to each of the plus buttons as well as the checkbox for project info
    document.getElementById('add_new_image_btn').addEventListener('click', (event) => add_form(event, 'image'));
    document.getElementById('add_new_event_btn').addEventListener('click', (event) => add_form(event, 'event'));

    // initialize the original remove function of the first entry buttons
    document.getElementById('image-0-rm').addEventListener('click', (event) => remove_form(event, 'image', 0));
    document.getElementById('event-0-rm').addEventListener('click', (event) => remove_form(event, 'event', 0));
    
    // clicking the checkbox shows the additional information fields needed to make a post a project
    document.getElementById('id_is_project').onclick = change_project_display
})

// only displays the project event field once this is a project
function change_project_display() {

    var checkBox = document.getElementById('id_is_project');
    var project_div = document.getElementById('event-container');
    

    if (checkBox.checked == true ){
        project_div.style.display = "block";
    }

    else {
        project_div.style.display = "none";
    }
}

// function which dynamically adds forms to a formset
function add_form(e, type) {
    e.preventDefault()

    // get all the stuff in the form class
    let Form = document.querySelectorAll(`.${type}-form`);
    let formNum = Form.length;

    if (formNum < 10) {

        // duplicate the original form in the set
        let newForm = Form[0].cloneNode(true);

        // get all the parts of the duplicated form with the standard format in order to format the new form
        let formRegex = RegExp(`${type}-(\\d){1}-`, 'g');
        newForm.innerHTML = newForm.innerHTML.replace(formRegex, `${type}-${formNum}-`);      

        // insert the new form before the submit buttom and increase the number of forms the management form knows about
        document.getElementById(`${type}-container`).insertBefore(newForm, document.getElementById(`add_new_${type}_btn`));
        //document.getElementById(`${type}-container`).insertBefore(new_btn, document.getElementById(`add_new_${type}_btn`));
        document.getElementById(`id_${type}-TOTAL_FORMS`).setAttribute('value', `${formNum + 1}`)

        //the button next to the row can be used to delete that particular entry
        document.getElementById(`${type}-${formNum}-rm`).addEventListener('click', (event) => remove_form(event, type, formNum));

    } 
}

// function which removes a particular form from a formset
function remove_form(e, type, number) {

    e.preventDefault()

    // get all the stuff in the form's class
    Form = document.querySelectorAll(`.${type}-form`);
    formNum = Form.length;

    // * the first field cannot be left empty because in order to add fields we need to clone something
    if (formNum > 1) {

        Form[number].remove();
        let formRegex = RegExp(`${type}-(\\d){1}-`, 'g');

        // updates the form to account for the newly removed item
        Form = document.querySelectorAll(`.${type}-form`);
        formNum = Form.length;

        for (let i=0; i<formNum; i++) {

            // stores all the form input so it isn't lost as everything is reset
            let Form_input = Form[i].getElementsByTagName("input");

            // changes the number of each form to reflect the removal of the field 
            for (const elm of Form[i].querySelectorAll('[name], [id]', '[htmlFor]')) {
                for (const attrib of ['name', 'id']) {
                  elm[attrib] = elm[attrib].replaceAll(formRegex, `${type}-${i}-`);
                }
            }

            // updates the remove buttons so that their function reflects the correct entries
            document.getElementById(`${type}-${i}-rm`).addEventListener('click', (event) => remove_form(event, type, i));
        }

        // updates the total form count in the form management records
        document.getElementById(`id_${type}-TOTAL_FORMS`).setAttribute('value', `${formNum}`)

    }

    else {

        // if this is the only entry the field has to be cleared instead      

        Form_inputs = Form[0].getElementsByTagName("input");
        
        for (i=0; i < Form_inputs.length; i++) {
            Form_inputs[i].value = Form_inputs[i].defaultValue 
        }        
    }
}