import os

try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve

from django.core.management import BaseCommand
from django.conf import settings
from django.core.validators import URLValidator

from static_import.base import (get_libs, is_css,
                                is_js, is_img)


url_validator = URLValidator()
base_dir = settings.BASE_DIR


class Command(BaseCommand):

    static = 'Url|Static File Name'
    help = 'download static files'

    @staticmethod
    def guess_path(name):
        if is_css(name):
            return os.path.join('css', name)
        elif is_js(name):
            return os.path.join('js', name)
        elif is_img(name):
            return os.path.join('img', name)

    @staticmethod
    def create_static_dir_if_not_exists(base_dir):
        if not os.path.exists(os.path.join(base_dir, 'static')):
            os.mkdir(os.path.join(base_dir, 'static'))

        if not os.path.exists(os.path.join(base_dir, 'static/js')):
            os.mkdir(os.path.join(base_dir, 'static/js'))

        if not os.path.exists(os.path.join(base_dir, 'static/css')):
            os.mkdir(os.path.join(base_dir, 'static/css'))

        if not os.path.exists(os.path.join(base_dir, 'static/img')):
            os.mkdir(os.path.join(base_dir, 'static/img'))

    def download_file(self, url, where_to_save):
        if not os.path.exists(where_to_save):
            self.stdout.write("downloading %s" % os.path.basename(where_to_save))
            urlretrieve(url, where_to_save)
            self.stdout.write("download done!")
        else:
            self.stdout.write('file %s already exists' % os.path.basename(where_to_save))

    def add_arguments(self, parser):
        parser.add_argument('args', metavar=self.static, nargs='+')
        parser.add_argument('--dir', action='store', dest='directory', default=base_dir, help='directory where to save static files')

    def handle(self, *args, **options):
        directory = options['directory']
        self.create_static_dir_if_not_exists(directory)

        for lib in args:
            try:
                url_validator(lib)
            except:
                continue

            path = self.guess_path(os.path.basename(lib))
            path = os.path.join(directory, 'static/' + path)
            self.download_file(lib, path)

        for lib in get_libs():
            if lib['name'] in args:
                path = self.guess_path(os.path.basename(lib['url']))
                path = os.path.join(directory, 'static/' + path)
                self.download_file(lib['url'], path)
