// general function to copy text and change the display of the copying button for a few seconds
function copy_text(this_button, button_display, text) {

        navigator.clipboard.writeText(text);
        const current_button = this_button;
        current_button.innerHTML = "Copied";
        setTimeout(function () {
            reset_copy_button(current_button, button_display)
        }, 3000);
    }
    

function reset_copy_button(button, button_display) {
    button.innerHTML = button_display
}
