# Springer Books (FREE) Download

Quick python automoation scripts to list and download books.

## Setup:

```shell script
git clone https://github.com/pingu1m/springer-books-downloader.git
cd springer-books-downloader
pip install
```

## Usage:

### List:
```shell script
cd springer-books-downloader
python3 ./sbd.py statistics Keyword2 --action list
# or
./sbd.py statistics calculus physics --action list
```
### Download
```shell script
cd springer-books-downloader
python3 ./sbd.py statistics Keyword2 --action download
# or
./sbd.py statistics calculus physics --action download
```

## TODO:

- Add method to download all
- Add method to download a single book
- Make it generic enough to be used with other datasets
- Add tests

