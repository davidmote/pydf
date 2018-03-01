""" Command-line interface to PDFy functions.

The intention of this script is to be callable from some deamon services
such as a dedicated Docker microservice
"""

import json
import tempfile
import shutil
import zipfile
import sys

import click

from ..utils import unzip, find_index, template_to_pdf


@click.command()
@click.option('-s', '--source', 'source_fp', type=click.File('rb'), help='Source template file or zip file')  # noqa
@click.option('-t', '--target', 'target_fp', type=click.File('wb'), help='Target PDF file')
@click.option('-p', '--params', 'params_fp', type=click.File('rb'), help='Temmplate parameters')
@click.option('-c', '--config', 'config_fp', type=click.File('rb'), help='PDF file configuration')
def main(source_fp, target_fp, params_fp, config_fp):
    """ Generates a PDF from an input HTML template with optional parameters

    Optionaly, this command will extract a zipped bundle that contains the
    template file as well as asset files. If using this feature, the main
    template MUST being with 'index' to allow for any file extension to be
    used.
    """

    if not source_fp:
        click.secho('Source required', fg='red', bold=True)
        sys.exit(1)

    if not target_fp:
        click.secho('Target required', fg='red', bold=True)
        sys.exit(1)

    tmp_dir = None          # temporary directory to extract files into
    index_fp = source_fp    # Index template file

    if zipfile.is_zipfile(source_fp):
        tmp_dir = tempfile.mkdtemp()
        files = list(unzip(source_fp, tmp_dir))
        index_path = find_index(files)

        if not index_path:
            click.secho('Could not find index file', fg='red', bold=True)
            sys.exit(1)

        index_fp = open(index_path)

    try:
        params = json.load(params_fp) if params_fp else {}
        config = json.load(config_fp) if config_fp else {}
        template_to_pdf(index_fp, target_fp, params, config)
    finally:
        # Ensure we cleanup after ourselves if there was a failure
        if tmp_dir:
            # Close index file we created
            index_fp.close()
            shutil.rmtree(tmp_dir)


if __name__ == '__main__':
    main()
