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

