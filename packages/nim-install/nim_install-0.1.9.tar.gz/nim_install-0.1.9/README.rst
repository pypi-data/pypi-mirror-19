
This package can be used to install the nim compiler in a virtualenv:

   virtualenv /your/venv
   source /your/venv/bin/activate
   pip install nim_install
   nim_install
   nim --version

installs nim version 0.16.0, nimble, nimgrep and nimsuggest

The compilation of nim is executed in parallel. Total installation time is about
40 seconds on my machine (including download time).
