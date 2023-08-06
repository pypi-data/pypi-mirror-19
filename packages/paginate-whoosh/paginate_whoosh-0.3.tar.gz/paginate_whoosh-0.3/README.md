paginate_whoosh
---------------

This module is an extension to the [paginate](https://github.com/Pylons/paginate) module. It divides
up search results obtained with Whoosh.


Usage
-----
```
from paginate_whoosh import WhooshPage

qp = QueryParser("text", myindex.schema)
q = qp.parse("a query")

with myindex.searcher() as searcher:
    page = WhooshPage(
        searcher.search(q, limit=None), # limit=None is required!
        page=1, items_per_page=10)
    # Now continue as you are used from the paginate module.
    # Iterate over page to obtain the Whoosh result dictionary
```