/**
 * Camera Capture Module - AI Evidence Protector
 * Streams webcam video and captures high-resolution photo snapshots as Files
 */
class CameraService {
  constructor(videoElementId) {
    this.videoElement = document.getElementById(videoElementId);
    this.stream = null;
  }

  async startCamera() {
    try {
      this.stream = await navigator.mediaDevices.getUserMedia({
        video: { width: { ideal: 1280 }, height: { ideal: 720 }, facingMode: "user" },
        audio: false
      });
      if (this.videoElement) {
        this.videoElement.srcObject = this.stream;
        await this.videoElement.play();
      }
      return true;
    } catch (err) {
      console.error("Camera access error:", err);
      throw new Error("Unable to access camera. Please check permissions.");
    }
  }

  stopCamera() {
    if (this.stream) {
      this.stream.getTracks().forEach(track => track.stop());
      this.stream = null;
    }
    if (this.videoElement) {
      this.videoElement.srcObject = null;
    }
  }

  takeSnapshot() {
    if (!this.videoElement) return null;
    const canvas = document.createElement("canvas");
    canvas.width = this.videoElement.videoWidth || 640;
    canvas.height = this.videoElement.videoHeight || 480;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(this.videoElement, 0, 0, canvas.width, canvas.height);
    
    return new Promise((resolve) => {
      canvas.toBlob((blob) => {
        const file = new File([blob], `evidence_photo_${Date.now()}.jpg`, { type: "image/jpeg" });
        resolve({ blob, file, dataUrl: canvas.toDataURL("image/jpeg") });
      }, "image/jpeg", 0.95);
    });
  }
}

window.CameraService = CameraService;
