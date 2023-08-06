#require no-msys # MSYS will translate web paths as if they were file paths

This is a test of passing our envconfig to wsgi

  $ . "$TESTDIR/testlib"

initialize repository

  $ hg init test
  $ cd test
  $ echo a > a
  $ hg ci -Aqma0
  $ echo a >> a
  $ hg ci -qma1
  $ cd ..

create wsgi script

  $ cat >hgweb.cgi <<HGWEB
  > #
  > # An example CGI script to use hgweb, edit as necessary
  > import cgitb
  > import os
  > cgitb.enable()
  > from wsgiref.simple_server import make_server
  > from mercurial import demandimport; demandimport.enable()
  > from mercurial.hgweb import hgweb
  > application = hgweb("test", "Empty test repository")
  > httpd = make_server('', $HGPORT, application)
  > open('hg.pid', 'w').write("%s\n" % os.getpid())
  > httpd.serve_forever()
  > HGWEB
  $ chmod 755 hgweb.cgi

start wsgi server

  $ HGCONFIG=phases.publish=False python hgweb.cgi > /dev/null 2>&1 &
  $ sleep 1

clone

  $ hg clone http://localhost:$HGPORT/ test-clone
  requesting all changes
  adding changesets
  adding manifests
  adding file changes
  added 2 changesets with 2 changes to 1 files
  updating to branch default
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved

  $ cd test-clone
  $ hg phase .
  1: draft
  $ cd ..

kill server

  $ kill $(cat hg.pid)
  $ wait 2>/dev/null >/dev/null
  $ sleep 1
