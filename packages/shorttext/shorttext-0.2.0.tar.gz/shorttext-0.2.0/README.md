# Short Text Categorization in Python

This repository is a collection of supervised learning algorithms for multi-class classification to short texts using Python. In addition to the bag-of-words representation of texts, word-embedding algorithms with a pre-trained model are used. Currently, Word2Vec is implemented. This package is still *under development*, and *not stable*. Feel free to give suggestions.

To install it, in a console, use `pip`.

```
>>> pip install shorttext
```

The Word2Vec model is implemented with [`gensim`](https://radimrehurek.com/gensim/), and various neural networks with [`keras`](https://keras.io/), with a [`Theano`](http://deeplearning.net/software/theano/) backend. Certain natural language processing tasks are implemented with [`nltk`](http://www.nltk.org/), and [`gensim`](https://radimrehurek.com/gensim/). This also imported [numpy](http://www.numpy.org/), [scipy](https://www.scipy.org/), and [pandas](http://pandas.pydata.org/). 

# Useful Links

* Documentation : [https://pythonhosted.org/shorttext/](https://pythonhosted.org/shorttext/)
* Github: [https://github.com/stephenhky/PyShortTextCategorization](https://github.com/stephenhky/PyShortTextCategorization)
* PyPI: [https://pypi.python.org/pypi/shorttext](https://pypi.python.org/pypi/shorttext)
* An [earlier version](https://github.com/stephenhky/PyShortTextCategorization/tree/b298d3ce7d06a9b4e0f7d32f27bab66064ba7afa) of this repository is a demonstration of the following blog post: [Short Text Categorization using Deep Neural Networks and Word-Embedding Models](https://datawarrior.wordpress.com/2016/10/12/short-text-categorization-using-deep-neural-networks-and-word-embedding-models/)

# Further Reading

* Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg Corrado, Jeffrey Dean, "Distributed Representations of Words and Phrases and their Compositionality", *NIPS Proceedings* __26__, 3111-3119 (2013). \[[arXiv](https://arxiv.org/abs/1310.4546)\]
* Yoon Kim, "Convolutional Neural Networks for Sentence Classification" (2014). \[[arXiv](https://arxiv.org/abs/1408.5882)\]
* For a theory of word embeddings, see the WordPress blog entry: [Probabilistic Theory of Word Embeddings: GloVe](https://datawarrior.wordpress.com/2016/07/25/probabilistic-theory-of-word-embeddings-glove/).
* Chunting Zhou, Chonglin Sun, Zhiyuan Liu, Francis Lau, "A C-LSTM Neural Network for Text Classification", arXiv:1511.08630 (2015). \[[arXiv](https://arxiv.org/abs/1511.08630)\]
* Sebastian Ruder, "An overview of gradient descent optimization algorithms." (2016) \[[Ruder](http://sebastianruder.com/optimizing-gradient-descent/)\].
