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



# E-M step to train the model
def EM(spe_u, spe_var, sil_u, sil_var, energy):
    N = len(energy)
    N_spe = 0.0
    N_sil = 0.0
    u_spe = 0.0,
    u_sil = 0.0
    var_spe = 0.0
    var_sil = 0.0
    # E step
    for i in range(N):
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
        # M-step
        # 计算属于speech、sil的样本个数
        N_spe += p_spe
        N_sil += p_sil
        # 计算speech和sil的能量均值
        u_spe += p_spe*energy[i]
        u_sil += p_sil*energy[i]
        # 计算speech和sil的能量方差
        var_spe += p_spe*energy[i]*energy[i]
        var_sil += p_sil*energy[i]*energy[i]
    # 计算speech和sil的能量均值
    u_spe /= N_spe
    u_sil /= N_sil
    # 计算speech和sil的能量方差
    var_spe = var_spe/N_spe - u_spe*u_spe
    var_sil = var_sil/N_sil - u_sil*u_sil
    return u_spe, var_spe, u_sil, var_sil


def trainging(filename, train_time):
    #get the energy
    audiofile, sr = readfile(filename+".wav")
    windows = cut_file(audiofile, sr)
    energy = []
    for i in range(0, len(windows)):
        energy.append(get_energy(windows[i]))

    # read the training data
    try:
        f = open(filename+"_data.txt", "r")
        data = f.read().split()
        spe_u = float(data[0]) #高斯分布中speech的期望
        spe_var = float(data[1]) #高斯分布中speech的
        sil_u = float(data[2])  #高斯分布中sil的期望
        sil_var = float(data[3]) #高斯分布中sil的方差
        f.close()
    except:
        spe_u, spe_var, sil_u, sil_var = 0.5, 1, 1e-05, 1e-8
    print "train with the initial Gauessian data: speech_mean:{} speech_varience:{} sil_mean:{} sil:varience:{}".format(spe_u, spe_var, sil_u, sil_var)
    #train
    for i in range(0, train_time):
        spe_u, spe_var, sil_u, sil_var = EM(
            spe_u, spe_var, sil_u, sil_var, energy)
        print "training",i,"times"

    #output the training data
    f = open(filename+"_data.txt", "w")
    f.write("{} {} {} {}".format(
        spe_u, spe_var, sil_u, sil_var))
    f.close()
    print str(train_time)+" times train finished with the final Gauessian data: speech_mean:{} speech_varience:{} sil_mean:{} sil:varience:{}".format(spe_u, spe_var, sil_u, sil_var)

train_time = 10
trainging("en_4092_b", train_time)