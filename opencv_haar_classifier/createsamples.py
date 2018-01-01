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
tmpfile  = 'tmp';

parser = argparse.ArgumentParser(description='using opencv_createsamples to create multiple samples')
parser.add_argument('-pos', help='txt file name which contains the positive file names',required = True)
parser.add_argument('-neg', help='txt file name which contains the negative file names',required=True)
parser.add_argument('-vec', help='vec file output dir',required=True)
args = parser.parse_args()

print args

#if (len(len(sys.argv)) < 3):
#    print "Usage: python createtrainsamples.py\n";
#    print "  <positives_collection_filename>\n";
#    print "  <negatives_collection_filename>\n";
#    print "  <output_dirname>\n";
#    exit();

positive  = args.pos;
negative  = args.neg;
outputdir = args.vec;
#if (len(args) > 2):
#	totalnum     = args[3] 
#$cmd          = argx[4] if (len(args) > 3);

with open(positive,'r') as pos:
	positives = pos.readlines()
print positives
with open(negative,'r') as neg:
	negatives = neg.readlines()
#open(POSITIVE, "< $positive");
#my @positives = <POSITIVE>;
#close(POSITIVE);

#open(NEGATIVE, "< $negative");
#my @negatives = <NEGATIVE>;
#close(NEGATIVE);

# number of generated images from one image so that total will be $totalnum
numfloor  = int(totalnum / len(positives));
numremain = totalnum - numfloor * len(positives);

# Get the directory name of positives
imgdir = positives[0];
imgdirlen = len(imgdir);

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

  			print>>text_file, item
  			print item

    #open(TMP, "> $tmpfile");
    #print TMP @localnegatives;
    #close(TMP);
    #system("cat $tmpfile");

    #!chomp($img);
    vec = "C:\\Users\\tingt\\Desktop\\Resistor\\opencv-haar-classifier-training\\samples\\samples.vec"#outputdir+substr(img, imgdirlen) +".vec" ;
    print "{cmd} -img {img} -bg {tmpfile} -vec {vec} -num {num}".format(cmd=cmd,img= img,tmpfile = negative,vec=vec,num=num)
    os.system("{cmd} -img {img} -bg {tmpfile} -vec {vec} -num {num}".format(cmd=cmd,img= img,tmpfile = negative,vec=vec,num=num));
#unlink($tmpfile);
