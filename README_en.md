# hdpic
Hidden picture generator.



## Features

This python script is used to synthesize two pictures into one picture, showing only one of them when the background is black (the other is hidden at this time), and showing the other picture when the background switches to white.



## Usage

Use the command line `python hdpic.py [-h] [-s SIZE] [-o OUTPUT] [-f] [-w] pic1 pic2`

- `-s` `--size` Specifies the size of the output picture (currently, only square picture are supported).
- `-o` `--output` Specifies the output path of the output picture.
- `-f` `--force` Force mode on.
- `-w` `--wordy` Wordy mode on, print all the log.

Let's say I want to show `./kamen rider decade.jpg` on a white background and show `./sakurajima.png` on a black background, the output size is 251x251，force mode on, the command is:

`python hdpic.py -s 251 -o "./output.png" -f "./kamen rider decade.jpg" "./sakurajima.png"`