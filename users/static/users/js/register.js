const passwordFields = document.querySelectorAll('input[type="password"]');
const firstName = document.getElementById('id_first_name').value;
const lastName = document.getElementById('id_last_name').value;
const email = document.getElementById('id_email').value;
const helpText = document.querySelectorAll('.help-text-link');

// Function to check if the password has uppercase
function containsUpper(password) {
    return /[A-Z]/.test(password);
}

// Function to check if the password has lowercase
function containsLower(password) {
    return /[a-z]/.test(password);
}

// Function to check if the password has a number
function containsNumber(password) {
    return /[0-9]/.test(password);
}

// Function to check if the password has a special character
function containsSpecial(password) {
    return /[^A-Za-z0-9]/.test(password);
}

// Function to handle password 1 input
function handlePassword1(event) {
    let counter = 0;
    let field = event.target;
    let password = field.value;
    let validityBarContainer = field.parentElement.querySelector('.password-strength-container');
    let validityBar = validityBarContainer.querySelector('.password-strength-bar');
    if (containsLower(password)) {
        counter++;
        removeInvalid('lowercase-help');
    } else {
        addInvalid('lowercase-help');
    }
    if (containsUpper(password)) {
        counter++;
        removeInvalid('uppercase-help');
    } else {
        addInvalid('uppercase-help');
    }
    if (containsNumber(password)) {
        counter++;
        removeInvalid('number-help');
    } else {
        addInvalid('number-help');
    }
    if (containsSpecial(password)) {
        counter++;
        removeInvalid('special-help');
    } else {
        addInvalid('special-help');
    }
    if (password.length >= 8) {
        counter++;
        removeInvalid('length-help')
    } else {
        addInvalid('length-help');
    }
    validityBar.style.width = `${(counter / 5) * 100}%`;
}

// Function to change the color of help text dynamically
// Function to change text to green
function removeInvalid(id) {
    document.querySelector(`#${id}`).classList.remove('invalid');
    document.querySelector(`#${id}`).classList.add('valid');
}

// Function to change text to red
function addInvalid(id) {
    document.querySelector(`#${id}`).classList.add('invalid');
    document.querySelector(`#${id}`).classList.remove('valid');
}

// Function to handle second password input
function handlePassword2(event) {
    let field = event.target;
    let password = field.value;
    let validityBarContainer = field.parentElement.querySelector('.password-strength-container');
    let validityBar = validityBarContainer.querySelector('.password-strength-bar');
    if (password === passwordFields[0].value) {
        validityBar.style.width = '100%';
        removeInvalid('password-match-help');
    } else {
        validityBar.style.width = '0%';
    }
}

// Function to handle password 2
function handlePassword2(event) {
    let field = event.target;
    let password = field.value;
    let validityBarContainer = field.parentElement.querySelector('.password-strength-container');
    let validityBar = validityBarContainer.children[0];
    if (field.value === '') {
        validityBar.style.width = '0%';
        return;
    } else {
        validityBar.style.width = '100%';
    }
    
    if (password === passwordFields[0].value) {
        validityBar.style.backgroundColor = 'green';
        removeInvalid('password-match-help');
    } else {
        validityBar.style.backgroundColor = 'red';
        addInvalid('password-match-help');
    }
}

// Function to handle when help text has been clicked
function handleHelpClick(event) {
    let field = event.target;
    let helpText = field.nextElementSibling;
    helpText.classList.toggle('hidden');
}

// Function to show and display the password strength container
function showPasswordStrength(event) {
    let field = event.target;
    field.parentElement.querySelector('.password-strength-container').classList.toggle('hidden');
}
function hidePasswordStrength(event) {
    let field = event.target;
    field.parentElement.querySelector('.password-strength-container').classList.toggle('hidden');
}

// When the window loads
document.addEventListener('DOMContentLoaded', () => {
    // Add placeholders for the password fields
    passwordFields[0].placeholder = 'Password';
    passwordFields[1].placeholder = 'Confirm password';

    // Add event listeners to the first password fields
    passwordFields[0].addEventListener('input', handlePassword1);

    // Add event listener to the second password field
    passwordFields[1].addEventListener('input', handlePassword2);

    // Looping through the help text elements
    helpText.forEach(link => {
        // Add a click event listener to each help text
        link.addEventListener('click', handleHelpClick);
    })

    // Loop through password fields
    passwordFields.forEach(field => {
        // Add focus and blur event listeners to each password field
        field.addEventListener('focus', showPasswordStrength);
        field.addEventListener('blur', hidePasswordStrength);
    })
});