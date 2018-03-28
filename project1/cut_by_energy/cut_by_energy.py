# -*- coding:utf-8 -*-
import sys
import librosa
from math import *
reload(sys)
sys.setdefaultencoding("utf-8")


def readfile(fname):
    return librosa.load(fname, sr=None)


def cut_file(audiofile):
    global sr
    res = []
    # 帧长=25ms　即sr/40数目的采样点 帧移=12.5ms
    for i in range(0, len(audiofile)-1, sr/80):
        res.append(audiofile[i:min(i+sr/40, len(audiofile)-1)])
    return res


# hamming window
def hamming(N, m):
    return (0.54-0.46*cos(2*3.1415926*m/(N-1)))


# 得到给定音频段的短时能量
def get_energy(window):
    N = len(window)
    res = 0
    for m in range(0, N):
        res += window[m]*hamming(N, N-m)*window[m]*hamming(N, N-m)
    return res


filename = "en_4092_b"
audiofile, sr = readfile(filename+".wav")
windows = cut_file(audiofile)

sil_before = True
sil_start = 0
speech_start = 0
res = open(filename+".trans", "wb")
for i in range(len(windows)):  # 该帧短时能量超过阈值
    if(get_energy(windows[i]) > 0.001):
        if(sil_before):  # 如果之前是sil的话，说明此时speech开始, sil结束，　需要写入之前记录的sil段
            sil_before = False
            res.write(str(sil_start*12.5) + " " +
                      str(i*12.5) + " sil\n")
            speech_start = i

    else:  # 该帧短时能量低于阈值
        if(not sil_before):  # 如果之前是speech的话，说明此时sil开始, speech结束，　需要写入之前记录的speech段
            sil_before = True
            res.write(str(speech_start*12.5) + " " +
                      str(i*12.5) + " speech\n")
            sil_start = i


#将结尾一段的状态写入
if(sil_before):
    res.write(str(sil_start*12.5) + " " +
              str(len(audiofile)/sr*1000) + " sil\n")
else:
    res.write(str(speech_start*12.5) + " " +
              str(len(audiofile)/sr*1000) + " speech\n")


res.close()
