/**
 * Audio Recorder Module - AI Evidence Protector
 * Records microphone audio streams using MediaRecorder and outputs Blob/File for evidence upload
 */
class AudioRecorderService {
  constructor() {
    this.mediaRecorder = null;
    this.audioChunks = [];
    this.isRecording = false;
  }

  async startRecording() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.audioChunks = [];
      this.mediaRecorder = new MediaRecorder(stream);
      
      this.mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          this.audioChunks.push(event.data);
        }
      };

      this.mediaRecorder.start();
      this.isRecording = true;
      return true;
    } catch (err) {
      console.error("Audio recording error:", err);
      throw new Error("Unable to access microphone.");
    }
  }

  stopRecording() {
    return new Promise((resolve) => {
      if (!this.mediaRecorder || !this.isRecording) {
        resolve(null);
        return;
      }

      this.mediaRecorder.onstop = () => {
        this.isRecording = false;
        const audioBlob = new Blob(this.audioChunks, { type: "audio/wav" });
        const audioFile = new File([audioBlob], `evidence_audio_${Date.now()}.wav`, { type: "audio/wav" });
        
        // Stop stream tracks
        this.mediaRecorder.stream.getTracks().forEach(track => track.stop());
        resolve({ blob: audioBlob, file: audioFile, audioUrl: URL.createObjectURL(audioBlob) });
      };

      this.mediaRecorder.stop();
    });
  }
}

window.AudioRecorderService = AudioRecorderService;
