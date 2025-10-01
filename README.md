# NGS
This repository contains the following: 
1. An automated Python pipeline for calling variants from whole genome sequencing data (opt_pipeline.py).
2. A pipeline for analyzing bulk RNA-seq data (RNA_seq_Workflow.pdf).
3. A screenshot of a BAM file (from the RNA-seq pipeline) being viewed in IGV (igv_brain1.png).
4. A heatmap from the hisat2 portion of the bulk RNA-seq pipeline (hisat2_heatmap.pdf).
5. A heatmap from the salmon portion of the bulk RNA-seq pipeline (salmon_heatmap.pdf).
6. Selected results from a gene set enrichment analysis (GSEA_results.pdf).
7. An image of GSEA results that were obtained using the hisat2 RNA-seq data in g:Profiler (hisat2_gProfiler.png).

WHOLE GENOME SEQUENCING VARIANT CALLING PIPELINE

This Python pipeline call variants using GATK HaplotypeCaller.  It takes five inputs: the base name of two paired-end FASTQ samples, the base name of hisat2 index files, the relative or absolute location of a FASTA reference sequence for GATK, the full name of a known indels file for base recalibration, and the full name of a known SNPs file for base recalibration.  Outputs include a sorted BAM file with duplicates marked and base quality scores recalibrated, a VCF file of variants, the mean MAPQ score from the hisat2 alignment, the total number of variants called, and the mean QUAL score from the VCF file.


BULK RNA-SEQ WORKFLOW

This workflow uses hisat2 to align transcripts to a reference genome, as well as Salmon to classify transcripts.  It then uses edgeR to perform differential expression analysis, followed by the production of heatmaps for visualizing within-group and between-group variability.  It also uses tin.py to calculate transcript integrity numbers (TIN).


