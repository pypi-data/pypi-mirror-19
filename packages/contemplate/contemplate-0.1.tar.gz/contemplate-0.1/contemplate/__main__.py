from __future__ import absolute_import, print_function
import pkg_resources as pkr
import argparse
import logging
import re
import json

def cmd_render(args):
    logger = logging.getLogger(__name__)
    # Engine
    engine = get_engine(args.engine)
    if engine is None:
        raise RuntimeError('unable to load "{0}" engine'.format(args.engine))
    logger.debug('engine={0}'.format(engine))

    # Payload
    payload = {}
    for data_source in args.data:
        key, value = get_data(data_source)
        if key:
            if key in payload:
                raise ValueError('data key "{0}" already in defined')
            payload.update({key: value})
        else:
            payload.update(value)
    logger.debug('payload={0}'.format(payload))

    # Render
    with open(args.input_file, 'r') as fd:
        content = engine().render(fd.read(), **payload)

    if args.output_file:
        with open(args.output_file, 'w') as output_fd:
            print(content, file=output_fd)
    else:
        print(content)

def cmd_engines(args):
    logger = logging.getLogger(__name__)
    print(json.dumps([entry.name for entry in pkr.iter_entry_points('contemplate_engine_v1')]))

def cmd_parsers(args):
    logger = logging.getLogger(__name__)
    print(json.dumps([entry.name for entry in pkr.iter_entry_points('contemplate_parser_v1')]))

def get_entry_point(group, name):
    for entry_point in pkr.iter_entry_points(group, name):
        return entry_point.load()
    return None

def get_engine(name):
    return get_entry_point('contemplate_engine_v1', name)

def get_data(datasource):
    """
    format is key=ds:source
    """
    res = re.match('^((\w+)=)?(\w+):(\S*)$', datasource)
    if not res:
        raise ValueError('not a valid datasource: {0}'.format(datasource))
    _, key, name, source = res.groups()
    parser = get_entry_point('contemplate_parser_v1', name)
    if parser is None:
        raise ImportError('unable to load "{0}" parser'.format(name))
    return (key, parser(source).data())

def main(arguments=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--loglevel', default='WARNING',
                        choices=('DEBUG', 'INFO', 'WARNING', 'ERROR'))

    subparsers = parser.add_subparsers()
    subparsers.required = True

    p_engines = subparsers.add_parser('engines')
    p_engines.set_defaults(func=cmd_engines)

    p_parsers = subparsers.add_parser('parsers')
    p_parsers.set_defaults(func=cmd_parsers)

    p_render = subparsers.add_parser('render')
    p_render.set_defaults(func=cmd_render)

    p_render.add_argument('input_file', help='input_file')
    p_render.add_argument('-o', '--output-file',
                          metavar='output_file', help='output file')
    p_render.add_argument('-e', '--engine', default='format',
                          help='the template engine to use')
    p_render.add_argument('-d', '--data', action='append',default=[],
                          help='data source (var=parser:file)')

    args = parser.parse_args(arguments)
    logging.basicConfig(level=getattr(logging, args.loglevel))
    return args.func(args)


if __name__ == '__main__':
    main()
