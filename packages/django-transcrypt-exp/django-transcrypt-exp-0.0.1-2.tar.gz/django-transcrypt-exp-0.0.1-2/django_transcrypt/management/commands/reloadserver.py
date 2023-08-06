import os
import itertools
from django.conf import settings
from django.apps import apps
from django.core.management.base import BaseCommand
from livereload import livereload_port, server as S, livereload_host
from livereload.server import shell
from ..getdeps import getdeps

class Command(BaseCommand):
    help = 'Runs a livereload server watching static files and templates.'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            'extra',
            nargs='*',
            action='store',
            help='Extra files or directories to watch',
        )
        parser.add_argument(
            '--host',
            dest='host',
            default=livereload_host(),
            help='Host address for livereload sever.'
        )
        parser.add_argument(
            '--port',
            dest='port',
            default=livereload_port(),
            help='Listening port for livereload sever.'
        )

    def handle(self, *args, **options):
        server = S.Server()

        #  The reason not to ask the staticfile finders to list the files is
        # to get a watch when new files are added as well
        for dir in itertools.chain(
                settings.STATICFILES_DIRS,
                getattr(settings, 'TEMPLATE_DIRS', []),
                options.get('extra', []),
                args):
            server.watch(dir)
        for template in getattr(settings, 'TEMPLATES', []):
            for dir in template['DIRS']:
                server.watch(dir)
        for app_config in apps.get_app_configs():
            server.watch(os.path.join(app_config.path, 'static'))
            server.watch(os.path.join(app_config.path, 'templates'))

        if hasattr(settings, "TRANSCRYPT_MAINS"):
            def transpile_js(path, file):
                os.chdir(path)

                def inner_transpile():
                    os.system("transcrypt " + file)

                return inner_transpile

            for paths in settings.TRANSCRYPT_MAINS:
                path = os.path.abspath(
                    os.path.join(paths, "../"))
                main_file = os.path.basename(paths)

                transpile_js(path, main_file)()
                server.watch(
                    paths,
                    transpile_js(path, main_file))

                for dep in getdeps(paths):
                    server.watch(
                        dep,
                        transpile_js(path, main_file))

        server.serve(
            host=options['host'],
            liveport=options['port'],
        )
