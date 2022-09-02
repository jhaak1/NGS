# NGS
This repository contains a Python pipeline for calling variants from whole genome sequencing data.

This Python pipeline call variants using GATK HaplotypeCaller.  It takes five inputs: the base name of two paired-end FASTQ samples, the base name of hisat2 index files, the relative or absolute location of a FASTA reference sequence for GATK, the full name of a known indels file for base recalibration, and the full name of a known SNPs file for base recalibration.  Outputs include a sorted BAM file with duplicates marked and base quality scores recalibrated, a VCF file of variants, the mean MAPQ score from the hisat2 alignment, the total number of variants called, and the mean QUAL score from the VCF file.
