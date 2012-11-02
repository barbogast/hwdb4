from hwdb import model as M


def get_initial_objects():
    u_mm = M.Unit(name='Milimeter')
    u_mhz = M.Unit(name='Megahertz', note='We dont use the minimal unit Hertz because processors are in the mhz area')
    u_date = M.Unit(name='Date')
    u_year = M.Unit(name='Year')
    u_count = M.Unit(name='Count')
    u_byte = M.Unit(name='Byte')
    u_transfer = M.Unit(name='Transfer/Second', note='MT/s (Megatranfer) used with Front side bus')
    u_factor = M.Unit(name='Factor', note='ie cpu clock multiplier')
    u_volt = M.Unit(name='Volt')
    u_watt = M.Unit(name='Watt')
    u_dollar = M.Unit(name='Dollar')
    u_url = M.Unit(name='Url')
    u_text = M.Unit(name='Text')
    u_boolean = M.Unit(name='Boolean')
    u_hex = M.Unit(name='Hex')

    # Parent parts
    p_socket = M.Part(name='CPU-Socket')
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

    # Standards
    s_cpu_standard = M.Part(name='CPU Instruction set', is_standard=True)
    s_cpu_sse4 = M.Part(name='SSE 4.x', parent_part=s_cpu_standard, is_standard=True)
    s_cpu_32bit = M.Part(name='32bit', parent_part=s_cpu_standard, is_standard=True)
    s_cpu_64bit = M.Part(name='64bit', parent_part=s_cpu_standard, is_standard=True)
    s_cpu_xd_bit = M.Part(name='XD bit', parent_part=s_cpu_standard, is_standard=True)
    s_cpu_smart_cache = M.Part(name='Smart Cache', parent_part=s_cpu_standard, is_standard=True)
    s_ram_standards = M.Part(name='RAM Standards', is_standard=True)
    s_ddr3 = M.Part(name='DDR3', parent_part=s_ram_standards, is_standard=True)
    s_socket = M.Part(name='CPU Socket Standard', is_standard=True)
    s_socket_1155 = M.Part(name='Socket 1155', parent_part=s_socket, is_standard=True)


    at_name = M.AttrType(name='Name', unit=u_text)

    # Socket
    #TODO: at_socket_package = M.AttrType(name='Package', unit=part=p_socket)
    at_year_intro = M.AttrType(name='Year of introduction', unit=u_year)

    at_pin_count = M.AttrType.init(name='Pin count', unit=u_count, parts=[p_socket])
    at_pin_count = M.AttrType.init(name='Pin pitch', unit=u_mm, parts=[p_socket])
    at_bus_speed = M.AttrType.init(name='Bus speed', unit=u_mhz, from_to=True, parts=[p_socket])

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

    # PC of BA
    at_modified = M.AttrType.init(name='Modified', unit=u_boolean, parts=[p_computer], note='Was this computer modified after initial delivery?')
    at_vendor = M.AttrType.init(name='Vendor', unit=u_text, parts=[p_computer, p_motherboard, p_casing, p_cpu])
    at_serial = M.AttrType.init(name='Serial number', unit=u_text, parts=[p_computer, p_motherboard])
    at_l1cache = M.AttrType.init(name='L1 cache', unit=u_byte, parts=[p_cpu])
    at_hyperthreading = M.AttrType.init(name='Hyperthreading', unit=u_boolean, parts=[p_cpu])
    at_ram_size = M.AttrType.init(name='Size', unit=u_byte, parts=[p_ram])
    at_casing_size = M.AttrType.init(name='Size', unit=u_text, parts=[p_casing], note='Minitower, miditower, bigtower')
    at_vendor_hex = M.AttrType.init(name='Vendor hex', unit=u_hex, parts=[p_ram])
    at_version = M.AttrType.init(name='Version', unit=u_text, parts=[p_pentium4])
    return locals()


def get_objects_computer_BA(o):
    p_hpd530 = M.Part(name='HP d530 CMT(DF368A)', parent_part=o['p_desktop'])
    a_hpd530_a_hp = M.Attr.init(part=p_hpd530, value='Hewlett-Packard', attr_type=o['at_vendor'])
    a_hpd530_a_serial = M.Attr.init(part=p_hpd530, attr_type=o['at_serial'], value='CZC4301WB9')

    p_mini_tower = M.Part(name='Anonymous Mini Tower', parent_part=o['p_casing'])
    a_mini_tower_vendor = M.Attr.init(part=p_mini_tower, attr_type=o['at_vendor'], value='Hewlett-Packard')
    a_mini_tower_casing_size = M.Attr.init(part=p_mini_tower, attr_type=o['at_casing_size'], value='Minitower')

    p_hpmboard = M.Part(name='085Ch', parent_part=o['p_motherboard'])
    a_hpmboard_a_hp = M.Attr.init(part=p_hpmboard, attr_type=o['at_vendor'], value='Hewlett-Packard')
    a_hpmboard_a_serial = M.Attr.init(part=p_hpmboard, attr_type=o['at_serial'], value='CZC4301WB9')

    p_hp_pentium4 = M.Part(name='Intel Pentium 4 2.80GHz 15.2.9', parent_part=o['p_pentium4'])
    a_hp_pentium4_vendor = M.Attr.init(part=p_hp_pentium4, attr_type=o['at_vendor'], value='Intel Corp.')
    a_hp_pentium4_version = M.Attr.init(part=p_hp_pentium4, attr_type=o['at_version'], value='15.2.9')
    a_hp_pentium4_frequency = M.Attr.init(part=p_hp_pentium4, attr_type=o['at_frequency'], value='2800')
    o['s_cpu_32bit'].children.append(p_hp_pentium4)

    pm_hpd530_minitower = M.PartMap(container_part=p_hpd530, content_part=p_mini_tower)
    pm_minitower_hpmboard = M.PartMap(container_part=p_mini_tower, content_part=p_hpmboard)
    pm_hpmboard_hp_pentium4 = M.PartMap(container_part=p_hpmboard, content_part=p_hp_pentium4)

    obj = locals()
    # Remove argument
    del(obj['o'])

    return obj
