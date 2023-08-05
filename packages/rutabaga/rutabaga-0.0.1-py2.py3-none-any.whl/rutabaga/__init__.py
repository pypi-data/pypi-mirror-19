import re
import logging
from collections import defaultdict

try:
    from pathlib import Path, PurePath
except ImportError:
    from pathlib2 import Path, PurePath

from jinja2 import Template, FileSystemLoader, Environment


LOG = logging.getLogger(__name__)


class _Context(object):
    """register context generator methods by template name with decorators"""

    def __init__(self, renderer, string, regex=False):
        self.string = string
        self.regex = regex
        self.renderer = renderer

    def __call__(self, func):
        if self.regex:
            return self.renderer.register_matched_ctx(self.string, func)
        return self.renderer.register_named_ctx(self.string, func)


class Renderer(object):

    def __init__(self):
        self.ctx_by_match = defaultdict(lambda: dict)
        self.ctx_by_name = defaultdict(lambda: dict)
        self.excludes = set()

    def _template_filter(self, name):
        return name not in self.excludes

    def register_named_ctx(self, name, func):
        if name in self.ctx_by_name:
            raise RuntimeError(
                'function {}() duplicates context for template {}'
                .format(func.__name__, name))

        self.ctx_by_name[name] = func
        return func

    def register_matched_ctx(self, pattern, func):
        if pattern in self.ctx_by_match:
            raise RuntimeError(
                'function {}() duplicates context for templates matching {}'
                .format(func.__name__, pattern))


        self.ctx_by_match[pattern] = func
        return func

    def create_context(self, name):

        ctx_funcs = []
        for pattern, func in self.ctx_by_match.items():
            if re.match(pattern, name):
                ctx_funcs.append(func)

        ctx_funcs.append(self.ctx_by_name[name])

        context = {}
        for f in ctx_funcs:
            context.update(f())

        return context

    def _render_template(self, env, orig_name, output_path):
        context = self.create_context(orig_name)

        name = Environment().from_string(orig_name).render(context)
        path = output_path / PurePath(name)

        try:
            path.parent.mkdir(parents=True)
        except FileExistsError: pass

        LOG.info('Writing: %s', path)

        with path.open('w') as outfile:
            outfile.write(env.get_template(orig_name).render(context))

        return path

    def render_file(self, src_path, output_path):
        orig_name = src_path.name
        context = self.create_context(orig_name)

        with src_path.open('r') as infile:
            text = Environment().from_string(infile.read()).render(context)

        name = Environment().from_string(orig_name).render(context)
        path = output_path / PurePath(name)

        LOG.info('Writing: %s', path)

        with path.open('w') as outfile:
            outfile.write(text)

        return path

    def render_diectory(self, src_path, output_path):
        env = Environment(loader=FileSystemLoader(src_path))
        template_names = env.list_templates(filter_func=self._template_filter)

        files = []
        for t_name in template_names:
            f = self._render_template(env, t_name, output_path)
            files.append(f)

        return files

    def context_for(self, string, regex=False):
        return _Context(self, string, regex)
