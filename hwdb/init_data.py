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
    p_hpd530 = M.Part(name='HP d530 CMT(DF368A)', parent_part=p_desktop)
    p_casing = M.Part(name='Casing', note='Computer casing')
    p_casing = M.Part(name='Motherboard')
    p_ram = M.Part(name='RAM')
    p_ddr = M.Part(name='DDR RAM', parent_part=p_ram)
    p_flash = M.Part(name='Flash memory', parent_part=p_ram)

    at_modified = M.AttrType(name='Modified', unit=u_boolean, part=p_computer, note='Was this computer modified after initial delivery?')
    at_vendor = M.AttrType(name='Vendor', unit=u_text, note='p_computer, p_motherboard')
    at_serial = M.AttrType(name='Serial', unit=u_text, note='p_computer, p_mainboard')
    at_width = M.AttrType(name='Width', unit=u_text, note='cpu, ram, 32 bit oder 64 bit')
    at_l1cache = M.AttrType(name='L1 cache', unit=u_byte, part=p_cpu)
    at_hyperthreading = M.AttrType(name='Hyperthreading', unit=u_boolean, part=p_cpu)
    at_size = M.AttrType(name='Size', unit=u_byte, part=p_ram)
    at_vendor_hex = M.AttrType(name='Vendor hex', unit=u_hex, part=p_ram)


    return locals().values()

