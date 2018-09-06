import os.path
import tempfile
import zipfile

import pystache
from weasyprint import HTML


def unzip(fp, dest):
    """ Unzips a file and returns the list of extracted paths

    This method will ignore any hidden files in the archive.

    :param fp: File-like object of the archive
    :type fp: file
    :param dest: Directory to put extracted files in
    :type dest: str

    :return: list of extracted paths
    """
    with zipfile.ZipFile(fp) as zip_fp:
        for name in zip_fp.namelist():
            if not os.path.basename(name).startswith('.'):
                yield zip_fp.extract(name, dest)


def find_index(names):
    """ Finds an index file in a list of file names

    This function addresses the issue of locating the index file in
    an archive file which could have nested directories.

    :param names: list of path names
    :type names: list
    :return: the value that contains index
    """
    for name in names:
        if os.path.basename(name).startswith('index.'):
            return name


def template_to_pdf(source_fp, target_fp=None, params={}, config={}):
    """ Runs the full stack of template file to PDF file

    :param source_fp: source template file object
    :type source_fp: file
    :param target_fp: (optional) target pdf file object
    :type target_fp: file
    :param params: template parameters
    :type params: dict
    :param config: pdf configuration
    :type config:

    :return: PDF byte string if not target_fp was specified
    """
    source_fp.seek(0)  # start at the beginning of a potentially read file

    template_content = source_fp.read()
    html_content = pystache.render(template_content, params)

    # Create a temporay file in the same location as the template file so that
    # all of the relative assets still work
    with tempfile.NamedTemporaryFile(dir=os.path.dirname(source_fp.name)) as temp_fp:
        temp_fp.write(bytes(html_content, 'utf8'))
        temp_fp.flush()
        temp_fp.seek(0)
        return HTML(file_obj=temp_fp).write_pdf(target=target_fp, **config)
