# -*- coding:utf-8 -*-
import sys
import librosa
from math import *
reload(sys)
sys.setdefaultencoding("utf-8")


def readfile(fname):
    return librosa.load(fname, sr=None)


def cut_file(audiofile, sr):
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

# Gauess function
def Gauess(u, var, x):
    return exp(-(x-u)**2.0/(2.0*var))/sqrt(2.0*pi*var)


def output(filename):
    #get the energy
    audiofile, sr = readfile(filename+".wav")
    windows = cut_file(audiofile, sr)
    energy = []
    for i in range(0, len(windows)):
        energy.append(get_energy(windows[i]))

    #get training data
    try:
        f = open(filename+"_data.txt", "r")
        data = f.read().split()
        spe_u = float(data[0]) #高斯分布中speech的期望
        spe_var = float(data[1]) #高斯分布中speech的
        sil_u = float(data[2])  #高斯分布中sil的期望
        sil_var = float(data[3]) #高斯分布中sil的方差
        f.close()
    except:
        spe_u, spe_var, sil_u, sil_var = 0.5, 1,  1e-05, 1e-8

    #VAD
    sil_before = True
    sil_start = 0
    speech_start = 0
    res = open(filename+".trans", "wb")
    for i in range(len(windows)):
                # 计算第ｉ帧是speech、sil的概率
        if(energy[i] > 1):  # 能量太大必然是speech
            p_spe = 1
            p_sil = 0
        elif(energy[i] < 1e-8):  # 能量太小必然是sil
            p_sil = 1
            p_spe = 0
        else:
            p_spe = Gauess(spe_u, spe_var, energy[i])/(Gauess(
                spe_u, spe_var, energy[i])+Gauess(sil_u, sil_var, energy[i]))
            p_sil = 1.0 - p_spe

        if(p_spe > p_sil):   # 该帧speech概率大
            if(sil_before):  # 如果之前是sil的话，说明此时speech开始, sil结束，　需要写入之前记录的sil段
                sil_before = False
                res.write(str(sil_start*12.5) + " " +
                          str(i*12.5) + " sil\n")
                speech_start = i

        else:     # 该帧sil概率大
            if(not sil_before):  # 如果之前是speech的话，说明此时sil开始, speech结束，　需要写入之前记录的speech段
                sil_before = True
                res.write(str(speech_start*12.5) + " " +
                          str(i*12.5) + " speech\n")
                sil_start = i
    # 将结尾一段的状态写入
    if(sil_before):
        res.write(str(sil_start*12.5) + " " +
                  str(len(audiofile)/sr*1000) + " sil\n")
    else:
        res.write(str(speech_start*12.5) + " " +
                  str(len(audiofile)/sr*1000) + " speech\n")
    print filename+".trans has been created, with the Gauessian data: speech_mean:{} speech_varience:{} sil_mean:{} sil:varience:{}".format(spe_u, spe_var, sil_u, sil_var)

output("en_4092_b")
