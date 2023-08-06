# -*- coding: utf-8 -*-
import json
from watson.di import ContainerAware
from watson.assets.webpack import exceptions


class Webpack(ContainerAware):

    __ioc_definition__ = {
        'init': {
            'config': lambda container: container.get('application.config')['assets']['webpack']
        }
    }

    cached_stats = None

    def __init__(self, config):
        self.config = config

    def _render(self, asset, type=None):
        extension = asset.split('.')[-1]
        if extension == type or not type:
            asset_path = '{}/{}'.format(self.config['bundle_dir'], asset)
            return self._render_tag(asset_path)

    def _render_tag(self, asset):
        if asset.endswith('.js'):
            return '<script type="text/javascript" src="{}"></script>'.format(
                asset)
        else:
            return '<link type="text/css" href="{}" rel="stylesheet">'.format(
                asset)

    def load_stats(self):
        if self.cached_stats:
            return
        data = {
            'chunks': {
                'main': []
            }
        }
        try:
            with open(self.config['stats_file']) as f:
                data = json.load(f)
        except:
            raise exceptions.NotReadyError('Stats file not found, run Webpack.')
        self.cached_stats = data

    def __call__(self, bundle='main', type=None):
        self.load_stats()
        if self.cached_stats['status'] != 'done':
            raise exceptions.NotReadyError(
                'Invalid stats file, please run Webpack again.')
        assets = []
        for _bundle in self.cached_stats['chunks'].get(bundle, []):
            asset = self._render(_bundle['name'], type)
            if asset:
                assets.append(asset)
        return ''.join(assets)


webpack = Webpack
