# NTU_Ceiba_TA_hw_scores_crawler
This is a tool, which is for Mac OS, help TAs to download the scores of assignment and transform score from grade to marks, collect them into a dataframe and export as .csv file.


## Requirements
- python 3
- Google Chrome 
- Google Chrome driver
- selenium
- pathlib 
- pandas
- tqdm

```bash
$ conda install -c conda-forge selenium
$ conda install -c menpo pathlib
$ conda install -c anaconda pandas
$ conda install -c conda-forge tqdm
```

## Chrome driver
You need Chrome driver which support  your Chrome version, you can find it here:
https://chromedriver.chromium.org/downloads


## Using in Terminal
```bash
$ python hw_score_crawl_and_tran.py
# 1. Drag your Chrome driver into the terminal or type in the path of it.
# 2. Input yor account.
# 3. Input your password.
# 4. Wait for it!
# 5. <=== Program Done ===>
```
