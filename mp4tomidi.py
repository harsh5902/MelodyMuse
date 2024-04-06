from pydub import AudioSegment
import numpy as np
import librosa
from music21 import midi, stream, note
import os

# Get the absolute path to the MP4 file
# mp4_file = "-6HBGg1cAI0.mp4"
# mp4_path = os.path.abspath(mp4_file)
# print(mp4_path)

def convertToMIDI(file):
    # Load the MP4 file using pydub
    audio = AudioSegment.from_file(f"D:/Capstone/mp4_set1/{file}", format="mp4")

    # Export audio to WAV format
    output_wav = "output.wav"
    audio.export(output_wav, format="wav")

    # Load the audio file using librosa
    y, sr = librosa.load(output_wav)

    # Perform pitch detection using librosa
    pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)

    # MIDI settings
    output_stream = stream.Stream()

    # Convert pitches to MIDI notes
    for frame in range(pitches.shape[1]):
        midi_notes = []
        for pitch in pitches[:, frame]:
            if pitch > 0:  # Ignore pitches with frequency <= 0
                midi_note = int(librosa.hz_to_midi(pitch))
                midi_notes.append(midi_note)
        if midi_notes:
            output_stream.append(note.Note(np.mean(midi_notes)))  # Taking average pitch for the frame

    # Add the stream to the MIDI file
    filename = file.split(".")
    output_stream.write('midi', fp=f'D:/Capstone/musicCaps_midi/{filename[0]}.mid')


import os
# Get the list of all files and directories
path = "D:/Capstone/mp4_set1"
dir_list = os.listdir(path)

for file in dir_list:
    convertToMIDI(file)