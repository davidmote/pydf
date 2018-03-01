from unittest import mock


class Test_unzip:
    """ unzip() """

    def test_success(self, tmpdir):
        """ It should be able to unzip a file and return a list of paths """
        import os.path
        import zipfile

        from pdfy.utils import unzip

        zip_file = tmpdir.join('bundle.zip')
        unzip_dir = tmpdir.join('files')

        with zipfile.ZipFile(str(zip_file), 'w') as zip_fp:
            zip_fp.writestr('test.txt', 'My test')

        names = list(unzip(zip_file.open('rb'), unzip_dir))
        assert os.path.basename(names[0]) == 'test.txt'

    def test_ignore_hidden_files(self, tmpdir):
        """ It should ignore hidden files """
        import zipfile

        from pdfy.utils import unzip

        zip_file = tmpdir.join('bundle.zip')
        unzip_dir = tmpdir.join('files')

        with zipfile.ZipFile(str(zip_file), 'w') as zip_fp:
            zip_fp.writestr('.hidden.txt', 'My test')

        names = list(unzip(zip_file.open('rb'), str(unzip_dir)))
        assert names == []


class Test_find_index:
    """ find_index() """

    def test_found(self):
        """ It should find a name that begins with "index." """
        from pdfy.utils import find_index

        expected = 'index.htm'
        result = find_index([expected])
        assert result == expected

    def test_not_found(self):
        """ It returns None if not the index was not found """
        from pdfy.utils import find_index

        result = find_index(['something.html'])
        assert result is None


class Test_template_to_pdf:
    """ template_to_pdf() """

    def test_success(self, tmpdir):
        """ It should successfull generate a PDF from a template file """

        from pdfy.utils import template_to_pdf

        template_path = tmpdir.join('template.html')
        template_path.write('My {foo}')
        params = {'foo': 'World'}

        with template_path.open() as source_fp:
            pdf_bytes = template_to_pdf(source_fp, params=params)

        assert pdf_bytes.startswith(b'%PDF-')

    @mock.patch('pdfy.utils.tempfile.NamedTemporaryFile')
    @mock.patch('pdfy.utils.HTML')
    def test_html_relative(self, NamedTemporaryFile, HTML, tmpdir):
        """ It should render the template same directory so assets still work """

        import os.path
        from pdfy.utils import template_to_pdf

        template_path = tmpdir.join('template.html')
        template_path.write('My {foo}')
        params = {'foo': 'World'}

        with template_path.open() as source_fp:
            template_to_pdf(source_fp, params=params)
            assert NamedTemporaryFile.called_once_with(dir=os.path.dirname(source_fp.name))
