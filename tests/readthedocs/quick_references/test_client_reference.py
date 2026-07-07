import re

from splusthon import SoroushClient


def test_all_methods_present(docs_dir):
    with (docs_dir / 'quick-references/client-reference.rst').open(encoding='utf-8') as fd:
        present_methods = set(map(str.lstrip, re.findall(r'^ {4}\w+$', fd.read(), re.MULTILINE)))

    assert len(present_methods) > 0
    for name in dir(SoroushClient):
        attr = getattr(SoroushClient, name)
        if callable(attr) and not name.startswith('_') and name != 'sign_up':
            assert name in present_methods
