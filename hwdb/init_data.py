from hwdb import model as M


def get_units():
    return [
    M.Unit(name='Nanosecond', format='%(unit)s ns'),
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
    M.Unit(name='Megatransfer/Second', format='%(unit)s MT/s'),
    M.Unit(name='Megabyte/Second', format='%(unit)s MB/s'),
    M.Unit(name='Factor', format='%(unit)sx', note='ie cpu clock multiplier'),
    M.Unit(name='Volt', format='%(unit)s V'),
    M.Unit(name='Watt', format='%(unit)s W'),
    M.Unit(name='Dollar', format='$%(unit)s'),
    M.Unit(name='Url', format='<a href="%(unit)s">%(unit)s</a>'),
    M.Unit(name='Text'),
    M.Unit(name='Boolean'),
    M.Unit(name='Hex'),
    M.Unit(name='Number of clock cycles', note='Should this be merged with "Count"? Used for RAM timings'),
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
    M.Part(name='PCIe'), # number of lanes as attribute

    ]

    def _connectify(objs):
        for c in objs:
            c.is_connector = True
            _connectify(c.children)

    _connectify(objs)
    return objs

def get_parts():
    objs = [
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
    M.Part(name='Flash memory'),
    M.Part(name='DIMM'),
    M.Part(name='Power supply'),
    M.Part(name='Chipset'),
    M.Part(name='Harddrive'),
    M.Part(name='Memory card reader'),
    M.Part(name='Memory card controller'),
    M.Part(name='RAM', children=[
        M.Part(name='DDR3 SDRAM', children=[
            M.Part(name='DDR3-1333')
        ]),
    ]),
    ]

    M.db_session.add_all(objs)
    M.db_session.flush()

    M.add_standards_to_part(M.Part.search('DDR3 SDRAM'), 'DDR3 SDRAM (Standard)')
    M.add_standards_to_part(M.Part.search('DDR3-1333'), 'DDR3-1333 (Standard)')


    pin_count = M.AttrType.init('Pin count', 'Count').add_to_parts('DIMM')
    M.db_session.add(M.Attr(attr_type=pin_count, value='240'))
    M.db_session.flush()


    # http://en.wikipedia.org/wiki/DIMM
    dimm168 = M.Part.init('168-pin DIMM', 'DIMM', {'Pin count': 168})
    dimm184 = M.Part.init('184-pin DIMM', 'DIMM', {'Pin count': 184})
    dimm240_ddr2 = M.Part.init('240-pin DIMM (DDR2 SDRAM)', 'DIMM', {'Pin count': 240})
    dimm240_ddr3 = M.Part.init('240-pin DIMM (DDR3 SDRAM)', 'DIMM', {'Pin count': 240})

    M.add_standards_to_part(dimm168, 'SDRAM (Standard)')
    M.add_standards_to_part(dimm184, 'DDR SDRAM (Standard)')
    M.add_standards_to_part(dimm240_ddr2, 'DDR2 SDRAM (Standard)')
    M.add_standards_to_part(dimm240_ddr3, 'DDR3 SDRAM (Standard)')
    return objs


def get_standards():
    objs = [

    M.Part(name='CPU Instruction set', children=[
        M.Part(name='SSE 4.x'),
        M.Part(name='32bit'),
        M.Part(name='64bit'),
        M.Part(name='XD bit'),
        M.Part(name='Smart Cache'),
    ]),

    M.Part(name='RAM', children=[
        M.Part(name='SDRAM', children=[
            # http://de.wikipedia.org/wiki/Synchronous_Dynamic_Random_Access_Memory#Verschiedene_Typen
            M.Part(name='PC-66'),
            M.Part(name='PC-100'),
            M.Part(name='PC-133'),
        ]),

        M.Part(name='DDR SDRAM', children=[
            # http://en.wikipedia.org/wiki/DDR_SDRAM#Chips_and_modules
            M.Part(name='DDR-200'),
            M.Part(name='DDR-266'),
            M.Part(name='DDR-333'),
            M.Part(name='DDR-400', children=[
                M.Part(name='DDR-400A'),
                M.Part(name='DDR-400B'),
                M.Part(name='DDR-400C'),
            ]),
        ]),

        M.Part(name='DDR2 SDRAM', children=[
            # http://en.wikipedia.org/wiki/DDR2_SDRAM#Chips_and_modules
            M.Part(name='DDR2-400', children=[
                M.Part(name='DDR2-400B'),
                M.Part(name='DDR2-400C'),
            ]),
            M.Part(name='DDR2-533', children=[
                M.Part(name='DDR2-533B'),
                M.Part(name='DDR2-533C'),
            ]),
            M.Part(name='DDR2-667', children=[
                M.Part(name='DDR2-667C'),
                M.Part(name='DDR2-667D'),
            ]),
            M.Part(name='DDR2-800', children=[
                M.Part(name='DDR2-800C'),
                M.Part(name='DDR2-800D'),
                M.Part(name='DDR2-800E'),
            ]),
            M.Part(name='DDR2-1066', children=[
                M.Part(name='DDR2-1066E'),
                M.Part(name='DDR2-1066F'),
            ]),
        ]),

        M.Part(name='DDR3 SDRAM', children=[
            # http://en.wikipedia.org/wiki/DDR3_SDRAM#JEDEC_standard_modules
            M.Part(name='DDR3-800', children=[
                M.Part(name='DDR3-800D'),
                M.Part(name='DDR3-800E'),
            ]),
            M.Part(name='DDR3-1066', children=[
                M.Part(name='DDR3-1066E'),
                M.Part(name='DDR3-1066F'),
                M.Part(name='DDR3-1066G'),
            ]),
            M.Part(name='DDR3-1333', children=[
                M.Part(name='DDR3-1333F'),
                M.Part(name='DDR3-1333G'),
                M.Part(name='DDR3-1333H'),
                M.Part(name='DDR3-1333J'),
            ]),
            M.Part(name='DDR3-1600', children=[
                M.Part(name='DDR3-1600G'),
                M.Part(name='DDR3-1600H'),
                M.Part(name='DDR3-1600J'),
                M.Part(name='DDR3-1600K'),
            ]),
            M.Part(name='DDR3-1866', children=[
                M.Part(name='DDR3-1866J'),
                M.Part(name='DDR3-1866K'),
                M.Part(name='DDR3-1866L'),
                M.Part(name='DDR3-1866M'),
            ]),
            M.Part(name='DDR3-2133', children=[
                M.Part(name='DDR3-2133K'),
                M.Part(name='DDR3-2133L'),
                M.Part(name='DDR3-2133M'),
                M.Part(name='DDR3-2133N'),
            ]),
        ]),
    ]),

    M.Part(name='CPU Socket Standard', children=[
        M.Part(name='Socket 1155')
    ]),
    M.Part(name='AGP (Standard)'),
    M.Part(name='PCI (Standard)', children=[
        # http://en.wikipedia.org/wiki/Conventional_PCI#History
        M.Part(name='PCI 1.0'), # year=1992
        M.Part(name='PCI 2.0'), # year=1993
        M.Part(name='PCI 2.1'), # year=1995
        M.Part(name='PCI 2.2'), # year=1998
        M.Part(name='PCI 2.3'), # year=2002
        M.Part(name='PCI 3.0'), # year=2002
    ]),
    M.Part(name='PCI Express', children=[
        # http://en.wikipedia.org/wiki/PCI_Express#History_and_revisions
        M.Part(name='PCIe 1.0a'),
        M.Part(name='PCIe 1.1'),
        M.Part(name='PCIe 2.0'),
        M.Part(name='PCIe 2.1'),
        M.Part(name='PCIe 3.0'),
    ]),
    M.Part(name='USB', children=[
        M.Part(name='USB 1'),
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
            o.name += ' (Standard)'
            o.is_standard = True
            _standardify(o.children)

    _standardify(objs)
    return objs


def get_attr_types():
    ddr = ('DDR SDRAM (Standard)', 'DDR2 SDRAM (Standard)', 'DDR3 SDRAM (Standard)', )
    return [
    M.AttrType.init('Name', 'Text'),
    M.AttrType.init('Position', 'Order', note='The position of the associated Part in relation to other Parts'),

    # Socket
    #TODO: at_socket_package = M.AttrType(name='Package', part=p_cpusocket)
    M.AttrType.init('Year of introduction', 'Year'),

    M.AttrType.init('Pin count', 'Count').add_to_parts('CPU-Socket'),
    M.AttrType.init('Pin pitch', 'Millimeter').add_to_parts('CPU-Socket'),
    M.AttrType.init('Bus speed', 'Megahertz', from_to=True).add_to_parts('CPU-Socket'),

    M.AttrType.init('Frequency', 'Megahertz').add_to_parts('CPU'),
    M.AttrType.init('Memory clock', 'Megahertz').add_to_parts(*ddr),
    M.AttrType.init('I/O bus clock', 'Megahertz').add_to_parts(*ddr),
    M.AttrType.init('L2 cache', 'Byte').add_to_parts('CPU'),
    M.AttrType.init('Front side bus', 'Megatransfer/Second').add_to_parts('CPU'),
    M.AttrType.init('Data rate', 'Megatransfer/Second').add_to_parts(*ddr),
    M.AttrType.init('Clock multiplier', 'Factor').add_to_parts('CPU'),
    M.AttrType.init('Voltage range', 'Volt', from_to=True).add_to_parts('CPU'),
    M.AttrType.init('Thermal design power', 'Watt').add_to_parts('CPU'),
    M.AttrType.init('Release date', 'Date').add_to_parts('CPU'),
    M.AttrType.init('Release price', 'Dollar').add_to_parts('CPU'),
    M.AttrType.init('Part number', 'Text', multi_value=True).add_to_parts('CPU'),
    M.AttrType.init('URL', 'Text').add_to_parts('CPU'),
    M.AttrType.init('Number of cores', 'Count').add_to_parts('CPU'),
    M.AttrType.init('Cycle time', 'Nanosecond').add_to_parts(*ddr),
    M.AttrType.init('Module name', 'Text').add_to_parts(*ddr),
    M.AttrType.init('Peak transfer rate', 'Megabyte/Second').add_to_parts(*ddr),
    M.AttrType.init('Column Address Strobe latency [CL]', 'Number of clock cycles').add_to_parts(*ddr),
    M.AttrType.init('Row Address to Column Address Delay [T<lower>RCD</lower>]', 'Number of clock cycles').add_to_parts(*ddr),
    M.AttrType.init('Row Precharge Time [T<lower>RP</lower>]', 'Number of clock cycles').add_to_parts(*ddr),
    M.AttrType.init('Row Active Time [T<lower>RAS</lower>]', 'Number of clock cycles').add_to_parts(*ddr),

    # PC of BA
    M.AttrType.init('Modified', 'Boolean', note='Was this computer modified after initial delivery?').add_to_parts('Computer'),
    M.AttrType.init('Vendor', 'Text').add_to_parts('Computer', 'Motherboard', 'Casing', 'CPU', 'Chipset'),
    M.AttrType.init('Serial number', 'Text').add_to_parts('Computer', 'Motherboard'),
    M.AttrType.init('L1 cache', 'Byte').add_to_parts('CPU'),
    M.AttrType.init('Hyperthreading', 'Boolean').add_to_parts('CPU'),
    M.AttrType.init('RAM Size', 'Byte').add_to_parts('RAM'),
    M.AttrType.init('Casing Size', 'Text', note='Minitower, miditower, bigtower').add_to_parts('Casing'),
    M.AttrType.init('Vendor hex', 'Hex').add_to_parts('RAM'),
    M.AttrType.init('Version', 'Text').add_to_parts('Pentium 4'),

    # PC alt
    M.AttrType.init('Color', 'Text').add_to_parts('Casing'),
    M.AttrType.init('Width', 'Millimeter').add_to_parts('Casing'),
    M.AttrType.init('Length', 'Millimeter').add_to_parts('Casing'),
    M.AttrType.init('Height', 'Millimeter').add_to_parts('Casing'),
    M.AttrType.init('Power', 'Watt', note='electric power (output? input?)').add_to_parts('Power supply'),
    M.AttrType.init('Memory channels', 'Count').add_to_parts('Memory controller'),
    M.AttrType.init('Average half-pitch of a memory cell', 'Count', note='not yet connected ;-)'),
    M.AttrType.init('Maximal power consumption', 'Watt').add_to_parts('CPU'),
    M.AttrType.init('Maximal RAM capacity', 'Megabyte').add_to_parts('Motherboard'),
    M.AttrType.init('Harddrive size', 'Gigabyte').add_to_parts('Harddrive'),
    # TODO: Bauform, GPU-Takt, Prozessorkern (Sandy bridge)
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
    M.add_standards_to_part(p_hp_pentium4, '32bit (Standard)')

    p_hpd530.add_part_connection(p_hpd530, p_mini_tower)
    p_hpd530.add_part_connection(p_mini_tower, p_hpmboard)
    p_hpd530.add_part_connection(p_hpmboard, p_hp_pentium4)
    return [p_hpd530]


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

    p_ram = M.Part.init('Anonymous RAM', 'DDR3-1333', {'RAM Size': 2048})

    p_ramsocket = M.Part.search('240-pin DIMM (DDR3 SDRAM)')

    p_chipset = M.Part.init('Intel B75 Express', 'Chipset', {'Vendor': 'Intel'})

    p_pci = M.Part.search('PCIe x16 Socket')

    p_usb2_port = M.Part(name='Anonymous USB 2.0 Port',
                         parent_part=M.Part.search('USB 2.0 Port'),
                         is_connector=True)
    M.add_standards_to_part(p_usb2_port, 'USB 2.0 (Standard)')

    # HELP: Ports may support multiple standards
    p_usb3_port = M.Part(name='Anonymous USB 3.0 Port',
                         parent_part=M.Part.search('USB 3.0 Port'),
                         is_connector=True)
    M.add_standards_to_part(p_usb3_port, 'USB 2.0 (Standard)', 'USB 3.0 (Standard)')

    p_rj45 = M.Part(name='Anonymous RJ-45',
                    parent_part=M.Part.search('RJ-45'),
                    is_connector=True)
    M.add_standards_to_part(p_rj45,
                          'Ethernet (10Mbits) (Standard)',
                          'Fast Ethernet (100Mbits) (Standard)',
                          'Gigabit Ethernet (1000Mbits) (Standard)')

    p_harddrive = M.Part.init('Anonymous harddrive', 'Harddrive', {
        'Harddrive size': 500
    })

    # HELP: A memory card reader can be seperated into a controller being on the
    # motherboard and the card ports being in the casing
    p_card_reader_controller = M.Part(name='Anonymous card reader controller',
                                      parent_part=M.Part.search('Memory card controller'))
    M.add_standards_to_part(p_card_reader_controller,
                          'SD card (Standard)',
                          'MMC card (Standard)',
                          'MMCplus card (Standard)',
                          'xD card (Standard)',
                          'MS card (Standard)',
                          'MS PRO card (Standard)')

    p_cpusocket = M.Part.search('CPU-Socket') # anonymous
    p_audioport = M.Part.search('Audio port') # anonymous
    p_audiocontr = M.Part.search('Audio controller') # anonymous
    p_sata = M.Part.search('SATA') # anonymous

    p_m1935.add_part_connection(p_m1935, p_mini_tower)

    p_m1935.add_part_connection(p_mini_tower, p_power_supply)
    p_m1935.add_part_connection(p_mini_tower, p_motherboard)
    p_m1935.add_part_connection(p_mini_tower, p_mem_card_sd)
    p_m1935.add_part_connection(p_mini_tower, p_mem_card_mmc)
    p_m1935.add_part_connection(p_mini_tower, p_mem_card_mmcplus)
    p_m1935.add_part_connection(p_mini_tower, p_mem_card_xd)
    p_m1935.add_part_connection(p_mini_tower, p_mem_card_ms)
    p_m1935.add_part_connection(p_mini_tower, p_mem_card_mspro)

    p_m1935.add_part_connection(p_motherboard, p_cpusocket)
    p_m1935.add_part_connection(p_motherboard, p_ramsocket, 4)
    p_m1935.add_part_connection(p_motherboard, p_chipset)
    p_m1935.add_part_connection(p_motherboard, p_pci)
    p_m1935.add_part_connection(p_motherboard, p_usb2_port, 6)
    p_m1935.add_part_connection(p_motherboard, p_usb3_port, 2)
    p_m1935.add_part_connection(p_motherboard, p_audioport, 2)
    p_m1935.add_part_connection(p_motherboard, p_rj45)
    p_m1935.add_part_connection(p_motherboard, p_audiocontr)
    p_m1935.add_part_connection(p_motherboard, p_card_reader_controller)
    p_m1935.add_part_connection(p_motherboard, p_sata)
    p_m1935.add_part_connection(p_ramsocket, p_ram, 2)
    p_m1935.add_part_connection(p_sata, p_harddrive)
    p_m1935.add_part_connection(p_cpusocket, p_cpu)
    p_m1935.add_part_connection(p_cpu, p_mem_contr)
    p_m1935.add_part_connection(p_cpu, M.Part.search('SSE 4.x (Standard)'))
    p_m1935.add_part_connection(p_cpu, M.Part.search('64bit (Standard)'))
    p_m1935.add_part_connection(p_cpu, M.Part.search('XD bit (Standard)'))
    p_m1935.add_part_connection(p_cpu, M.Part.search('Smart Cache (Standard)'))

    return [p_m1935]
