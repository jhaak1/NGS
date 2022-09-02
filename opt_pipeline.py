import sys
import argparse
import subprocess

#Note that bwa mem and hisat2 are of equal quality, although hisat2 is faster.  
#Use parameter sweeps to optimize the alignment beforehand.

def main():
	"""Parse args, align using hisat2, sort with samtools, add read groups for gatk, mark duplicates using picard MarkDuplicates, sort the marked duplicates file and index it, recalibrate base quality scores using BaseRecalibrator and ApplyBQSR, use HaplotypeCaller to call variants, calculate mean MAPQ score, number of variants, and mean QUAL score"""
	args = parse_args()
	
	#Input the base file name and print it to the screen.
	subprocess.run("echo " + args.input_sample_name, stderr = subprocess.PIPE, shell = True)
	
		
	#Align sequences to reference genome using hisat2.
	#Before the alignment, use parameter sweeps to determine the optimal --mp, --rdg, and --rfg.
	#The hisat2 index files should be in the same folder as the FASTQ seq files.
	subprocess.run("hisat2 -x " + args.input_ref_name + " -1 " + args.input_sample_name + "_1.fastq -2 " + args.input_sample_name + "_2.fastq -S " + args.input_sample_name + ".bam", shell = True)
		
	#Sort the alignment using samtools.
	subprocess.run("samtools sort " + args.input_sample_name + ".bam > " + args.input_sample_name + "_sorted.bam", shell = True)
	
		
	#Add read groups for GATK.  I got an error during variant calling saying that read groups were missing, so I added this step.
	subprocess.run("picard AddOrReplaceReadGroups -I " + args.input_sample_name + "_sorted.bam -O " + args.input_sample_name + "_sorted_rg.bam -SORT_ORDER coordinate -RGID 1 -RGLB lib1 -RGPL illumina -RGSM Sample1 -CREATE_INDEX True -RGPU unit1", shell = True)
	
		
	#Mark duplicates, which will be excluded during variant calling.
	subprocess.run("picard MarkDuplicates -I " + args.input_sample_name + "_sorted_rg.bam -O " + args.input_sample_name + "_marked_dups.bam -M " + args.input_sample_name + "_marked_dups_metrics.txt", shell = True)
	
	#Sort the "marked duplicates" file.
	subprocess.run("samtools sort " + args.input_sample_name + "_marked_dups.bam > " + args.input_sample_name + "_dups_sorted.bam", shell = True)
	
	#Index the resulting file.
	subprocess.run("samtools index " + args.input_sample_name + "_dups_sorted.bam", shell = True)
	
	#Perform base quality recalibration.
	#Make sure that your SNP and indel files are indexed before this step.  You can use gatk IndexFeatureFile to do this.
	subprocess.run("gatk BaseRecalibrator -I " + args.input_sample_name + "_dups_sorted.bam -R " + args.input_vcf_ref_loc + " --known-sites " + args.known_indels_file + " --known-sites " + args.known_snps_file + " -O recal_" + args.input_sample_name + ".report", shell = True)
	subprocess.run("gatk ApplyBQSR -R " + args.input_vcf_ref_loc + " -I " + args.input_sample_name + "_dups_sorted.bam --bqsr-recal-file recal_" + args.input_sample_name + ".report -O " + args.input_sample_name + "_recal.bam", shell = True)
	
	#Call variants.
	subprocess.run("gatk HaplotypeCaller -I " + args.input_sample_name + "_recal.bam -O " + args.input_sample_name + ".vcf -R " + args.input_vcf_ref_loc, shell = True)
	
	#Calculate mean MAPQ score from recalibrated hisat2 alignment after converting the BAM file to SAM.
	subprocess.run("samtools view -h " + args.input_sample_name + "_recal.bam > " + args.input_sample_name + "_recal.sam", shell = True)
	print('Mean MAPQ Score From Recalibrated hisat2 Alignment')
	subprocess.run("grep -v '^@' " + args.input_sample_name + "_recal.sam | awk '{sum += $5; n++} END {if (n > 0) print sum/n;}'", shell = True)
	
	#Calculate total number of variants.
	print('Total Number of Variants Called by HaplotypeCaller')
	subprocess.run("grep -v '^#' " + args.input_sample_name + ".vcf | wc -l", shell = True)
	
	#Calculate mean QUAL score from final VCF file.
	print('Mean QUAL Score from VCF File')
	subprocess.run("grep -v '^#' " + args.input_sample_name + ".vcf | awk '{sum += $6; n++} END {if (n>0) print sum/n;}'", shell = True)
	
		
	
		
def parse_args():
	"""Standard argument parsing"""
	parser = argparse.ArgumentParser(description = 'Parses arguments.')
	
	parser.add_argument('-i', '--input_sample_name', type = str, required = True, help = 'Base sample name')
	parser.add_argument('-r', '--input_ref_name', type = str, required = True, help = 'Name of hisat2 index')
	parser.add_argument('-v', '--input_vcf_ref_loc', type = str, required = True, help = 'Relative or absolute location of the reference sequence for gatk')
	parser.add_argument('-k', '--known_indels_file', type = str, required = True, help = 'Name of the known indels file for base recalibration')
	parser.add_argument('-s', '--known_snps_file', type = str, required = True, help = 'Name of the known SNPs file for base recalibration')
	return parser.parse_args()
	
if __name__ == '__main__':
	sys.exit(main())
	
	
		
		
