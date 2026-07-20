import os
from utils.security import generate_file_sha256

class AIService:
    @staticmethod
    def analyze_evidence(file_path: str, expected_hash: str) -> dict:
        """
        Analyze evidence file integrity, compute hash match, and summarize findings.
        """
        if not os.path.exists(file_path):
            return {
                "authentic": False,
                "status": "file_not_found",
                "summary": "Evidence file could not be found on server."
            }

        current_hash = generate_file_sha256(file_path)
        is_authentic = (current_hash == expected_hash)

        if is_authentic:
            status = "verified_authentic"
            summary = "AI Integrity Check Passed: No digital tampering detected. File hash matches original capture timestamp."
        else:
            status = "tampered"
            summary = "AI Integrity Warning: File hash mismatch detected. Potential metadata or bit manipulation identified."

        return {
            "authentic": is_authentic,
            "status": status,
            "current_hash": current_hash,
            "expected_hash": expected_hash,
            "summary": summary
        }
