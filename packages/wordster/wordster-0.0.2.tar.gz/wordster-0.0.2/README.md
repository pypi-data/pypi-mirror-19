
Wordster
====

A simple python wrapper for [Merriam Webster](https://www.merriam-webster.com/) Website. Use it to get meanings of words.


Installation
============

```
pip install wordster
```


Example
=======

### Code

```python

from wordster import wordster

# get list of different meanings for a given word
print wordster.find_meaning("jargon")
```    
   
### Output

```
['confused unintelligible language', 'the technical terminology or characteristic idiom of a special activity or group', 'obscure and often pretentious language marked by circumlocutions and long words']
```


    