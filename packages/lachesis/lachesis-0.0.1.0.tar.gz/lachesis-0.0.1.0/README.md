# lachesis

**lachesis** automates the segmentation of a transcript into closed captions

* Version: 0.0.1
* Date: 2017-01-18
* Developed by: [Alberto Pettarin](http://www.albertopettarin.it/)
* License: the GNU Affero General Public License Version 3 (AGPL v3)
* Contact: [info@readbeyond.it](mailto:info@readbeyond.it)

## Goal

TBW


## Installation

```bash
pip install lachesis
```

TODO: add directions about installing model files and Python NLP libraries.


## Usage

Tokenize, split sentences, and POS tagging:

```python
from lachesis.elements import Text
from lachesis.nlpwrappers import NLPEngine

# work on this Unicode string
s = u"Hello, World. This is a second sentence, with a comma too! And a third sentence."

# but you can also pass a list with pre-split text
# s = [u"Hello World.", u"This is a second sentence.", u"Third one, bla bla"]

# create a Text object from the Unicode string
t = Text(s, language=u"eng")

# tokenize, split sentences, and POS tagging
# the best NLP library will be chosen,
# depending on the language of the text
nlp1 = NLPEngine()
nlp1.analyze(t)
for s in t.sentences:
    print(s)
    print(s.tagged_string)

# explicitly specify an NLP library
# in this case, use "nltk"
# (other options include: "pattern", "spacy", "udpipe")
nlp2 = NLPEngine()
nlp2.analyze(t, wrapper="nltk")
...

# preload NLP libraries
nlp3 = NLPEngine(preload=[
    ("eng", "spacy"),
    ("deu", "nltk"),
    ("ita", "pattern"),
    ("fra", "udpipe")
])
nlp3.analyze(t)
...
```

Download closed captions from YouTube or parse an existing TTML file:

```python
from lachesis.downloaders import Downloader

# URL of the video
url = u"http://www.youtube.com/watch?v=NSL_xx2Qnyc"

# download English automatic CC, storing the raw TTML file in /tmp/
language = u"en"
options = { "auto": True, "output_file_path": "/tmp/auto.ttml" }
ccl = Downloader.download_closed_captions(url, language, options)
print(ccl)

# download English manual CC
language = u"en"
options = { "auto": False }
ccl = Downloader.download_closed_captions(url, language, options)
print(ccl)

# parse a given TTML file (downloaded from YouTube)
ifp = "/tmp/auto.ttml"
ccl = Downloader.read_closed_captions(ifp, options={u"downloader": u"youtube"})

# get various representations of the CCs
print(ccl.single_string)        # print as a single string, collapsing CCs and lines
print(ccl.plain_string)         # print as a plain string, one CC per row and collapsed lines
print(ccl.cc_string)            # print as blank-separated, multiple line, SRT-like string
                                # (but without timings and ids)
```


## License

**lachesis** is released under the terms of the
GNU Affero General Public License Version 3.
See the [LICENSE](LICENSE) file for details.
