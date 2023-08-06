lachesis
========

**lachesis** automates the segmentation of a transcript into closed
captions

-  Version: 0.0.3
-  Date: 2017-01-26
-  Developed by: `Alberto Pettarin <http://www.albertopettarin.it/>`__
-  License: the GNU Affero General Public License Version 3 (AGPL v3)
-  Contact: info@readbeyond.it

**DO NOT USE THIS PACKAGE IN PRODUCTION UNTIL IT REACHES v1.0.0 !!!**

Goal
----

**lachesis** automates the segmentation of a transcript into closed
captions (CCs).

The general idea is that writing a transcription (raw text) is easier
and faster than writing CCs, especially if you need to respect
constraints like a certain minimum/maximum number of characters per
line, a maximum number of lines per CC, etc.

You can transcribe your video into raw text and ``lachesis`` will take
on the job of segmenting the text into CCs for you. Once you have the
CCs, you can use a `forced
aligner <https://github.com/pettarin/forced-alignment-tools/>`__ like
`aeneas <https://github.com/readbeyond/aeneas/>`__ to align them with
the audio of your video, obtaining a subtitle file (SRT, TTML, VTT,
etc.).

With ``lachesis`` and a forced aligner, the manual labor for producing
CCs for a video is reduced to a. transcribing the video in raw text
form, and b. checking the final CCs and audio alignment. Instead of
transcribing from scratch, you can even start by checking/editing a
rough transcription made by an automated speech recognition engine, like
the "automatic CCs" from YouTube, speeding the process up further.

The "magic" behind ``lachesis`` consists in combining machine learning
techniques like `conditional random
fields <https://en.wikipedia.org/wiki/Conditional_random_field>`__ (CRF)
and classical NLP tools like `POS
tagging <https://en.wikipedia.org/wiki/Part-of-speech_tagging>`__ and
`sentence
segmentation <https://en.wikipedia.org/wiki/Text_segmentation>`__ to
split the text into CC lines. The machine learning models are learned
from existing, manually-edited, high-quality CCs, like those of
`TED <https://www.youtube.com/user/TEDtalksDirector>`__/`TEDx <https://www.youtube.com/user/TEDxTalks>`__
talks on YouTube. The NLP tools come from the well-established, free NLP
libraries for Python listed below.

In summary, ``lachesis`` contains the following major functions:

-  download closed captions from YouTube;
-  parse closed caption TTML files (downloaded from YouTube);
-  add POS tags to a given text or closed caption file;
-  segment a given text into sentences;
-  segment a given text into closed captions (several algorithms are
   available);
-  train and use machine learning models to segment raw text into CC
   lines.

Installation
------------

**DO NOT USE THIS PACKAGE IN PRODUCTION UNTIL IT REACHES v1.0.0 !!!**

.. code:: bash

    pip install lachesis

Installing dependencies
~~~~~~~~~~~~~~~~~~~~~~~

You might need additional packages, depending on how you plan to use
``lachesis``:

-  ``lxml >= 3.6.0`` for reading or downloading TTML files;
-  ``youtube-dl >= 2017.1.16`` for downloading TTML files;
-  ``python-crfsuite >= 0.9.1`` for training and using CRF-based
   splitters.

By design choice, none of the above dependencies is installed by
``pip install lachesis``. If you want to install them all, you can use:

.. code:: bash

    pip install lachesis[full]

Alternatively, manually install only the dependencies you need. (You can
do it before or after installing ``lachesis``, the order does not
matter.)

Installing NLP Libraries
~~~~~~~~~~~~~~~~~~~~~~~~

In addition to the dependencies listed above, to perform POS tagging and
sentence segmentation ``lachesis`` can use one or more of the following
libraries:

-  ``Pattern`` (install with ``pip install pattern``, `see
   here <http://www.clips.ua.ac.be/pattern>`__)
-  ``NLTK`` (install with ``pip install nltk``, `see
   here <http://www.nltk.org/>`__)
-  ``spaCy`` (install with ``pip install spacy``, `see
   here <https://spacy.io/>`__)
-  ``UDPipe`` (install with ``pip install ufal.udpipe``, `see
   here <https://ufal.mff.cuni.cz/>`__)

If you want to install them all, you can use:

.. code:: bash

    pip install lachesis[nlp]

or ``[fullnlp]`` if you also want ``[full]`` as above.

Each NLP library also needs language models which you need to
download/install separately. Consult the documentation of your NLP
library for details.

``lachesis`` expects the following directories in your home directory
(you can symlink them, if you installed each NLP library in a different
place):

-  ``~/lachesis_data/nltk_data`` for ``NLTK`` (`see
   here <http://www.nltk.org/data.html>`__);
-  ``~/lachesis_data/spacy_data`` for ``spaCy`` (`see
   here <https://spacy.io/docs/usage/>`__);
-  ``~/lachesis_data/udpipe_data`` for ``UDPipe`` (`see
   here <https://ufal.mff.cuni.cz/udpipe>`__).

The NLP library ``Pattern`` does not need a separate download of its
language models, as they are bundled in the file you download when
installing through ``pip install pattern``.

The following table summarizes the languages supported by each library
in their standard language models pack. (Additional languages might be
supported by third party projects/downloads or added over time.)

+-----------------------+-----------+--------+---------+----------+
| Language / Library    | Pattern   | NLTK   | spaCy   | UDPipe   |
+=======================+===========+========+=========+==========+
| Arabic                |           |        |         | ✓        |
+-----------------------+-----------+--------+---------+----------+
| Basque                |           |        |         | ✓        |
+-----------------------+-----------+--------+---------+----------+
| Bulgarian             |           |        |         | ✓        |
+-----------------------+-----------+--------+---------+----------+
| Croatian              |           |        |         | ✓        |
+-----------------------+-----------+--------+---------+----------+
| Czech                 |           | ✓      |         | ✓        |
+-----------------------+-----------+--------+---------+----------+
| Danish                |           | ✓      |         | ✓        |
+-----------------------+-----------+--------+---------+----------+
| Dutch                 | ✓         | ✓      |         | ✓        |
+-----------------------+-----------+--------+---------+----------+
| English               | ✓         | ✓      | ✓       | ✓        |
+-----------------------+-----------+--------+---------+----------+
| Estonian              |           | ✓      |         | ✓        |
+-----------------------+-----------+--------+---------+----------+
| Finnish               |           | ✓      |         | ✓        |
+-----------------------+-----------+--------+---------+----------+
| French                | ✓         | ✓      |         | ✓        |
+-----------------------+-----------+--------+---------+----------+
| German                | ✓         | ✓      | ✓       | ✓        |
+-----------------------+-----------+--------+---------+----------+
| Gothic                |           |        |         | ✓        |
+-----------------------+-----------+--------+---------+----------+
| Greek                 |           | ✓      |         | ✓        |
+-----------------------+-----------+--------+---------+----------+
| Greek (ancient)       |           |        |         | ✓        |
+-----------------------+-----------+--------+---------+----------+
| Hebrew                |           |        |         | ✓        |
+-----------------------+-----------+--------+---------+----------+
| Hindi                 |           |        |         | ✓        |
+-----------------------+-----------+--------+---------+----------+
| Hungarian             |           |        |         | ✓        |
+-----------------------+-----------+--------+---------+----------+
| Indonesian            |           |        |         | ✓        |
+-----------------------+-----------+--------+---------+----------+
| Irish                 |           |        |         | ✓        |
+-----------------------+-----------+--------+---------+----------+
| Italian               | ✓         | ✓      |         | ✓        |
+-----------------------+-----------+--------+---------+----------+
| Latin                 |           |        |         | ✓        |
+-----------------------+-----------+--------+---------+----------+
| Norwegian             |           | ✓      |         | ✓        |
+-----------------------+-----------+--------+---------+----------+
| Old Church Slavonic   |           |        |         | ✓        |
+-----------------------+-----------+--------+---------+----------+
| Persian               |           |        |         | ✓        |
+-----------------------+-----------+--------+---------+----------+
| Polish                |           | ✓      |         | ✓        |
+-----------------------+-----------+--------+---------+----------+
| Portuguese            |           | ✓      |         | ✓        |
+-----------------------+-----------+--------+---------+----------+
| Romanian              |           |        |         | ✓        |
+-----------------------+-----------+--------+---------+----------+
| Slovenian             |           | ✓      |         | ✓        |
+-----------------------+-----------+--------+---------+----------+
| Spanish               | ✓         | ✓      |         | ✓        |
+-----------------------+-----------+--------+---------+----------+
| Swedish               |           | ✓      |         | ✓        |
+-----------------------+-----------+--------+---------+----------+
| Tamil                 |           |        |         | ✓        |
+-----------------------+-----------+--------+---------+----------+
| Turkish               |           | ✓      |         |          |
+-----------------------+-----------+--------+---------+----------+

Usage
-----

Download closed captions from YouTube
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from lachesis.downloaders import Downloader
    from lachesis.language import Language

    # set URL of the video and language of the CCs
    url = u"http://www.youtube.com/watch?v=NSL_xx2Qnyc"
    language = Language.ENGLISH

    # download automatic CC, do not save to file
    options = { "auto": True }
    doc = Downloader.download_closed_captions(url, language, options)
    print(doc)

    # download manually-edited CC, saving the raw TTML file to disk
    options = { "auto": False, "output_file_path": "/tmp/ccs.ttml" }
    doc = Downloader.download_closed_captions(url, language, options)
    print(doc)

Parse an existing TTML file downloaded from YouTube
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from lachesis.downloaders import Downloader

    # parse a given TTML file downloaded from YouTube
    ifp = "/tmp/ccs.ttml"
    doc = Downloader.read_closed_captions(ifp, options={u"downloader": u"youtube"})
    print(doc.language)

    # print several representations of the CCs
    print(doc.raw_string)                       # multi line string, similar to SRT but w/o ids or times
    print(doc.raw_flat_clean_string)            # single line string, w/o CC line marks
    print(doc.raw.string(flat=True, eol=u"|"))  # single line string, CC lines separated by '|' characters

Tokenize, split sentences, and POS tagging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from lachesis.elements import Document
    from lachesis.language import Language
    from lachesis.nlpwrappers import NLPEngine

    # work on this Unicode string
    s = u"Hello, World. This is a second sentence, with a comma too! And a third sentence."

    # but you can also pass a list with pre-split sentences
    # s = [u"Hello World.", u"This is a second sentence.", u"Third one, bla bla"]

    # create a Text object from the Unicode string
    doc = Document(raw=s, language=Language.ENGLISH)

    # tokenize, split sentences, and POS tagging
    # the best available NLP library will be chosen
    nlp1 = NLPEngine()
    nlp1.analyze(doc)

    # the text has been divided into tokens, grouped in sentences
    for s in doc.sentences:
        print(s)                                        # raw
        print(s.string(tagged=True))                    # tagged
        print(s.string(raw=True, eol=u"|", eos=u""))    # raw w/o CC line and sentence marks

    # explicitly specify the NLP library NLTK,
    # other options include: "pattern", "spacy", "udpipe"
    nlp2 = NLPEngine()
    nlp2.analyze(doc, wrapper=u"nltk")
    ...

    # if you need to analyze many documents,
    # preload (and keep in cache) an NLP library,
    # even different ones for different languages
    nlp3 = NLPEngine(preload=[
        (u"en", u"spacy"),
        (u"de", u"nltk"),
        (u"it", u"pattern"),
        (u"fr", u"udpipe")
    ])
    nlp3.analyze(doc)
    ...

Split into closed captions
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from lachesis.elements import Document
    from lachesis.language import Language
    from lachesis.nlpwrappers import NLPEngine
    from lachesis.splitters import CRFSplitter
    from lachesis.splitters import GreedySplitter

    # create a document from a raw string
    s = u"Hello, World. This is a second sentence, with a comma too! And a third sentence."
    doc = Document(raw=s, language=Language.ENGLISH)

    # analyze it using the NLP library Pattern
    nlpe = NLPEngine()
    nlpe.analyze(doc, wrapper=u"pattern")

    # feed the document into the CRF splitter (max 42 chars/line, max 2 lines/cc)
    spl = CRFSplitter(doc.language, 42, 2)
    spl.split(doc)

    # print the segmented CCs
    for cc in doc.ccs:
        for line in cc.elements:
            print(line)
        print(u"")

    # the default location for CRF model files is ~/lachesis_data/crf_data/
    # but you can also specify a different path
    spl = CRFSplitter(doc.language, 42, 2, model_file_path="/tmp/yourmodel.crfsuite")
    spl.split(doc)

    # if you do not have pycrfsuite installed
    # or the CRF model file for the document language,
    # you can use the GreedySplitter
    gs = GreedySplitter(doc.language, 42, 2)
    gs.split(doc)

Train a CRF model to segment raw text into CC lines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ # /tmp/ccs/train contains several TTML files to learn from
    $ # you can download them from YouTube using lachesis (see above)
    $ ls /tmp/ccs/train
    0001.ttml
    0002.ttml
    ...

    $ # extract features and labels from them:
    $ python -m lachesis.ml.crf dump eng /tmp/ccs/train/ /tmp/ccs/train.pickle
    ...

    $ # train the CRF model:
    $ python -m lachesis.ml.crf train eng /tmp/ccs/train.pickle /tmp/ccs/model.crfsuite
    ...

    $ # evaluate the model on the training set
    $ python -m lachesis.ml.crf test eng /tmp/ccs/train.pickle /tmp/ccs/model.crfsuite
    ...

    $ # you might want to evaluate on a test set, disjoint from the training set,
    $ # that is, the test set contains CCs not seen during the training:
    $ ls /tmp/css/test
    1001.ttml
    1002.ttml
    ...
    $ python -m lachesis.ml.crf dump eng /tmp/ccs/test/ /tmp/ccs/test.pickle
    $ python -m lachesis.ml.crf test eng /tmp/ccs/test.pickle /tmp/ccs/model.crfsuite
    ...
    $ # now you can build a CRFSplitter
    $ # with model_file_path="/tmp/ccs/model.crfsuite" as shown above

TODO: decide and document where pre-trained model files can be
downloaded

License
-------

**lachesis** is released under the terms of the GNU Affero General
Public License Version 3. See the `LICENSE <LICENSE>`__ file for
details.
