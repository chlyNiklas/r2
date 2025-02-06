# r2 ~ Rehkitz Retter

## setup 


### POSIX systems (Linux, MacOS, BSD)

Make sure, that you have **git** and **python** installed.

``` sh
git clone https://github.com/chlyNiklas/r2.git

cd r2

## create a venv
python -m venv .venv

## activate the venv
source .venv/bin/activate

## install all dependencies
pip install -r requirements.txt

## start the application
python main.py

```

### Windows

Make sure, that you have **git** and **python** installed.

``` sh
## download git bash

## open git bash

## go to the directory, where you want to download r2 in.

git clone https://github.com/chlyNiklas/r2.git

cd r2

## check if you have the latest pip and wheel
python -m pip install --upgrade pip wheel setuptools

## install kivy
python -m pip install kivy

## install all other dependencies
python -m pip install opencv-python
python -m pip install numpy
python -m pip install kivymd
python -m pip install plyer
python -m pip install tk

## start the application
python main.py

```

Currently on MacOS 15.1 (Sequoia) on ARM choosing a file crashes the application, due to incompatible system API's.


## processor

[test video](https://cloud.schreifuchs.ch/s/6YL8GaMR7bjgPSP)
[test_video_clean](https://cloud.schreifuchs.ch/s/wJGQNA3G6TRdrtm)

