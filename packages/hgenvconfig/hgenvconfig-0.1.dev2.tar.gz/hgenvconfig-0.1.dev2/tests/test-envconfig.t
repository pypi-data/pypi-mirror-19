  $ . "$TESTDIR/testlib"

  $ hg init pinky
  $ cd pinky

Test that we can pass in a single config

  $ echo readme >> README.md
  $ hg add -q
  $ hg ci -m c0
  $ hg log -pr .
  changeset:   0:e1e889f3db3c
  tag:         tip
  user:        test
  date:        Thu Jan 01 00:00:00 1970 +0000
  summary:     c0
  
  diff -r 000000000000 -r e1e889f3db3c README.md
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/README.md	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +readme
  
  $ HGCONFIG="diff.git=True" hg log -pr .  
  changeset:   0:e1e889f3db3c
  tag:         tip
  user:        test
  date:        Thu Jan 01 00:00:00 1970 +0000
  summary:     c0
  
  diff --git a/README.md b/README.md
  new file mode 100644
  --- /dev/null
  +++ b/README.md
  @@ -0,0 +1,1 @@
  +readme
  
Make sure multiple configs that have bogus ones don't mess up

  $ HGCONFIG="diff.git=True\nexperimental.foo=bar\n" hg log -pr .
  changeset:   0:e1e889f3db3c
  tag:         tip
  user:        test
  date:        Thu Jan 01 00:00:00 1970 +0000
  summary:     c0
  
  diff --git a/README.md b/README.md
  new file mode 100644
  --- /dev/null
  +++ b/README.md
  @@ -0,0 +1,1 @@
  +readme
  
Test multiple configs

  $ HGCONFIG="diff.git=True\nui.verbose=True" hg log -pr .
  changeset:   0:e1e889f3db3c
  tag:         tip
  user:        test
  date:        Thu Jan 01 00:00:00 1970 +0000
  files:       README.md
  description:
  c0
  
  
  diff --git a/README.md b/README.md
  new file mode 100644
  --- /dev/null
  +++ b/README.md
  @@ -0,0 +1,1 @@
  +readme
  
