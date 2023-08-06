#require test-repo pyflakes

Copied from Mercurial core (60ee2593a270)

  $ cd "`dirname "$TESTDIR"`"

run pyflakes on all tracked files ending in .py or without a file ending
(skipping binary file random-seed)

  $ hg locate 'set:**.py or grep("^!#.*python")' 2>/dev/null \
  > | xargs pyflakes 2>/dev/null  

run flake8 if it exists; if it doesn't, then just skip

  $ type flake8 >/dev/null 2>/dev/null && hg files -0 'glob:**.py' | xargs -0 flake8 || true
