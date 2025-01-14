import numpy as np
import librosa


def test_exhaust_sound(audio_path, P_ref=1.0, segment_duration=1.0, threshold=80):
    """
    Test the exhaust sound by analyzing audio in smaller segments.

    Args:
        audio_path (str): Path to the audio file.
        P_ref (float): Reference pressure level (default: 1.0).
        segment_duration (float): Duration of each segment in seconds.
        threshold (float): Loudness threshold in dB SPL.

    Returns:
        str: Detailed results for each segment and overall analysis.
    """
    try:
        # Load the audio file
        y, sr = librosa.load(audio_path, sr=None)

        # Calculate the number of samples per segment
        samples_per_segment = int(segment_duration * sr)
        total_segments = len(y) // samples_per_segment

        # Analyze each segment
        results = []
        louder_detected = False

        for i in range(total_segments):
            # Extract segment
            start = i * samples_per_segment
            end = start + samples_per_segment
            segment = y[start:end]

            # Calculate RMS for the segment
            rms = np.sqrt(np.mean(segment ** 2))

            # Convert RMS to dB SPL
            dB_SPL = 20 * np.log10(rms / P_ref) + 120

            # Check if the sound level exceeds the threshold
            if dB_SPL > threshold:
                louder_detected = True
                results.append(f"Segment {i + 1}: Louder Noise Detected (> {threshold} dB SPL, {dB_SPL:.2f} dB SPL)")
            else:
                results.append(f"Segment {i + 1}: Normal Noise Detected (<= {threshold} dB SPL, {dB_SPL:.2f} dB SPL)")

        # Combine results into a detailed report
        overall_result = "Louder Noise Detected" if louder_detected else "Normal Noise Detected"
        return f"Overall Result: {overall_result}\n" + "\n".join(results)
    except Exception as e:
        return f"Error processing audio: {str(e)}"
