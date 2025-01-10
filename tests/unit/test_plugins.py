import ngp.plugins
from ngp.core import discover_plugins


def test_plugins():
    plugins = discover_plugins(ngp.plugins)

    assert len(plugins) == 1
