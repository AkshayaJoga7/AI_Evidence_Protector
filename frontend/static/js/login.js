/**
 * Auth Login Controller - AI Evidence Protector
 */
document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("login-form");
  const API_URL = "http://localhost:5000/api/auth/login";

  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const email = document.getElementById("email").value.trim();
      const password = document.getElementById("password").value.trim();
      const submitBtn = loginForm.querySelector("button[type='submit']");

      if (!email || !password) {
        showToast("Please enter email and password", "error");
        return;
      }

      try {
        submitBtn.disabled = true;
        submitBtn.innerText = "Authenticating...";

        const response = await fetch(API_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password })
        });

        const result = await response.json();

        if (response.ok && result.success) {
          showToast("Login Successful! Redirecting...", "success");
          localStorage.setItem("user_token", result.data.token);
          localStorage.setItem("user_id", result.data.user_id);
          localStorage.setItem("username", result.data.username);
          localStorage.setItem("email", result.data.email);

          setTimeout(() => {
            window.location.href = "dashboard.html";
          }, 1000);
        } else {
          showToast(result.error || result.message || "Invalid credentials", "error");
        }
      } catch (err) {
        console.error("Login request failed:", err);
        showToast("Backend connection failed. Please ensure Flask server is running.", "error");
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerText = "Secure Sign In";
      }
    });
  }
});

function showToast(message, type = "info") {
  let container = document.getElementById("toast-container");
  if (!container) {
    container = document.createElement("div");
    container.id = "toast-container";
    document.body.appendChild(container);
  }

  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.innerText = message;

  container.appendChild(toast);
  setTimeout(() => {
    toast.remove();
  }, 4000);
}
