import os, django
os.chdir('c:/Users/ukur/Desktop/Yandex Practicum 3/django_sprint4')
os.environ.setdefault('DJANGO_SETTINGS_MODULE','blogicum.settings')
django.setup()
from mixer.backend.django import mixer
from django.test import Client
from django.utils import timezone
from django.core.files.images import ImageFile
from io import BytesIO
from PIL import Image

user = mixer.blend('auth.User')
cat = mixer.blend('blog.Category', is_published=True)
loc = mixer.blend('blog.Location', is_published=True)
img = Image.new('RGB', (100,100), color=(73,109,137))
img_io = BytesIO(); img.save(img_io,'JPEG'); img_io.seek(0)
image_file = ImageFile(img_io, name='temp_image.jpg')
post = mixer.blend('blog.Post', is_published=True, pub_date=timezone.now(), author=user, category=cat, location=loc, image=image_file)
client = Client(); client.force_login(user)
urls = ['/', f'/profile/{user.username}/', f'/category/{cat.slug}/']
for u in urls:
    res = client.get(u)
    print('before', u, res.status_code, res.content.decode().count('<img'))
post.image = None
post.save()
for u in urls:
    res = client.get(u)
    print('after', u, res.status_code, res.content.decode().count('<img'))
