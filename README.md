
Note: This is a fork of clone of https://github.com/Codebiosys/pydf.git,
which is no longer maintained.

# PyDF

A tool that generates a PDF from an re-usable HTML template


## Background

This library  will take a mustache template, render with parameters, apply a set of style
sheets, include images, and output a PDF file.


## Project Goals

* Must include dynamic templates (user should be able to choose template)
* Should be able to update template without having to update software
* Must be able to specify a page header and footer
* Must be able to include images
* Must be able to include CSS styling


## Implementation

### pystache (based off Mustache templating language)

This tool uses the [Mustache](http://mustache.github.io/mustache.5.html)
templating language for template rendering.

### weasyprint

This tool uses [weasyprint](http://weasyprint.readthedocs.io/en/latest/)
generating a PDF from HTML content.

For information on how to install on your environment, see:

http://weasyprint.readthedocs.io/en/latest/install.html#installing


## Installation

```
  > pip install git+git://github.com/davidmote/pydf.git@master#egg=pydf
```


## Development

```
  > mkvirtualenv pydf
  > git clone https://github.com/davidmote/pydf.git
  > cd pydf
  > pip install -r requirements-develop.txt
  > pip install -e .
  > pytest -vv
```

## Running Tests
To run tests, install pydf in development mode (as above), and run pytest

```
  > pytest
```

## Contributing
If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are welcome.
