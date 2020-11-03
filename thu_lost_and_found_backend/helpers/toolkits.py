import errno
import os

from django.shortcuts import get_object_or_404

from thu_lost_and_found_backend.settings import BASE_DIR


def delete_media_file(file_path):
    # Remove initial '/' in file path
    path = os.path.join(BASE_DIR, file_path[1:])
    # Silent remove
    try:
        os.remove(path)
    except OSError as e:
        if e.errno != errno.ENOENT:  # e
            # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occurred


def delete_media_instance(model, pk, media_attributes):
    # Handle single attribute
    if type(media_attributes) not in [list, tuple]:
        media_attributes = [media_attributes]

    instance = get_object_or_404(model, pk=pk)
    for attribute in media_attributes:
        url = getattr(instance, attribute).url
        delete_media_file(url)
    instance.delete()
