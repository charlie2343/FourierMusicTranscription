import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages')
from pydub import AudioSegment

audio = AudioSegment.from_file("DancingMoonlight.mp3")
audio.export("DancingMoonlight.wav", format="wav")
