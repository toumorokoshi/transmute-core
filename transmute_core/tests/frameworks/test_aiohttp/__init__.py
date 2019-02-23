import pytest
import sys

pytestmark = pytest.mark.skipif(sys.version_info < (3,), reason="Python version must be greater than 3.")