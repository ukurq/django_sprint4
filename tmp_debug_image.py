import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogicum.settings')
import django
django.setup()
from django.test import Client
from blog.models import Post, Category, Location
from django.contrib.auth import get_user_model
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files.images import ImageFile
from bs4 import BeautifulSoup, SoupStrainer

User = get_user_model()
user = User.objects.create_user('tester', 'test@test.com', '12345')
loc = Location.objects.create(name='loc', is_published=True)
cat = Category.objects.create(title='cat', description='d', slug='catt', is_published=True)
img = Image.new('RGB', (100, 100), (73, 109, 137))
img_io = BytesIO(); img.save(img_io, format='JPEG'); img_io.seek(0)
image_file = ImageFile(img_io, name='temp_im.jpg')
post = Post.objects.create(title='t', text='t', pub_date=timezone.now(), author=user, location=loc, category=cat, image=image_file)

c = Client()
resp = c.get(f'/profile/{user.username}/')
print('status', resp.status_code)
img_soup = BeautifulSoup(resp.content.decode('utf-8'), features='html.parser', parse_only=SoupStrainer('img'))
imgs = list(img_soup)
print('img_count', len(imgs))
for i, img in enumerate(imgs, start=1):
    print(i, img)
