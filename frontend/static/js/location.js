/**
 * Location Helper Module - AI Evidence Protector
 * Wraps HTML5 Geolocation API with Promise handling and fallback coordinates
 */
const LocationService = {
  getCurrentLocation() {
    return new Promise((resolve, reject) => {
      if (!navigator.geolocation) {
        reject(new Error("Geolocation is not supported by your browser."));
        return;
      }

      navigator.geolocation.getCurrentPosition(
        (position) => {
          resolve({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
            accuracy: position.coords.accuracy,
            timestamp: position.timestamp
          });
        },
        (error) => {
          console.warn("Geolocation warning:", error.message);
          // Fallback location if user denies permission or location is unavailable
          resolve({
            latitude: 12.9716,
            longitude: 77.5946,
            accuracy: 50,
            timestamp: Date.now(),
            isFallback: true
          });
        },
        {
          enableHighAccuracy: true,
          timeout: 10000,
          maximumAge: 0
        }
      );
    });
  }
};

window.LocationService = LocationService;
