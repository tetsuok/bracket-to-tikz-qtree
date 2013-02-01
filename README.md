bracket-to-tikz-qtree
=====================

A bracketed text to tikz-qtree format converter.

This tool provides users with automatic conversion froma a bracketed text to the corresponding [tikz-qtree](http://www.ctan.org/pkg/tikz-qtree) format. The bracketed text format is widely used to represent a phrase structure tree in natural language processing such as the data format in [Penn Treebank](http://www.cis.upenn.edu/~treebank/) and output data format of statistical parsers (e.g., [Stanford parser](http://nlp.stanford.edu/software/lex-parser.shtml) and [Berkeley parser](http://code.google.com/p/berkeleyparser/)).

The code is known to work on Linux and OS X.

### Software Requirements ###

- Python 2.6 or later

Note that to run this tool, there is no need to install the code and additional Python packages. However, tikz-qtree package is required when you want to compile the generated latex files with this converter.

### Usage ###

    $ ./bracket_to_tikz_qtree.py [options] FILE

    $ ./bracket_to_tikz_qtree.py [options] [FILE] -

Please note that you need to prepare for the input file `FILE` which contains bracket texts that you want to convert to the tikz-qtree format.

Please see `-h` or `--help` for all possible options.

#### An example ####

    $ cat sample/sample.parse | ./bracket_to_tikz_qtree.py | pdflatex

![sample output](https://raw.github.com/tetsuok/bracket-to-tikz-qtree/master/sample/sample.png "Sample output")

### Data format ###

under construction.

Here is a sample bracketed text:

    (S
      (NP (NNP International) (NN terrorism))
      (VP (VBZ is)
        (NP
          (NP (DT a) (JJ grave) (NN threat))
          (PP (TO to)
            (NP (NN world) (NN peace)
              (CC and)
              (NN security)))))
      (. .))
    
    ;; ...


### License ###

This code is distributed under the New BSD License. See the file LICENSE.