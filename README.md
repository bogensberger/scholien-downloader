# Scholarium Downloader

The scholarium downloader is a tool to automatically
download purchased eBooks from https://scholarium.at

Setup a virtualenv:

    python3 -m venv .venv
    .venv/bin/python -m pip install -U pip setuptools
    .venv/bin/python -m pip install -r requirements.txt
    .venv/bin/pip install -e .

Run the downloader:

    .venv/bin/download <email> <password>

The files will be downloaded into the `downloads` folder within this repo.
