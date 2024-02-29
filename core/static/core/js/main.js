const appIcon = document.querySelector('.app__icon');
const menuIcon = document.querySelector('.menu__icon');
const navbar = document.querySelector('.navbar');
const header = document.querySelector('.header');
const xIcon = document.querySelector('.x__icon');

// Function to handle mouseover for the app icon
function handleMouseOver(event) {
    let icon = event.target;
    icon.style.transform = 'scale(1.02)';   
}

// Function to handle mouseout for the app icon
function handleMouseOut(event) {
    let icon = event.target;
    icon.style.transform = 'scale(1)';
}

// Function to handle click for the menu icon
function handleClick(event) {
    header.classList.toggle('header__fixed');
    navbar.classList.toggle('fixed');
    xIcon.classList.toggle('hidden');
    menuIcon.classList.toggle('hidden');
}

// Function to handle click outside the navbar
function handleClickOutside(event) {
    if (!navbar.contains(event.target) && !menuIcon.contains(event.target) && !xIcon.contains(event.target)) {
        header.classList.remove('header__fixed');
        navbar.classList.remove('fixed');
        xIcon.classList.add('hidden');
        menuIcon.classList.remove('hidden');
    }
}

// When page loads
document.addEventListener('DOMContentLoaded', () => {
    // Add event listeners for the app icon
    appIcon.addEventListener('mouseover', handleMouseOver);
    appIcon.addEventListener('mouseout', handleMouseOut);

    // Add event listeners for the menu icon
    menuIcon.addEventListener('mouseover', handleMouseOver);
    menuIcon.addEventListener('mouseout', handleMouseOut);

    // Add an event listener for the menu icon: click
    menuIcon.addEventListener('click', handleClick);
    xIcon.addEventListener('click', handleClick);

    // Close navbar if click outside
    document.addEventListener('click', handleClickOutside);
});