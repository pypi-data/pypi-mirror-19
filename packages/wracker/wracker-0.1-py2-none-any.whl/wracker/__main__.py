from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import sys

import wracker


def main():
    parsed_args = wracker.parse_args()
    cmd = parsed_args.command
    if cmd == 'install':
        project_dir = wracker.look_up_for_file_or_die(wracker.INPUT_FILE)
        reqs, locks = wracker.get_requirements(project_dir)
        dists = wracker.ensure_packages(
            reqs, locks, wracker.get_platform_info())
        wracker.write_frozen(project_dir, [d.as_requirement() for d in dists])
    elif cmd == 'exec':
        wracker.handle_exec(parsed_args.exec_args)
    else:
        wracker.die("Unknown command:", sys.argv[1])


if __name__ == '__main__':
    main()
