from hwdb import model as M


def get_units():
    return [
    M.Unit(name='Nanometer', format='%(unit)s nm'),
    M.Unit(name='Millimeter', format='%(unit)s mm'),
    M.Unit(name='Megahertz', format='%(unit)s MHz', note='We dont use the minimal unit Hertz because processors are in the MHz area'),
    M.Unit(name='Date'),
    M.Unit(name='Year'),
    M.Unit(name='Count'),
    M.Unit(name='Order', note='Information about the order/sequence of a Part'),
    M.Unit(name='Byte', format='%(unit)s Byte'),
    M.Unit(name='Megabyte', format='%(unit)s Megabyte'),
    M.Unit(name='Gigabyte', format='%(unit)s Gigabyte'),
    M.Unit(name='Megatransfer/Second', format='%(unit)s MT/s', note='used with Front side bus'),
    M.Unit(name='Factor', format='%(unit)sx', note='ie cpu clock multiplier'),
    M.Unit(name='Volt', format='%(unit)s V'),
    M.Unit(name='Watt', format='%(unit)s W'),
    M.Unit(name='Dollar', format='$%(unit)s'),
    M.Unit(name='Url', format='<a href="%(unit)s">%(unit)s</a>'),
    M.Unit(name='Text'),
    M.Unit(name='Boolean'),
    M.Unit(name='Hex'),
    ]


def get_connectors():
    objs = [
    M.Part(name='Socket', note='Generic parent for all kinds of sockets', children=[
        M.Part(name='CPU-Socket'),
        M.Part(name='RAM Socket'),
        M.Part(name='PCIe Socket', children=[
            M.Part(name='PCIe x16 Socket'),
        ])
    ]),
    M.Part(name='Port', note='Generic parent for all kinds of ports', children=[
        M.Part(name='USB 2.0 Port'),
        M.Part(name='USB 3.0 Port'),
        M.Part(name='RJ-45'),
        M.Part(name='SATA'),
        M.Part(name='Audio port')
    ]),
    ]

    def _connectify(objs):
        for c in objs:
            c.is_connector = True
            _connectify(c.children)

    _connectify(objs)
    return objs

def get_parts():
    parts = [
    M.Part(name='Memory controller', note='Seems to be integrated into a cpu (pc alt)'),
    M.Part(name='Audio controller'),
    M.Part(name='CPU', children=[
        M.Part(name='Pentium', children=[
            M.Part(name='Pentium 4'),
        ])
    ]),
    M.Part(name='Computer', note='Part to safe fix compilations of parts, i.e. PCs, Laptops, Servers, ...)', children=[
        M.Part(name='Desktop'),
        M.Part(name='Laptop'),
        M.Part(name='Server'),
    ]),
    M.Part(name='Casing', note='Computer casing'),
    M.Part(name='Motherboard'),
    M.Part(name='RAM', children=[
        M.Part(name='Flash memory'),
        M.Part(name='SD-RAM', children=[
            M.Part(name='DDR RAM'),
        ])
    ]),
    M.Part(name='Power supply'),
    M.Part(name='Chipset'),
    M.Part(name='Harddrive'),
    M.Part(name='Memory card reader'),
    M.Part(name='Memory card controller'),
    ]
    return parts


def get_standards():
    objs = [

    M.Part(name='CPU Instruction set', children=[
        M.Part(name='SSE 4.x'),
        M.Part(name='32bit'),
        M.Part(name='64bit'),
        M.Part(name='XD bit'),
        M.Part(name='Smart Cache'),
    ]),

    M.Part(name='RAM Standards', children=[
        M.Part(name='DDR3', children=[
            M.Part(name='DDR3-1333'),
        ])
    ]),

    M.Part(name='CPU Socket Standard', children=[
        M.Part(name='Socket 1155')
    ]),

    M.Part(name='PCIe x16 Socket (Standard)'),
    M.Part(name='USB', children=[
        M.Part(name='USB 2.0'),
        M.Part(name='USB 3.0'),
    ]),

    M.Part(name='Ethernet (10Mbits)'),
    M.Part(name='Fast Ethernet (100Mbits)'),
    M.Part(name='Gigabit Ethernet (1000Mbits)'),
    M.Part(name='SATA (Standard)', children=[
        M.Part(name='SATA 1.0'),
        M.Part(name='SATA 2.0'),
        M.Part(name='SATA 3.0'),
        M.Part(name='SATA 3.1'),
        M.Part(name='SATA 3.2'),
    ]),

    M.Part(name='Memory card', children=[
        M.Part(name='SD card'),
        M.Part(name='MMC card'),
        M.Part(name='MMCplus card'),
        M.Part(name='xD card'),
        M.Part(name='MS card'),
        M.Part(name='MS PRO card'),
    ])
    ]

    def _standardify(objs):
        for o in objs:
            o.is_standard = True
            _standardify(o.children)

    _standardify(objs)
    return objs


def get_attr_types():
    return [
    M.AttrType.init('Name', 'Text'),
    M.AttrType.init('Position', 'Order', note='The position of the associated Part in relation to other Parts'),

    # Socket
    #TODO: at_socket_package = M.AttrType(name='Package', part=p_cpusocket)
    M.AttrType.init('Year of introduction', 'Year'),

    M.AttrType.init('Pin count', 'Count', ['CPU-Socket']),
    M.AttrType.init('Pin pitch', 'Millimeter', ['CPU-Socket']),
    M.AttrType.init('Bus speed', 'Megahertz', ['CPU-Socket'], from_to=True),

    # CPU
    M.AttrType.init('Frequency', 'Megahertz', ['CPU']),
    M.AttrType.init('L2 cache', 'Byte', ['CPU']),
    M.AttrType.init('Front side bus', 'Megatransfer/Second', ['CPU']),
    M.AttrType.init('Clock multiplier', 'Factor', ['CPU']),
    M.AttrType.init('Voltage range', 'Volt', ['CPU'], from_to=True),
    M.AttrType.init('Thermal design power', 'Watt', ['CPU']),
    M.AttrType.init('Release date', 'Date', ['CPU']),
    M.AttrType.init('Release price', 'Dollar', ['CPU']),
    M.AttrType.init('Part number', 'Text', ['CPU'], multi_value=True),
    M.AttrType.init('URL', 'Text', ['CPU']),
    M.AttrType.init('Number of cores', 'Count', ['CPU']),

    # PC of BA
    M.AttrType.init('Modified', 'Boolean', ['Computer'], note='Was this computer modified after initial delivery?'),
    M.AttrType.init('Vendor', 'Text', ['Computer', 'Motherboard', 'Casing', 'CPU', 'Chipset']),
    M.AttrType.init('Serial number', 'Text', ['Computer', 'Motherboard']),
    M.AttrType.init('L1 cache', 'Byte', ['CPU']),
    M.AttrType.init('Hyperthreading', 'Boolean', ['CPU']),
    M.AttrType.init('RAM Size', 'Byte', ['RAM']),
    M.AttrType.init('Casing Size', 'Text', ['Casing'], note='Minitower, miditower, bigtower'),
    M.AttrType.init('Vendor hex', 'Hex', ['RAM']),
    M.AttrType.init('Version', 'Text', ['Pentium 4']),

    # PC alt
    M.AttrType.init('Color', 'Text', ['Casing']),
    M.AttrType.init('Width', 'Millimeter', ['Casing']),
    M.AttrType.init('Length', 'Millimeter', ['Casing']),
    M.AttrType.init('Height', 'Millimeter', ['Casing']),
    M.AttrType.init('Power', 'Watt', ['Power supply'], note='electric power (output? input?)'),
    M.AttrType.init('Memory channels', 'Count', ['Memory controller']),
    M.AttrType.init('Average half-pitch of a memory cell', 'Count', note='not yet connected ;-)'),
    M.AttrType.init('Maximal power consumption', 'Watt', ['CPU']),
    M.AttrType.init('Maximal RAM capacity', 'Megabyte', ['Motherboard']),
    M.AttrType.init('Harddrive size', 'Gigabyte', ['Harddrive']),
    # TODO: Bauform, GPU-Takt, Prozessorkern (Sandy bridge)
    ]


def get_common_attributes():
    # Note: Attributes whose values should be contained in multiple Parts
    # have to be defined here so that the inserts can be commited and
    # SQLAlchemy can find them.
    return [
    M.Attr(attr_type=M.AttrType.search('Vendor'), value='Hewlett-Packard'),
    M.Attr(attr_type=M.AttrType.search('Vendor'), value='Intel'),
    M.Attr(attr_type=M.AttrType.search('Serial number'), value='CZC4301WB9')
    ]


def get_objects_computer_BA():
    p_hpd530 = M.Part.init('HP d530 CMT(DF368A)', 'Desktop', {
        'Vendor': 'Hewlett-Packard',
        'Serial number': 'CZC4301WB9',
    })

    p_mini_tower = M.Part.init('Anonymous Mini Tower', 'Casing', {
        'Vendor': 'Hewlett-Packard',
        'Casing Size': 'Minitower',
    })

    p_hpmboard = M.Part.init('085Ch', 'Motherboard', {
        'Vendor': 'Hewlett-Packard',
        'Serial number': 'CZC4301WB9',
    })

    p_hp_pentium4 = M.Part.init('Intel Pentium 4 2.80GHz 15.2.9', 'Pentium 4', {
        'Vendor': 'Intel',
        'Version': '15.2.9',
        'Frequency': '2800',
    })
    M.Part.append('32bit', p_hp_pentium4)

    system = M.System()
    system.add_part_mapping(p_hpd530, p_mini_tower)
    system.add_part_mapping(p_mini_tower, p_hpmboard)
    system.add_part_mapping(p_hpmboard, p_hp_pentium4)
    return [system]


def get_objects_computer_alt():
    p_m1935 = M.Part.init('Acer Aspire M1935', 'Desktop', {
        'Vendor': 'Acer',
    })

    p_mini_tower = M.Part.init('Anonymous Tower', 'Casing', {
        'Width': '180',
        'Length': '379',
        'Height': '402',
        'Color': 'black',
    })

    port = M.Part.search('Port')
    p_mem_card_sd = M.Part(name='SD card port', parent_part=port)
    p_mem_card_mmc = M.Part(name='MMC card port', parent_part=port)
    p_mem_card_mmcplus = M.Part(name='MMCplus card port', parent_part=port)
    p_mem_card_xd = M.Part(name='xD card port', parent_part=port)
    p_mem_card_ms = M.Part(name='MS card port', parent_part=port)
    p_mem_card_mspro = M.Part(name='MS PRO card port', parent_part=port)

    p_power_supply = M.Part.init('Anonymous Power Source', 'Power supply', {
        'Power': '250',
    })

    p_cpu = M.Part.init('Intel Pentium Processor G645 (2,9 GHz)', 'CPU', {
        'Number of cores': '2',
        'Frequency': '2900',
        'Front side bus': '5000',
        'Maximal power consumption': '65',
        'Vendor': 'Intel',
    })

    p_mem_contr = M.Part.init('Anonymous Memory Controller', 'Memory controller',
                              {'Memory channels': '2'})

    p_motherboard = M.Part.init('Anonymous Motherboard', 'Motherboard', {
        'Maximal RAM capacity': 16384
    })

    p_ram = M.Part.init('Anonymous RAM', 'DDR RAM', {'RAM Size': 2048})
    M.Part.append('DDR3-1333', p_ram)

    p_ramsocket = M.Part(name='DDR3 RAM Socket',
                         parent_part=M.Part.search('RAM Socket'),
                         is_connector=True)
    M.Part.append('DDR3', p_ramsocket)

    p_chipset = M.Part.init('Intel B75 Express', 'Chipset', {'Vendor': 'Intel'})

    p_pci = M.Part(name='Anonymous PCIe x16 Socket',
                   parent_part=M.Part.search('PCIe x16 Socket'),
                   is_connector=True)
    M.Part.append('PCIe x16 Socket (Standard)', p_pci)

    p_usb2_port = M.Part(name='Anonymous USB 2.0 Port',
                         parent_part=M.Part.search('USB 2.0 Port'),
                         is_connector=True)
    M.Part.append('USB 2.0', p_usb2_port)

    # HELP: Ports may support multiple standards
    p_usb3_port = M.Part(name='Anonymous USB 3.0 Port',
                         parent_part=M.Part.search('USB 3.0 Port'),
                         is_connector=True)
    M.Part.append('USB 2.0', p_usb3_port)
    M.Part.append('USB 3.0', p_usb3_port)

    p_rj45 = M.Part(name='Anonymous RJ-45',
                    parent_part=M.Part.search('RJ-45'),
                    is_connector=True)
    M.Part.append('Ethernet (10Mbits)', p_rj45)
    M.Part.append('Fast Ethernet (100Mbits)', p_rj45)
    M.Part.append('Gigabit Ethernet (1000Mbits)', p_rj45)

    p_harddrive = M.Part.init('Anonymous harddrive', 'Harddrive', {
        'Harddrive size': 500
    })
    M.Part.append('SATA (Standard)', p_harddrive)

    # HELP: A memory card reader can be seperated into a controller being on the
    # motherboard and the card ports being in the casing
    p_card_reader_controller = M.Part(name='Anonymous card reader controller',
                                      parent_part=M.Part.search('Memory card controller'))
    M.Part.append('SD card', p_card_reader_controller)
    M.Part.append('MMC card', p_card_reader_controller)
    M.Part.append('MMCplus card', p_card_reader_controller)
    M.Part.append('xD card', p_card_reader_controller)
    M.Part.append('MS card', p_card_reader_controller)
    M.Part.append('MS PRO card', p_card_reader_controller)

    p_cpusocket = M.Part.search('CPU-Socket') # anonymous
    p_audioport = M.Part.search('Audio port') # anonymous
    p_audiocontr = M.Part.search('Audio controller') # anonymous
    p_sata = M.Part.search('SATA') # anonymous

    system = M.System()
    system.add_part_mapping(p_m1935, p_mini_tower)

    system.add_part_mapping(p_mini_tower, p_power_supply)
    system.add_part_mapping(p_mini_tower, p_motherboard)
    system.add_part_mapping(p_mini_tower, p_mem_card_sd)
    system.add_part_mapping(p_mini_tower, p_mem_card_mmc)
    system.add_part_mapping(p_mini_tower, p_mem_card_mmcplus)
    system.add_part_mapping(p_mini_tower, p_mem_card_xd)
    system.add_part_mapping(p_mini_tower, p_mem_card_ms)
    system.add_part_mapping(p_mini_tower, p_mem_card_mspro)

    system.add_part_mapping(p_motherboard, p_cpusocket)
    system.add_part_mapping(p_motherboard, p_ramsocket, 4)
    system.add_part_mapping(p_motherboard, p_chipset)
    system.add_part_mapping(p_motherboard, p_pci)
    system.add_part_mapping(p_motherboard, p_usb2_port, 6)
    system.add_part_mapping(p_motherboard, p_usb3_port, 2)
    system.add_part_mapping(p_motherboard, p_audioport, 2)
    system.add_part_mapping(p_motherboard, p_rj45)
    system.add_part_mapping(p_motherboard, p_audiocontr)
    system.add_part_mapping(p_motherboard, p_card_reader_controller)
    system.add_part_mapping(p_motherboard, p_sata)
    system.add_part_mapping(p_ramsocket, p_ram, 2)
    system.add_part_mapping(p_sata, p_harddrive)
    system.add_part_mapping(p_cpusocket, p_cpu)
    system.add_part_mapping(p_cpu, p_mem_contr)
    system.add_part_mapping(p_cpu, M.Part.search('SSE 4.x'))
    system.add_part_mapping(p_cpu, M.Part.search('64bit'))
    system.add_part_mapping(p_cpu, M.Part.search('XD bit'))
    system.add_part_mapping(p_cpu, M.Part.search('Smart Cache'))

    return [system]


