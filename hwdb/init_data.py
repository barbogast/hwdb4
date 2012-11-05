from hwdb import model as M


def get_initial_objects():
    u_nm = M.Unit(name='Nanometer', format='%(unit)s nm')
    u_mm = M.Unit(name='Milimeter', format='%(unit)s mm')
    u_mhz = M.Unit(name='Megahertz', format='%(unit)s MHz', note='We dont use the minimal unit Hertz because processors are in the MHz area')
    u_date = M.Unit(name='Date')
    u_year = M.Unit(name='Year')
    u_count = M.Unit(name='Count')
    u_order = M.Unit(name='Order', note='Information about the order/sequence of a Part')
    u_byte = M.Unit(name='Byte', format='%(unit)s Byte')
    u_mb = M.Unit(name='Megabyte', format='%(unit)s Megabyte')
    u_gb = M.Unit(name='Gigabyte', format='%(unit)s Gigabyte')
    u_transfer = M.Unit(name='Megatransfer/Second', format='%(unit)s MT/s', note='used with Front side bus')
    u_factor = M.Unit(name='Factor', format='%(unit)sx', note='ie cpu clock multiplier')
    u_volt = M.Unit(name='Volt', format='%(unit)s V')
    u_watt = M.Unit(name='Watt', format='%(unit)s W')
    u_dollar = M.Unit(name='Dollar', format='$%(unit)s')
    u_url = M.Unit(name='Url', format='<a href="%(unit)s">%(unit)s</a>')
    u_text = M.Unit(name='Text')
    u_boolean = M.Unit(name='Boolean')
    u_hex = M.Unit(name='Hex')

    # Sockets & Ports
    p_socket = M.Part(name='Socket', note='Generic parent for all kinds of sockets')
    p_cpusocket = M.Part(name='CPU-Socket', parent_part=p_socket)
    p_ram_socket = M.Part(name='RAM Socket', parent_part=p_socket)
    p_pcie_socket = M.Part(name='PCIe Socket', parent_part=p_socket)
    p_pcie_x16_socket = M.Part(name='PCIe x16 Socket', parent_part=p_pcie_socket)
    p_port = M.Part(name='Port', note='Generic parent for all kinds of ports')
    p_usb2_port = M.Part(name='USB 2.0 Port', parent_part=p_port)
    p_usb3_port = M.Part(name='USB 3.0 Port', parent_part=p_port)
    p_rj45 = M.Part(name='RJ-45', parent_part=p_port)
    p_sata = M.Part(name='SATA', parent_part=p_port)
    p_audioport = M.Part(name='Audio port', parent_part=p_port)

    # Components
    p_memory_controller = M.Part(name='Memory controller', note='Seems to be integrated into a cpu (pc alt)')
    p_audio_controller = M.Part(name='Audio controller')
    p_cpu = M.Part(name='CPU')
    p_pentium = M.Part(name='Pentium', parent_part=p_cpu)
    p_pentium4 = M.Part(name='Pentium 4', parent_part=p_pentium)
    p_computer = M.Part(name='Computer', note='Part to safe fix compilations of parts, i.e. PCs, Laptops, Servers, ...)')
    p_desktop = M.Part(name='Desktop', parent_part=p_computer)
    p_laptop = M.Part(name='Laptop', parent_part=p_computer)
    p_server = M.Part(name='Server', parent_part=p_computer)
    p_casing = M.Part(name='Casing', note='Computer casing')
    p_motherboard = M.Part(name='Motherboard')
    p_ram = M.Part(name='RAM')
    p_sdram = M.Part(name='SD-RAM', parent_part=p_ram)
    p_ddr = M.Part(name='DDR RAM', parent_part=p_sdram)
    p_flash = M.Part(name='Flash memory', parent_part=p_ram)
    p_power_supply = M.Part(name='Power supply')
    p_chipset = M.Part(name='Chipset')
    p_harddrive = M.Part(name='Harddrive')
    p_memorycard_reader = M.Part(name='Memory card reader')

    # Standards
    s_cpu_standard = M.Part(name='CPU Instruction set', is_standard=True)
    s_cpu_sse4 = M.Part(name='SSE 4.x', parent_part=s_cpu_standard, is_standard=True)
    s_cpu_32bit = M.Part(name='32bit', parent_part=s_cpu_standard, is_standard=True)
    s_cpu_64bit = M.Part(name='64bit', parent_part=s_cpu_standard, is_standard=True)
    s_cpu_xd_bit = M.Part(name='XD bit', parent_part=s_cpu_standard, is_standard=True)
    s_cpu_smart_cache = M.Part(name='Smart Cache', parent_part=s_cpu_standard, is_standard=True)
    s_ram_standards = M.Part(name='RAM Standards', is_standard=True)
    s_ddr3 = M.Part(name='DDR3', parent_part=s_ram_standards, is_standard=True)
    s_ddr3_1333 = M.Part(name='DDR3-1333', parent_part=s_ddr3, is_standard=True)
    s_cpusocket = M.Part(name='CPU Socket Standard', is_standard=True)
    s_socket_1155 = M.Part(name='Socket 1155', parent_part=s_cpusocket, is_standard=True)
    s_pcie_x16 = M.Part(name='PCIe x16 Socket', is_standard=True)
    s_usb = M.Part(name='USB', is_standard=True)
    s_usb2 = M.Part(name='USB 2.0', parent_part=s_usb, is_standard=True)
    s_usb3 = M.Part(name='USB 3.0', parent_part=s_usb, is_standard=True)
    s_ethernet = M.Part(name='Ethernet (10Mbits)', is_standard=True)
    s_fast_ethernet = M.Part(name='Fast Ethernet (100Mbits)', is_standard=True)
    s_gigabit_ethernet = M.Part(name='Gigabit Ethernet (1000Mbits)', is_standard=True)
    s_sata = M.Part(name='SATA', is_standard=True)
    s_sata10 = M.Part(name='SATA 1.0', parent_part=s_sata, is_standard=True)
    s_sata20 = M.Part(name='SATA 2.0', parent_part=s_sata, is_standard=True)
    s_sata30 = M.Part(name='SATA 3.0', parent_part=s_sata, is_standard=True)
    s_sata31 = M.Part(name='SATA 3.1', parent_part=s_sata, is_standard=True)
    s_sata32 = M.Part(name='SATA 3.2', parent_part=s_sata, is_standard=True)
    s_mem_card = M.Part(name='Memory card', is_standard=True)
    s_mem_card_sd = M.Part(name='SD card', parent_part=s_mem_card, is_standard=True)
    s_mem_card_mmc = M.Part(name='MMC card', parent_part=s_mem_card, is_standard=True)
    s_mem_card_mmcplus = M.Part(name='MMCplus card', parent_part=s_mem_card, is_standard=True)
    s_mem_card_xd = M.Part(name='xD card', parent_part=s_mem_card, is_standard=True)
    s_mem_card_ms = M.Part(name='MS card', parent_part=s_mem_card, is_standard=True)
    s_mem_card_mspro = M.Part(name='MS PRO card', parent_part=s_mem_card, is_standard=True)

    at_name = M.AttrType(name='Name', unit=u_text)
    at_position = M.AttrType(name='Position', unit=u_order, note='The position of the associated Part in relation to other Parts')

    # Socket
    #TODO: at_socket_package = M.AttrType(name='Package', unit=part=p_cpusocket)
    at_year_intro = M.AttrType(name='Year of introduction', unit=u_year)

    at_pin_count = M.AttrType.init(name='Pin count', unit=u_count, parts=[p_cpusocket])
    at_pin_count = M.AttrType.init(name='Pin pitch', unit=u_mm, parts=[p_cpusocket])
    at_bus_speed = M.AttrType.init(name='Bus speed', unit=u_mhz, from_to=True, parts=[p_cpusocket])

    # CPU
    at_frequency = M.AttrType.init(name='Frequency', unit=u_mhz, parts=[p_cpu])
    at_l2cache = M.AttrType.init(name='L2 cache', unit=u_byte, parts=[p_cpu])
    at_front_side_bus = M.AttrType.init(name='Front side bus', unit=u_transfer, parts=[p_cpu])
    at_clock_multiplier = M.AttrType.init(name='Clock multiplier', unit=u_factor, parts=[p_cpu])
    at_voltage_range = M.AttrType.init(name='Voltage range', unit=u_volt, from_to=True, parts=[p_cpu])
    at_tdp = M.AttrType.init(name='Thermal design power', unit=u_watt, parts=[p_cpu])
    at_release_date = M.AttrType.init(name='Release date', unit=u_date, parts=[p_cpu])
    at_release_price = M.AttrType.init(name='Release price', unit=u_dollar, parts=[p_cpu])
    at_part_number = M.AttrType.init(name='Part number', unit=u_text, multi_value=True, parts=[p_cpu])
    at_url = M.AttrType.init(name='URL', unit=u_url, parts=[p_cpu])
    at_number_cores = M.AttrType.init(name='Number of cores', unit=u_count, parts=[p_cpu])

    # PC of BA
    at_modified = M.AttrType.init(name='Modified', unit=u_boolean, parts=[p_computer], note='Was this computer modified after initial delivery?')
    at_vendor = M.AttrType.init(name='Vendor', unit=u_text, parts=[p_computer, p_motherboard, p_casing, p_cpu, p_chipset])
    at_serial = M.AttrType.init(name='Serial number', unit=u_text, parts=[p_computer, p_motherboard])
    at_l1cache = M.AttrType.init(name='L1 cache', unit=u_byte, parts=[p_cpu])
    at_hyperthreading = M.AttrType.init(name='Hyperthreading', unit=u_boolean, parts=[p_cpu])
    at_ram_size = M.AttrType.init(name='Size', unit=u_byte, parts=[p_ram])
    at_casing_size = M.AttrType.init(name='Size', unit=u_text, parts=[p_casing], note='Minitower, miditower, bigtower')
    at_vendor_hex = M.AttrType.init(name='Vendor hex', unit=u_hex, parts=[p_ram])
    at_version = M.AttrType.init(name='Version', unit=u_text, parts=[p_pentium4])

    # PC alt
    at_color = M.AttrType.init(name='Color', unit=u_text, parts=[p_casing])
    at_width = M.AttrType.init(name='Width', unit=u_mm, parts=[p_casing])
    at_length = M.AttrType.init(name='Length', unit=u_mm, parts=[p_casing])
    at_height = M.AttrType.init(name='Height', unit=u_mm, parts=[p_casing])
    at_power = M.AttrType.init(name='Power', unit=u_watt, parts=[p_power_supply], note='electric power (output? input?)')
    at_memory_channels = M.AttrType.init(name='Memory channels', unit=u_count, parts=[p_memory_controller])
    at_cmos_average_half_pitch = M.AttrType(name='Average half-pitch of a memory cell', unit=u_count, note='not yet connected ;-)')
    at_max_power_consumtion = M.AttrType.init(name='Maximal power consumption', unit=u_watt, parts=[p_cpu])
    at_max_ram_capacity = M.AttrType.init(name='Maximal RAM capacity', unit=u_mb, parts=[p_motherboard])
    at_harddrive_size = M.AttrType.init(name='Harddrive size', unit=u_gb, parts=[p_harddrive])
    # TODO: Bauform, GPU-Takt, Prozessorkern (Sandy bridge)
    return locals()


def get_objects_computer_BA(o):
    p_hpd530 = M.Part.init(name='HP d530 CMT(DF368A)', parent_part=o['p_desktop'], attributes={
        o['at_vendor']: 'Hewlett-Packard',
        o['at_serial']: 'CZC4301WB9',
    })

    p_mini_tower = M.Part.init(name='Anonymous Mini Tower', parent_part=o['p_casing'], attributes={
        o['at_vendor']: 'Hewlett-Packard',
        o['at_casing_size']: 'Minitower',
    })

    p_hpmboard = M.Part.init(name='085Ch', parent_part=o['p_motherboard'], attributes={
        o['at_vendor']: 'Hewlett-Packard',
        o['at_serial']: 'CZC4301WB9',
    })

    p_hp_pentium4 = M.Part.init(name='Intel Pentium 4 2.80GHz 15.2.9', parent_part=o['p_pentium4'], attributes={
        o['at_vendor']: 'Intel Corp.',
        o['at_version']: '15.2.9',
        o['at_frequency']: '2800',
    })
    o['s_cpu_32bit'].children.append(p_hp_pentium4)

    system = M.System()
    system.add_part_mapping(p_hpd530, p_mini_tower)
    system.add_part_mapping(p_mini_tower, p_hpmboard)
    system.add_part_mapping(p_hpmboard, p_hp_pentium4)

    obj = locals()
    # Remove argument
    del(obj['o'])

    return obj


def get_objects_computer_alt(o):
    p_m1935 = M.Part.init(name='Acer Aspire M1935', parent_part=o['p_desktop'], attributes={
        o['at_vendor']: 'Acer',
    })

    p_mini_tower = M.Part.init(name='Anonymous Tower', parent_part=o['p_casing'], attributes={
        o['at_width']: '180',
        o['at_length']: '379',
        o['at_height']: '402',
        o['at_color']: 'black',
    })

    p_mem_card_sd = M.Part(name='SD card port', parent_part=o['p_port'])
    p_mem_card_mmc = M.Part(name='MMC card port', parent_part=o['p_port'])
    p_mem_card_mmcplus = M.Part(name='MMCplus card port', parent_part=o['p_port'])
    p_mem_card_xd = M.Part(name='xD card port', parent_part=o['p_port'])
    p_mem_card_ms = M.Part(name='MS card port', parent_part=o['p_port'])
    p_mem_card_mspro = M.Part(name='MS PRO card port', parent_part=o['p_port'])

    p_power_supply = M.Part.init(name='Anonymous Power Source', parent_part=o['p_power_supply'], attributes={
        o['at_power']: '250',
    })

    p_cpu = M.Part.init(name='Intel Pentium Processor G645 (2,9 GHz)', parent_part=o['p_cpu'], attributes={
        o['at_number_cores']: '2',
        o['at_frequency']: '2900',
        o['at_front_side_bus']: '5000',
        o['at_max_power_consumtion']: '65',
    })

    p_mem_contr = M.Part.init(name='Anonymous Memory Controller', parent_part=o['p_memory_controller'], attributes={
        o['at_memory_channels']: '2',
    })

    p_motherboard = M.Part.init(name='Anonymous Motherboard', parent_part=o['p_motherboard'], attributes={
        o['at_max_ram_capacity']: 16384
    })

    p_ram = M.Part.init(name='Anonymous RAM', parent_part=o['p_ddr'], attributes={
        o['at_ram_size']: 2048
    })
    o['s_ddr3'].children.append(o['s_ddr3_1333'])

    p_ramsocket = M.Part(name='RAM Socket', parent_part=o['p_ram_socket'], is_connector=True)
    o['s_ddr3'].children.append(p_ramsocket)

    p_chipset = M.Part.init(name='Intel B75 Express', parent_part=o['p_chipset'], attributes={
        o['at_vendor']: 'Intel',
    })

    p_pci = M.Part(name='Anonymous PCIe x16 Port', parent_part=o['p_pcie_x16_socket'], is_connector=True)
    o['s_pcie_x16'].children.append(p_pci)

    p_usb2_port = M.Part(name='Anonymous USB 2.0 Port', parent_part=o['p_usb2_port'], is_connector=True)
    o['s_usb2'].children.append(p_usb2_port)

    # HELP: Ports may support multiple standards
    p_usb3_port = M.Part(name='Anonymous USB 3.0 Port', parent_part=o['p_usb3_port'], is_connector=True)
    o['s_usb3'].children.append(p_usb3_port)
    o['s_usb2'].children.append(p_usb2_port)

    p_rj45 = M.Part(name='Anonymous RJ-45', parent_part=o['p_rj45'], is_connector=True)
    o['s_gigabit_ethernet'].children.append(p_rj45)
    o['s_fast_ethernet'].children.append(p_rj45)
    o['s_ethernet'].children.append(p_rj45)

    p_harddrive = M.Part.init(name='Anonymous harddrive', parent_part=o['p_harddrive'], attributes={
        o['at_harddrive_size']: 500
    })
    o['s_sata'].children.append(p_harddrive)

    # HELP: A memory card reader can be seperated into a controller being on the
    # motherboard and the card ports being in the casing
    p_card_reader_controller = M.Part(name='Anonymous card reader controller', parent_part=o['p_memorycard_reader'])
    o['s_mem_card_sd'].children.append(p_card_reader_controller)
    o['s_mem_card_mmc'].children.append(p_card_reader_controller)
    o['s_mem_card_mmcplus'].children.append(p_card_reader_controller)
    o['s_mem_card_xd'].children.append(p_card_reader_controller)
    o['s_mem_card_ms'].children.append(p_card_reader_controller)
    o['s_mem_card_mspro'].children.append(p_card_reader_controller)

    p_cpusocket = o['p_cpusocket'] # anonymous
    p_audioport = o['p_audioport'] # anonymous
    p_audiocontr = o['p_audio_controller'] # anonymous
    p_sata = o['p_sata'] # anonymous

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
    system.add_part_mapping(p_cpu, o['s_cpu_sse4'])
    system.add_part_mapping(p_cpu, o['s_cpu_64bit'])
    system.add_part_mapping(p_cpu, o['s_cpu_xd_bit'])
    system.add_part_mapping(p_cpu, o['s_cpu_smart_cache'])

    obj = locals()
    # Remove argument
    del(obj['o'])

    return obj


