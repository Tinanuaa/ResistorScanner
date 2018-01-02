import argparse
import os
import random
import sys
##########################################################################
# Create samples from a list of images 
# (create many many samples from many images applying distortions)
#
#  perl createtrainsamples.pl <positives.dat> <negatives.dat> <vec_output_dir>
#      [<totalnum = 7000>] [<createsample_command_options = ./createsamples -w 20 -h 20...>]
#  ex) perl createtrainsamples.pl positives.dat negatives.dat samples
#
# Author: Tina Feng 
# Date  : 1/1/2018
#########################################################################
cmd = 'C:\\OpenCV\opencv\\build\\x64\\vc14\\bin\\opencv_createsamples.exe -bgcolor 0 -bgthresh 0 -maxxangle 1.1 -maxyangle 1.1 maxzangle 0.5 -maxidev 40 -w 20 -h 20';
totalnum = 1500;
tmpfile  = 'tmp.txt';

parser = argparse.ArgumentParser(description='using opencv_createsamples to create multiple samples')
parser.add_argument('-dir', help='dir for the negative,positive and vec output folder',required = True)
#parser.add_argument('-pos_dir', help='txt file name which contains the positive file names',required = True)
parser.add_argument('-pos', help='folder name which contains the positive files',required = True)
parser.add_argument('-neg', help='folder name which contains the negative file names',required=True)
parser.add_argument('-vec', help='vec file output folder name',required=True)
parser.add_argument('-totalnum', help='totalnum for the vec',required=False)
args = parser.parse_args()


parent_dir = args.dir
positive_dir  = os.path.join(parent_dir,args.pos);
negative_dir  = os.path.join(parent_dir,args.neg);
output_dir = os.path.join(parent_dir,args.vec);
totalnum     = int(args.totalnum )

positives = []
negatives = []

for file in os.listdir(positive_dir):
	#if file.endswith(".txt"):
	#print file
	if file.upper().endswith("JPG") or file.upper().endswith("JPEG"):
		positives.append(os.path.join(positive_dir,file))

for file in os.listdir(negative_dir):
	if file.upper().endswith("JPG") or file.upper().endswith("JPEG"):
		negatives.append(os.path.join(negative_dir,file))
	    

# number of generated images from one image so that total will be $totalnum
numfloor  = int(totalnum / len(positives));
numremain = totalnum - numfloor * len(positives);

imgdirlen = len(positive_dir);

for k in range(0,len(positives)):
    img = positives[k];
    num = numfloor+1 if (k < numremain) else numfloor

    # Pick up negative images randomly
    localnegatives = [];
    for i in range(0,num):
        ind = int(random.uniform(0,len(negatives)-1));
        localnegatives.append(negatives[ind]);
    
    #write_to_tmp(localnegatives)
    with open(tmpfile, "wb") as text_file:
    	for item in localnegatives:
            text_file.write(item)
            text_file.write("\r\n")
  			#print>>text_file, item+"\n"
  			#print item

    vec = os.path.join(output_dir,img[imgdirlen+1:].split('.')[0]+".vec")
    #print output_dir,vec
    print "{cmd} -img {img} -bg {tmpfile} -vec {vec} -num {num}".format(cmd=cmd,img= img,tmpfile = tmpfile,vec=vec,num=num)
    os.system("{cmd} -img {img} -bg {tmpfile} -vec {vec} -num {num}".format(cmd=cmd,img= img,tmpfile = tmpfile,vec=vec,num=num));
#unlink($tmpfile);
