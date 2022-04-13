area_dict = {
    'header_area':
        {'start_address': '0x00 0x00',
         'length': 8,
         'checksum_address': '0x07 0x00'
         },
    'internal_use_area':
        {'start_address': '0x00 0x08',
         'length': 80,
         'checksum_address': '0x57 0x00'
         },
    'chassis_area':
        {'start_address': '0x00 0x58',
         'length': 72,
         'checksum_address': '0x9F 0x00'
         },
    'board_area':
        {'start_address': '0x00 0xA0',
         'length': 64,
         'checksum_address': '0xDF 0x00'
         },
    'product_area':
        {'start_address': '0x00 0xE0',
         'start_address_255': '0x01 0xDF',
         'length': 288,
         'checksum_address': '0xFF 0x01'
         }

}
item_dict = {
    'chassis_type':
        {'start_address': '0x5a 0x00',
         'length': 1,
         'flag': 0,
         'field_area': 'chassis_area',
         'param': '-ct',
         'param_num': '*',
         'param_help': 'set chassis type'
         },
    'chassis_part_number':
        {'start_address': '0x5c 0x00',
         'length': 12,
         'flag': 1,
         'field_area': 'chassis_area',
         'param': '-cpn',
         'param_num': 1,
         'param_help': 'set chassis part number'
         },
    'chassis_serial':
        {'start_address': '0x69 0x00',
         'length': 11,
         'flag': 1,
         'field_area': 'chassis_area',
         'param': '-cs',
         'param_num': 1,
         'param_help': 'set chassis serial'
         },
    'chassis_extra':
        {'start_address': '0x75 0x00',
         'length': 32,
         'flag': 1,
         'field_area': 'chassis_area',
         'param': '-ce',
         'param_num': 1,
         'param_help': 'set chassis extra'
         },
    'board_mfg_date':
        {'start_address': '0xA3 0x00',
         'length': 3,
         'flag': 0,
         'field_area': 'board_area',
         'param': '-bmd',
         'param_num': '*',
         'param_help': 'set board mfg date'
         },
    'board_mfg':
        {'start_address': '0xA7 0x00',
         'length': 12,
         'flag': 1,
         'field_area': 'board_area',
         'param': '-bm',
         'param_num': 1,
         'param_help': 'set board mfg'
         },
    'board_product':
        {'start_address': '0xB4 0x00',
         'length': 16,
         'flag': 1,
         'field_area': 'board_area',
         'param': '-bp',
         'param_num': 1,
         'param_help': 'set board product'
         },
    'board_serial':
        {'start_address': '0xC5 0x00',
         'length': 10,
         'flag': 1,
         'field_area': 'board_area',
         'param': '-bs',
         'param_num': 1,
         'param_help': 'set board serial'
         },
    'board_part_number':
        {'start_address': '0xD0 0x00',
         'length': 12,
         'flag': 1,
         'field_area': 'board_area',
         'param': '-bpn',
         'param_num': 1,
         'param_help': 'set board part number'
         },
    'product_manufacturer':
        {'start_address': '0xE4 0x00',
         'length': 12,
         'flag': 1,
         'field_area': 'product_area',
         'param': '-pm',
         'param_num': 1,
         'param_help': 'set product manufacturer'
         },
    'product_name':
        {'start_address': '0xF1 0x00',
         'length': 32,
         'flag': 1,
         'field_area': 'product_area',
         'param': '-pn',
         'param_num': 1,
         'param_help': 'set product name'
         },
    'product_part_number':
        {'start_address': '0x12 0x01',
         'length': 24,
         'flag': 1,
         'field_area': 'product_area',
         'param': '-ppn',
         'param_num': 1,
         'param_help': 'set product part number'
         },
    'product_version':
        {'start_address': '0x2B 0x01',
         'length': 6,
         'flag': 1,
         'field_area': 'product_area',
         'param': '-pv',
         'param_num': 1,
         'param_help': 'set product version'
         },
    'product_serial':
        {'start_address': '0x32 0x01',
         'length': 24,
         'flag': 1,
         'field_area': 'product_area',
         'param': '-ps',
         'param_num': 1,
         'param_help': 'set product serial'
         },
    'product_asset_tag':
        {'start_address': '0x4B 0x01',
         'length': 32,
         'flag': 1,
         'field_area': 'product_area',
         'param': '-pat',
         'param_num': 1,
         'param_help': 'set product asset tag'
         },
    'product_extra':
        {'start_address': '0x6D 0x01',
         'length': 24,
         'flag': 1,
         'field_area': 'product_area',
         'param': '-pe',
         'param_num': 1,
         'param_help': 'set product extra '
         },
}

# {start_address:value}
recovery = {
    '0x00 0x00': '0x01 0x01 0x0B 0x14 0x1C 0x00 0x00 0xC3',
    '0x08 0x00': '0x01 0x0A',
    '0x57 0x00': '0xF5',
    '0x58 0x00': '0x01 0x09 0x17 0xCC',
    '0x68 0x00': '0xCB',
    '0x74 0x00': '0xE0',
    '0x95 0x00': '0xC8',
    '0x9E 0x00': '0xC1',
    '0xA0 0x00': '0x01 0x08 0x00',
    '0xA6 0x00': '0xCC',
    '0xB3 0x00': '0xD0',
    '0xC4 0x00': '0xCA',
    '0xCF 0x00': '0xCC',
    '0xDC 0x00': '0xC0 0xC1 0x00',
    '0xE0 0x00': '0x01 0x24 0x00 0xCC',
    '0xF0 0x00': '0xE0',
    '0x11 0x01': '0xD8',
    '0x2A 0x01': '0xC6',
    '0x31 0x01': '0xD8',
    '0x4A 0x01': '0xE0',
    '0x6B 0x01': '0xC0 0xC1',
	#product extra 
    '0x6B 0x01': '0xC0 0xD8',
    '0x85 0x01': '0xC1',
}

# fru write/read command for arbok
fru_write_command = 'raw 0x0a 0x12 0x00 '
fru_read_command = 'raw 0x06 0x52 0x07 0xa6 '
