#get mfcc
HCopy -C  config.feat -S feats.scp
#create gram.txt
echo '(< speech | sil | noise >)' > gram.txt
#create dict.txt
echo speech [speech] speech > dict.txt
echo noise [noise] noise >> dict.txt
echo sil [sil] sil >> dict.txt
#get the net from the gram.txt
HParse -A -D -T 1 gram.txt net.slf
#check the mistake
HSGen -A -D -n 10 -s net.slf dict.txt
#get the result
HVite -A -D -T 1 -H vad.gmm -L en_4092_a.mlf -w net.slf dict.txt vad.gmm.list chen_0004092_A.mfcc
HVite -A -D -T 1 -H vad.gmm -L en_4092_b.mlf -w net.slf dict.txt vad.gmm.list chen_0004092_B.mfcc
#process the HTK result to .trans
eval python cut_htkres.py a
eval python cut_htkres.py b

