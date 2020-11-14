import errno
import os
import time
from PIL import Image
from django.conf import settings

from django.shortcuts import get_object_or_404

from thu_lost_and_found_backend.settings import BASE_DIR


def timestamp_filename(file_name, file_extension):
    return f'{file_name}_{int(time.time())}.{file_extension}'


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


def save_uploaded_images(request, upload_to, instance):
    """
    @return: array of JSON string if success, None if fail
    """

    # /media/
    k_media_url = settings.MEDIA_URL
    # BASE_DIR/media/
    k_media_root = settings.MEDIA_ROOT
    # http://website.com
    k_app_url = settings.APP_URL

    result = []

    try:
        for filename, file in request.FILES.items():
            # Save image
            image = Image.open(request.FILES[filename])

            save_file_dir = os.path.join(k_media_root, upload_to)
            if not os.path.exists(save_file_dir):
                os.makedirs(save_file_dir)

            save_file_name = timestamp_filename(f'id_{instance.id}', filename.split('.')[-1])
            save_file_path = os.path.join(save_file_dir, save_file_name)

            image.save(save_file_path)

            # Image url for database
            file_abs_url = k_app_url + k_media_url + save_file_name

            result.append(file_abs_url)

        return result

    except (ValueError, OSError) as error:
        print(f'Save Image Error: {error}')
        return None
