# Quality assessment of RNAseq data in .fastq files.
Project for course Practical Bioinformatics for Biologists (2018) by Koen Meijer and Emma Gerrits.

The file project_pbfb.py is a python script which analyzes the quality in RNAseq data in fastq files. From this github page the following files have to be downloaded: project_pbfb.py and histogram.R. These files have to be located in the directory of your fastq files. The project_pbfb.py script requires the following to be installed: NumPy and R version 3.4.3 with the ggplot2 package.

The script will automatically determine the number and name of your fastq files and will create a an outputdirectory for each file. In this output directory 6 files will be stored, of which 4 .txt files, 1 .R script and 1 .png image. The textfile output.txt contains the sequence and quality information, e.g. the quality per base and the mean quality. The quality.txt file contains the sequence of ASCII characters, originating from the fastq file. The file qualityscore.txt contains the qualityscores translated from the ASCII characters. The file sequence.txt contains the nucleotide sequence originating from the fastq file. The script histogram.R was edited by the project_pbfb.py script to locate the directory of the input file. The image qualityscores.png is the result of the histogram.R script. 

As a test datafile the file testSRR4242432.fastq can be used, which contains the first 40 lines of the original SRR4242432.fastq file which we downloaded from GEO with the SRA-toolkit in the terminal. 
