# SearchEngine
This is the project for information retreival.

## Attention

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
|ID | int |
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
first NO
second AND
third OR

## Problems
1. token processing problem: '-'
current solution: 
in tokenize.py:
`primordialTokens = inputStr.replace("-"," ").replace("'"," ").replace("/"," ").split(' ')`

2. numpy version problem
I must use the pre-installed numpy with version '1.8.0rc1' to make program run correctly.
reference link: http://comments.gmane.org/gmane.comp.ai.gensim/5643

3. Problematic preprocessing
processed tokens:
1)..113.................123.00 -> cannot find well

U.S --tokenize--> u.s --stemming--> u.
	query ok
