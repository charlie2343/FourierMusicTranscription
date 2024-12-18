from music21 import * 

# Get the user settings
us = environment.UserSettings()
print(us['musescoreDirectPNGPath'])
us.delete()

# Set the path to MuseScore executable
us['musescoreDirectPNGPath'] = '/Applications/MuseScore 4.app/Contents/MacOS/mscore'
 # Replace with your MuseScore path
print("MuseScore path set successfully!")
print(us['musescoreDirectPNGPath'])

# Example paths
# Windows: us['musescoreDirectPNGPath'] = 'C:\\Program Files\\MuseScore 4\\bin\\MuseScore4.exe'
# Mac: us['musescoreDirectPNGPath'] = '/Applications/MuseScore 4.app/Contents/MacOS/mscore'
# Linux: us['musescoreDirectPNGPath'] = '/usr/bin/musescore4'


s = stream.Stream()
s.append(stream.Part())
s.show()  
# s = corpus.parse('bach/bwv65.2.xml')
# s.show()