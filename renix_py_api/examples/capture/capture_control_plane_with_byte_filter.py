from renix_py_api.renix import *
import time
initialize(log_level=logging.INFO)


def create_interface(upper, work_layers):
    interface = Interface(upper=upper)
    build_interface_cmd = BuildInterfaceCommand(InterfaceList=[interface.handle], NetworkLayers=work_layers)
    build_interface_cmd.execute()
    interface.get()

    return interface


def set_dhcpv4_server_mac_address(interface, mac):
    for layer in interface.lower:
        if isinstance(layer, EthIILayer):
            layer.Address = mac
            # layer.edit(Address=mac)
            return
    else:
        renix_error('No EthernetII layer in interface: {}'.format(interface.handle))


def wait_port_online(port, times=10):
    port.set_force_auto_sync(True)
    while times:
        if port.Online:
            return True
        else:
            times -= 1
            time.sleep(1)
    else:
        return False


def create_protocol(protocl_name, port, interface):
    protocol_cls = ROMManager.get_cls(protocl_name)
    if protocol_cls:
        protocol = protocol_cls(force_auto_sync=True, upper=port)
        select_interface_cmd = SelectInterfaceCommand(ProtocolList=[protocol.handle], InterfaceList=[interface.handle])
        select_interface_cmd.execute()
        protocol.get()
        return protocol
    else:
        raise Exception('No protocol with name: {}'.format(protocl_name))


def check_dhcp_vendor_class_id(cap_data):
    if len(cap_data) < 30:
        renix_error('Capture packet length is too short')
        return False

    vendor_class_id = [int(x, 16) for x in cap_data[26: 30]]
    if vendor_class_id != [0x00, 0x00, 0x00, 0x00]:
        renix_error('Capture packet is not the filter value')
        return False

    return True


if __name__ == '__main__':
    sys_entry = get_sys_entry()
    # create 2 port
    location1 = '//10.1.5.10/2/1'
    location2 = '//10.1.5.10/2/2'
    port1 = Port(upper=sys_entry, Location=location1)
    port2 = Port(upper=sys_entry, Location=location2)
    port_handles = []
    port_handles.append(port1.handle)
    port_handles.append(port2.handle)
    # bring on two ports and wait for online
    bring_port_online_cmd = BringPortsOnlineCommand(PortList=port_handles)
    bring_port_online_cmd.execute()
    if not wait_port_online(port1):
        raise Exception('bring online port({}) failed'.format(port1.handle))
    if not wait_port_online(port2):
        raise Exception('bring online port({}) failed'.format(port2.handle))

    # create 2 interface with working layer
    work_layers1 = ['eth', 'ipv4']
    interface1 = create_interface(port1, work_layers1)
    interface1.Count = 100
    interface2 = create_interface(port2, work_layers1)
    set_dhcpv4_server_mac_address(interface2, '00:00:07:01:01:03')
    interface2.get()

    # create dhcpv4 client and server
    dhcpv4_client = create_protocol(Dhcpv4ClientConfig.cls_name(), port1, interface1)
    dhcpv4_client.VendorClassIdentifier = 'teletest'
    dhcpv4_server = create_protocol(Dhcpv4ServerConfig.cls_name(), port2, interface2)
    dhcp_ip_pool = Dhcpv4AddressPool(upper=dhcpv4_server)

    # set capture byte condition
    capture_cfgs = port2.get_relatives('lower', relative_name=CaptureConfig.cls_name())
    if not capture_cfgs or len(capture_cfgs) <= 0:
        raise Exception('No capture config on port: {}'.format(port2.handle))
    capture_cfg1 = capture_cfgs[0]

    capture_cfg1.FilterMode = EnumFilterMode.BYTE
    capture_cfg1.CacheCapacity = EnumCacheCapacity.Cache_16MB
    capture_cfg1.edit(CaptureMode=EnumCaptureMode.CTRL_PLANE)
    byte_filter = CaptureByteFilter(upper=capture_cfg1)
    data = [0x00, 0x00, 0x00, 0x00]
    mask = [0xff, 0xff, 0xff, 0xff]
    offset = 0
    byte_condition = CaptureByteCondition(upper=byte_filter, Data=data, Mask=mask, Offset=26)
    start_capture_cmd = StartCaptureCommand(CaptureConfigs=[capture_cfg1.handle])
    start_capture_cmd.execute()

    # start pppoe
    start_all_cmd = StartAllProtocolCommand()
    start_all_cmd.execute()

    dhcpv4_client.set_force_auto_sync(True)
    delay_time = 10
    while delay_time:
        if dhcpv4_client.State == EnumDhcpv4ClientState.BOUND:
            renix_debug('dhcpv4 connection established.')
            break
        else:
            time.sleep(1)
            delay_time = delay_time - 1
    else:
        renix_warn('Dhcpv4 client bind time out')

    # download capture
    stop_capture_cmd = StopCaptureCommand(CaptureConfigs=[capture_cfg1.handle])
    stop_capture_cmd.execute()
    pcap_dir = os.path.normpath(os.path.join(os.path.dirname(sys.argv[0]), 'logs'))
    download_capture_cmd = DownloadCaptureDataCommand(FileDir=pcap_dir, FileName='CaptureControlPlaneWithByteCondtion.pcap', CaptureConfigs=[capture_cfg1.handle])
    download_capture_cmd.execute()

    capture_cfg1.set_force_auto_sync(True)
    while True:
        if capture_cfg1.CaptureState == EnumCaptureState.IDLE:
            break
        else:
            time.sleep(1)

    renix_info('Capture packet count is : {}'.format(capture_cfg1.DownloadedPacketCount))
    for i in range(capture_cfg1.DownloadedPacketCount):
        get_index_cmd = GetCaptureDataByIndexCommand(capture_cfg1.handle, i + 1)
        get_index_cmd.execute()
        cap_data = get_index_cmd.Data.strip().split()
        if not check_dhcp_vendor_class_id(cap_data):
            raise Exception('Capture Byte Filter failed in Control mode')

    renix_info('Capture byte filter test successfully')
