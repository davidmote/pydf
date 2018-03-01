# PDFy

A tool that generates a PDF from an re-usable HTML template


## Background

Several project require PDF report generation with included images and graphs,
such as application validation/verification via automated testing,
templated reports, customized documents, etc. Therefore the need for a service
to automate this workflow is desired.

The component will take a template, render with parameters, apply a set of style
sheets, include images, and output a PDF file.


## Project Goals

* Must include dynamic templates (user should be able to choose template)
* Should be able to update template without having to update software
* Must be able to specify a header and footer
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
  > pip install pdfy
```


## Development

```
  > mkvirtualenv pdfy
  > git clone https://github.com/Codebiosys/pdfy.git
  > cd pdfy
  > pip install -r requirements-develop.txt
  > pip install -e .
  > pytest -vv
```
