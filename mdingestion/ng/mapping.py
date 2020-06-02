import os
import json
import pathlib

from .command import Command
from .util import parse_source_list
from .walker import Walker
from .community import (
    EnvidatDatacite,
    EnvidatISO19139,
    SLKSDublinCore,
    Herbadrop,
)

import logging


MAPPER = {
    'envidat-datacite': EnvidatDatacite,
    'envidat-iso19139': EnvidatISO19139,
    'slks-dc': SLKSDublinCore,
    'herbadrop-hjson': Herbadrop,
}


def mapper_factory(community, mdprefix):
    logging.debug(f'community={community}, mdprefix={mdprefix}')
    return MAPPER.get(f'{community}-{mdprefix}')


class Mapper(Command):
    def __init__(self, community, mdprefix=None, outdir=None, source_list=None):
        self.sources = parse_source_list(source_list)
        source = self.sources.get(community, dict())
        self.community = community
        self.mdprefix = mdprefix or source.get('mdprefix')
        self.outdir = outdir
        self.walker = Walker(outdir)
        self.map_tool = mapper_factory(self.community, self.mdprefix)

    def walk(self):
        mdprefix = self.mdprefix
        if mdprefix == 'hjson':
            mdprefix = 'json'
        for filename in self.walker.walk_community(
                community=self.community,
                mdprefix=mdprefix,
                ext=self.map_tool.extension()):
            yield filename

    def map(self, filename):
        mapped = self.map_tool(filename)
        logging.info(f'map: community={self.community}, mdprefix={self.mdprefix}, file={filename}')
        self.write_output(mapped.json(), filename)

    def write_output(self, data, filename):
        source_path = pathlib.Path(filename)
        path_parts = list(source_path.parts)
        path_parts[-2] = 'json'
        path_parts[-1] = source_path.name.replace(source_path.suffix, '.json')
        out = pathlib.Path(*path_parts)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open(mode='w') as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True, ensure_ascii=False)
            logging.info(f'map output written to {out}')
