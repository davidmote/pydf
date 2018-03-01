import pytest


@pytest.fixture
def runner():
    """ Returns a runner to invoke click commands """
    from click.testing import CliRunner
    return CliRunner()


class Test_main:
    """ main() """

    def test_source_required(self, runner, tmpdir):
        """ It should require template source """
        from pdfy.commands.cli import main
        result = runner.invoke(main, ['--target', str(tmpdir.join('output.pdf'))])
        assert result.exit_code == 1, result.output
        assert 'Source required' in result.output

    def test_target_required(self, runner, tmpdir):
        """ It should require a target output file """
        from pdfy.commands.cli import main
        source = tmpdir.join('source.html')
        source.write('<b>Hello World!</b>')
        result = runner.invoke(main, ['--source', str(source)])
        assert result.exit_code == 1, result.output
        assert 'Target required' in result.output

    def test_success_regular_template(self, runner, tmpdir):
        """ It should generate a PDF for a regular template file """
        from pdfy.commands.cli import main
        source = tmpdir.join('source.html')
        source.write('<b>Hello World!</b>')
        target = tmpdir.join('output.pdf')
        result = runner.invoke(main, [
            '--source', str(source),
            '--target', str(target),
        ])
        assert result.exit_code == 0
        assert target.size() > 0

    def test_sucess_zip_template(self, runner, tmpdir):
        """ It should accept a zip file that contains template assets """
        import zipfile
        from pdfy.commands.cli import main

        source = tmpdir.join('template.zip')
        target = tmpdir.join('output.pdf')

        with zipfile.ZipFile(str(source), 'w') as zip_fp:
            zip_fp.writestr('index.html', '<b>Hello {foo}</b>')

        result = runner.invoke(main, [
            '--source', str(source),
            '--target', str(target),
        ])
        assert result.exit_code == 0
        assert target.size() > 0

    def test_fail_zip_template_no_index(self, runner, tmpdir):
        """ It should fail if the zip bundle has no index file """
        import zipfile
        from pdfy.commands.cli import main

        source = tmpdir.join('template.zip')
        target = tmpdir.join('output.pdf')

        with zipfile.ZipFile(str(source), 'w') as zip_fp:
            zip_fp.writestr('notindex.html', '<b>Hello {foo}</b>')

        result = runner.invoke(main, [
            '--source', str(source),
            '--target', str(target),
        ])
        assert result.exit_code == 1
        assert 'Could not find index file' in result.output
