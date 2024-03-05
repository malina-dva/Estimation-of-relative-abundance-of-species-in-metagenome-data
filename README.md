# Estimation-of-relative-abundance-of-species-in-metagenenome-data
Complete pipeline for estimating the relative abundance of microbial species using kraken2 and bracken 
## install the conda env 
conda config --add channels bioconda
conda create --yes -n kraken kraken2 bracken
conda activate kraken

## obtain kraken DB with capped at 8GB  
wget https://genome-idx.s3.amazonaws.com/kraken/k2_standard_08gb_20240112.tar.gz 
tar -xvzf k2_standard_08gb_20240112.tar.gz
## test
```{bash, eval=FALSE}
# This is a Bash code chunk
ls -l
echo "Hello, World!" ```
