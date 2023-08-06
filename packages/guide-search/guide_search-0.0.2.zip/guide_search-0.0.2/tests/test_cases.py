
import os
from guide_search.esearch import Esearch

root = os.path.dirname(__file__)
esearch = Esearch('http://gl-know-ap33.lnx.lr.net:9200',
                  'dev', 'knowledge_config/control')


def test_pass():
    url = esearch.makeUrl("dev")
    if url == 'http://gl-know-ap33.lnx.lr.net:9200/dev':
        return True
    else:
        raise ValueError(msg)
        return False

def test_fail():
    raise ValueError("Test failure")
    assert False
