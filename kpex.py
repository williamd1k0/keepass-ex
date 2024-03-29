import sys
from argparse import ArgumentParser

from bullet import utils, SlidePrompt, Bullet, Password
from pykeepass import PyKeePass
from pykeepass.entry import Entry
from pykeepass.group import Group
from pyspin.spin import make_spin

from server import expose_entry
import theme


KP: PyKeePass = None

@make_spin(theme.SPIN, "Decrypting...")
def load_database(db, password=None, keyfile=None):
    return PyKeePass(db, password=password, keyfile=keyfile)

def groups2str(groups):
    return [g.name for g in groups]

def entries2str(entries):
    return [e.title for e in entries]

def get_group_by_name(name, groups):
    for g in groups:
        if g.name == name:
            return g

def get_entry_by_title(title, entries):
    for e in entries:
        if e.title == title:
            return e

def main(args):
    cli = None
    if args.entry_only:
        cli = SlidePrompt([
            Password('Type the %s password: ' % args.db, **theme.PASSWORD)
        ])
    else:
        cli = SlidePrompt([
            Password('Type the database password: ', **theme.PASSWORD)
        ])
    password = cli.launch()[0][1]

    if args.entry_only:
        entry_title = args.db
        entry_password = password
        expose_entry(entry_title, entry_password, args.port)
        sys.exit(0)

    try:
        KP = load_database(args.db, password, args.keyfile)
        del password
    except Exception as err:
        utils.clearConsoleUp(1)
        if not isinstance(err, KeyboardInterrupt):
            print('Something went wrong. Please check your password/keyfile and try again.')
            sys.exit(1)
        sys.exit()
    utils.clearConsoleUp(1)
    utils.clearConsoleDown(1)
    utils.moveCursorHead()

    group: Group = KP.root_group
    entry: Entry = None
    nav = True
    while nav:
        subgroups = group.subgroups
        if entry:
            cli = SlidePrompt([
                Bullet(prompt='Expose %s to localhost?' % entry.title, choices=['Yes', 'No'], margin=1, pad_right=1, **theme.BULLET)
            ])
            result = cli.launch()[0][1]
            if result == 'Yes':
                entry_title = entry.title
                entry_password = entry.password
                del entry, group, subgroups, KP
                expose_entry(entry_title, entry_password, args.port)
                nav = False
            else:
                entry = None
        elif len(subgroups) > 0:
            group_list = groups2str(subgroups)
            if group != KP.root_group:
                group_list = ['..'] + group_list
            if len(group.entries) > 0:
                group_list = ['.'] + group_list
            cli = SlidePrompt([
                Bullet(prompt=group.name, choices=group_list, margin=1, pad_right=1, **theme.BULLET)
            ])
            result = cli.launch()[0][1]
            if result == '..':
                group = group.parentgroup
            elif result == '.':
                pass
            else:
                group = get_group_by_name(result, subgroups)
        else:
            entries = group.entries
            group_list = entries2str(entries)
            if group != KP.root_group:
                group_list = ['..'] + group_list
            cli = SlidePrompt([
                Bullet(prompt=group.name, choices=group_list, margin=1, pad_right=1, **theme.BULLET)
            ])
            result = cli.launch()[0][1]
            if result == '..':
                group = group.parentgroup
            else:
                entry = get_entry_by_title(result, entries)

if __name__ == "__main__":
    arg_parser = ArgumentParser('KeePassEX', description="WARNING: Do not use your KeePass password for basic auth (-a/--auth) if SSL is disabled.")
    arg_parser.add_argument('db', metavar='<database.kdbx | entry-title>', help='KeePass database file OR the entry title if -e/--entry-only')
    arg_parser.add_argument('-k', '--keyfile', metavar='<master.key>', help='Database keyfile (Optional)')
    arg_parser.add_argument('-p', '--port', type=int, default=8000, metavar='<8000>', help='Port to serve [Default=8000]')
    arg_parser.add_argument('-e', '--entry-only', action="store_true", help='Expose a password directly instead of opening a database')
    args = arg_parser.parse_args()
    main(args)
