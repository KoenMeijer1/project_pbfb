#! /usr/bin/env python

# FASTQ quality scores are encoded in 5 different formats
# each format has a unique reach

# Sanger (S)	reads between "!" and "I"
# Solexa (X)	reads between ";" and "h"
# Illumina 1.3+	reads between "@" and "h"
# Illumina 1.5+	reads between "B" and "h"
# Illumina 1.8+	reads between "!" and "J"

# This scripts prints the output of a ASCII table
# Based on the output it is possible to determine the format that is used to encode
# the quality scores in the FASTQ file.

# the os module had to be downloaded to ensure a working script
import os

# Dictionary containing all the possible ascii characters, and their corresponding 
# values used in quality scores
UniqCharDict = {
'!':33,
'"':34,
'#':35,
'$':36,
'%':37,
'&':38,
"'":39,
'(':40,
')':41,
'*':42,
'+':43,
',':44,
'-':45,
'.':46,
'/':47,
'0':48,
'1':49,
'2':50,
'3':51,
'4':52,
'5':53,
'6':54,
'7':55,
'8':56,
'9':57,
':':58,
';':59,
'<':60,
'=':61,
'>':62,
'?':63,
'@':64,
'A':65,
'B':66,
'C':67,
'D':68,
'E':69,
'F':70,
'G':71,
'H':72,
'I':73,
'J':74,
'K':75,
'L':76,
'M':77,
'N':78,
'O':79,
'P':80,
'Q':81,
'R':82,
'S':83,
'T':84,
'U':85,
'V':86,
'W':87,
'X':88,
'Y':89,
'Z':90,
'[':91,
'\\':92,
']':93,
'^':94,
'_':95,
'`':96,
'a':97,
'b':98,
'c':99,
'd':100,
'e':101,
'f':102,
'g':103,
'h':104,
'i':105,
'j':106,
'k':107,
'l':108,
'm':109,
'n':110,
'o':111,
'p':112,
'q':113,
'r':114,
's':115,
't':116,
'u':117,
'v':118,
'w':119,
'x':120,
'y':121,
'z':122,
'{':123,
'|':124,
'}':125,
'~':126 
}

# make a list of the quality scores of the sample (in this case the sample is "test_SRR4242432.fastq".
quality = os.popen("grep ^[+] -A 1 test_SRR4242432.fastq | grep -v length=51$ | grep [^\-{3:}] | tr -d '\n'").read()
qualitylist = [''.join(character) for character in quality]

qualitylength = float(len(qualitylist))

#print all characters that appear in the list as a percentage of the total
for character in UniqCharDict.keys():
	Percent = 100 * qualitylist.count(character) / qualitylength
	if Percent > 0:		
		print "%s: %4.1f" % (character,Percent)