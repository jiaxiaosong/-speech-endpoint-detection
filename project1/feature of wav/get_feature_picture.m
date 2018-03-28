[signal,fs,bit] = wavread('C:\Users\89364\Desktop\��������\homework\en_4092_a.wav');  
framelength = fs/40;  
framenumber = fix(length(signal)/framelength);
hamming = @(N,m)0.54-0.46*cos(2*3.1415926*m/(N-1));
for i = 1:framenumber;%��֡����  
    framesignal = signal((i-1)*framelength+1:i*framelength);%��ȡһ֡�ź�  
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
title('en4092a.wav�����źŲ���');
subplot(3,1,2)  
plot(Energy);  
title('��ʱ����')  
subplot(3,1,3)  
plot(ZCR);  
title('��ʱƽ��������')  
