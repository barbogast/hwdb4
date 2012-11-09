from hwdb import model as M


def get_units():
    return [
    M.Unit(name='ns',     label='Nanosecond', format='%(unit)s ns'),
    M.Unit(name='nm',     label='Nanometer', format='%(unit)s nm'),
    M.Unit(name='mm',     label='Millimeter', format='%(unit)s mm'),
    M.Unit(name='mm^2',     label='Square millimeter', format='%(unit)s mm<sup>2</sup>'),
    M.Unit(name='MHz',    label='Megahertz', format='%(unit)s MHz', note='We dont use the minimal unit Hertz because processors are in the MHz area'),
    M.Unit(name='date',   label='Date'),
    M.Unit(name='year',   label='Year'),
    M.Unit(name='count',  label='Count'),
    M.Unit(name='order',  label='Order', note='Information about the order/sequence of a Part'),
    M.Unit(name='B',      label='Byte', format='%(unit)s Byte'),
    M.Unit(name='KB',      label='Kilobyte', format='%(unit)s Kilobyte'),
    M.Unit(name='MB',     label='Megabyte', format='%(unit)s Megabyte'),
    M.Unit(name='GB',     label='Gigabyte', format='%(unit)s Gigabyte'),
    M.Unit(name='MT/s',   label='Megatransfer/Second', format='%(unit)s MT/s'),
    M.Unit(name='MB/s',   label='Megabyte/Second', format='%(unit)s MB/s'),
    M.Unit(name='factor', label='Factor', format='%(unit)sx', note='ie cpu clock multiplier'),
    M.Unit(name='V',      label='Volt', format='%(unit)s V'),
    M.Unit(name='W',      label='Watt', format='%(unit)s W'),
    M.Unit(name='$',      label='Dollar', format='$%(unit)s'),
    M.Unit(name='url',    label='Url', format='<a href="%(unit)s">%(unit)s</a>'),
    M.Unit(name='text',   label='Text'),
    M.Unit(name='bool',   label='Boolean'),
    M.Unit(name='hex',    label='Hex'),
    M.Unit(name='clock_cycles', label='Number of clock cycles', note='Should this be merged with "Count"? Used for RAM timings'),
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
    M.Part(name='CPU Core', children=[
        M.Part(name='Intel 80486'),
        M.Part(name='P5'),
        M.Part(name='P6'),
        M.Part(name='Netburst'),
        M.Part(name='Intel Core'),
        M.Part(name='Enhanced Pentium M'),
        M.Part(name='Nehalem'),
        M.Part(name='Penryn'),
        M.Part(name='Sandy Bridge'),
        M.Part(name='Westmere'),
        M.Part(name='Ivy Bridge'),
        M.Part(name='Haswell Bridge'),
    ]),
    M.Part(name='CPU', children=[
        M.Part(name='Desktop CPU', children=[
            M.Part(name='Pentium', children=[
                M.Part(name='Pentium 4'),
                M.Part(name='Pentium 4 Extreme Edition'),
                M.Part(name='Pentium 4-M'),
                M.Part(name='Mobile Pentium 4')
            ]),
        ]),
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
    return objs


def get_sub_parts():
    M.Part.search('DDR3 SDRAM').add_standards('DDR3 SDRAM (Standard)')
    M.Part.search('DDR3-1333').add_standards('DDR3-1333 (Standard)')

    dimm_url = 'http://en.wikipedia.org/wiki/DIMM'
    dimm168 = M.Part.init('168-pin DIMM', 'DIMM', {'Pin count': 168, 'Source': dimm_url},
                          standards=('SDRAM (Standard)',))
    dimm184 = M.Part.init('184-pin DIMM', 'DIMM', {'Pin count': 184, 'Source': dimm_url},
                          standards=('DDR SDRAM (Standard)',))
    dimm240_ddr2 = M.Part.init('240-pin DIMM (DDR2 SDRAM)', 'DIMM',
                               attributes={'Pin count': 240, 'Source': dimm_url},
                               standards=('DDR2 SDRAM (Standard)',))
    dimm240_ddr3 = M.Part.init('240-pin DIMM (DDR3 SDRAM)', 'DIMM',
                               attributes={'Pin count': 240, 'Source': dimm_url},
                               standards=('DDR3 SDRAM (Standard)',))

    # CPU cores
    willamette = M.Part.init('Willamette', 'Netburst', attributes={
        'Average half-pitch of a memory cell': 180,
        'L2 cache': 256,
        'Front side bus': 400,
        'Transistors': 42000000,
        'Die size': 217,
    }, standards=('B2 (Stepping 65nm) (Standard)',
                  'C1 (Stepping 45nm) (Standard)',
                  'D0 (CPU Stepping) (Standard)',
                  'E0 (Stepping 45nm) (Standard)',
                  'MMX (Standard)',
                  'SSE (Standard)',
                  'SSE2 (Standard)')
    )

    M.Part.init('Northwood', 'Netburst', attributes={
        'L2 cache': 512,
    })
    M.Part.init('Prescott', 'Netburst', attributes={'L2 cache': 1024, 'Front side bus': 533}),
    M.Part.init('Prescott (HT)', 'Netburst', attributes={'L2 cache': 1024, 'Front side bus': 800}),
    M.Part.init('Prescott 2M', 'Netburst', attributes={'L2 cache': 2048}),
    M.Part.init('Cedar Mill', 'Netburst', attributes={'L2 cache': 2048, 'Front side bus': 800}),
    M.Part.init('Gallatin', 'Netburst', attributes={'L2 cache': 512, 'L3 cache': 2048}),

    return []


def get_standards():
    objs = [

    M.Part(name='CPU Instruction set', children=[
        M.Part(name='MMX'),
        M.Part(name='SSE'),
        M.Part(name='SSE2'),
        M.Part(name='SSE 4.x'),
        M.Part(name='32bit'),
        M.Part(name='64bit'),
        M.Part(name='XD bit'),
        M.Part(name='Smart Cache'),
    ]),

    M.Part(name='CPU Stepping', children=[
        M.Part(name='D0 (CPU Stepping)'),
        M.Part(name='CPU Stepping 65nm',
            children=[M.Part(name=name+' (Stepping 65nm)') for name in 'B2 B3 L2 E1 G0 G2 M0 A1'.split()]
        ),
        M.Part(name='CPU Stepping 45nm',
            children=[M.Part(name=name+' (Stepping 45nm)') for name in 'C0 M0 C1 M1 E0 R0 A1'.split()]
        )
    ]),

    M.Part(name='RAM', children=[
        M.Part(name='SDRAM', children=[
            # http://de.wikipedia.org/wiki/Synchronous_Dynamic_Random_Access_Memory#Verschiedene_Typen
            M.Part(name='PC-66'),
            M.Part(name='PC-100'),
            M.Part(name='PC-133'),
        ]),

        M.Part(name='DDR SDRAM', children=[
            M.Part(name='DDR-200'),
            M.Part(name='DDR-266'),
            M.Part(name='DDR-333'),
            M.Part(name='DDR-400'),
        ]),

        M.Part(name='DDR2 SDRAM', children=[
            M.Part(name='DDR2-400'),
            M.Part(name='DDR2-533'),
            M.Part(name='DDR2-667'),
            M.Part(name='DDR2-800'),
            M.Part(name='DDR2-1066'),
        ]),

        M.Part(name='DDR3 SDRAM', children=[
            M.Part(name='DDR3-800'),
            M.Part(name='DDR3-1066'),
            M.Part(name='DDR3-1333'),
            M.Part(name='DDR3-1600'),
            M.Part(name='DDR3-1866'),
            M.Part(name='DDR3-2133'),
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
    M.AttrType.init('Position', 'order', note='The position of the associated Part in relation to other Parts'),

    # Socket
    #TODO: at_socket_package = M.AttrType(name='Package', part=p_cpusocket)
    M.AttrType.init('Year of introduction', 'year'),

    M.AttrType.init('Pin count', 'count').add_to_parts('CPU-Socket', 'DIMM'),
    M.AttrType.init('Pin pitch', 'mm').add_to_parts('CPU-Socket'),
    M.AttrType.init('Bus speed', 'MHz', from_to=True).add_to_parts('CPU-Socket'),
    M.AttrType.init('Area (mm<sup>2</sup>', 'mm^2').add_to_parts('CPU Stepping (Standard)'),
    M.AttrType.init('CPUID', 'text').add_to_parts('CPU Stepping (Standard)'),
    M.AttrType.init('Maximal Clock', 'MHz').add_to_parts('CPU Stepping (Standard)'),

    M.AttrType.init('Frequency', 'MHz').add_to_parts('CPU'),
    M.AttrType.init('Memory clock', 'MHz').add_to_parts(*ddr),
    M.AttrType.init('I/O bus clock', 'MHz').add_to_parts(*ddr),
    M.AttrType.init('Data rate', 'MT/s').add_to_parts(*ddr),
    M.AttrType.init('Clock multiplier', 'factor').add_to_parts('CPU'),
    M.AttrType.init('Voltage range', 'V', from_to=True).add_to_parts('CPU'),
    M.AttrType.init('Thermal design power', 'W').add_to_parts('CPU'),
    M.AttrType.init('Release date', 'date').add_to_parts('CPU'),
    M.AttrType.init('Release price', '$').add_to_parts('CPU'),
    M.AttrType.init('Part number', 'text', multi_value=True).add_to_parts('CPU'),
    M.AttrType.init('Source', 'url', note='Where does the information for this part come from?').add_to_parts('CPU', 'DIMM', *ddr),
    M.AttrType.init('Number of cores', 'count').add_to_parts('CPU'),
    M.AttrType.init('Cycle time', 'ns').add_to_parts(*ddr),
    M.AttrType.init('Module name', 'text').add_to_parts(*ddr),
    M.AttrType.init('Peak transfer rate', 'MB/s').add_to_parts(*ddr),
    M.AttrType.init('Column Address Strobe latency [CL]', 'clock_cycles').add_to_parts(*ddr),
    M.AttrType.init('Row Address to Column Address Delay [T<sub>RCD</sub>]', 'clock_cycles').add_to_parts(*ddr),
    M.AttrType.init('Row Precharge Time [T<sub>RP</sub>]', 'clock_cycles').add_to_parts(*ddr),
    M.AttrType.init('Row Active Time [T<sub>RAS</sub>]', 'clock_cycles').add_to_parts(*ddr),

    # PC of BA
    M.AttrType.init('Modified', 'bool', note='Was this computer modified after initial delivery?').add_to_parts('Computer'),
    M.AttrType.init('Vendor', 'text').add_to_parts('Computer', 'Motherboard', 'Casing', 'CPU', 'Chipset'),
    M.AttrType.init('Serial number', 'text').add_to_parts('Computer', 'Motherboard'),
    M.AttrType.init('Hyperthreading', 'bool').add_to_parts('CPU'),
    M.AttrType.init('RAM Size', 'B').add_to_parts('RAM'),
    M.AttrType.init('Casing Size', 'text', note='Minitower, miditower, bigtower').add_to_parts('Casing'),
    M.AttrType.init('Vendor hex', 'hex').add_to_parts('RAM'),
    M.AttrType.init('Version', 'text').add_to_parts('Pentium 4'),

    # PC alt
    M.AttrType.init('Color', 'text').add_to_parts('Casing'),
    M.AttrType.init('Width', 'mm').add_to_parts('Casing'),
    M.AttrType.init('Length', 'mm').add_to_parts('Casing'),
    M.AttrType.init('Height', 'mm').add_to_parts('Casing'),
    M.AttrType.init('Power', 'W', note='electric power (output? input?)').add_to_parts('Power supply'),
    M.AttrType.init('Memory channels', 'count').add_to_parts('Memory controller'),
    M.AttrType.init('Maximal power consumption', 'W').add_to_parts('CPU'),
    M.AttrType.init('Maximal RAM capacity', 'MB').add_to_parts('Motherboard'),
    M.AttrType.init('Harddrive size', 'GB').add_to_parts('Harddrive'),
    # TODO: Bauform, GPU-Takt

    M.AttrType.init('L1 cache', 'B').add_to_parts('CPU'),
    M.AttrType.init('L2 cache', 'KB').add_to_parts('CPU', 'CPU Core'),
    M.AttrType.init('L3 cache', 'KB').add_to_parts('CPU', 'CPU Core'),
    M.AttrType.init('Front side bus', 'MT/s').add_to_parts('CPU', 'CPU Core'),
    M.AttrType.init('Transistors', 'count').add_to_parts('CPU Core'),
    M.AttrType.init('Die size', 'mm^2').add_to_parts('CPU Core'),
    M.AttrType.init('Average half-pitch of a memory cell', 'nm').add_to_parts('CPU Core'),
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
    }, standards=('32bit (Standard)',))

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

    p_usb2_port = M.Part.init('Anonymous USB 2.0 Port', 'USB 2.0 Port',
                         is_connector=True, standards=('USB 2.0 (Standard)',))

    # HELP: Ports may support multiple standards
    p_usb3_port = M.Part.init('Anonymous USB 3.0 Port', 'USB 3.0 Port',
                              is_connector=True,
                              standards=('USB 2.0 (Standard)', 'USB 3.0 (Standard)'))

    p_rj45 = M.Part.init('Anonymous RJ-45', 'RJ-45', is_connector=True,
                         standards=(
                             'Ethernet (10Mbits) (Standard)',
                             'Fast Ethernet (100Mbits) (Standard)',
                             'Gigabit Ethernet (1000Mbits) (Standard)')
                    )

    p_harddrive = M.Part.init('Anonymous harddrive', 'Harddrive', {
        'Harddrive size': 500
    })

    # HELP: A memory card reader can be seperated into a controller being on the
    # motherboard and the card ports being in the casing
    p_card_reader_controller = M.Part(name='Anonymous card reader controller',
                                      parent_part=M.Part.search('Memory card controller'))
    p_card_reader_controller.add_standards(
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
