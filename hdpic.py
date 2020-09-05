import cv2 as cv
import numpy as np
import time
import math
import os
import argparse

DESC = '隐藏图生成器 @Laplacedoge'

class HiddenPic(object):

    def __init__(self, path_b: str, path_w: str, force: bool=True, wordy: bool=False):
        if wordy: print('\n', end='')
        self.hidden_pic = None
        if not self.load_pic(path_b, path_w, force=force, wordy=wordy):
            if wordy: print('\n[程序终止]')
            exit()

    def load_pic(self, path_b: str, path_w: str, force: bool=True, wordy: bool=False) -> bool:
        """加载图片

        :param path_b: 背景为黑色时会被隐藏的图片
        :param path_w: 背景为白色时会被隐藏的图片
        :return: 成功则返回True, 否则返回False
        """
        if wordy: print('\n', end='')
        if not os.path.isfile(path_b):
            if wordy: print('\t[load_pic: 错误, 路径\'{}\'不是文件]'.format(path_b))
            return False
        if not os.path.isfile(path_w):
            if wordy: print('\t[load_pic: 错误, 路径\'{}\'不是文件]'.format(path_w))
            return False
        self.pic_b = cv.imread(path_b, cv.IMREAD_GRAYSCALE)
        self.pic_w = cv.imread(path_w, cv.IMREAD_GRAYSCALE)
        if not force:
            if self.pic_b.shape[0] != self.pic_b.shape[1]:
                if wordy: print('\t[load_pic: 错误, 图片\'{}\'尺寸不符合要求]'.format(path_b))
                return False
            if self.pic_w.shape[0] != self.pic_w.shape[1]:
                if wordy: print('\t[load_pic: 错误, 图片\'{}\'尺寸不符合要求]'.format(path_w))
                return False
        else:
            if self.pic_b.shape[0] != self.pic_b.shape[1] or self.pic_w.shape[0] != self.pic_w.shape[1]:
                print('\t[load_pic: 图像将会被强制缩放, 最终生成的图像可能会失真!]')
        if wordy:
            _, file_name_b = os.path.split(path_b)
            _, file_name_w = os.path.split(path_w)
            print('\t[load_pic: 已加载图像\'{}\'与\'{}\']'.format(file_name_b, file_name_w))
        return True

    def dump_pic(self, path: str, force: bool=True, wordy: bool=False) -> bool:
        """将制作好的图片存储为文件

        :param path: 存储路径
        :return: 存储成功则返回True, 否则返回False
        """
        if wordy: print('\n', end='')
        if self.hidden_pic is None:
            if wordy: print('\t[dump_pic: 隐藏图未生成, 存储失败!]')
            return False
        if not force:
            if not path.lower().endswith('.png'):
                path = path + '.png'
                if wordy: print('\t[dump_pic: 输出路径已修正为\'{}\'(可以启用强制模式来关闭自动修正)]'.format(path))
            if os.path.isfile(path):
                if wordy: print('\t[dump_pic: 文件\'{}\'已存在, 存储失败!]'.format(path))
                return False
        cv.imwrite(path, self.hidden_pic)
        if wordy: print('\t[dump_pic: 文件\'{}\'已存储!]'.format(path))
        return True

    def make_hidden_pic(self, size: int, wordy: bool=False):
        """

        :param size: 图片尺寸
        :return:
        """

        if wordy: print('\n', end='')

        # 校正'size'参数, 使其为奇数(便于后面直接使用numpy的API进行计算)
        if size % 2 == 0:
            size += 1
            if wordy: print('\t[make_hidden_pic: 输出图像尺寸已校正为{}x{}]'.format(size, size))

        # 将原图转换成指定的尺寸
        self.pic_b = cv.resize(self.pic_b, (size, size), interpolation=cv.INTER_LINEAR_EXACT)
        self.pic_w = cv.resize(self.pic_w, (size, size), interpolation=cv.INTER_LINEAR_EXACT)
        if wordy: print('\t[make_hidden_pic: 图像缩放完成!]')

        # 计算像素数量
        total_pixel_num = size * size
        black_pixel_num = math.floor((total_pixel_num) / 2) + 1
        white_pixel_num = black_pixel_num

        # '黑条'与'白条'
        black_bar = np.zeros(black_pixel_num, dtype=np.uint8).reshape((black_pixel_num, 1))
        white_bar = np.full(white_pixel_num, 255, dtype=np.uint8).reshape((white_pixel_num, 1))

        # 将'黑条'与'白条'按照水平方向拼接，将其展开成1维，去除最后一个元素后reshape成边长为'size'的正方形
        rgb = np.hstack((black_bar, white_bar)).flatten()[:-1].reshape((size, size))
        if wordy: print('\t[make_hidden_pic: RGB通道已构建!]')

        # Alpha通道的构建
        alpha_b = np.append(self.pic_b.flatten(), np.array([255], dtype=np.uint8)).reshape((-1, 2))[:, 0]
        alpha_b = 255 - alpha_b

        alpha_w = np.append(self.pic_w.flatten(), np.array([255], dtype=np.uint8)).reshape((-1, 2))[:, 1]

        alpha = np.stack((alpha_b, alpha_w), axis=1).flatten()[:-1].reshape((size, size))
        if wordy: print('\t[make_hidden_pic: Alpha通道已构建!]')

        # RGBA图像合成
        self.hidden_pic = np.stack((rgb, rgb, rgb, alpha), axis=2)
        if wordy: print('\t[make_hidden_pic: RGBA图像已生成!]')


if __name__ == '__main__':
    start_time = time.time()
    parse = argparse.ArgumentParser(description=DESC)
    parse.add_argument('pic1', type=str, help='在背景为黑色时隐藏的图')
    parse.add_argument('pic2', type=str, help='在背景为白色时隐藏的图')
    parse.add_argument('-s', '--size', default=241, type=str, help='输出尺寸(默认241)')
    parse.add_argument('-o', '--output', default='./', type=str, help='输出路径(默认在当前目录)')
    parse.add_argument('-f', '--force', action='store_true', help='启动强制执行模式')
    parse.add_argument('-w', '--wordy', action='store_true', help='启动啰嗦模式')
    args = parse.parse_args()
    if args.wordy:
        if args.force:
            print('\n[已启动强制模式]')
        print('\n[已启动啰嗦模式]')
    hp = HiddenPic(args.pic1, args.pic2, force=args.force, wordy=args.wordy)
    # hp = HiddenPic(r'C:\Users\Administrator\Desktop\Kamen Rider Decade.png', r'C:\Users\Administrator\Desktop\Kamen Rider Decade Love.png')
    hp.make_hidden_pic(args.size, wordy=args.wordy)
    hp.dump_pic(args.output, force=args.force, wordy=args.wordy)
    if args.wordy: print('\n[耗时: {:.3}s]\n'.format(time.time() - start_time))
    # hp.dump_pic(r'C:\Users\Administrator\Desktop\hidden_pic.png')

