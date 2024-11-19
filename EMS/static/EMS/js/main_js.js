// // JavaScript for automatic sliding
// const slides = document.querySelector('.slides');
// const slideCount = document.querySelectorAll('.slide').length;
// let currentIndex = 0;

// function showNextSlide() {
//     // Update the index
//     currentIndex = (currentIndex + 1) % slideCount;

//     // Move the slides container
//     slides.style.transform = `translateX(-${currentIndex * 100}%)`;
// }

// // Automatically slide every 3 seconds
// setInterval(showNextSlide, 5000);

const slides = document.querySelector('.slides');
const slideCount = document.querySelectorAll('.slide').length;
let currentIndex = 0;

// Function to update the slide position
function updateSlide(index) {
    slides.style.transform = `translateX(-${index * 100}%)`;
}

// Show the next slide
function showNextSlide() {
    currentIndex = (currentIndex + 1) % slideCount;
    updateSlide(currentIndex);
}

// Show the previous slide
function showPreviousSlide() {
    currentIndex = (currentIndex - 1 + slideCount) % slideCount;
    updateSlide(currentIndex);
}

// Event listeners for buttons
document.querySelector('.next').addEventListener('click', showNextSlide);
document.querySelector('.prev').addEventListener('click', showPreviousSlide);

// Automatically slide every 3 seconds
setInterval(showNextSlide, 10000);

const dropdownToggle = document.getElementById('dropdownToggle');
const dropdownContainer = document.querySelector('.dropdown-container');

// Toggle dropdown menu
dropdownToggle.addEventListener('click', () => {
    dropdownContainer.classList.toggle('active');
});

// Close dropdown when clicking outside
window.addEventListener('click', (e) => {
    if (!dropdownContainer.contains(e.target)) {
        dropdownContainer.classList.remove('active');
    }
});