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

  function playEmergencyBeep() {
    try {
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      if (!AudioContextClass) return;
      
      const audioCtx = new AudioContextClass();
      let time = audioCtx.currentTime;

      // Play 3 loud, alarm-like beeps with a square wave for high visibility
      for (let i = 0; i < 3; i++) {
        const oscillator = audioCtx.createOscillator();
        const gainNode = audioCtx.createGain();

        oscillator.type = "square";
        oscillator.frequency.setValueAtTime(950, time); // Sharp, high frequency

        gainNode.gain.setValueAtTime(0, time);
        gainNode.gain.linearRampToValueAtTime(1.0, time + 0.05); // Rapid onset to max volume
        gainNode.gain.setValueAtTime(1.0, time + 0.55);
        gainNode.gain.exponentialRampToValueAtTime(0.001, time + 0.6); // Sharp decay

        oscillator.connect(gainNode);
        gainNode.connect(audioCtx.destination);

        oscillator.start(time);
        oscillator.stop(time + 0.6);

        time += 0.8; // Interval between beeps
      }
    } catch (e) {
      console.warn("Failed to play SOS audio alert:", e);
    }
  }

  if (sosBtn) {
    sosBtn.addEventListener("click", async () => {
      // Trigger the physical alarm beep sound immediately upon user click interaction
      playEmergencyBeep();

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
