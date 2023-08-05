# -*- coding: utf-8 -*-
import sys
from optparse import OptionParser
from generator import AppGenerator, APP_TYPES


def main():
    usage = '''usage: %prog [options]
        ex) run.py -t 1 -n hello_python
        '''
    parser = OptionParser(usage=usage)
    parser.add_option('-t', '--type', dest='type',
                      help='[Required] Type: simple, large', type='string')
    parser.add_option('-n', '--name', dest='name', type='string',
                      help='[Required] Project name')
    (options, args) = parser.parse_args()

    app_type = options.type
    app_name = options.name

    if app_type is None and app_name is None:
        parser.print_help()
        sys.exit()

    assert app_type, parser.error('type is required')
    assert app_name, parser.error('name is required')

    app_type = app_type.upper()

    if app_type == 'SIMPLE':
        app_type = APP_TYPES.SIMPLE
    elif app_type == 'LARGE':
        app_type = APP_TYPES.LARGE
    else:
        parser.error('type is not support %s' % app_type)

    gen = AppGenerator(app_type, app_name)
    gen.init_app()
    gen.build_app()


if __name__ == '__main__':
    main()
