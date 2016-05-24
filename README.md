# SearchEngine
This is the project for information retreival.

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
