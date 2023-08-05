import os
import collections
import email
import pathlib
import horetu
import horetu.types as t
from email.policy import SMTPUTF8

FORMATS = {
    'mh': [
        '%(identifier)s: %(name)s <%(email)s>',
        '%(identifier)s: %(email)s',
    ],
    'mutt': [
        'alias %(identifier)s %(name)s <%(email)s>',
        'alias %(identifier)s %(email)s',
    ],
    'newsbeuter': [
        '%(feed)s "~%(name)s"',
        '%(feed)s',
    ],
    'post': [
        '%(name)s / %(post)s',
        '%(identifier)s / %(post)s',
    ],
}
HEADERS = {'name', 'phone', 'email', 'feed', 'web', 'post'}

def FileOrDir(x):
    if os.path.isfile(x):
        return x
    else:
        return t.InputDirectory(x)

def dump(contact: FileOrDir, output_format: FORMATS):
    '''
    Convert from a contact file to a different format.

    :param contact: A contact file or a directory of contact files
    :param output_format: "mh" for nmh ~/.aliases file,
        "mutt" for mutt alias_file, "newsbeuter" for ~/.newsbeuter/urls,
        "post" for postal addresses
    :rtype: iter
    :returns: Iterable of str output chunked by line
    '''
    root = pathlib.Path(contact)
    if root.is_file():
        paths = [root]
    else:
        paths = root.iterdir()
    for path in paths:
        if not path.name.startswith('.') and path.is_file():
            person = parse(path)
            if root.is_file():
                person['identifier'] = root.name
            else:
                person['identifier'] = path.relative_to(root)
            for sub_format in output_format:
                try:
                    line = sub_format % person
                except KeyError:
                    pass
                else:
                    yield line
                    break

def parse(path):
    person = email.message_from_string(path.read_text(), policy=SMTPUTF8)
    headers = collections.Counter(header.lower() for header in person \
                                  if not header.lower().startswith('x-'))
    if set(headers).issubset(HEADERS):
        if max(headers.values()) <= 1:
            return {k:person[k] for k in headers}
        else:
            raise horetu.Error('%s: Only one of each key is allowed' % path)
    else:
        raise horetu.Error('%s: Only these keys are allowed: %s' % \
                           (path, str(HEADERS)))
