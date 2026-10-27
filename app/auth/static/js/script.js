// make it so password gets filtered with asterix when typing it

const passwordContents = document.querySelectorAll('input[name="pass"], input[name="pass1"], input[name="pass2"]')

const checkBox = document.getElementById("showPassId")

checkBox.addEventListener("change", displayPass)

function displayPass() {
    passwordContents.forEach(function(input) {
        if (checkBox.checked) {
            input.type = "text"
        } else {
            input.type = "password"
        }
    })
}
