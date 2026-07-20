/**
 * Auth Register Controller - AI Evidence Protector
 */
document.addEventListener("DOMContentLoaded", () => {
  const registerForm = document.getElementById("register-form");
  const API_URL = "http://localhost:5000/api/auth/register";

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
          showToast("Account Created! Redirecting to login...", "success");
          setTimeout(() => {
            window.location.href = "login.html";
          }, 1200);
        } else {
          showToast(result.error || result.message || "Registration failed", "error");
        }
      } catch (err) {
        console.error("Register request failed:", err);
        showToast("Backend connection failed.", "error");
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerText = "Register Account";
      }
    });
  }
});
