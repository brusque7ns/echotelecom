document.addEventListener('DOMContentLoaded', function () {
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.nav-link');
    const popups = document.querySelectorAll('.popup');

    // Scroll Spy - Update Active Link
    const updateActiveLink = () => {
        let index = sections.length;

        while (--index && window.scrollY + 50 < sections[index].offsetTop) {}
        navLinks.forEach(link => link.classList.remove('active'));
        navLinks[index].classList.add('active');
    };

    // Display Popups on Load
    const displayPopups = () => {
        setTimeout(() => popups[0].classList.add('visible'), 1000); // Middle Popup
        setTimeout(() => popups[1].classList.add('visible'), 3000); // Left Popup
        setTimeout(() => popups[2].classList.add('visible'), 5000); // Right Popup
    };

    // Attach Scroll Event Listener
    window.addEventListener('scroll', updateActiveLink);

    // Initial Actions
    updateActiveLink();
    displayPopups();
});
