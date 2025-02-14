document.addEventListener("DOMContentLoaded", function () {
    const backgrounds = [
        { img: "url('/static/images/MIMO Outdoor 18dBi Sector Antenna for Base Station with N Female Type Connector-5400-6000MHz.jpg')", text: "Your Trusted Partner for High-Performance Networks!" },
        { img: "url('/static/images/How to Transfer Data From Android to Android Via Bluetooth.jpg')", text: "Reliable, High-Quality Network Hardware & Software!" },
        { img: "url('/static/images/db1ba0e4-4b8a-4aa6-9358-4af5adb82da8.jpg')", text: "Contact us for Tailored Network Solutions!" }
    ];

    let currentIndex = 0;
    const container = document.querySelector('.background-container');
    const textElement = document.getElementById('text');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');

    function updateBackground(index) {
        container.style.opacity = 0;
        setTimeout(() => {
            container.style.backgroundImage = backgrounds[index].img;
            textElement.textContent = backgrounds[index].text;
            container.style.opacity = 1;
        }, 500);
    }

    prevBtn.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + backgrounds.length) % backgrounds.length;
        updateBackground(currentIndex);
    });

    nextBtn.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % backgrounds.length;
        updateBackground(currentIndex);
    });

    setInterval(() => {
        currentIndex = (currentIndex + 1) % backgrounds.length;
        updateBackground(currentIndex);
    }, 5000);

    updateBackground(currentIndex);

    // Payment Methods
    function payWith(method) {
        const paymentUrls = {
            paypal: "https://www.paypal.com/",
            credit_card: "https://www.example.com/credit-card-payment",
            stripe: "https://www.stripe.com/",
            mpesa: "https://www.example.com/mpesa-payment",
            cashapp: "https://cash.app/"
        };

        if (paymentUrls[method]) {
            alert(`Redirecting to ${method.toUpperCase()}...`);
            window.location.href = paymentUrls[method];
        } else {
            alert("Unknown payment method!");
        }

        // Simulate a success message (for demo purposes)
        setTimeout(() => alert("Payment Successful!"), 3000);
    }

    // Check Hotspot Availability
    function checkHotspotAvailability() {
        fetch('/check_hotspot')
            .then(response => response.json())
            .then(data => {
                if (!data.available) {
                    alert("Hotspot is not available at the moment.");
                }
            })
            .catch(error => console.error("Error:", error));
    }

    // Show Phone Number Form
    function showPhoneNumberForm(speed, price) {
        document.getElementById("phoneNumberForm").style.display = "block";
        document.getElementById("speed").value = speed;
        document.getElementById("price").value = price;
    }

    // Submit Phone Number Form
    function submitPhoneNumberForm(event) {
        event.preventDefault();
        let phoneNumber = document.getElementById("phoneNumber").value;
        let speed = document.getElementById("speed").value;
        let price = document.getElementById("price").value;
        let deviceMac = "AB:CD:EF:12:34:56";  // Simulated MAC (replace with real one)
        let pin = prompt("Enter PIN to confirm payment:");

        fetch("/process_payment", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ phone: phoneNumber, speed, price, mac_address: deviceMac, pin })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Payment successful! Connecting to WiFi...");
                window.location.href = `/connect_wifi?mac=${deviceMac}`;
            } else {
                alert("Payment failed: " + data.message);
            }
        })
        .catch(error => console.error("Error:", error));
    }

    // Check WiFi Access
    function checkWiFiAccess() {
        fetch("/check_access", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            if (data.access === "granted") {
                window.location.href = "https://your_wifi_network";
            } else {
                alert(data.message);
                window.location.href = "/packages";
            }
        })
        .catch(error => console.error("Error:", error));
    }

   // Function to show the spinner
function showSpinner() {
    document.getElementById('spinner').style.display = 'flex';
}

// Function to hide the spinner
function hideSpinner() {
    document.getElementById('spinner').style.display = 'none';
}

// Bind the spinner to form submissions
document.addEventListener('DOMContentLoaded', function () {
    const forms = document.querySelectorAll('form');

    forms.forEach(function (form) {
        form.addEventListener('submit', function () {
            showSpinner();
        });
    });

    // Example: Hide the spinner after 3 seconds (for testing purposes)
    setTimeout(hideSpinner, 4000);
});
window.addEventListener('load', function() {
    hideSpinner();
});
document.getElementById("submitSupport").addEventListener("click", function () {
    let name = document.getElementById("name").value.trim();
    let email = document.getElementById("email").value.trim();
    let issue = document.getElementById("issue").value.trim();
    let emailError = document.getElementById("emailError");

    // Validate email format
    let emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
        emailError.classList.remove("d-none");
        return;
    } else {
        emailError.classList.add("d-none");
    }

    // Ensure no field is empty
    if (name === "" || email === "" || issue === "") {
        alert("All fields are required!");
        return;
    }

    // Send data to backend (Flask)
    fetch("/send-support-email", {
        method: "POST",
        body: JSON.stringify({ name: name, email: email, issue: issue }),
        headers: { "Content-Type": "application/json" }
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.success) {
            document.getElementById("supportForm").reset();
            $("#supportModal").modal("hide");
        }
    })
    .catch(error => console.error("Error:", error));
});
const technologies = document.querySelectorAll('.technology');
const modals = document.querySelectorAll('.modal');

technologies.forEach(tech => {
    tech.addEventListener('click', (event) => {
        // Prevent the link from opening the YouTube video if it's a modal click
        if (!event.target.closest('a')) { // Check if the click target is NOT inside an 'a' tag
            const modalId = tech.dataset.modal;
            openModal(modalId);
            event.preventDefault(); // Prevent the default link behavior
        }
    });
});

    function openModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = "block";
        }
    }

    function closeModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = "none";
        }
    }

    // Close modals if the user clicks outside the modal content
    window.addEventListener('click', (event) => {
        if (event.target.classList.contains('modal')) {
            modals.forEach(modal => {
                modal.style.display = "none";
            });
        }
    });
    const supportIcon = document.getElementById('support-icon');
        const chatWindow = document.getElementById('chat-window');
        const chatMessages = document.getElementById('chat-messages');
        const userInput = document.getElementById('user-input');
        const sendButton = document.getElementById('send-button');
        const chatHeader = document.getElementById('chat-header');

        const socket = io.connect('http://127.0.0.1:5000'); 

        supportIcon.addEventListener('click', () => {
            chatWindow.style.display = (chatWindow.style.display === 'block') ? 'none' : 'block';
        });

        chatHeader.addEventListener('click', () => {
            chatWindow.style.display = 'none';
        });

        sendButton.addEventListener('click', sendMessage);
        userInput.addEventListener('keyup', (event) => {
            if (event.key === 'Enter') sendMessage();
        });

        function sendMessage() {
            const message = userInput.value.trim();
            if (message === "") return;

            appendMessage(message, 'user-message');
            userInput.value = '';

            socket.emit('user_message', { message: message });
        }

        socket.on('bot_response', function(data) {
            appendMessage(data.response, 'bot-message');
        });

        socket.on('support_response', function(data) {
            appendMessage(data.response, 'support-message');
        });

        function appendMessage(message, className) {
            const msgDiv = document.createElement('div');
            msgDiv.className = className;
            msgDiv.textContent = message;
            chatMessages.appendChild(msgDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
});
