import pygame
import os
import math
import numpy as np

# Change the working directory to the correct path
os.chdir('/Users/charleskim/FourierMusicTranscription/Rendering')



####STUFFF 
clefs = {
        "treble": "B5",
        "bass": "D3",
        "alto": "C4"
    }
           
def findDistance(note1, note2): 
    distance = 0
    #*not accounting for # or flats
    n1_letter_val  = ord(note1[0])
    n1_octave  = int(note1[1])
    n2_letter_val  = ord(note2[0])
    n2_octave  = int(note2[1])

    # print(f"Note 1 letter: {note1[0]}, Value: ", n1_letter_val, " Octave: ", n1_octave)
    # print(f"Note 2 letter: {note2[0]}, Value: ", n2_letter_val, " Octave: ", n2_octave)
    
    distance = n1_letter_val - n2_letter_val + 8 * (n1_octave - n2_octave)
    #print(f"Distance between {note1} and {note2} = ", distance)
    
    
    # print("Letter B: ", n1_letter_val, " Octave: ", n1_octave)
    # print("Letter C: ", n2_letter_val, " Octave: ", n2_octave)
    # print("Distance: ", distance)
    return distance

def findClef(score): 
    measure = 0
    min = 9999999999999
    closestClef = ""
    for clef in clefs: 
        middlenote = clefs[clef]
        print("Middle Note: ", middlenote)
        measure = 0 
        for data in score:
            difference = findDistance(data[0], middlenote)
            
            #* emphasize close notes more
            measure += difference ** 2
            #print("Measure: ", measure)
        if measure <= min: 
            min = measure
            closestClef = clef
        
    return closestClef

#CLEF = findClef(score)


def findKeySignature(score): 
    keySignatures = { 
        # Key Signatures in the Treble Clef
        "C Major": ["C", "D", "E", "F", "G", "A", "B"],  # No sharps or flats
        "G Major": ["G", "A", "B", "C", "D", "E", "F#"],  # One sharp (F#)
        "D Major": ["D", "E", "F#", "G", "A", "B", "C#"],  # Two sharps (F#, C#)
        "A Major": ["A", "B", "C#", "D", "E", "F#", "G#"],  # Three sharps (F#, C#, G#)
        "E Major": ["E", "F#", "G#", "A", "B", "C#", "D#"],  # Four sharps (F#, C#, G#, D#)
        "B Major": ["B", "C#", "D#", "E", "F#", "G#", "A#"],  # Five sharps (F#, C#, G#, D#, A#)
        "F# Major": ["F#", "G#", "A#", "B", "C#", "D#", "E#"],  # Six sharps (F#, C#, G#, D#, A#, E#)
        "C# Major": ["C#", "D#", "E#", "F#", "G#", "A#", "B#"],  # Seven sharps (F#, C#, G#, D#, A#, E#, B#)
        "F Major": ["F", "G", "A", "Bb", "C", "D", "E"],  # One flat (Bb)
        "Bb Major": ["Bb", "C", "D", "Eb", "F", "G", "A"],  # Two flats (Bb, Eb)
        "Eb Major": ["Eb", "F", "G", "Ab", "Bb", "C", "D"],  # Three flats (Bb, Eb, Ab)
        "Ab Major": ["Ab", "Bb", "C", "Db", "Eb", "F", "G"],  # Four flats (Bb, Eb, Ab, Db)
        "Db Major": ["Db", "Eb", "F", "Gb", "Ab", "Bb", "C"],  # Five flats (Bb, Eb, Ab, Db, Gb)
        "Gb Major": ["Gb", "Ab", "Bb", "Cb", "Db", "Eb", "F"],  # Six flats (Bb, Eb, Ab, Db, Gb, Cb)
        "Cb Major": ["Cb", "Db", "Eb", "Fb", "Gb", "Ab", "Bb"],  # Seven flats (Bb, Eb, Ab, Db, Gb, Cb, Fb
                     }
    
    for key_sig in keySignatures:
        count = 0
        min = 999
        bestKey = ""
        for data in score: 
            note = data[0]
            note_name = note[0] #cuts out octave 
            #print(note_name)
            if note_name not in keySignatures[key_sig]: 
                count += 1 
        if count <= min: 
            bestKey = key_sig
        
    return bestKey
                                                                                                         
# print("Closest Clef: ", findClef(score))
#print("Key Signature: ", findKeySignature())

BPM =60
def get_duration(count): 
    min = 10
    closestnote = ""
    durations = {}
    time = count * w["interval_seconds"]
    durations["whole"] = 60/BPM * 4
    durations["half"] = durations["whole"] /2 
    durations["quarter"] = durations["whole"]/4
    durations["eighth"] = durations["whole"]/8
    durations["sixteenth"] = durations["whole"]/16
    durations["thirtysecond"] = durations["whole"]/32
    #durations["sixtyfourth"] = durations["whole"]/64
    for length in durations: 
        if abs(time-durations[length]) < min:
            closestnote = length
            min = abs(time-durations[length])
    return closestnote

def makeScore(notes): 
    score = []
    count = 0 
    for note_index in range(len(notes)): 
        if note_index == len(notes) - 1:
            continue
        cur_note = notes[note_index]
        next_note = notes[note_index + 1]
        if cur_note == next_note:
            count += 1
        else: 
            score.append((cur_note, get_duration(count)))
            count = 0
        
        for data in score: 
            note = data[0]
            if note == '': 
                count += 1
                score.remove(data)
    print("COUNT OF mess up notes: ", count)    
    return score


def getNoteCoords(score): 
    positions = []
    horizontal_position = 0
    screen_length = 800
    for data in score:
        note = data[0]
        vert_position = -10 - 5 * findDistance(note, clefs[CLEF])
        positions.append((horizontal_position, vert_position))
        horizontal_position += 15
        #wraps  around
        if horizontal_position >= screen_length: 
            horizontal_position = 0
            vert_position += 60
    return positions
        
    
def renderStaff():
    screen.blit(staff, (0, -300))
    screen.blit(staff, (0, -240))
    screen.blit(staff, (0, -180))
    screen.blit(staff, (0, -120))
    screen.blit(staff, (0, -60))
    screen.blit(staff, (0, 0))
    screen.blit(staff, (0, 60))
    screen.blit(staff, (0, 120))


def renderNote(score): 
    positions = getNoteCoords(score)
    for n in  range(len(positions)):
        screen.blit(score[n][1], positions[n])
        

########PYGAME RUNNER

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('Pygame Image Rendering')
run = True
DEFAULT_NOTE_SIZE = (100, 100)
whole = pygame.image.load('whole.png')
quarter = pygame.image.load('quarter.png')
eighth = pygame.image.load('eighth.png')
sixteenth = pygame.image.load('16th.png')
thirtysecond = pygame.image.load('32nd.png')
staff = pygame.image.load('staff.png')
score = [("C4",eighth),("C4",thirtysecond),("A4",eighth),("C4",whole),("C4",eighth),("C4",eighth),("C4",eighth)]


# Scale the image to 50x50 pixels
whole = pygame.transform.scale(whole, DEFAULT_NOTE_SIZE)

quarter = pygame.transform.scale(quarter, DEFAULT_NOTE_SIZE)  # Scale the image to 50x50 pixels
eighth = pygame.transform.scale(eighth, DEFAULT_NOTE_SIZE)
sixteenth = pygame.transform.scale(sixteenth, DEFAULT_NOTE_SIZE)
thirtysecond = pygame.transform.scale(sixteenth, DEFAULT_NOTE_SIZE)

staff = pygame.transform.scale(staff, (800, 800))
CLEF = findClef(score)
while run:
    # screen.fill((255, 255, 255))
    # screen.blit(quarter, (0, -10))
    # screen.blit(eighth, (10, 0))
    # screen.blit(sixteenth, (20, 0))
    # screen.blit(whole, (30, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    screen.fill((255, 255, 255))
    renderStaff()
    renderNote(score)
    pygame.display.update() 
    
pygame.quit()