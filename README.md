# Instagram-dl

Simple script to download Instagram images and comments to .csv without selenium (purely http get requests).

Only downloads parent comments, does not download child replies.

No protections against rate-limiting.

## Usage

```sh
usage: instagram-dl.py [-h] [-i] [-c] input_link

Downloads Instagram images/comments

positional arguments:
  input_link  The link, or shortcode, of the post to download

optional arguments:
  -h, --help  show this help message and exit
  -i          Download images only
  -c          Download comments only

Omit both optional arguments to download both
```

## Output

All files are downloaded to the current directory

### Comments

Parent comments are formatted as the following in `comments.csv`:

| date             | username | comment |
|------------------|----------|---------|
| YYYYMMDDThhmmssZ | <>       | <>      |

### Images

Image filenames are formatted as: `[date]_[author]_[id].jpg`

## Future TODO

* try/except for rate-limit/error status codes
* option to save to xlsx so utf-8 emoji renders properly
* save other metadata from comment scrape
