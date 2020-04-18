import re
import numpy as np
from tqdm import tqdm
from collections import *


class BPETokenize():
    """
    After building a BPE vocabulary using the `BuildBPEVocab()` this class will
    takes list of texts and tokenize those.
    """

    def __init__(self, strtoint: dict, inttostr: dict, vocab_tokens: dict):

        self.strtoint = strtoint
        self.do_lower = do_lower
        self.inttostr = inttostr
        self.vocab_tokens = vocab_tokens
        self.clean_d = lambda x: ''.join(re.findall("[a-zA-Z0-9!@#$%&*?,':]", x))

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

    def tokenize_text_chunk(self, string: str, sorted_tokens: list, unk_word='</u>'):

        if string == "":
            return []
        if sorted_tokens == []:
            return [unk_word]

        string_tokens = []
        for i in range(len(sorted_tokens)):

            token = sorted_tokens[i]
            token_reg = re.escape(token.replace(".", "[.]"))

            matched_positions = [(m.start(0), m.end(0)) for m in re.finditer(token_reg, string)]

            if len(matched_positions) == 0:
                continue

            substring_end_positions = [matched_position[0] for matched_position in matched_positions]

            substring_start_position = 0

            for substring_end_position in substring_end_positions:
                substring = string[substring_start_position:substring_end_position]
                string_tokens += self.tokenize_text_chunk(string=substring, sorted_tokens=sorted_tokens[i + 1:],
                                                          unk_word=unk_word)
                string_tokens += [token]
                substring_start_position = substring_end_position + len(token)
            remaining_substring = string[substring_start_position:]
            string_tokens += self.tokenize_text_chunk(string=remaining_substring, sorted_tokens=sorted_tokens[i + 1:],
                                                      unk_word=unk_word)
            break
        return string_tokens

    def tokenize_string(self, string: str, sorted_tokens: list):

        if string in list(self.strtoint.keys()) and string in self.vocab_tokens:
            return [string]
        elif string not in list(self.strtoint.keys()) and string in self.vocab_tokens:
            return self.vocab_tokens[string]
        else:
            return self.tokenize_text_chunk(string, sorted_tokens)

    def tokenize_sentence(self, sentence: str, sorted_tokens: list):
        str_toks = []
        int_toks = []
        input_sent = sentence
        sentence = self.cleaned_text(sentence)
        sent_splt = [s + "</w>" for s in sentence.split()]
        for token in sent_splt:
            str_ = self.tokenize_string(token, sorted_tokens)
            str_toks.append(str_)
            for tok in str_:
                if tok not in self.strtoint:
                    tok = self.tokenize_string(tok, sorted_tokens)
                    for t in tok:
                        int_toks.append(self.strtoint[t])
                else:
                    int_toks.append(self.strtoint[tok])
        return input_sent, str_toks, int_toks

    def tokenize_text_corpus(self, text_corpus: list, sorted_tokens: list):
        dict_text_corpus = dict()
        with tqdm(total=len(text_corpus)) as pbar:
            for text in text_corpus:
                inp, str_, int_ = self.tokenize_sentence(text, sorted_tokens)
                dict_text_corpus[inp] = {"int_tokens": int_, "str_tokens": str_}
                pbar.update()
        return dict_text_corpus


