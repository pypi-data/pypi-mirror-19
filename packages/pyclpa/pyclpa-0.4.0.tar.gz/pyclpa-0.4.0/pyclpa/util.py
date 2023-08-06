# coding: utf-8
from __future__ import unicode_literals, print_function, division
import unicodedata

from clldutils.path import Path
from clldutils import jsonlib


def local_path(*comps):
    """Helper function to create a local path to the current directory of CLPA"""
    return Path(__file__).parent.joinpath('data', *comps)


def load_CLPA():
    """
    Load the main data file.
    """
    return jsonlib.load(local_path('clpa.main.json'))


def write_CLPA(clpadata, path):
    """
    Basic function to write clpa-data.
    """
    if isinstance(path, Path):
        outdir, fname = path.parent, path.name
    else:
        outdir, fname = local_path(), path  # pragma: no cover
    old_clpa = load_CLPA()
    jsonlib.dump(old_clpa, outdir.joinpath(fname + '.bak'), indent=4)
    jsonlib.dump(clpadata, outdir.joinpath(fname), indent=4)


def load_whitelist():
    """
    Basic function to load the CLPA whitelist.
    """
    _clpadata = jsonlib.load(local_path('clpa.main.json'))
    whitelist = {}
    for group in ['consonants', 'vowels', 'markers', 'tones', 'diphtongs']:
        for val in _clpadata[group]:
            whitelist[_clpadata[val]['glyph']] = _clpadata[val]
            whitelist[_clpadata[val]['glyph']]["ID"] = val

    return whitelist


def load_alias(_path):
    """
    Alias are one-character sequences which we can convert on a step-by step
    basis by applying them successively to all subsegments of a segment.
    """
    path = Path(_path)
    if not path.is_file():
        path = local_path(_path)

    alias = {}
    with path.open(encoding='utf-8') as handle:
        for line in handle:
            if not line.startswith('#') and line.strip():
                source, target = line.strip().split('\t')
                alias[eval('"' + source + '"')] = eval('r"' + target + '"')
    return alias


def split(string):
    return string.split(' ')


def join(tokens):
    return ' '.join(tokens)


def check_string(seq, whitelist):
    return [
        '*' if t in whitelist else '?' for t in split(unicodedata.normalize('NFC', seq))]
