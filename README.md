# FLIPHTML5 Downloader

Extract book page images from [FLIPHTML5](fliphtml5.com). The downloaded images can then be converted into PDF using the included `pdfconverter.py`

## Usage

### Downloader

Make sure that the packages `requests`, `argparse`, `queue`, `os`, `errno`, `random` and `threading` are installed.

Then simply run

```
python run downloader.py [book id] [from page] [until page] [no of threads]
```

`book id` is the pair of codes in the URL. For example, the book id of `https://fliphtml5.com/bbwjp/xnfu` is `bbwjp/xnfu`.

The extracted images are stored in the folder with the name corresponding to the book id.

### PDF Converter

Make sure that the packages `img2pdf` is installed.

Then simply run

```
python run pdfconverter.py [foldername] [from page] [until page]
```

The output PDF file is stored in the same folder as the images.