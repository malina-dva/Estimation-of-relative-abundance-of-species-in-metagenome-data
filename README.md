# Estimation-of-relative-abundance-of-species-in-metagenenome-data
Complete pipeline for estimating the relative abundance of microbial species using kraken2 and bracken 
## 1. Install the Conda Environment

```{bash, eval=FALSE}
conda config --add channels bioconda  
conda create --yes -n kraken kraken2 bracken  
conda activate kraken 
```
## 2. Obtain kraken DB capped at 8GB
Contains archaea, bacteria, viral, plasmid and human 
```{bash, eval=FALSE}
mkdir krakenDB  
cd krakenDB  
wget https://genome-idx.s3.amazonaws.com/kraken/k2_standard_08gb_20240112.tar.gz    
tar -xvzf k2_standard_08gb_20240112.tar.gz  
!Attention! Takes a while to run...
```
## 3. Run kraken for sample1 
```{bash, eval=FALSE}
kraken2 --use-names --threads 4 --db /home/malina/kraken_DB/  --report sample1.report --paired tara_reads_R1.5000.fastq tara_reads_R2.5000.fastq > sample1.kraken
```
Loading database information... done.
5000 sequences (1.26 Mbp) processed in 0.480s (624.8 Kseq/m, 157.44 Mbp/m).
  353 sequences classified (7.06%)
  4647 sequences unclassified (92.94%)
## 4. Run kraken for sample2
```{bash, eval=FALSE}
kraken2 --use-names --threads 4 --db /home/malina/kraken_DB/ --report sample2.report --paired tara_reads_R1.5000.100.fastq tara_reads_R2.5000.100.fastq > sample2.kraken
```
Loading database information... done.
5000 sequences (1.26 Mbp) processed in 0.398s (753.2 Kseq/m, 189.81 Mbp/m).
  408 sequences classified (8.16%)
  4592 sequences unclassified (91.84%)


