import os, shlex
import subprocess as subp
from datetime import datetime

def performBackup(config = None, args = None):
    ''' Performs a MySQL backup using mysqldump tool 
        and a specific config file 
    ''' 

    print('o Performing MySQL Backup...')
    print('\t=> Checking for the mysqldump tool...')

    try:
        with open(os.devnull, 'w') as devnull:
            if subp.call(['which', 'mysqldump'], stdout = devnull, stderr = devnull) == 1:
                print('\t=> mysqldump NOT found. Aborting.')
                return
    except Exception as ex:
        print('\t=> An exception occured. Unable to use "which"')
        print(ex)
        return

    print('\t=> mysqldump found. Proceeding with backup...')
    print('\t\t[Backup Path is \'{}\']'.format(config['path']))

    for i, database in enumerate(config['databases'].split(), start = 1):
        print('\t\t* Backing up database {db} ({i}/{total})'.format(db = database, i = i, 
                                                                    total = len(config['databases'].split())), end = ' ')

        filename = '{}_{}.sql'.format(database, datetime.now().strftime('%d-%m-%Y_%H:%M:%S:%f'))

        if not args.dryRun:
            with open(os.path.join(config['path'], filename), 'w') as backupFile:
                command = 'mysqldump -h {host} -u {user} -p{password} --databases {database}'.format(
                    host = config['host'], user = config['usernames'].split()[i - 1],
                    password = config['passwords'].split()[i - 1], database = database)

                subp.call(shlex.split(command), stdout = backupFile)

        if os.path.isfile(os.path.join(config['path'], filename)):
            print(' -> file \'{}\' created'.format(filename))
        else:
            print('[{}] File not created!'.format('DRYRUN' if args.dryRun else 'ERROR'))
    print('\t=> MySQL Backup Finished.')
