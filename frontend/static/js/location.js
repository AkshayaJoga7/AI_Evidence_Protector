/**
 * Location Helper Module - AI Evidence Protector
 * High-Accuracy GPS Geolocation Service with accuracy radius and fallback handling
 */
const LocationService = {
  getCurrentLocation() {
    return new Promise((resolve) => {
      if (!navigator.geolocation) {
        console.warn("Geolocation API unavailable in current browser.");
        resolve(this.getFallbackLocation("Browser Geolocation API Unsupported"));
        return;
      }

      navigator.geolocation.getCurrentPosition(
        (position) => {
          resolve({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
            accuracy: position.coords.accuracy || 5,
            altitude: position.coords.altitude || null,
            timestamp: position.timestamp || Date.now(),
            isFallback: false
          });
        },
        (error) => {
          console.warn("Geolocation permission or timeout error:", error.message);
          resolve(this.getFallbackLocation(error.message));
        },
        {
          enableHighAccuracy: true,
          timeout: 8000,
          maximumAge: 0
        }
      );
    });
  },

  getFallbackLocation(reason = "Fallback Active") {
    return {
      latitude: 12.971598,
      longitude: 77.594562,
      accuracy: 12,
      timestamp: Date.now(),
      isFallback: true,
      reason: reason
    };
  },

  formatCoords(lat, lng, accuracy) {
    const safeLat = parseFloat(lat || 12.971598).toFixed(5);
    const safeLng = parseFloat(lng || 77.594562).toFixed(5);
    const accStr = accuracy ? ` (±${Math.round(accuracy)}m)` : '';
    return `📍 ${safeLat}, ${safeLng}${accStr}`;
  }
};

window.LocationService = LocationService;
