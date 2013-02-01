#!/usr/bin/env python
# Copyright 2013 Tetsuo Kiso. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""
A simple converter from bracketting text of a phrase structure tree to the Qtree format.

Conventionally, phrase structure trees are represented in form of a bracketting string
(very similar to Lisp's S-expression).

In particular, this tool aims at converting to work with the David Chiang's tikz-qtree.
"""

import optparse
import sys

class LaTeXFormatter(object):

  def __init__(self, doc_opt, tikz_opt):
    self.doc_opt = doc_opt
    self.tikz_opt = tikz_opt

  def doc_header(self):
    return '''\documentclass{%s}
\usepackage{tikz}
\usepackage{tikz-qtree}
\\begin{document}''' % self.doc_opt

  def doc_footer(self):
    return '''\end{document}'''

  def wrap_tikzpicture(self, tree):
    """Wrap Qtree with the tikzpicture environment."""
    opt = '[' + self.tikz_opt + ']' if self.tikz_opt != '' else self.tikz_opt
    return '''\\begin{tikzpicture}%s
%s
\end{tikzpicture}''' % (opt, tree)

### Actual converter.

def to_qtree(text):
  """Convert a bracketed text to the Qtree style brackets."""
  return '''\Tree ''' + text.replace('(', '[.').replace(')', ' ]')

### Reader

def _read(f):
  """Read lines of bracketed texts.

  Note that we don't check whether the text have valid trees or not
  since the format of the bracket text depends on corpus (e.g., Penn
  Treebank) or parser (e.g. Stanford parser).
  """
  sents = []
  s = ''
  for i, l in enumerate(f):
    if l.startswith(';'):       # comment
      continue

    # TODO: change the assumption that each parse tree is delimitted by newline.
    if i > 0 and l.startswith('\n'):
      # strip the last line only.
      sents.append(s.rstrip())
      s = ''
      continue

    if l.startswith('( (S'):    # Hack for Penn Treebank's style format.
      l = l.replace('( (S', '(ROOT (S')

    s += l
  return sents

def read(file):
  if file == sys.stdin:
    return _read(file)
  else:
    with open(file) as f:
      return _read(f)


def parse_options():
  parser = optparse.OptionParser(usage='%prog [options] [FILE]')
  parser.add_option('--doc-option', dest='doc_opt', default='standalone',
                    help='option of documentclass [default: %default]')
  parser.add_option('--tikz-opt', dest='tikz_opt', default='',
                    help='option to change the style of the Qtree [default: %default]')
  (options, unused_args) = parser.parse_args()
  return (options, unused_args)

def main():
  opts, unused_args = parse_options()

  if len(unused_args) == 0:
    sents = read(sys.stdin)
  else:
    sents = read(unused_args[0])

  formatter = LaTeXFormatter(opts.doc_opt, opts.tikz_opt)
  for s in sents:
    print formatter.doc_header()
    print formatter.wrap_tikzpicture(to_qtree(s))
    print formatter.doc_footer()

if __name__ == '__main__':
  main()
