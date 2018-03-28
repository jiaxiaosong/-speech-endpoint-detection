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

def sgn(x):
    if(x>0):
        return 1
    return -1 

#得到给定音频的短时过零率
def get_ZCR(window):
    N = len(window)
    res = 0
    for m in range(1, N):
        res += abs(sgn(window[m])-sgn(window[m-1]))*hamming(N, N-m)
    return res


filename = "en_4092_b"
audiofile, sr = readfile(filename+".wav")
windows = cut_file(audiofile)
energy = []
ZCR = []
res = open(filename+".trans", "wb")

for i in range(0,len(windows)):
    energy.append(get_energy(windows[i]))
    ZCR.append(get_ZCR(windows[i]))


maxsilence = 2  #语音段中允许出现的最大静音长度
minlen = 8  #语音最短长度
status = 0  #初始默认为静音 0静音　1可能开始　２语音段
speech_len = 0 #初始语音段长度０
sil_len = 0 #初始静音段长度０

zcr1 = 20  #初始短时过零率高门限
zcr2 = 10   #初始短时过零率低门限
amp1 = 0.005
amp2 = 0.001


start = 0   #语音开始点记录
end = 0     #语音结束点

for i in range(0,len(windows)):
    goto = 0
    if(status == 2): #是语音段
        if(energy[i] > amp2 or ZCR[i] > zcr2): #保持在语音段
            speech_len += 1
        else:  #语音将要结束
            sil_len += 1
            if(sil_len < maxsilence): #静音不够长语音尚未结束
                speech_len += 1
            elif(speech_len < minlen): #静音很长　语音不够长　噪音
                status = 0
                sil_len = 0
                speech_len = 0
            else:   #语音结束
                speech_len = speech_len - sil_len/2
                end = start + speech_len - 1
                res.write(str(start*12.5) + " " +
                      str(end*12.5) + " speech\n")
                status = 0
                sil_len = 0
                speech_len = 0
    else:    #非语音段
        if(energy[i] > amp1 or ZCR[i] > zcr1):  #进入语音段
            start = max(i-speech_len-1, 1)
            status = 2
            speech_len += 1
        elif(energy[i]>amp2 or ZCR[i] > zcr2):  #可能处于语音段
            status = 1
            speech_len += 1
        else:    #静音段
            status = 0
            speech_len = 0


res.close()
