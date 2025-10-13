t="Hello world is life !"


def clean_text(text, lower=True, remove_punct=True, extra_replacement=None):
    if lower:
        text = text.lower()
    if extra_replacement:
        for old, new in extra_replacement.items():
            text = text.replace(old, new)
    if remove_punct:
        punc = [',', '.', '!', '?', ':', ';']
        for ch in punc:
            text = text.replace(ch, '')
    return text

def tokenize(text, split_char=' '):
    return text.split(split_char)

def remove_stopwords(tokens, stopwords=('is', 'am', 'are', 'the', 'a', 'an')):
    return [t for t in tokens if t not in stopwords]

def build_vocab(*texts, min_freq=1, special_tokens=('<unk>', '<pad>', '<bos>', '<eos>')):
    freq = {}
    for text in texts:
        if isinstance(text, str):
            tokens = text.split()
        else:
            tokens = list(text)
        for token in tokens:
            freq[token] = freq.get(token, 0) + 1
    tokens_list = [tok for tok, c in freq.items() if c >= min_freq]
    vocab = {}
    idx = 0
    for tok in special_tokens:
        vocab[tok] = idx
        idx += 1
    for tok in tokens_list:
        if tok not in vocab:
            vocab[tok] = idx
            idx += 1
    return vocab

def encode_and_pad(tokens, vocab, max_len=10, pad_token='<pad>'):
    unk = vocab.get('<unk>')
    pad = vocab.get(pad_token)
    ids = [vocab.get(t, unk) for t in tokens]
    if len(ids) < max_len:
        ids += [pad] * (max_len - len(ids))
    return ids[:max_len]

def preprocess_pipeline(text, vocab=None, max_len=10, **clean_opts):
    t = clean_text(text, **clean_opts)
    toks = tokenize(t)
    toks = remove_stopwords(toks)
    if vocab is None:
        vocab = build_vocab(toks)
    enc = encode_and_pad(toks, vocab, max_len=max_len)
    return enc, vocab

# Quick tests (prints)
s = "AI, is Amazing!!!"
print("original:", s)
c = clean_text(s)
print("clean:", c)
toks = tokenize(c)
print("tokens:", toks)
rs = remove_stopwords(toks)
print("no stop:", rs)
v = build_vocab("ai is amazing", "ai is cool")
print("vocab:", v)
enc = encode_and_pad(['ai', 'amazing'], {'<unk>':0,'<pad>':1,'ai':2,'amazing':3}, max_len=5)
print("encode_and_pad:", enc)
out = preprocess_pipeline('AI is amazing!!!', vocab={'<unk>':0,'<pad>':1,'ai':2,'amazing':3}, max_len=5)
print("preprocess_pipeline:", out)


# function to tokenize

def tokenize(text,split_char=" "):
    tokens=[]
    tokens=text.split(' ')
    return tokens

o=tokenize(o)

print(o)

# function to remove stopwords

def remove_stopwords(tokens, stopwords=('is', 'am', 'are', 'the', 'a', 'an')):
    for i in stopwords:
        if i in tokens:
            tokens.remove(i)
    return tokens

o=remove_stopwords(o)
print(o)

# function to build vocabulary

def build_vocab(*texts, min_freq=1, special_tokens=('<unk>', '<pad>', '<bos>', '<eos>')):
    freq = {}
    for text in texts:
        for token in text:
            freq[token] = freq.get(token, 0) + 1
    vocab = [tok for tok, c in freq.items() if c >= min_freq]
    vocab = list(special_tokens) + vocab
    return {tok: idx for idx, tok in enumerate(vocab)}
    
o=build_vocab(o)
print(o)

# function to encode and pad

def encode_and_pad(tokens, vocab, max_len=10, pad_token='<pad>'):
    ids = [vocab.get(t, vocab.get('<unk>')) for t in tokens]
    while len(ids) < max_len:
        ids.append(vocab[pad_token])
    return ids[:max_len]

o=encode_and_pad(o)
print(o)

# function for preprocessing pipeline

def preprocess_pipeline(text, vocab=None, max_len=10, **clean_opts):
    t = clean_text(text, **clean_opts)
    t = tokenize(t)
    t = remove_stopwords(t)
    if vocab is None:
        vocab = build_vocab(t)
    encoded = encode_and_pad(t, vocab, max_len=max_len)
    return encoded, vocab

o=preprocess_pipeline(t)
print(o)