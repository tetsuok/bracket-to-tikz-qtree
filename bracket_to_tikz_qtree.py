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
import os
import sys
import subprocess
import tempfile

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

# LaTeX treats the following characters as special characters in the
# syntax.
special_chars = ['{', '}', '$', '&', '%']

def replace_special(s):
  for c in special_chars:
    s = s.replace(c, '\\' + c)
  return s

def to_qtree(text):
  """Convert a bracketed text to the Qtree style brackets."""
  return '''\Tree ''' + text.replace('(', '[.').replace(')', ' ]')

### Reader

def tokenize(s):
  return s.replace('(',' ( ').replace(')',' ) ').split()

def _read(f):
  """Read lines of bracketed texts.

  Note that we don't check whether the text have valid trees or not
  since the format of the bracket text depends on corpus (e.g., Penn
  Treebank) or parser (e.g. Stanford parser).
  """
  sents = []
  s = ''
  depth = 0
  for i, l in enumerate(f):
    if l.startswith(';'):       # comment
      continue

    if depth == 0 and l.startswith('\n'):
      continue
    elif l.startswith('\n'):
      raise SyntaxError('unexpected EOF line while reading')

    if l.startswith('( (S'):    # Hack for Penn Treebank's style format.
      l = l.replace('( (S', '(ROOT (S')

    lis = tokenize(l)
    for v in lis:
      if v == '(':
        depth += 1
      elif v == ')':
        depth -= 1

    l = replace_special(l)

    if depth == 0:
      s += l
      sents.append(s.rstrip())
      s = ''
      depth = 0
      continue

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
  parser.add_option('--enable-pdf', dest='enable_pdf', action="store_true", default=False,
                    help='Flag to enable to compile with pdfLaTeX [default: %default]')
  parser.add_option('--out-prefix', dest='out_prefix', default='qt00',
                    help='Prefix name to name generated pdf files. This option has a meaning when you turn `--enable-pdf` on [default %default]')
  (options, unused_args) = parser.parse_args()
  return (options, unused_args)

def check_and_remove(filename):
  if os.path.exists(filename):
    os.remove(filename)

def exec_latex(file, latex_cmd='pdflatex'):
  cmd = [latex_cmd, file]
  try:
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

  except:
    print '========='
    print 'ERROR: %s' % ' '.join(sys.argv)
    print '========='
    raise

  (stdout_content, err) = process.communicate()
  process.wait()
  return (stdout_content, err)

def main():
  opts, unused_args = parse_options()

  if len(unused_args) == 0:
    sents = read(sys.stdin)
  else:
    sents = read(unused_args[0])

  formatter = LaTeXFormatter(opts.doc_opt, opts.tikz_opt)
  for i, s in enumerate(sents):
    # Generate a pdf file directly for each tree structure.
    if opts.enable_pdf:
      temp = tempfile.NamedTemporaryFile(mode='w+t')
      try:
        print >>temp, formatter.doc_header()
        print >>temp, formatter.wrap_tikzpicture(to_qtree(s))
        print >>temp, formatter.doc_footer()

        print >>sys.stderr, 'LOG: Writing generated latex file as a temporary file = %s' % temp.name

        temp.seek(0)
        base = os.path.basename(temp.name)
        # os.system('pdflatex %s' % temp.name)

        out, err = exec_latex(temp.name)
        with open(opts.out_prefix + str(i) + '.log', 'w') as fout:
          print >>fout, out
          print >>fout, err

        if os.path.exists(base + '.pdf'):
          os.rename(base + '.pdf', opts.out_prefix + str(i) + '.pdf')

        check_and_remove(base + '.aux')
        check_and_remove(base + '.log')
      finally:
        temp.close()
    else:
      if i > 0: print
      print formatter.doc_header()
      print formatter.wrap_tikzpicture(to_qtree(s))
      print formatter.doc_footer()

if __name__ == '__main__':
  main()
