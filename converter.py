import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages')
from pydub import AudioSegment

audio = AudioSegment.from_file("JingleBells.mp3")
audio.export("JingleBells.wav", format="wav")
