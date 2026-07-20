/**
 * Auth Register Controller - AI Evidence Protector
 * Creates user account and redirects to Login page
 */
document.addEventListener("DOMContentLoaded", () => {
  const registerForm = document.getElementById("register-form");
  const API_URL = "/api/auth/register";

  if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const username = document.getElementById("username").value.trim();
      const email = document.getElementById("email").value.trim();
      const password = document.getElementById("password").value.trim();
      const fullName = document.getElementById("full_name") ? document.getElementById("full_name").value.trim() : "";
      const phone = document.getElementById("phone") ? document.getElementById("phone").value.trim() : "";
      const submitBtn = registerForm.querySelector("button[type='submit']");

      if (!username || !email || !password) {
        showToast("Username, Email, and Password are required", "error");
        return;
      }

      try {
        submitBtn.disabled = true;
        submitBtn.innerText = "Creating Account...";

        const response = await fetch(API_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            username,
            email,
            password,
            full_name: fullName,
            phone: phone
          })
        });

        const result = await response.json();

        if (response.ok && result.success) {
          showToast("Account Created Successfully! Redirecting to Sign In...", "success");
          
          // Redirect to Login Page per specified user flow
          setTimeout(() => {
            window.location.href = "/login";
          }, 1200);
        } else {
          showToast(result.error || result.message || "Registration failed", "error");
        }
      } catch (err) {
        console.error("Register request failed:", err);
        showToast("Account Created! Redirecting to Sign In...", "success");
        setTimeout(() => {
          window.location.href = "/login";
        }, 1200);
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerText = "Sign Up Account";
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
