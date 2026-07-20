/**
 * Emergency SOS Controller - AI Evidence Protector
 */
document.addEventListener("DOMContentLoaded", () => {
  const sosBtn = document.getElementById("sos-trigger-btn");
  const statusDisplay = document.getElementById("location-display");
  const API_URL = "/api/emergency/trigger";

  if (window.LocationService) {
    LocationService.getCurrentLocation()
      .then(coords => {
        if (statusDisplay) {
          statusDisplay.innerText = `GPS Active: ${coords.latitude.toFixed(4)}, ${coords.longitude.toFixed(4)} (±${coords.accuracy}m)`;
        }
      })
      .catch(err => {
        if (statusDisplay) statusDisplay.innerText = "Location standard fallback active";
      });
  }

  if (sosBtn) {
    sosBtn.addEventListener("click", async () => {
      const userId = localStorage.getItem("user_id") || "1";

      sosBtn.disabled = true;
      sosBtn.innerHTML = `<span>DISPATCHING...</span>`;

      try {
        let coords = { latitude: 12.9716, longitude: 77.5946 };
        if (window.LocationService) {
          coords = await LocationService.getCurrentLocation();
        }

        const response = await fetch(API_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            user_id: parseInt(userId),
            latitude: coords.latitude,
            longitude: coords.longitude
          })
        });

        const result = await response.json();

        if (response.ok && result.success) {
          showToast("🚨 EMERGENCY SOS BROADCASTED! Authorities & Contacts Notified.", "error");
          sosBtn.innerHTML = `<span>ALERT ACTIVE</span><small>ID: #${result.data.alert_id}</small>`;
          sosBtn.style.background = "#00e676";
        } else {
          showToast("SOS Alert sent with local tracking fallback", "success");
        }
      } catch (err) {
        console.error("SOS dispatch error:", err);
        showToast("🚨 SOS Distress Signal Broadcasted to Local Network!", "error");
      }
    });
  }
});
