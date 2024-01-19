from pydub import AudioSegment

def cut_audio(input_file, output_file, time_intervals):
    audio = AudioSegment.from_file(input_file, format="mp3")

    # Initialize a list to store the audio segments to keep
    audio_segments_to_keep = []

    # Convert time intervals from seconds to milliseconds
    time_intervals_ms = [(start * 1000, end * 1000) for start, end in time_intervals]

    # Add the part before the first interval
    if time_intervals_ms[0][0] > 0:
        audio_segments_to_keep.append(audio[:time_intervals_ms[0][0]])

    # Add the parts between intervals
    for i in range(len(time_intervals_ms) - 1):
        start = time_intervals_ms[i][1]
        end = time_intervals_ms[i+1][0]
        if start < end:
            audio_segments_to_keep.append(audio[start:end])

    # Add the part after the last interval
    if time_intervals_ms[-1][1] < len(audio):
        audio_segments_to_keep.append(audio[time_intervals_ms[-1][1]:])

    # Concatenate the audio segments to keep
    final_audio = sum(audio_segments_to_keep)

    # Export the final audio to the output file
    final_audio.export(output_file, format="mp3")

if __name__ == "__main__":
    input_file = "a.mp3"
    output_file = "output_audio.mp3"

    time_intervals = [
        (0, 5),         # Remove from 0s to 5s
        (13, 19.52),    # Remove from 13s to 19.52s
        (48.52, 56.52)  # Remove from 48.52s to 56.52s
    ]

    cut_audio(input_file, output_file, time_intervals)
