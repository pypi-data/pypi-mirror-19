import sys
import os
import django

current_dir = os.path.dirname(os.path.abspath(__file__))
example_dir = os.path.join(current_dir, 'example')
sys.path.append(example_dir)

if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'example.settings'
    DJANGO_SETTINGS_MODULE = 'example.settings'

django.setup()


def runtests(args=None):
    import pytest

    if not args:
        args = []

    if not any(a for a in args[1:] if not a.startswith('-')):
        args.append('tests')

    result = pytest.main(['-x', 'example/example_app/tests.py'])
    sys.exit(result)


if __name__ == '__main__':
    runtests(sys.argv)

