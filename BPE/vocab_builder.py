import re
from tqdm import tqdm
from collections import *
import os

class BuildBPEVocab():
    """
    Byte Pair Encoding for any text-oriented-corpus can be done using this.
    """

    def __init__(self, corpus, iters):
        """
        args -
        corpus: the text corpus.
        iters = number of merges required while building a BPE vocab. (*Can be probably treated as a hyperparameter)
        """
        self.corpus = corpus
        self.iters = iters
        self.clean_d = lambda x: ''.join(re.findall("[a-zA-Z0-9!@#$%&*?,':]", x))
        self.vocab = self.build_corpus_vocab()
        self.vocab = self.build_vocab()
        # self.do_lower = do_lower

    #         self.sorted_tokens = []

    def split_string(self, string):
        """
        Clean the string and check for things like `HereEveryoneIsGood` and split such texts
        """
        string = " ".join(re.split("[.,;:]", string))
        string = " ".join(string.split())
        # if self.do_lower:
        #     string = string.lower()
            
        string = " ".join(string.split())
        return string

    def splits_(self, string):
        """
        Splits the string to tokens
        """
        return [
            self.clean_d(t) for t in self.split_string(string).split(" ")
            if len(self.clean_d(t)) > 0
        ]

    def cleaned_text(self, string):
        """
        Returns a cleaned string
        """
        return " ".join(self.splits_(string))

    def build_corpus_vocab(self):
        """
        Builds the initial BPE vocab
        """
        corpus = self.cleaned_text(self.corpus)
        tokens = [" ".join(word) + " </w>" for word in corpus.split()]
        vocab = Counter(tokens)
        return vocab

    def get_stats(self):
        """
        Iterates over pairs of character in the initial vocab and returns
        dictionary with paris of characters occuring together and their count
        """
        pairs = defaultdict(int)

        for word, freq in self.vocab.items():
            symbols = word.split()

            for i in range(len(symbols) - 1):
                pairs[symbols[i], symbols[i + 1]] += freq

        return pairs

    def merge_corpus_vocab(self, pair):
        """
        During every merge step or iteration takes the pair of characters occuring the most number
        of times and joins them to a single character
        """
        v_out = {}
        bigram = re.escape(" ".join(pair))
        p = re.compile(r"(?<!\S)" + bigram + r"(?!\S)")

        for word in self.vocab:
            w_out = p.sub(''.join(pair), word)
            v_out[w_out] = self.vocab[word]

        self.vocab = v_out

    def build_vocab(self):
        """
        Provided with the number of iterations at the start the build vocab provides the final vocab after all the
        merges in each iteration.
        """

        for itr in tqdm(range(self.iters)):
            pairs = self.get_stats()
            if not pairs:
                break
            best = max(pairs, key=pairs.get)
            vocab = self.merge_corpus_vocab(best)

        self.sorted_tokens = self.get_sorted_token_tuple()
        self.tokens_frequencies, self.vocab_tokenization = self.get_tokens_from_vocab(
        )
        self.strtoint, self.inttostr = self.vocab_strtoint_inttostr()

    def get_tokens(self):
        """
        Returns the frequency of each token and its subwords if available.
        """

        tokens = defaultdict(int)
        for word, freq in self.vocab.items():
            word_tokens = word.split()
            for token in word_tokens:
                tokens[token] += freq
        return tokens

    def get_tokens_from_vocab(self):
        """
        Returns token frequencies along with the token vocab i.e.
        if a word like "wonder" is being splitted into ["wo", "n", "de", "r"], the
        vocabulary would be wonder: ["wo", "n", "de", "r"]
        """
        tokens_frequencies = defaultdict(int)
        vocab_tokenization = {}
        for word, freq in self.vocab.items():
            word_tokens = word.split()
            for token in word_tokens:
                tokens_frequencies[token] += freq
            vocab_tokenization[''.join(word_tokens)] = word_tokens
        return tokens_frequencies, vocab_tokenization

    def measure_token_length(self, token):
        """
        while building a sorted vocab of token the length of each token needs to be meausred,
        this returns  the length of a token based on where it ends.
        """
        if token[-4:] == '</w>':
            return len(token[:-4]) + 1
        else:
            return len(token)

    def get_sorted_token_tuple(self):
        """
        Returns a list of tokens in the vocabulary
        """
        tokens_frequencies, vocab_tokenization = self.get_tokens_from_vocab()

        sorted_token_tuple = sorted(
            tokens_frequencies.items(),
            key=lambda item: (self.measure_token_length(item[0]), item[1]),
            reverse=True)
        return [token for (token, freq) in sorted_token_tuple]

    def vocab_strtoint_inttostr(self):
        token_freqs, _ = self.get_tokens_from_vocab()
        lst_token_freq = list(token_freqs.keys())
        lst_token_freq.append("</u>")
        lst_token_freq.append('</space/></w>')
        strtoint, inttostr = {
                                 w: i+1
                                 for i, w in enumerate(lst_token_freq)
                             }, {i+1: w
                                 for i, w in enumerate(lst_token_freq)}

        return strtoint, inttostr


