# present.io

I really got tired of setting up my pandoc-beamer based presentations every time,
so I decided to create a helper script to setup everything for me. Please note
this is an early early version that is created for my private needs, but feel free to contribute.

## Installing

### GNU/Linux

1. Fork the repo somewhere where you won't delete it.
2. Run the `install.sh` script.
3. Run it with `presentio` from command line

`install.sh` will create a symlink towards the `presentio.py` script by
the name `presentio`.

### ~~Windows~~
Not officially supported at the moment. Feel free to support it.

## Uninstalling
Ok... :pensive:

Run the `uninstall.sh` script.

## How to use it
To get the help menu use the `-h` or `--help`:
```txt
$ presentio -h
usage: presentio [-h] [-a AUTHOR] [-t TITLE] [-f FILENAME]

optional arguments:
  -h, --help            show this help message and exit
  -a AUTHOR, --author AUTHOR
                        Author of the presentation
  -t TITLE, --title TITLE
                        Title of the presentation
  -f FILENAME, --filename FILENAME
                        Name of the file to be created
```

If you hate reading the docs, just run the script
and fill in the requested information.

```txt
$ presentio
Author of your presentation: Nemanja Mićović
Title of your presentation: Tutorial for present.io
 Created tutorial_for_present.io.md. 
 Created images directory. 
 Created compile.sh. 
 Edited compile.sh to be executable. 
 Your document Nemanja Mićović is ready! Enjoy!
```

If you prefer giving arguments, then you can:

```txt
$ presentio -a 'Nemanja Mićović' -t 'Tutorial for present.io'
 Created tutorial_for_present.io.md. 
 Created images directory. 
 Created compile.sh. 
 Edited compile.sh to be executable. 
 Your document Nemanja Mićović is ready! Enjoy! 
```

Or if you prefer long text:

```txt
$ presentio -author='Nemanja Mićović' --title='Tutorial for present.io'
 Created tutorial_for_present.io.md. 
 Created images directory. 
 Created compile.sh. 
 Edited compile.sh to be executable. 
 Your document Nemanja Mićović is ready! Enjoy! 
```

If you wish to name the file to be created,
you can give the `filename` (`-f` or `--filename`) argument.

```txt
presentio -a 'Nemanja Mićović' -t 'Tutorial for present.io' -f slides
 Created slides.md. 
 Created images directory. 
 Created compile.sh. 
 Edited compile.sh to be executable. 
 Your document Nemanja Mićović is ready! Enjoy!
```