#!/usr/bin/python
# encoding: UTF-8

import sys
import re
from subprocess import check_output  # call
import argparse


DEV = "/dev/i2c-8"

BASE_COMMAND = ["sudo", "ddcci-tool"]


def getBaseCommand(dev=DEV): return BASE_COMMAND+[DEV]


controls_range = {
    'brightness': (0x10, 100, 'Brightness'),
    'contrast':   (0x12, 100, 'Contrast'),
}

controls_disc = {
    # "SAM: DPMS control (1 - on/4 - stby)"
    'dpms': (0xd6, {1: 'on', 4: 'stby'}, "DPMS control"),
    # "[SAM: Power control (0 - off/1 - on)]"
    'power': (0xe1, {0: 'off', 1: 'on'}, "Power control"),
}


control_line_patt = re.compile(
    r'^Control\s+(0[xX][\dA-f]+)\:\s+\+\/(\d+)\/(\d+)\s+\[(.+)\]\s*$', re.M)


def parseInt(s, val=None, base=10):
    try:
        return int(s, base)
    except ValueError:
        return val


def runCmd(cmd): return check_output(cmd)


def readControlCmd(n):
    # '(:#x)' prints as hexadecimal (0x00)
    # cmd = getBaseCommand()+['-r', '(:#x)'.format(n)]
    cmd = getBaseCommand()+['-r', '{}'.format(n)]
    return runCmd(cmd)


def writeControlCmd(n, v):
    # '(:#x)' prints as hexadecimal (0x00)
    # cmd = getBaseCommand()+['-r', '(:#x)'.format(n)]
    cmd = getBaseCommand()+['-r', '{}'.format(n), '-w', '{}'.format(v)]
    return runCmd(cmd)


def parseResult(result):
    matches = control_line_patt.findall(result)
    lines = (
        {k: match[i] for (i, k) in enumerate(['n', 'value', 'mx', 'desc'])}
        for match in matches)
    return lines


def print_range(line):
    print u"{n} (0–{mx}): {value:>4}  ({desc})".format(**line)


def parseAndPrintRange(result):
    for line in parseResult(result):
        print_range(line)


def print_disc(name, value, line):
    control = controls_disc[name]
    fmt_opts = "/".join("{}-{}".format(*i) for i in control[1].items())
    if fmt_opts:
        line['opts'] = " ({})".format(fmt_opts)

    vdesc = control[1].get(value, None)
    if vdesc is not None:
        line['vdesc'] = " ({})".format(vdesc)

    print u"{n}{opts}: {value:>4}{vdesc}  ({desc})".format(**line)


if __name__ == '__main__':

    # TODO devices
    # print args.device

    parser = argparse.ArgumentParser(description="Control monitor configuration using ddcci-tool")
    add_arg = parser.add_argument

    add_arg('-b', '--brightness', metavar='x', type=int, nargs='?', const=True,
            help='Get or set brightness')
    add_arg('-c', '--contrast', metavar='x', type=int, nargs='?', const=True,
            help='Get or set contrast')

    add_arg('-d', '--dpms', dest='dpms', action='store_const', const=True,
            default=None, help='Set the monitor to sleep')
    add_arg('-do', '--dpms-on', dest='dpms', action='store_const', const=1,
            default=None, help='Set the monitor to sleep')
    add_arg('-ds', '--dpms-stby', dest='dpms', action='store_const', const=4,
            default=None, help='Set the monitor to sleep')

    #add_arg('-i', '--device',  # default=None,
            #help='Device')

    # add_arg('-po', '--power-off', action='store_true',
    #         help='Power off')

    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(1)

    args = parser.parse_args()

    # brightness should come first, for some reason
    for name in ['brightness', 'contrast']:
        v = getattr(args, name)

        if v is True:
            result = readControlCmd(controls_range[name][0])
            # lines = parseResult(result)
            # for line in lines: print_range(line)
            parseAndPrintRange(result)

        elif type(v) == int:
            result = writeControlCmd(controls_range[name][0], v)
            # lines = parseResult(result)
            # for line in lines: print_range(line)
            parseAndPrintRange(result)

    name = 'dpms'
    v = args.dpms
    if v is True:
        # lines = parseResult(readControlCmd(controls_disc[name][0]))
        for line in lines:
            value = parseInt(line.get('value', None), None)
            print_disc(name, value, line)

    elif type(v) == int:
        lines = parseResult(writeControlCmd(controls_disc[name][0], v))
        for line in lines:
            value = parseInt(line.get('value', None), None)
            print_disc(name, value, line)

    # name = 'power'
    # v = args.power_off
    # if v == True:
    #     lines = parseResult(writeControlCmd(controls_disc[name][0], 1))  # 0 -> off
    #     for line in lines:
    #         value = parseInt(line.get('value', None), None)
    #         print_disc(name, value, line)

