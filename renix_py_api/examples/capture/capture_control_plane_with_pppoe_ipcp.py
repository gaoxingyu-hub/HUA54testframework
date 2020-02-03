from renix_py_api.renix import *
import time
initialize(log_level=logging.INFO)

def create_interface(upper, work_layers):
    interface = Interface(upper=upper, Count=2)
    build_interface_cmd = BuildInterfaceCommand(InterfaceList=[interface.handle], NetworkLayers=work_layers)
    build_interface_cmd.execute()
    interface.get()

    return interface


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


def set_pppoe_mac_address(interface, mac):
    for layer in interface.lower:
        if isinstance(layer, EthIILayer):
            layer.Address = mac
            # layer.edit(Address=mac)
            return
    else:
        renix_error('No EthernetII layer in interface: {}'.format(interface.handle))


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


def set_filter_pppoe_ipcp(pdu_filter):
    pdu_pattern1 = CapturePduPattern(upper=pdu_filter)

    template_string1 = '<XetRoot><XetProtocol name="ethernetII_1" type="Ethernet.ethernetII"></XetProtocol><XetProtocol name="pppoe_1" type="PPPoE.pppoe"><code>00</code></XetProtocol></XetRoot>'
    pdu_pattern1.edit(TemplateString=template_string1)
    pdu_pattern1.get()

    pdu_pattern2 = CapturePduPattern(upper=pdu_filter)
    # template_string2 = '<XetRoot><XetProtocol name="ethernetII_1" type="Ethernet.ethernetII"></XetProtocol><XetProtocol name="pppoe_1" type="PPPoE.pppoe" /><XetProtocol name="custom_1" type="Custom.custom"><patternByte><customOption name="customOption_0"><customPatternByteOption><patternByteOption>8021</patternByteOption></customPatternByteOption></customOption></patternByte></XetProtocol></XetRoot>'
    template_string2 = '<XetRoot><XetProtocol name="ethernetII_1" type="Ethernet.ethernetII"></XetProtocol><XetProtocol name="pppoe_1" type="PPPoE.pppoe" /><XetProtocol name="ppp_1" type="PPP.ppp"><protocol auto="false">8021</protocol></XetProtocol></XetRoot>'
    pdu_pattern2.edit(TemplateString=template_string2)
    pdu_pattern2.get()
    expression = '{} && {}'.format(pdu_pattern1.Name, pdu_pattern2.Name)
    pdu_filter.edit(LogicExpression=expression)
    print(pdu_filter.LogicExpression)


def check_pppoe_ipcp(data):
    pppoe_ipcp = data.strip().split()
    if len(pppoe_ipcp) < 22:
        renix_info('Packet length is shorter than a pppoe ipcp packet.')
        return False

    if pppoe_ipcp[15] != '00' or pppoe_ipcp[20:22] != ['80', '21']:
        renix_info('This is not a pppoe ipcp packet.')
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
    work_layers1 = ['eth', 'pppoe', 'ipv4']
    interface1 = create_interface(port1, work_layers1)
    interface2 = create_interface(port2, work_layers1)
    client_mac = '00:00:02:02:01:02'
    set_pppoe_mac_address(interface2, client_mac)
    interface2.get()

    # create pppoe server
    pppoe_server = create_protocol(PppoeServerConfig.cls_name(), port1, interface1)
    pppoe_server.edit(Ipv4Count=2)
    pppoe_client = create_protocol(PppoeClientConfig.cls_name(), port2, interface2)

    ret = pppoe_client.get('PadiTimeout', 'PadrTimeout')
    if ret:
        print(pppoe_client.PadiTimeout, pppoe_client.PadrTimeout)

    # start capture
    capture_cfgs = port1.get_relatives('lower', relative_name=CaptureConfig.cls_name())
    if not capture_cfgs or len(capture_cfgs) <= 0:
        raise Exception('No capture config on port: {}'.format(port1.handle))
    capture_cfg1 = capture_cfgs[0]

    capture_cfgs = port2.get_relatives('lower', relative_name=CaptureConfig.cls_name())
    if not capture_cfgs or len(capture_cfgs) <= 0:
        raise Exception('No capture config on port: {}'.format(port2.handle))
    capture_cfg2 = capture_cfgs[0]

    if capture_cfg1 is None or capture_cfg2 is None:
        raise Exception('No capture config on port')

    capture_cfg1.edit(CaptureMode=EnumCaptureMode.CTRL_PLANE)
    capture_cfg2.edit(CaptureMode=EnumCaptureMode.CTRL_PLANE)
    capture_cfg2.edit(FilterMode=EnumFilterMode.PDU)
    pdu_filter = CapturePduFilter(upper=capture_cfg2)
    set_filter_pppoe_ipcp(pdu_filter)
    start_all_capture_cmd = StartAllCaptureCommand()
    start_all_capture_cmd.execute()

    # start pppoe
    start_all_cmd = StartAllProtocolCommand()
    start_all_cmd.execute()

    wait_time = 20
    while wait_time:
        if pppoe_server.IpcpState == EnumPppoeCpState.CONNECTED and pppoe_client.IpcpState == EnumPppoeCpState.CONNECTED:
            renix_debug('pppoe connection established.')
            break
        else:
            wait_time = wait_time - 5
            time.sleep(5)

    # download capture
    stop_all_capture_cmd = StopAllCaptureCommand()
    stop_all_capture_cmd.execute()
    capture_cfg1.get()
    capture_cfg2.get()
    current_path, current_file_name_ext = os.path.split(os.path.abspath(sys.argv[0]))
    file_dir = os.path.join(current_path, 'logs')
    if capture_cfg1.CapturedPacketCount:
        download_capture_cmd = DownloadCaptureDataCommand(FileDir=file_dir, FileName='capture_control_plane_pppoe_ipcp1.pcap', CaptureConfigs=[capture_cfg1.handle])
        download_capture_cmd.execute()
    else:
        print('No Packet has been captured on {}'.format(capture_cfg1.handle))

    if capture_cfg2.CapturedPacketCount:
        download_capture_cmd = DownloadCaptureDataCommand(FileDir=file_dir, FileName='capture_control_plane_pppoe_ipcp2.pcap',
                                                          CaptureConfigs=[capture_cfg2.handle])
        download_capture_cmd.execute()
    else:
        print('No Packet has been captured on {}'.format(capture_cfg2.handle))

    capture_cfg1.set_force_auto_sync(True)
    capture_cfg2.set_force_auto_sync(True)
    while True:
        if capture_cfg1.CaptureState == EnumCaptureState.IDLE and capture_cfg2.CaptureState == EnumCaptureState.IDLE:
            break
        else:
            time.sleep(1)

    cap_data1 = []
    pppoe_ipcp_count = 0
    for i in range(capture_cfg1.DownloadedPacketCount):
        get_index_cmd = GetCaptureDataByIndexCommand(capture_cfg1.handle, i + 1)
        get_index_cmd.execute()
        if check_pppoe_ipcp(get_index_cmd.Data):
            pppoe_ipcp_count = pppoe_ipcp_count + 1

    if pppoe_ipcp_count != capture_cfg2.CapturedPacketCount:
        raise Exception('Captured packet count is not equal to pppoe ipcp packet count.')

    for i in range(capture_cfg2.DownloadedPacketCount):
        get_index_cmd = GetCaptureDataByIndexCommand(capture_cfg2.handle, i + 1)
        get_index_cmd.execute()
        if not check_pppoe_ipcp(get_index_cmd.Data):
            raise Exception('This is not a pppoe ipcp packet.')

    renix_info('Capture pdu filter with pppoe ipcp in control plane mode successfully')
