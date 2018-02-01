#! /usr/bin/env python
# -----------------------------------------------------------------------------------------------
# requirements: 
# this script needs to be run from the directory where the fastq files are located
# the histogram.R script also needs to be located in this directory
# requires numpy and R version 3.4.3  with the ggplot2 package to be installed
# -----------------------------------------------------------------------------------------------
# this script will produce 4 .txt files per .fastq file found in the directory where this script 
# is run
# these files are named 'sample'_output.txt, 'sample'_quality,txt, 'sample'_qualityscore.txt and 
# 'sample'_sequence.txt
# 'sample'_qualityscore.txt is used as input for R, which makes a histogram.png which is placed
# in the same outputdirectory as the other outputfiles

# modules to be imported
import os
import glob
from numpy import median
import sys
import subprocess

# ASCII dictionary
# Illumina 1.8
ASCII = { '!':0,
'"':1,
'#':2,
'$':3,
'%':4,
'&':5,
"'":6,
'(':7,
')':8,
'*':9,
'+':10,
',':11,
'-':12,
'.':13,
'/':14,
'0':15,
'1':16,
'2':17,
'3':18,
'4':19,
'5':20,
'6':21,
'7':22,
'8':23,
'9':24,
':':25,
';':26,
'<':27,
'=':28,
'>':29,
'?':30,
'@':31,
'A':32,
'B':33,
'C':34,
'D':35,
'E':36,
'F':37,
'G':38,
'H':39,
'I':40,
'J':41,
}

# initialize settings
myfastqfiles = []
for file in glob.glob("*.fastq"): # search in the current directory all files that end with .fastq
    myfastqfiles.append(file) # append the name of each of these files to the list 'myfastqfiles'
if len(myfastqfiles) > 0: # if the length of the list is > 0 , so if there are any files found
	fastqlist = '\n'.join(myfastqfiles) # make a list called fastqlist with enters between the filenames
	print "%d FASTQ file(s) found." % (len(myfastqfiles)) # print how many .fastq files are found
else:
	fastqlist = [] # if there are no fastq files found then the fastqlist is an empty list
if len(fastqlist) > 0: # if the length of this list is > 0, to if there are fastq files found
	print "The following files will be analyzed:\n%s" % (fastqlist) # print the names of the fastq files nicely on the screen
else:  # if there are no files found
	print "No FASTQ files found.\nPlace this script in the same folder as your FASTQ files!!" # print that there are no files found
	raw_input("Press Enter to close.") # press enter to quit the script
if len(fastqlist) >0 and len(myfastqfiles) > 0: # if there are fastq files found
	raw_input("Press Enter to continue...") # after displayinghow many fastq files will be analyzed press enter to continue

# start of the script that runs on the files
for fastqfile in myfastqfiles: # the follwing lines (until the end of the script) will run on each of the files found
	# name of the sample
	sample = os.popen("grep length=..$ %s | grep -v + | tr -d @ | cut -d ' ' -f 1 | cut -d '.' -f 1 | uniq | tr -d '\n'" % (fastqfile)).read()
	path = os.getcwd() # specify your path
	os.makedirs("%s_outputfiles" % (sample)) # make a directory for the output files
	outputdirectory = "%s/%s_outputfiles" % (path, sample) # name the output directory
	Outname = "%s/%s_output" % (outputdirectory, sample) # make an output file for the contents that will also be printed to the screen
	Out = open(Outname, 'w') # oepn the _output file
	Out.write ("File name: %s\n" % (fastqfile)) # write the file name to the _output file
	Out.write ("Sample name: %s\n" % (sample))	# write the sample name to the _output file
	
	# make a list of the quality scores of the sample
	quality = os.popen("grep ^[+] -A 1 %s | grep -v length=..$ | grep [^\-{3:}] | tr -d '\n'" % (fastqfile)).read() # use shell greps to find only the lines containing the quality scores
	qualitylist = [''.join(character) for character in quality] # convert to a list
	# print the quality list to an output file
	Outfilename = "%s/%s_quality.txt" % (outputdirectory, sample) # make an outputfile and place it in the output directory
	Outfile = open(Outfilename, 'w') # open the _quality output file
	qualitystring = '\n'.join(qualitylist) # make a string of the qualitylist with enters between the characters
	Outfile.write(qualitystring) # write the quality to the the _quality output file
	Outfile.close() # close the output file
	Out.write("List of quality scores can be found in the file %s/%s_quality.txt" % (outputdirectory, sample)) # write to the _output file where the quality-score sequence can be found
		
	# total length of file
	lengthfile = os.popen("wc -l %s | cut -d ' ' -f 1" % (fastqfile)).read()
	lengthfile = int(lengthfile) # write as integer
	Out.write("Length '%s': %s lines\n" % (fastqfile,lengthfile)) # write to the _output file the length of the fastqfile
	Out.write("----------------------------------------------\n")	
	
	# length of the characterlist = length of the sequence
	qualitylength = float(len(qualitylist)) 
	seqlength = qualitylength
		
	# calcalute counts and percentage of each character and print
	Out.write("Count and percentage of each ASCII character:\n") # write to the _output file
	for character in ASCII.keys(): # calculate for each character that is in the ASCII.keys 
		Count = qualitylist.count(character) # how often each character is present in the qualitylist
		Percent = 100 * Count / qualitylength # the percentage of each character in the qualitylist
		if Count > 0 or Percent > 0: # if both are > 0 (so if the character is present)
			Out.write("%s: %.0f, %.1f\n" % (character,Count,Percent)) # then write to the _output file the character with count and percent			
			
	# translate the characters into numeric quality scores
	output_quality = [] # make a list for the translated quality scores
	for character in qualitylist: # loop through each character in qualitylist
		if character in ASCII.keys(): # if the character is in the ASCII.keys
			output_quality.append(ASCII[character]) # then append the value of that character (as defined in the ASCII dictionary) to the output_quality list
			
	# print output quality in a txt file
	Outfilescorename = "%s/%s_qualityscore.txt" % (outputdirectory, sample) # make an outputfile and place it in the output directory
	Outfilescore = open(Outfilescorename, 'w') # open the file
	output_qualitystring = [str(i) for i in output_quality] # make a string of each character
	qualityscorestring = '\n'.join(output_qualitystring) # join the characters in a new string with enters between them
	Outfilescore.write(qualityscorestring) # write the translated quality to the _qualityscore output file
	Outfilescore.close() # close the file
		
	# statistics for quality scores output
	Out.write("--------\n")
	Out.write("Quality scores:\n")
	Out.write("Translated quality scores can be found in %s/%s_qualityscore.txt\n" % (outputdirectory, sample)) # write in the _output file where the translated qualityscores can be found
	# mean of the quality scores outpot
	output_mean = sum(output_quality) / float(len(output_quality)) # calculate the mean of the translated quality scores
	Out.write("Mean quality score: %.2f\n" %(output_mean)) # write it to the _output file
	# median of the quality scores output
	output_median = median(output_quality) # calculate the median of the translated quality scores
	Out.write("Median quality score: %.0f\n" %(output_median)) # write it to the _output file
	
	# calculate quality score per base
	# first make a list of the bases
	sequence = os.popen("grep [ACGTN] -A 1 %s | grep -v [^ACGTN] | tr -d '\n'" % (fastqfile)).read() # take the lines containing the nucleotide sequence of the fasta file
	sequencelist = [''.join(base) for base in sequence] # convert the sequence in a list of elements
	# print the sequence in a txt file
	Outfilenameseq = "%s/%s_sequence.txt" % (outputdirectory, sample) # make an outputfile and place it in the output directory
	Outfileseq = open(Outfilenameseq, 'w') # open the _sequence file
	sequencestring = '\n'.join(sequencelist) # make a string of the sequence with enters between the bases
	Outfileseq.write(sequencestring) # write it to the _sequence output file
	Outfileseq.close() # close the file
		
	Aquality = [] # make emtpy list for quality scores of A
	Cquality = [] # make empty list for quality scores of C
	Gquality = [] # make empty list for quality scores of G
	Tquality = [] # make empty list for quality scores of T
	Nquality = [] # make empty list for quality scores of N
	
	if len(sequencelist) == len(output_quality): # checkpoint
		seqindex = list(enumerate(sequencelist, 0)) # add index to the sequencelist
		qualindex = list(enumerate(output_quality, 0)) # add index to the list with quality scores
		
		for index, base in seqindex: # loop through the seqindex
			if base == 'A': # if the base is A do the following command
				Aquality.append(qualindex[index]) # add the quality score with the same index as in the sequence to the Aquality list
				AQ = [element[1] for element in Aquality] # remove the indexes
			if base == 'C':
				Cquality.append(qualindex[index])
				CQ = [element[1] for element in Cquality]
			if base == 'G':
				Gquality.append(qualindex[index])
				GQ = [element[1] for element in Gquality]
			if base == 'T':
				Tquality.append(qualindex[index])
				TQ = [element[1] for element in Tquality]
			if base == 'N':
				Nquality.append(qualindex[index])
				NQ = [element[1] for element in Nquality]
	else: # display text if the checkpoint does not succeed
		print "Error: Length sequence does not match length quality output!!" # print to screen
		Out.write("Error: Length sequence does not match length quality output!!\n") # write this to the _output file
	
	# checkpoint
	if len(sequencelist) == len(AQ) + len(CQ) + len(GQ) + len(TQ) + len(NQ):
		# following lines can be placed in a loop but then the above lines also have to be looped (is more difficult)
		# statistics for quality of A's
		meanA = sum(AQ) / float((len(AQ))) # calculate the mean quality score of A's
		Out.write("Mean quality for A's: %.2f\n" % (meanA)) # write to _output file
		#statistics for quality of C's
		meanC = sum(CQ) / float((len(CQ)))
		Out.write("Mean quality for C's: %.2f\n" % (meanC))
		#statistics for quality of T's
		meanT = sum(TQ) / float((len(TQ)))
		Out.write("Mean quality for T's: %.2f\n" % (meanT))
		#statistics for quality of G's
		meanG = sum(GQ) / float((len(GQ)))
		Out.write("Mean quality for G's: %.2f\n" % (meanG))
		#statistics for quality of N's
		meanN = sum(NQ) / float((len(NQ)))
		Out.write("Mean quality for N's: %.2f\n" % (meanN))
	else: 
		print "Error in calculating quality scores!" # print to the screen
		Out.write("Error in calculating quality scores!\n") # write to the _output file
		
	# checkpoint
	if meanA * len(AQ) + meanC * len(CQ) + meanG * len(GQ) + meanT * len(TQ) + meanN * len(NQ) == sum(output_quality): # only continue if the calculations above were correct
		Out.write("--------\n")
		Out.write("Sequence information:\n")
		Out.write("The sequence can be found in %s/%s_sequence.txt\n" % (outputdirectory, sample)) # write in the _output file where the nucleotide sequence can be found
		Out.write("Sequencelength = %d nucleotides\n" % (seqlength)) # write the sequencelength to the _output file
		# Calculate GC content
		BaseList = list(set(sequence)) # all unique character in the nucleotide sequence
		for base in BaseList: # loop through these characters
			Percent = 100 * sequence.count(base) / seqlength # percentage of each base 
			Out.write("Percentage of %s's: %.2f\n" % (base, Percent)) # write percentage of each base to the _output file
		GCcontent = float(((sequence.count("C") + sequence.count("G"))*100 / seqlength)) # calculate the GC content of the sequence
		Out.write("Percentage GC content: %.2f\n" %(GCcontent)) # write it to the _output file
	else: # display text is checkpoint does not succeed
		print "Error in calculating sequence information!" # print to the screen
		Out.write("Error in calculating sequence information!") # write to the _output file
	
	print "----------------------------------------------"
	Out.write("----------------------------------------------\n")
	
	print "R comments:"
	os.system("cp %s/histogram.R %s/%s_histogram.R" % (path, outputdirectory, sample)) # copy the histogram.R file to the outputdirectory and add the sample name
	os.system("sed -i -e 's|outputdirectory|%s|g' %s/%s_histogram.R" % (outputdirectory, outputdirectory, sample)) # change the outputdirectory name in the R script
	os.system("sed -i -e 's|sample|%s|g' %s/%s_histogram.R" % (sample, outputdirectory, sample)) # change the sample name in the R script
	subprocess.check_call(['Rscript', '%s/%s_histogram.R' % (outputdirectory, sample)]) # make histogram of the qualityscores in R
	os.system("mv %s/qualityscores.png %s/%s_qualityscores.png" % (path, outputdirectory, sample)) # store output in the outputdirectory and change name
	print "----------------------------------------------"
	print "Output saved to %s" % (outputdirectory) # print to the screen that the script is finished for this sample
	# now all above will be repeated for the next .fastq file
	



		
	