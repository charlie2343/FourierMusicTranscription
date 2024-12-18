from music21 import *
import os
# Create a Music21 stream
# s = stream.Stream()
# s.append(stream.Part())
# s.append(stream.Note("C"))



s = stream.Stream()

# Create a note with a specific duration
C = note.Note("C4")
E = note.Note("E4")
G = note.Note("G4")
D = note.Note("D4")
for n in s.notes: 
    n.duration.type = "half"  # Half note

s.append(note.Note("E4"))
s.append(note.Note("D4"))
s.append(note.Note("C4"))
s.append(note.Note("D4"))
s.append(note.Note("E4"))
s.append(note.Note("E4"))
s.append(note.Note("E4"))

s.append(note.Note("D4"))
s.append(note.Note("D4"))
s.append(note.Note("D4"))
s.append(note.Note("E4"))
s.append(note.Note("G4"))
s.append(note.Note("G4"))

s.append(note.Note("D4"))
s.append(note.Note("D4"))
s.append(note.Note("E4"))
s.append(note.Note("D4"))
s.append(note.Note("C4"))

# Add another note with a duration
  # Quarter note




# Save the stream to a MusicXML file

name = input("Enter file name (without extension): ").strip()  # Remove extra spaces

# Create the full output path

output_path = os.path.expanduser(f'~/Fourier/scores/{name}')  # Expand `~` to the home directory
s.write('musicxml', fp=output_path)
print(f"MusicXML file saved to {output_path}")
