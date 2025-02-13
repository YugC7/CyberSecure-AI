// Change header background on scroll
window.addEventListener("scroll", function () {
  const header = document.querySelector(".dark-header");
  if (window.scrollY > 50) {
    header.style.background = "#000"; // Darker background on scroll
  } else {
    header.style.background = "#1f1f1f"; // Default background
  }
});

// Add a fade-in effect for the hero section on page load
document.addEventListener("DOMContentLoaded", function () {
  const heroContent = document.querySelector(".hero-content");
  const heroImage = document.querySelector(".hero-image");

  heroContent.style.opacity = 0;
  heroImage.style.opacity = 0;

  setTimeout(() => {
    heroContent.style.transition = "opacity 2s ease";
    heroImage.style.transition = "opacity 2s ease";
    heroContent.style.opacity = 1;
    heroImage.style.opacity = 1;
  }, 500);
});

// Highlight a feature card on hover
document.querySelectorAll(".feature-card").forEach(card => {
  card.addEventListener("mouseenter", () => {
    card.style.borderColor = "#00bcd4";
  });

  card.addEventListener("mouseleave", () => {
    card.style.borderColor = "transparent";
  });
});

// Add a fade-in effect to service cards on scroll
window.addEventListener("scroll", () => {
  const serviceCards = document.querySelectorAll(".service-card");
  const scrollPosition = window.scrollY + window.innerHeight;

  serviceCards.forEach(card => {
    if (card.offsetTop < scrollPosition) {
      card.style.opacity = 1;
      card.style.transform = "translateY(0)";
      card.style.transition = "opacity 1s ease, transform 1s ease";
    }
  });
});

// Initialize service cards as hidden
document.querySelectorAll(".service-card").forEach(card => {
  card.style.opacity = 0;
  card.style.transform = "translateY(20px)";
});

// Add a fade-in effect for the home section content
document.addEventListener("DOMContentLoaded", function () {
  const homeContent = document.querySelector(".home-content");
  const homeImage = document.querySelector(".home-image");

  homeContent.style.opacity = 0;
  homeImage.style.opacity = 0;

  setTimeout(() => {
    homeContent.style.transition = "opacity 1.5s ease";
    homeImage.style.transition = "opacity 1.5s ease";
    homeContent.style.opacity = 1;
    homeImage.style.opacity = 1;
  }, 500);
});

// Handle contact form submission
document.querySelector(".contact-form").addEventListener("submit", function (event) {
  event.preventDefault(); // Prevent default form submission behavior

  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const message = document.getElementById("message").value;

  if (name && email && message) {
    alert("Thank you for reaching out! We will get back to you soon.");
    // Clear the form fields after submission
    document.getElementById("name").value = "";
    document.getElementById("email").value = "";
    document.getElementById("message").value = "";
  } else {
    alert("Please fill in all fields before submitting.");
  }
});

// Chatbot functionality
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const chatboxMessages = document.getElementById("chatbox-messages");

// Backend URL for Flask API
const API_URL = 'http://127.0.0.1:5000/ask';

// Add messages to chatbox
function addMessage(content, sender = "user") {
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message", sender === "bot" ? "bot-message" : "user-message");
  messageDiv.textContent = content;
  chatboxMessages.appendChild(messageDiv);
  chatboxMessages.scrollTop = chatboxMessages.scrollHeight; // Auto-scroll to the latest message
}

// Handle user input and fetch AI response
async function handleUserQuery(query) {
  addMessage(query, "user");
  userInput.value = ""; // Clear input field

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });

    const data = await response.json();
    if (response.ok) {
      addMessage(data.answer, "bot");
    } else {
      addMessage("⚠ Error: Unable to process your request.", "bot");
    }
  } catch (error) {
    addMessage("⚠ Network error. Please try again.", "bot");
  }
}

// Event Listeners
sendBtn.addEventListener("click", () => {
  const userQuery = userInput.value.trim();
  if (userQuery) {
    handleUserQuery(userQuery);
  }
});

userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    sendBtn.click();
  }
});

// Back to Top Button
const backToTopBtn = document.getElementById("back-to-top");

window.addEventListener("scroll", () => {
  if (window.scrollY > 300) {
    backToTopBtn.style.display = "block";
  } else {
    backToTopBtn.style.display = "none";
  }
});

backToTopBtn.addEventListener("click", () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
});
