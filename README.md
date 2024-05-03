# Estimation-of-relative-abundance-of-species-in-metagenenome-data
Complete pipeline for estimating the relative abundance of microbial species using kraken2 and bracken    
Youtube video tutorial series:    

![](https://www.youtube.com/watch?v=LoMORt9u1ys)    

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
Only run it if you have the computational resources! Even if you do, loeading the database may take up to 30 min ... so be patient..      
```{bash, eval=FALSE}
kraken2 --use-names --threads 4 --db /home/malina/krakenDB/  --report sample1.report --paired sample1_R1.fastq sample1_R2.fastq > sample1.kraken
```
Loading database information... done.  
5000 sequences (1.26 Mbp) processed in 0.480s (624.8 Kseq/m, 157.44 Mbp/m).  
  353 sequences classified (7.06%)  
  4647 sequences unclassified (92.94%)  
## 4. Run kraken for sample2
```{bash, eval=FALSE}
kraken2 --use-names --threads 4 --db /home/malina/krakenDB/ --report sample2.report --paired sample2_R1.fastq sample2_R2.fastq > sample2.kraken
```
Loading database information... done.  
5000 sequences (1.26 Mbp) processed in 0.398s (753.2 Kseq/m, 189.81 Mbp/m).  
  408 sequences classified (8.16%)  
  4592 sequences unclassified (91.84%)  
 ## 5. Run bracken for sample1 
 ```{bash, eval=FALSE}
bracken -d /home/malina/krakenDB -i sample1.report -l S -o sample1.bracken.tsv
```
 >> Checking for Valid Options...  
 >> Running Bracken  
      >> python src/est_abundance.py -i sample1.report -o sample1.bracken.tsv -k /home/malina/krakenDB/database100mers.kmer_distrib -l S -t 0  
PROGRAM START TIME:  
BRACKEN SUMMARY (Kraken report: sample1.report)  
    >>> Threshold: 0  
    >>> Number of species in sample: 104  
          >> Number of species with reads > threshold: 104  
          >> Number of species with reads < threshold: 0  
    >>> Total reads in sample: 5000  
          >> Total reads kept at species level (reads > threshold): 207  
          >> Total reads discarded (species reads < threshold): 0  
          >> Reads distributed: 141  
          >> Reads not distributed (eg. no species above threshold): 5  
          >> Unclassified reads: 4647  
BRACKEN OUTPUT PRODUCED: sample1.bracken.tsv  
PROGRAM END TIME:  
  Bracken complete.  

## 5. Run bracken for sample2 
```{bash, eval=FALSE}
bracken -d /home/malina/krakenDB -i sample2.report -l S -o sample2.bracken.tsv 
```
>> Checking for Valid Options...  
 >> Running Bracken  
      >> python src/est_abundance.py -i sample2.report -o sample2.bracken.tsv -k /home/malina/krakenDB/database100mers.kmer_distrib -l S -t 0  
PROGRAM START TIME:  
BRACKEN SUMMARY (Kraken report: sample2.report)  
    >>> Threshold: 0  
    >>> Number of species in sample: 113  
          >> Number of species with reads > threshold: 113  
          >> Number of species with reads < threshold: 0  
    >>> Total reads in sample: 5000  
          >> Total reads kept at species level (reads > threshold): 241  
          >> Total reads discarded (species reads < threshold): 0  
          >> Reads distributed: 156  
          >> Reads not distributed (eg. no species above threshold): 11  
          >> Unclassified reads: 4592  
BRACKEN OUTPUT PRODUCED: sample2.bracken.tsv  
PROGRAM END TIME:  
  Bracken complete.  

## 6. Merge the bracken output files for the two samples using the provided python script (merge_profiling_reports.py)
To be able to run the python script, we will need to install pandas in our conda environment
```{bash, eval=FALSE}
conda install pandas
mkdir bracken_output
cp sample2_bracken.report sample1_bracken.report bracken_output/
python merge_profiling_reports.py -i bracken_output/ -o merged
```
You can obtain the results not only for S (species level) but any other taxlevel, by simply filtering the taxlevel column for it.   
Yet, the full lineage specification won't be available after running the step #6.  
In order to obtain it, we can use taxpasta  
## 7. Merge the bracken output files for the two samples using taxapasta and obtain the full taxonomic lineage for each species
Taxpasta works with python>=3.8, so it will be better if we create a whole new conda environment specifying the version of python needed for taxpasta to work
```{bash, eval=FALSE}
conda create -n myenv python=3.8
conda activate myenv
pip install taxpasta
```
if pip requires additional dependences you will have to install them, as per usual.  
Taxpasta also needs provided a set of 'taxonomy' files for full lineage info to be appended to the bracken results.  
One can download those files in a new directory   
```{bash, eval=FALSE}
mkdir taxa_DB
cd taxa_DB
curl -O ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz.md5
curl -O ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz
md5sum --check taxdump.tar.gz.md5
mkdir taxdump
tar -C taxdump -xzf taxdump.tar.gz
tree taxdump
```
taxdump  
├── citations.dmp  
├── delnodes.dmp  
├── division.dmp  
├── gc.prt  
├── gencode.dmp  
├── images.dmp  
├── merged.dmp  
├── names.dmp  
├── nodes.dmp  
└── readme.txt  
Finally we need to run taxpasta on the bracken tsv outputs 
```{bash, eval=FALSE}
taxpasta merge -p bracken -o report_bracken_with_lineage.tsv --taxonomy   /home/malina/taxa_DB/taxdump --add-lineage sample1.bracken.tsv sample2.bracken.tsv
```
And we end up having the entire lineage next to the species taxids. The info of taxa lineage together with the estimated counts accross samples, provided in a tabular format, will be sufficient to continue our analyses in R and work on identifying the differentially abundant species between groups of samples for example. Enjoy!
