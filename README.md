MELODIA has been tested for python2.7. Hence we need to make a virtual environment to run python2.7 and the other dependencies.
## To create virutalenv
```
python2.7 -m pip install virtualenv

python2.7 -m virtualenv sanskrit
```

### To run the virtual environemnt

`source sanskrit/bin/activate`

### To stop the environment

`deactivate`

Link for downloading files for **Melodia**: https://github.com/justinsalamon/audio_to_midi_melodia
The page states which libraries are required for running melodia. Use the following command to install all the libraries

`python2.7 -m pip install <library_name>`

## Install the libraries only in the virtualenv
There is a list of the libraries required in the requirements.txt file.
### Simply run the file as follows

`python2.7 -m pip install -r requirements.txt`

### To save any new libraries in requirements.txt

`python2.7 -m pip freeze > requirements.txt`

## Place the files of Melodia in the Vamp folder. Use the following commands
### The standard path for VAMP

`sudo mkdir /usr/local/lib/vamp`

### Copy the files

`sudo cp /home/Downloads/...<Location_of_extracted_files> /usr/local/lib/vamp`

## To generate the melody in midi format
### Use the following command

`python2.7 audio_to_midi_melodia.py wav/1.wav midi/1.mid 60 --smooth 0.25 --minduration 0.1 --jams`

### The extraction also returns a .jams file which can be moved to another folder

```
mkdir jams

cd midi

mv *.jams ../jams
```

## To extract the melodies from multiple wav files there is a script - script_wav_midi.sh
### To run the file use the following commands

```
sudo chmod +x script_wav_midi.sh

./script_wav_midi.sh
```

## To play the midi file there is no pre-installed pulgin in Ubuntu 16.04
Download the following tool

`sudo apt-get install timidity timidity-interfaces-extra`

## To play an mid file in Timidity

`file > load > <location_of_file>`

## To manipulate the audio pieces we can use **pydub** 
* https://github.com/jiaaro/pydub
* It requires ffmpeg OR libav for manipulation of mp3 files

```
sudo apt-get install libav-tools
            or
sudo apt-get install ffmpeg
```

## To split the shloka in anushthup format
* You will have to use python3.6 as cltk supports only that version

`python Transliteration.py <location_of_shloka_file> <location_of_split_file>`

* Example:

`python Transliteration.py bhagvad_gita/original/12.txt bhagvad_gita/split/12.txt`

## To extract unique words from the text file of shlokas

`python uniquewords.py <location_of_shloka_file>`

* Example:

`python uniquewords.py bhagvad_gita/split/12.txt`