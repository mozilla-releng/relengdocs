Manual testing of dep-signed mar files
======================================

Usually, mar files are created and tested in automation.  Occasionally,
we need to create special-purpose mar files, typically for
channel-switching purposes (e.g. OS de-support).

In those cases it's preferable to test the mar file before it gets
signed for production, so we have to essentially replicate what
update-verify does for staging releases: patch the updater to accept a
"dep" certificate, run it against the dep-signed mar file and an
existing firefox release, and check that it has the expected outcome.

The following example assumes we're on Linux and want to test a mar file
applied to a windows install::

  cd $(mktemp -d)
  wget https://archive.mozilla.org/pub/firefox/releases/114.0/linux-x86_64/en-US/firefox-114.0.tar.bz2
  tar xf firefox-114.0.tar.bz2
  mkdir update
  CERT_DIR="${GECKO}/tools/update-verify/release/mar_certs"
  python3 "${GECKO}/tools/update-verify/release/replace-updater-certs.py" \
    "${CERT_DIR}" \
    firefox/updater update/updater \
    release_primary.der dep1.der \
    release_secondary.der dep2.der
  chmod +x update/updater

If the source install is a nightly build rather than beta or release,
use `nightly_aurora_level3_{primary,secondary}.der` instead of
`release_{primary,secondary}.der`.

Copy your dep-signed mar to `update/update.mar`, e.g.::

  wget https://firefox-ci-tc.services.mozilla.com/api/queue/v1/task/afYMhkhXSw6PsG0dWthmUA/runs/0/artifacts/public%2Fbuild%2Fswitch-to-esr115.0-eol-win.mar
  cp public%2Fbuild%2Fswitch-to-esr115.0-eol-win.mar update/update.mar

Next, run the patched updater against the target binary::

  wget https://archive.mozilla.org/pub/firefox/releases/114.0/win64/en-US/Firefox%20Setup%20114.0.exe
  mkdir target
  7z x -otarget "Firefox Setup 114.0.exe"
  LD_LIBRARY_PATH=$PWD/firefox $PWD/update/updater $PWD/update $PWD/target/core/ $PWD/target/core/ 0
  res=$?
  cat update/update.log
  if [ $res -ne 0 ]; then echo UPDATE FAILED (updater exited $res) >&2; fi

Finally check that the target directory looks as expected.

The `wiki
<https://wiki.mozilla.org/Software_Update:Manually_Installing_a_MAR_file>`_ has
more info on running the updater manually on the various platforms.
