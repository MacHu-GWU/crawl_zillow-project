pushd "%~dp0"
cd crawl_zillow
python3 zzz_manual_install.py
cd ..
python3 create_doctree.py
make html