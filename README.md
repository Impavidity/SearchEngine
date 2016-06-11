# SearchEngine
This is the project for information retreival.

## Attention
分工
A. UI + 说明文档

B. 通配符查询
   Top K查询（7.1 节的内容）
   层次型索引

C. 短语查询
   同义词查询
   拼写矫正

1. To let the title search more accurate, I add the title tokens to the doc tokens twice.
So, you need to extract new tokens for position index.

2. Run buildIndex to build index first, then run main.py

## Data Cleaning

Download the dataset [here if you are in ZJU](http://10.76.3.76/Reuters.rar) or [here if you are out of ZJU](http://o6y0thkyx.bkt.clouddn.com/Reuters.rar).
Extract in the fold.

### Info Extractor
This module will extract all the information from the original data.

We will save the following data separately.

|Info|Format|
|:--:|:----:|
|Title|String|
|Passage|String|


All this information will save as the above sequence.


Attention Here: You will find that there are many '&lt'; in the documents. It means <.

If there is only one sentence in the passage, we regard the sentence as *title* and there is no *content*.

How to use:
```
cd Data Cleaning
python InfoExtractor
```

## Boolean search
search form:
X AND Y AND NOT Z ... OR P OR Q ...

Priority:
highest NO
second AND
third OR

## Top k search and wildcard search

Wildcard search is based on Top k search, wildcard search just finds all the possible query strings and then get all the results for these strings with top k search.

These search methods are encapsulated in query.py, and it is very easy to use them, you can see the demo in utils/debug.py

First, use pickle module to load the index file and the id-html map file.
Then, just use topK_query(index, voc, entries, query, index_type='tiered') and wildcard_query(index, voc, entries, query, index_type='tiered') to get the corresponding result.


## Problems

1. numpy version problem

I must use the pre-installed numpy with version '1.8.0rc1' to make program run correctly.
reference link: http://comments.gmane.org/gmane.comp.ai.gensim/5643
Numpy 1.10 would stuck

2. list_dir doesn't list file in a fixed way, so if we use integer to be document id, then we should build a map.
I strongly suggest we should use document name as document id.

