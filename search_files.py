import os
lines = list()

for(dirname,dirs,files) in os.walk('./train_data'):
	for filename in files:
		if filename.endswith('.png'):
			thefile = os.path.join(dirname,filename)

			lines.append(thefile)

lines.sort()

# print lines
with open('file_name.txt','w') as f:
	for ii in lines:
		f.write(ii+'\n')
	f.close()


