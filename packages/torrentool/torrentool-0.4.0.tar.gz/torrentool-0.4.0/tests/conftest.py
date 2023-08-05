import pytest
from os.path import dirname, abspath, join


@pytest.fixture
def read_fixture(request):

    path_module = dirname(abspath(request.module.__file__))
    path_fixtures = join(path_module, 'fixtures')

    def read_it(fname):
        with open(join(path_fixtures, fname)) as f:
            return f.read()

    return read_it