0.4.13 (2016-12-30)

- gitignore release.sh temp files so they dont affect git status.
- move most of 1100-line main into four new files.
- add Form class.
- domain.py->irs.py.
- extractFillableFields.El derives from dict.
- combined rst format files into a single README file.
- noticed markdown readme is not rendered on pypi, fixing [part of fix is in release.sh].

0.4.12 (2016-12-23)
- bind arrow keys to next/prev page links [for demo video].
- [release.sh remains untracked while it is being tested.]

0.4.11 (2016-12-21)
- allow multiple 'rootForms' via call or commandline.
- output form statuses for external processing.
- clean up "import *".
- add cleanup script.
- merge the missing and spurious categories into the form status message.
- use bumpversion as cookiecutter does.

