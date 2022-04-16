import time
import os
import sys
import subprocess
import argparse
try:
    import ipaddress
except ImportError as e:
    pass
from config import *


def recovery_action():
    for i in recovery.keys():
        command = tool + fru_write_command + i + ' ' + recovery[i]
        exec_command('', command)
    # recovery area checksum
    for i in area_dict.keys():
        update_area_checksum(i)


def str2_hex_ascii(value):
    tmp = ''
    for char in value:
        tmp = tmp + hex(ord(char)) + ' '
    return tmp


def gen_command(item, start_address, length, value):
    if item_dict[item]['flag']:
        if len(value) > length:
            print(item.replace('_', ' ') + ' only support ' + str(length) + ' chars')
            exit(0)
        value_hex = str2_hex_ascii(value)
        tmp = fru_write_command + ' ' + start_address + ' ' + value_hex
        command = tmp + (length - len(value)) * '0x20 '
    else:
        tmp = fru_write_command + ' ' + start_address + ' ' + value
        command = tmp
    return command


def cal_board_mfg_date(new_time=time.gmtime(), old_time='1996-1-1 00:00:00'):
    if isinstance(new_time, list):
        new_time = new_time[0]
    # Number of minutes from 0:00 hrs 1/1/96. LSbyte first (little endian)
    old_time_seconds = time.mktime(time.strptime(old_time, "%Y-%m-%d %H:%M:%S"))
    # time.gmtime transform the time to UTC time(zero time zone)
    if isinstance(new_time, str):
        new_time_seconds = time.mktime(time.gmtime(time.mktime(time.strptime(new_time, "%Y-%m-%d %H:%M:%S"))))
    elif isinstance(new_time, time.struct_time):
        new_time_seconds = time.mktime(new_time)
    else:
        print('your time format is wrong,EX: 1996-1-1 00:00:00')
        exit()
    # minutes from 1996-1-1 00:00:0
    minutes = int((new_time_seconds - old_time_seconds) / 60)
    lsb_mfg_date = hex(minutes & 0xff)
    msb_mfg_date = hex((minutes & 0xff00) >> 8)
    hsb_mfg_date = hex((minutes & 0xff0000) >> 16)
    return lsb_mfg_date + ' ' + msb_mfg_date + ' ' + hsb_mfg_date


def format_chassis_type(item_value='0x17'):
    if item_value in ('0x17', '0x10', '0x19'):
        value = item_value
        return value
    else:
        print(
            '"Chassis Type Define","Please enter the chassis type code as bellow:\
            \nRack Mount Chassis : 0x17\
            \nMulti-system Chassis :0x19\
            \nOther :0x01"')
        exit()


# fru read command for arbok
# raw 0x06 0x52 0x07 0xa6 <read count>  <start addr MLB> <start addr LSB>
# fru read command for kingler
# raw 0x06 0x52 0x07 0xac <read count>  <start addr MLB> <start addr LSB>


def update_area_checksum(area):
    #   read fru area datas except checksum byte
    area_length = area_dict[area]['length']
    if area_length > 255:
        command = tool + fru_read_command + hex(255) + ' ' + area_dict[area]['start_address']
        area_value = exec_command("", command)
        command = tool + fru_read_command + hex(area_length - 255 - 1) + ' ' + area_dict[area]['start_address_255']
        area_value += exec_command("", command)
    else:
        command = tool + fru_read_command + hex(area_length - 1) + ' ' + area_dict[area]['start_address']
        area_value = exec_command("", command)
    #   calc the fru data's sum
    if area_value:
        data_sum = 0
        for data in area_value.split():
            data_sum += int(data, 16)
        #   calc fru area check sum
        check_sum_value = hex((0x100 - (data_sum & 0xff)) & 0xff)
        checksum_address = area_dict[area]['checksum_address']
        command = tool + fru_write_command + ' ' + checksum_address + ' ' + check_sum_value
        exec_command('checksum', command)
        return check_sum_value


def exec_command(description, command):
    print(command)
    status, output = subprocess.getstatusoutput(command)
    #status, output = commands.getstatusoutput(command)
    if status:
        print(description + ' modify failed')
        print(output)
    else:
        print(description + ' modify sucessfully')
        # print(output)
    return output


def set_item(item, value):
    if isinstance(value, list):
        real_value = value[0]
    else:
        real_value = value
    print(real_value)
    if real_value:
        start_address = item_dict[item]['start_address']
        length = item_dict[item]['length']
        command = gen_command(item, start_address, length, real_value)
        real_command = tool + command
        exec_command(item.replace('_', ' '), real_command)
        # update checksum
        item_area = item_dict[item]['field_area']
        update_area_checksum(item_area)


def getopt():
    args = argparse.ArgumentParser(usage="%(prog)s + [ Option ]", description="FRU Edit Tool")
    for item in item_dict.keys():
        if item_dict[item]['param']:
            args.add_argument(item_dict[item]['param'],
                              dest=item,
                              nargs=item_dict[item]['param_num'],
                              help=item_dict[item]['param_help']
                              )
    args.add_argument('-r', dest='repair', action='store_true', help='recovry the BMC FRU')
    try:
        args.add_argument('-H', dest='bmc_ip', type=ipaddress.ip_address,
                          help='set the bmc ip which one you will modify the fru')
    except Exception as e:
        pass
    args.add_argument('-U', dest='bmc_user', help='set the bmc user name')
    args.add_argument('-P', dest='bmc_passwd', help='set the password of the bmc user')
    args.add_argument('-V', action='version', version="%(prog)s-0.2", help="Show Version")
    args = args.parse_args()
    return args.__dict__


params = getopt()
print(params)

_HOME_PATH = os.path.dirname(__file__)
_TOOL_PATH = os.path.join(_HOME_PATH, 'tools')
_tool = os.path.join(_TOOL_PATH, sys.platform)
if params['bmc_ip'] and params['bmc_user'] and params['bmc_passwd']:
    tool = _tool + os.sep + 'ipmitool -I lanplus  -H %s -U %s -P %s ' % (params['bmc_ip'], params['bmc_user'], params['bmc_passwd'])
    print(tool)
elif params['bmc_ip'] or params['bmc_user'] or params['bmc_passwd']:
        print('bmc ip & username & password should be setted at the same time')
        exit()
else:
    tool = _tool + os.sep + 'ipmitool '
for i in params.keys():
    if i not in ('bmc_ip', 'bmc_user', 'bmc_passwd'):
        if i == 'repair' and params[i]:
            print('start to recovery the fru')
            recovery_action()
            exit()
        elif i == 'board_mfg_date':
            if params[i] != None:
                if params[i] == 0:
                    value = cal_board_mfg_date()
                    set_item(i, value)
                else:
                    value = cal_board_mfg_date(params[i])
                    set_item(i, value)
        elif i == 'chassis_type' and params[i]:
            value = format_chassis_type(params[i])
            set_item(i, value)
        elif params[i]:
            set_item(i, params[i])
