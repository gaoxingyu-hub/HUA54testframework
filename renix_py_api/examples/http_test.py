from renix_py_api.renix import *
import time
# from module.protocol.l4l7.core import l47_types
# from module.protocol.l4l7.http import http_common

def create_interface(upper, work_layers):
    interface = Interface(upper=upper)
    build_interface_cmd = BuildInterfaceCommand(InterfaceList=[interface.handle], NetworkLayers=work_layers)
    build_interface_cmd.execute()
    interface.get()

    return interface

def set_mac_address(interface, mac):
    for layer in interface.lower:
        if isinstance(layer, EthIILayer):
            layer.Address = mac
            return
    else:
        renix_error('No EthernetII layer in interface: {}'.format(interface.handle))

def set_ipv4_address(interface, address, gateway):
    for layer in interface.lower:
        if isinstance(layer, Ipv4Layer):
            layer.Address = address
            layer.Gateway = gateway
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
        renix_error('No protocol with name: {}'.format(protocl_name))

if __name__ == '__main__':
    initialize()
    sys_entry = get_sys_entry()

    # client
    port1 = Port(upper=sys_entry, Location='//10.1.5.15/2/3')
    bring_port_online_cmd = BringPortsOnlineCommand(PortList = [port1.handle])
    bring_port_online_cmd.execute()

    interface1 = create_interface(port1, ['eth', 'ipv4'])

    set_ipv4_address(interface1, address='192.168.1.1', gateway='192.168.1.2')

    http_client_config = create_protocol(L47ClientConfig.cls_name(), port1, interface1)

    load_profile = L47LoadProfile(upper=sys_entry)
    load_profile.edit(LoadType=EnumLoadType.Users)
    load_profile.edit(MaxOutstandingCon=10)
    load_profile.edit(MaxConcurrentCon=10)

    load_pattern = L47LoadPattern(upper=load_profile)
    load_pattern.edit(LoadValue=5)
    load_pattern.edit(RampTime=5)
    load_pattern.edit(SteadyTime=5)

    command_list = L47CmdList(upper=sys_entry)
    # command_list.edit(ProtoType=l47_types.ProtocolType.HTTP)
    command_list.edit(ProtoType=0)

    http_get_command = HttpGetCommand(upper=command_list)
    http_get_command.DestAddress = '192.168.1.2'
    http_get_command.DestPort = 80
    http_get_command.Page = '/index.html'

    http_client_profile = HttpClientProfile(upper=sys_entry)
    # http_client_profile.edit(HttpVersion=http_common.EnumHttpVersion.HTTP10)
    http_client_profile.edit(HttpVersion=0)
    http_client_profile.set_relatives(relation_name='CommandList', relation_obj=command_list, direction=EnumRelationDirection.TARGET)

    http_client_config.set_relatives(relation_name='LoadProfile', relation_obj=load_profile, direction=EnumRelationDirection.TARGET)
    http_client_config.set_relatives(relation_name='ProtoProfiles', relation_obj=http_client_profile, direction=EnumRelationDirection.TARGET)

    # server
    port2 = Port(upper=sys_entry, Location='//10.1.5.15/2/4')
    bring_port_online_cmd = BringPortsOnlineCommand(PortList = [port2.handle])
    bring_port_online_cmd.execute()

    interface2 = create_interface(port2, ['eth', 'ipv4'])

    set_mac_address(interface2, '00:00:01:00:00:01')
    set_ipv4_address(interface2, address='192.168.1.2', gateway='192.168.1.1')

    http_server_config = create_protocol(L47ServerConfig.cls_name(), port2, interface2)

    http_server_profile = HttpServerProfile()

    http_headers = HttpHeaderProfile()
    http_header = HttpHeader(upper=http_headers)

    http_response = HttpResponse()
    http_response.set_relatives(relation_name='HeaderProfile', relation_obj=http_headers, direction=EnumRelationDirection.TARGET)

    http_payload = HttpPayload()

    http_page_profile = HttpWebPageProfile()

    http_page = HttpWebPage(upper=http_page_profile)
    # http_page.PayloadType = http_server_profile.EnumHttpPayloadType.File
    http_page.PayloadType = 1
    http_page.FileName = 'test_http'
    http_page.set_relatives(relation_name='Response', relation_obj=http_response, direction=EnumRelationDirection.TARGET)
    http_page.set_relatives(relation_name='Payload', relation_obj=http_payload, direction=EnumRelationDirection.TARGET)

    http_server_profile.set_relatives(relation_name='WebPageProfile', relation_obj=http_page_profile, direction=EnumRelationDirection.TARGET)

    http_server_config.set_relatives(relation_name='ProtoProfiles', relation_obj=http_server_profile, direction=EnumRelationDirection.TARGET)

    # start capture
    capture_cfgs = port1.get_relatives('lower', relative_name=CaptureConfig.cls_name())
    if not capture_cfgs or len(capture_cfgs) <= 0:
        raise Exception('No capture config on port: {}'.format(port1.handle))
    capture_cfg1 = capture_cfgs[0]

    # capture all packets
    capture_cfg1.edit(CaptureMode=1)
    start_capture_cmd = StartCaptureCommand(CaptureConfigs=[capture_cfg1.handle])
    start_capture_cmd.execute()

    # start http
    start_all_cmd = StartAllProtocolCommand()
    start_all_cmd.execute()

    time.sleep(40)

    # stop capture
    stop_capture_cmd = StopCaptureCommand(CaptureConfigs=[capture_cfg1.handle])
    stop_capture_cmd.execute()

    time.sleep(5)

    pcap_dir = os.path.normpath(os.path.join(os.path.dirname(sys.argv[0]), 'logs'))
    download_capture_cmd = DownloadCaptureDataCommand(FileDir=pcap_dir, FileName='http_test.pcap', CaptureConfigs=[capture_cfg1.handle])
    download_capture_cmd.execute()

    capture_cfg1.set_force_auto_sync(True)
    while True:
        if capture_cfg1.CaptureState == EnumCaptureState.IDLE:
            break
        else:
            time.sleep(1)

