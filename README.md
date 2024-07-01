# Eridian To English Translator

In Andy Weirs 'Project Hail Mary', Grace hacks together an eridian (music chord language) to english translator by using a freqency analysis program on a laptop taped to another laptop running excel. 

I got [nerdsniped](https://xkcd.com/356/) by the program being described as being "barely even a program—more of a script", so this is my attempt to capture the waveform of the bits of eridian the audiobook gives us and spit out a corresponding english translation. 

Grace says that he is "not a computer expert, but [he knows] some rudimentary programming" and that it only took him an hour. Only an hour, I wish! Most of the difficulty came from me doing the waveform analysis myself. Maybe it would have gone quicker if I had been less afraid to look into analysis software like https://friture.org/

DOESN'T YET WORK LOL, just spits out the notes of the loudest freqencies in each sample it takes 

```
python -m venv env
./env/scripts/activate
pip install -r requirements.txt
```

## Dev Notes / Log
- https://www.scales-chords.com/chord-namer/
- https://www.szynalski.com/tone-generator/
- may require ffmpeg on PATH?
- https://techlib.com/reference/musical_note_frequencies.htm
- https://webcammictest.com/headphones/generator/notes/
- https://www.reddit.com/r/ProjectHailMary/comments/oflvi6/humanalien_automated_translation_device/
- https://stackoverflow.com/questions/6663222/doing-fft-in-realtime
- https://www.reddit.com/r/cpp_questions/comments/12qgycz/struggling_understanding_fft_for_realtime_audio/
- real time fourier transform
- https://fftw.org/
- https://github.com/orgurar/recognotes looks interesting but idk if crepe could do the chord stuff
- 5:52:58