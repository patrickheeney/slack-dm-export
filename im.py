
from datetime import timedelta, datetime
from time import mktime
import os, argparse
import json

try:
    from slacker import Slacker
except ImportError:
    raise ImportError('slacker required: pip install slacker')

parser = argparse.ArgumentParser(description='Slack direct messages, private groups and general channel export')
parser.add_argument('-t', '--token', action='store', default=False, help='Slack token',
                    dest='slack_token')
parser.add_argument('-d', '--direct', action='store_true', default=False, help='Export direct messages',
                    dest='dm_flag')
parser.add_argument('-g', '--groups', action='store_true', default=False, help='Export private groups',
                    dest='groups_flag')
parser.add_argument('-c', '--channels', action='store_true', default=False, help='Export channels',
                    dest='channels_flag')
parser.add_argument('-s', '--start', action='store',
                    default='2015.07.01', help="Start date", dest='start_date')
parser.add_argument('-e', '--end', action='store',
                    default='2015.08.01', help='End date', dest='end_date')
parser.add_argument('-o', '--output', action='store',
                    default=False, help='Output folder', dest='output')
results = parser.parse_args()

token = results.slack_token
dm_flag = results.dm_flag
groups_flag = results.groups_flag
channels_flag = results.channels_flag
start = results.start_date
end = results.end_date
output = results.output

if not token:
    parser.error( 'Token is required (-t)' )

if not dm_flag and not groups_flag and not channels_flag:
    parser.error( 'Export type is required (-d, -g, or -c)' )

slack = Slacker(token)


def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)


def get_path(source):
    dest = output
    if not dest:
        dest = './export/'
    ensure_dir(dest)
    return dest + source


def daterangetimestamp(start_range_date, end_range_date):
    for n in range(int((end_range_date - start_range_date).days)):
        current_date = start_range_date + timedelta(n)
        current_date_time = datetime.combine(current_date, datetime.min.time())
        yield mktime(current_date_time.timetuple())+1e-6*current_date_time.microsecond


def dm_export():
    im_list = slack.im.list().body['ims']
    for i in range(0, len(im_list)):
        current_user = im_list[i]['user']
        current_username = slack.users.info(current_user).body['user']['name']
        path_file = get_path(current_username+'.json')
        log_file = open(path_file, 'a')
        print('[+] ' + current_username)
        for single_date_timestamp in daterangetimestamp(start_date, end_date):
            history = slack.im.history(im_list[i]['id'], count=1000, oldest=single_date_timestamp,
                                       latest=single_date_timestamp+86400.0).body['messages']
            if not history:
                continue
            json.dump(history, log_file)
        log_file.close()
        if os.stat(path_file).st_size == 0:
            os.remove(path_file)


def channels_export():
    group_id = False
    groups_list = slack.channels.list().body['channels']
    for i in range(0, len(groups_list)):
        if groups_list[i]['is_general']:
            group_id = i
            break
    if group_id:
        path_file = get_path(groups_list[group_id]['name']+'.json')
        file = open(path_file, 'a')
        for single_date_timestamp in daterangetimestamp(start_date, end_date):
            response = slack.channels.history(groups_list[group_id]['id'], count=1000, oldest=single_date_timestamp,
                                              latest=single_date_timestamp+86400.0)
            if not response.body['messages']:
                continue
            json.dump(response.body['messages'], file)
        file.close()


def private_groups_export():
    groups_list = slack.groups.list().body['groups']
    for i in range(0, len(groups_list)):
        current_group_id = groups_list[i]['id']
        current_group_name = slack.groups.info(current_group_id).body['group']['name']
        path_file = get_path(current_group_name+'.json')
        log_file = open(path_file, 'a')
        print('[+] ' + current_group_name)
        for single_date_timestamp in daterangetimestamp(start_date, end_date):
            response = slack.groups.history(current_group_id, count=1000, oldest=single_date_timestamp,
                                            latest=single_date_timestamp+86400.0)
            if not response.body['messages']:
                continue
            json.dump(response.body['messages'], log_file)
        log_file.close()
        if os.stat(path_file).st_size == 0:
            os.remove(path_file)


start_date = datetime.strptime(start, "%Y.%m.%d")
end_date = datetime.strptime(end, "%Y.%m.%d")

print('========================================================================')
print('[+] Start date: ' + str(start_date))
print('[+] End date: ' + str(end_date))
print('[+] Destination: ' + str(get_path('')))
if dm_flag:
    print('========================================================================')
    print('[+] Starting direct messages export')
    dm_export()
    print('[+] Direct messages export finished')
if channels_flag:
    print('========================================================================')
    print('[+] Starting channel export')
    channels_export()
    print('[+] Channel export finished')
if groups_flag:
    print('========================================================================')
    print('[+] Starting private groups export')
    private_groups_export()
    print('[+] Private groups export finished')
print('========================================================================')
print('[+] All tasks finished')
print('========================================================================')
