# present.io

I really got tired of setting up my pandoc-beamer based presentations every time,
so I decided to create a helper script to setup everything for me. Please note
this is an early early version that is created for my private needs, but feel free to contribute.

## Installing

### GNU/Linux

1. Fork the repo somewhere where you won't delete it.
2. Run the `install.sh` script.
3. Make sure to install python `pandoc-beamer-block` package
4. Run it with `presentio` from command line

`install.sh` will create a symlink towards the `presentio.py` script by
the name `presentio`.

Also make sure you have `pandoc` and `LaTeX` installed on your system.

### ~~Windows~~
Not officially supported at the moment. Feel free to support it.

## Uninstalling
Ok... :pensive:

Run the `uninstall.sh` script.

## How to use it
To get the help menu use the `-h` or `--help`:
```txt
$ presentio -h
usage: presentio [-h] [-a AUTHOR] [-t TITLE] [-b] [-f FILENAME]

optional arguments:
  -h, --help            show this help message and exit
  -a AUTHOR, --author AUTHOR
                        Author of the presentation
  -t TITLE, --title TITLE
                        Title of the presentation
  -b, --bibliography    Add the bibliography support
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

And if you wish to add the bibliography support in slides, use the `-b` (`--bibliography`) flag

```txt
presentio -a 'Nemanja Mićović' -t 'Tutorial for present.io' -f slides -b
 Created slides.md. 
 Created images directory. 
 Created literature.bib. 
 Created compile.sh. 
 Edited compile.sh to be executable. 
 Your document Tutorial for present.io is ready! Enjoy! 
```

To get your slides simply call the `compile.sh` script.

### Automatic compile

There are [multiple ways](https://superuser.com/questions/181517/how-to-execute-a-command-whenever-a-file-changes)
to do this. As I am using neovim, I mostly just use this command inside vim:

```
:au BufWritePost myfile.md :silent !./compile.sh
```

which causes my lovely editor to run the `compile.sh` script whenever I save the file I'm writing.
It also avoids any disk access compared to some different approaches like I've seen on internet.
