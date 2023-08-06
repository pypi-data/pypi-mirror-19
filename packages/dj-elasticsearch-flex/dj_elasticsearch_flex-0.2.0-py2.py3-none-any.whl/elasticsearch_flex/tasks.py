from celery import shared_task


@shared_task
def update_indexed_document(index, created, pk):
    if created:
        indexed_doc = index.init_using_pk(pk)
    else:
        indexed_doc = index.get(id=pk)
    # Call the prepare method
    indexed_doc.prepare()
    indexed_doc.save()


@shared_task
def delete_indexed_document(index, pk):
    indexed_doc = index.get(id=pk)
    indexed_doc.delete()


__all__ = ('update_indexed_document', 'delete_indexed_document')
