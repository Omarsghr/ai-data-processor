from pydub import AudioSegment, silence

def detect_silence_gaps(audio_file_path,silence_thresh=-50, min_silence_len=1000):
    """scans frequencies to find gaps in speech for automatic cuts .
    - silence_thresh : anything quiter than this (in dB)is considered as silence
    -min_silence_len : the minimum length of silence to be considered as a gap (in ms)
    """
    audio = AudioSegment.from_file(audio_file_path)
    # this function finds the starts and end timestamps of silence 
    slient_ranges = silence.detect_silence(
        audio, 
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh
    )
    #convert the timestamps from ms to seconds
    formatted_cuts = []
    for start, end in slient_ranges:
        formatted_cuts.append({
            "start": start / 1000,  # convert ms to s
            "end": end / 1000, # convert from ms to s
            "duration": (end - start) / 1000, # duration of silence in seconds
            "action": "cut"
        })
    return formatted_cuts
if __name__ == "__main__":
    # Test with a local audio file
    test_file = "assets/raw_audio.mp3"
    try:
        cuts = detect_silence_gaps(test_file)
        print(f"Detected {len(cuts)} silence gaps for automatic cutting.")
        for cut in cuts:
            print(f"Cut from {cut['start']}s to {cut['end']}s")
    except Exception as e:
        print(f"Error: {e}")