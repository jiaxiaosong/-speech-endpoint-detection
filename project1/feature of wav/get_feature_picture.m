[signal,fs,bit] = wavread('C:\Users\89364\Desktop\智能语音\homework\en_4092_a.wav');  
framelength = fs/40;  
framenumber = fix(length(signal)/framelength);
hamming = @(N,m)0.54-0.46*cos(2*3.1415926*m/(N-1));
for i = 1:framenumber;%分帧处理  
    framesignal = signal((i-1)*framelength+1:i*framelength);%提取一帧信号  
    Energy(i)= 0;
    ZCR(i) = 0;  
    for j = 1:framelength;
        Energy(i) = Energy(i) + (framesignal(j)*hamming(framelength,framelength-j-1)).^2;
        if j ~= 1
            ZCR(i) = ZCR(i) + abs(sign(framesignal(j))-sign(framesignal(j-1)))*hamming(framelength,framelength-j-1);
        end
    end  
end

subplot(3,1,1)  
plot(signal);  
title('en4092a.wav语音信号波形');
subplot(3,1,2)  
plot(Energy);  
title('短时能量')  
subplot(3,1,3)  
plot(ZCR);  
title('短时平均过零率')  
