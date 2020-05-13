## Byte Pair Encoding(BPE) Python Package

#### Clone and Install (Still under development so not available on `pip`)

```
git clone https://github.com/vatsalsaglani/BytePairEncoding.git
pip install BytePairEncoding/.
```

#### Building Vocabulary
```
from BPE.vocab_builder import *
document = 'a long string or anything as a string'
bpevocab = BuildBPEVocab(document, iters = 5000)
```

#### Tokenizing
```
from BPE.tokenizer import *
tokenizer = BPETokenize(bpevocab.strtoint, bpevocab.inttostr, bpevocab.vocab_tokenization)

sentence = 'hello world'

tokenizer.tokenize_sentence(sentence, bpevocab.sorted_tokens)
```

#### The following notebook shows an example to build a vocab on a book from Gutenberg Project, and tokenize a sentence.

Go through the following notebook to understand how things work
https://beta.deepnote.com/publish/0a4be21b-db44-4155-9a75-329754bc53b3-05d3511c-9ede-4ff7-8cc6-8552342fe3df
