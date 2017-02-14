import six
from elasticsearch.helpers import scan

from aleph.core import es, es_index
from aleph.index.mapping import TYPE_DOCUMENT, TYPE_RECORD, TYPE_ENTITY  # noqa
from aleph.index.admin import flush_index
from aleph.index.util import bulk_op


def delete_collection(collection_id):
    """Delete all documents from a particular collection."""
    q = {'query': {'term': {'collection_id': collection_id}}, '_source': False}

    def deletes():
        types = [TYPE_RECORD, TYPE_DOCUMENT, TYPE_ENTITY]
        for res in scan(es, query=q, index=es_index, doc_type=types):
            yield {
                '_op_type': 'delete',
                '_index': six.text_type(es_index),
                '_parent': res.get('_parent'),
                '_type': res.get('_type'),
                '_id': res.get('_id')
            }

    flush_index()
    bulk_op(deletes())
