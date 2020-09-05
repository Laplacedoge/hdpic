> If you wanna borwse the English version of this doc, click [here](./README_en.md).

# hdpic
隐藏图生成器



## 功能

本脚本用于将两张图合成为一张图，当图片背景为黑色时只显示其中一张图片（此时另一张处于隐藏状态），当背景切换至白色时显示另一张。



## 用法

使用命令行 `python hdpic.py [-h] [-s SIZE] [-o OUTPUT] [-f] [-w] pic1 pic2`

- `-s` `--size` 指定输出图像尺寸（目前只支持输出正方形图像）
- `-o` `--output` 指定输出图像的输出路径
- `-f` `--force` 开启强制模式
- `-w` `--wordy` 开启啰嗦模式，开启将打印所有日志

比如我想要在白色背景时显示图片`./kamen rider decade.jpg`而在黑色背景时候显示图片`./sakurajima.png`，输出尺寸为251x251，开启强制模式，命令如下：

`python hdpic.py -s 251 -o "./output.png" -f "./kamen rider decade.jpg" "./sakurajima.png"`