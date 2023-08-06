from os.path import join, normpath, isfile, dirname, getmtime
from importlib.util import find_spec
from functools import lru_cache
from logging import getLogger

from jinja2 import BaseLoader, TemplateNotFound


log = getLogger(__name__)


class Loader(BaseLoader):
    def __init__(self, *, root_dir='templates', app_subdir='templates',
                 lstrip=False):
        self.root_dir = root_dir
        self.app_subdir = app_subdir
        self.lstrip = lstrip

    def get_source(self, env, template):
        filename = self.get_filename(template)
        if not filename:
            raise TemplateNotFound(template)

        if not env.auto_reload and filename in env.cache:
            # Do not reload template source if it is not necessary
            return '', filename, lambda: True

        log.debug('Load template source: %s', template)
        with open(filename, encoding='utf-8') as f:
            source = f.read()
        if self.lstrip:
            source = '\n'.join(row.lstrip() for row in source.split('\n'))
        mtime = getmtime(filename)
        return source, filename, lambda: mtime == getmtime(filename)

    @lru_cache()
    def get_filename(self, template):
        for filename in self.iter_filenames(template):
            if isfile(filename):
                return filename

    def iter_filenames(self, template):
        if self.root_dir:
            yield join(self.root_dir, normpath(template))
        if '/' in template:
            modname, filename = template.split('/', 1)
            spec = find_spec(modname)
            if spec:
                moddir = dirname(spec.loader.path)
                yield join(moddir, self.app_subdir, filename)
