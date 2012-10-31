from hwdb import model as M


def get_initial_objects():
    u_mm = M.Unit(name='Milimeter')
    u_hz = M.Unit(name='Hertz')
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

    p_socket = M.Part(name='CPU-Socket')
    p_cpu = M.Part(name='CPU')
    p_pentium = M.Part(name='Pentium', parent_part=p_cpu)
    p_pentium4 = M.Part(name='Pentium 4', parent_part=p_pentium)
    p_computer = M.Part(name='Computer', note='Part to safe fix compilations of parts, i.e. PCs, Laptops, Servers, ...)')
    p_desktop = M.Part(name='Desktop', parent_part=p_computer)
    p_laptop = M.Part(name='Laptop', parent_part=p_computer)
    p_server = M.Part(name='Server', parent_part=p_computer)

    at_name = M.AttrType(name='Name', unit=u_text)

    # Socket
    #TODO: at_socket_package = M.AttrType(name='Package', unit=part=p_socket)
    at_year_introduction = M.AttrType(name='Year of introduction', unit=u_year, part=p_socket)
    at_pin_count = M.AttrType(name='Pin count', unit=u_count, part=p_socket)
    at_pin_count = M.AttrType(name='Pin pitch', unit=u_mm, part=p_socket)
    at_bus_speed = M.AttrType(name='Bus speed', unit=u_hz, from_to=True, part=p_socket)

    # CPU
    at_frequency = M.AttrType(name='Frequency', unit=u_hz, part=p_cpu)
    at_l2cache = M.AttrType(name='L2 cache', unit=u_byte, part=p_cpu)
    at_front_side_bus = M.AttrType(name='Front side bus', unit=u_transfer, part=p_cpu)
    at_clock_multiplier = M.AttrType(name='Clock multiplier', unit=u_factor, part=p_cpu)
    at_voltage_range = M.AttrType(name='Voltage range', unit=u_volt, from_to=True, part=p_cpu)
    at_tdp = M.AttrType(name='Thermal design power', unit=u_watt, part=p_cpu)
    at_release_date = M.AttrType(name='Release date', unit=u_date, part=p_cpu)
    at_release_price = M.AttrType(name='Release price', unit=u_dollar, part=p_cpu)
    at_part_number = M.AttrType(name='Part number', unit=u_text, multi_value=True, part=p_cpu)
    at_url = M.AttrType(name='URL', unit=u_url, part=p_cpu)

    # PC of BA
    p_casing = M.Part(name='Casing', note='Computer casing')
    p_motherboard = M.Part(name='Motherboard')
    p_ram = M.Part(name='RAM')
    p_ddr = M.Part(name='DDR RAM', parent_part=p_ram)
    p_flash = M.Part(name='Flash memory', parent_part=p_ram)

    at_modified = M.AttrType(name='Modified', unit=u_boolean, part=p_computer, note='Was this computer modified after initial delivery?')
    at_vendor = M.AttrType(name='Vendor', unit=u_text, note='p_computer, p_motherboard')
    at_serial = M.AttrType(name='Serial number', unit=u_text, note='p_computer, p_mainboard')
    at_cpuwidth = M.AttrType(name='Width', unit=u_text, note='cpu, ram, 32 bit oder 64 bit')
    at_l1cache = M.AttrType(name='L1 cache', unit=u_byte, part=p_cpu)
    at_hyperthreading = M.AttrType(name='Hyperthreading', unit=u_boolean, part=p_cpu)
    at_ram_size = M.AttrType(name='Size', unit=u_byte, part=p_ram)
    at_casing_size = M.AttrType(name='Size', unit=u_text, part=p_casing, note='Minitower, miditower, bigtower')
    at_vendor_hex = M.AttrType(name='Vendor hex', unit=u_hex, part=p_ram)
    at_version = M.AttrType(name='Version', unit=u_text, part=p_pentium4)

    p_hpd530 = M.Part(name='HP d530 CMT(DF368A)', parent_part=p_desktop)
    a_hpd530_a_hp = M.Attr(part=p_hpd530, attr_type=at_vendor, value='Hewlett-Packard')
    a_hpd530_a_serial = M.Attr(part=p_hpd530, attr_type=at_serial, value='CZC4301WB9')

    p_mini_tower = M.Part(name='Anonymous Mini Tower', parent_part=p_casing)
    a_mini_tower_vendor = M.Attr(part=p_mini_tower, attr_type=at_vendor, value='Hewlett-Packard')
    a_mini_tower_casing_size = M.Attr(part=p_mini_tower, attr_type=at_casing_size, value='Minitower')

    p_hpmboard = M.Part(name='085Ch', parent_part=p_motherboard)
    a_hpmboard_a_hp = M.Attr(part=p_hpmboard, attr_type=at_vendor, value='Hewlett-Packard')
    a_hpmboard_a_serial = M.Attr(part=p_hpmboard, attr_type=at_serial, value='CZC4301WB9')

    p_hp_pentium4 = M.Part(name='Intel Pentium 4 2.80GHz 15.2.9', parent_part=p_pentium4)
    a_hp_pentium4_vendor = M.Attr(part=p_hp_pentium4, attr_type=at_vendor, value='Intel Corp.')
    a_hp_pentium4_version = M.Attr(part=p_hp_pentium4, attr_type=at_version, value='15.2.9')
    a_hp_pentium4_frequency = M.Attr(part=p_hp_pentium4, attr_type=at_frequency, value='2800000000')
    a_hp_pentium4_width = M.Attr(part=p_hp_pentium4, attr_type=at_cpuwidth, value='32') # TODO: this should be an extra Part (is_standard=True)

    pm_hpd530_minitower = M.PartMapping(container_part=p_hpd530, content_part=p_mini_tower)
    pm_minitower_hpmboard = M.PartMapping(container_part=p_mini_tower, content_part=p_hpmboard)
    pm_hpmboard_hp_pentium4 = M.PartMapping(container_part=p_hpmboard, content_part=p_hp_pentium4)

    return locals().values()

