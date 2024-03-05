# Estimation-of-relative-abundance-of-species-in-metagenenome-data
Complete pipeline for estimating the relative abundance of microbial species using kraken2 and bracken 
## Install the Conda Environment

```{bash, eval=FALSE}
conda config --add channels bioconda  
conda create --yes -n kraken kraken2 bracken  
conda activate kraken 

## obtain kraken DB  capped at 8GB
```{bash, eval=FALSE}
wget https://genome-idx.s3.amazonaws.com/kraken/k2_standard_08gb_20240112.tar.gz  
tar -xvzf k2_standard_08gb_20240112.tar.gz  

