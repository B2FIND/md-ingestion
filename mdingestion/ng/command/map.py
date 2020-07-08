from tqdm import tqdm
import colander

from .base import Command
from ..walker import Walker
from ..community import reader
from ..writer import CKANWriter, B2FWriter
from ..core import B2FSchema

import logging


class Map(Command):
    def __init__(self, **args):
        super().__init__(**args)
        self.walker = Walker(self.outdir)
        self.reader = reader(self.community, self.mdprefix)
        self.writer = CKANWriter()
        self.summary = {
            'total': 0,
            'valid': 0,
            'written': 0,
            'required': {
                'title': 0,
                'identifier': 0,
            },
            'optional': {},
            'invalid': {},
        }

    def run(self, force=False):
        for filename in tqdm(self.walk(), ascii=True, desc="Mapping", unit=' records'):
            doc = self.map(filename)
            is_valid = self.validate(doc)
            if force or is_valid:
                self.writer.write(doc, filename)
                self.summary['written'] += 1
        self.print_summary()

    def walk(self):
        for filename in self.walker.walk_community(
                community=self.community,
                mdprefix=self.mdprefix,
                mdsubset=self.mdsubset,
                ext=self.reader.extension()):
            yield filename

    def map(self, filename):
        reader = self.reader()
        doc = reader.read(filename, self.url, self.community, self.mdprefix)
        logging.info(f'map: community={self.community}, mdprefix={self.mdprefix}, file={filename}')
        # self.writer.write(doc, filename)
        return doc

    def validate(self, doc):
        # TODO: use counter? https://pymotw.com/2/collections/counter.html
        jsondoc = B2FWriter().json(doc)
        self.summary['total'] += 1
        try:
            B2FSchema().deserialize(jsondoc)
            self.summary['valid'] += 1
            valid = True
        except colander.Invalid as e:
            logging.warning(f"{e}")
            valid = False
            self._update_summary(e.asdict(), valid=False)
        except Exception as e:
            logging.warning(f"{e}")
            valid = False
        self._update_summary(jsondoc)
        return valid

    def _update_summary(self, fields, valid=True):
        if valid:
            for key, value in fields.items():
                if not value:
                    continue
                if key in self.summary['required']:
                    self.summary['required'][key] += 1
                elif key not in self.summary['optional']:
                    self.summary['optional'][key] = 1
                else:
                    self.summary['optional'][key] += 1
        else:
            for key, value in fields.items():
                if key not in self.summary['invalid']:
                    self.summary['invalid'][key] = 1
                else:
                    self.summary['invalid'][key] += 1

    def print_summary(self):
        print("\nSummary:")
        print(f"\tvalid={self.summary['valid']}/{self.summary['total']}, written={self.summary['written']}")
        print("\nRequired Fields:")
        print(f"\ttitle={self.summary['required']['title']}, identifier={self.summary['required']['identifier']}")
        print("\nOptional Fields (complete):")
        for key, value in self.summary['optional'].items():
            if value == self.summary['total']:
                print(f"\t{key}")
        print("\nOptional Fields (incomplete):")
        for key, value in self.summary['optional'].items():
            if value < self.summary['total']:
                print(f"\t{key}={value}")
        print("\nInvalid Fields:")
        for key, value in self.summary['invalid'].items():
            print(f"\t{key}={value}")
