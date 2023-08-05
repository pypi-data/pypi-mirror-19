from pkg_resources import parse_requirements
from subprocess import Popen, PIPE
from .errors import ImproperlyConfigured
import json
import click


def parse_python(fh):
    reqs = []

    for line in fh.readlines():
        if not line.startswith("-"):
            reqs.append(line)

    for req in parse_requirements("\n".join(reqs)):
        if len(req.specs) == 1 and req.specs[0][0] == "==":
            yield {"vendor": "pypi", "name": req.key, "v": req.specs[0][1]}
        else:
            click.secho(
                "Warning: unpinned requirement '{req}' found, unable to check.".format(
                    req=req.key), fg="yellow"
            )


def _call_bundler():
    try:
        process = Popen(['bundler', 'show'], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        if stdout.startswith("Gems included"):
            return stdout
    except OSError as e:
        raise ImproperlyConfigured("Gemfile detected, but bundler is not installed. "
                                   "Please install bundler.")


def parse_ruby(fh):
    for line in _call_bundler().splitlines():
        line = line.strip()
        if line.startswith("*"):
            line = line.replace("* ", "").replace("(", "").replace(")", "")
            name, version = line.split(" ")
            yield {"vendor": "gem", "name": name, "v": version}


def parse_node(fh):
    data = json.loads(fh.read())
    for name, spec in data["dependencies"].items():
        version = spec.replace("~", "").replace("^", "")
        yield {"vendor": "npm", "name": name, "v": version}


def parse(fh):
    """
    Reads requirements from a file like object and (optionally) from referenced files.
    :param resolve: boolean. resolves referenced files.
    :return: generator
    """  # filter out all "non-requirement" lines and resolve all referenced files.
    # "non-requirement" lines typically begin with a dash, e.g:
    # -e git://some-repo, or --index-server=https://foo.bar
    # lines referenced files start with a '-r'
    if fh.name.endswith("package.json"):
        return parse_node(fh=fh)
    elif fh.name.endswith("Gemfile") or fh.name.endswith("Gemfile.lock"):
        return parse_ruby(fh)
    return parse_python(fh)
