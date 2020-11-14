import errno
import os
import time
from PIL import Image
from django.conf import settings
from django.db.models import Max

from django.shortcuts import get_object_or_404

from thu_lost_and_found_backend.settings import BASE_DIR


def timestamp_filename(file_name, file_extension):
    return f'{file_name}_{int(round(time.time() * 1000))}.{file_extension}'


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


def delete_media_instance(instance, media_attributes):
    # Handle single attribute
    if type(media_attributes) not in [list, tuple]:
        media_attributes = [media_attributes]

    for attribute in media_attributes:
        url = getattr(instance, attribute).url
        delete_media_file(url)
    instance.delete()


def save_uploaded_images(request, upload_to, instance=None, model=None):
    """
    Save images as urls in json in database
    @return: True if success, False if fail
    """

    # /media/
    k_media_url = settings.MEDIA_URL
    # BASE_DIR/media/
    k_media_root = settings.MEDIA_ROOT
    # http://website.com
    k_app_url = settings.APP_URL

    result = []

    if instance:
        instance_id = instance.id
    else:
        id_max = model.objects.all().aggregate(Max('id'))['id__max']
        id_next = id_max + 1 if id_max else 1
        instance_id = id_next

    try:
        for filename, file in request.FILES.items():
            # Save image
            image = Image.open(request.FILES[filename])

            save_file_dir = os.path.join(k_media_root, upload_to)
            if not os.path.exists(save_file_dir):
                os.makedirs(save_file_dir)

            save_file_name = timestamp_filename(f'id_{instance_id}', filename.split('.')[-1])
            save_file_path = os.path.join(save_file_dir, save_file_name)

            image.save(save_file_path)

            # Image url for database
            file_abs_url = k_app_url + k_media_url + f'{upload_to}/' + save_file_name

            result.append(file_abs_url)

        if instance:
            # Update instance's database
            if not instance.images:
                instance_images = {'image_urls': []}
            else:
                instance_images = instance.images

            instance_images['image_urls'].extend(result)
            instance.images = instance_images
            instance.save()

        return result

    except (ValueError, OSError) as error:
        print(f'Save Image Error: {error}')
        return None
