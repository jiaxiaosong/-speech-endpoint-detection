import sys
if(sys.argv[1] == 'a'):
	output_name = "en_4092_a"
	input_name = "chen_0004092_A"
else:
	output_name = "en_4092_b"
	input_name = "chen_0004092_B"
fin = open(input_name+".rec")
res = open(output_name+".trans","wb")
fin.readline()
fin.readline()
for line in fin.readlines():
	line = line.strip().split()
	start, end, state = int(line[0])/10000,int(line[1])/10000,line[2]
	res.write(str(start)+' '+str(end)+' '+state+'\n')

res.close()
fin.close()

