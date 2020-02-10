from renix_py_api.renix import *
import time
initialize(log_level=logging.INFO)


def create_interface(upper, work_layers):
    interface = Interface(upper=upper)
    build_interface_cmd = BuildInterfaceCommand(InterfaceList=[interface.handle], NetworkLayers=work_layers)
    build_interface_cmd.execute()
    interface.get()

    return interface


def set_interface(interface, mac, vlan):
    for layer in interface.lower:
        if isinstance(layer, EthIILayer):
            layer.edit(Address=mac)
        elif isinstance(layer, VlanLayer):
            layer.edit(VlanId=vlan)
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
        protocol = protocol_cls(upper=port)
        select_interface_cmd = SelectInterfaceCommand(ProtocolList=[protocol.handle], InterfaceList=[interface.handle])
        select_interface_cmd.execute()
        protocol.get()
        return protocol
    else:
        raise Exception('No protocol with name: {}'.format(protocl_name))


if __name__ == '__main__':
    sys_entry = get_sys_entry()
    # create 2 port
    port1 = Port(upper=sys_entry, Location='//10.1.5.16/1/1')
    port2 = Port(upper=sys_entry, Location='//10.1.5.16/1/2')
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
    work_layers1 = ['eth', 'vlan', 'ipv4']
    interface1 = create_interface(port1, work_layers1)
    interface2 = create_interface(port2, work_layers1)

    set_interface(interface1, '00:00:02:01:01:01', 100)
    set_interface(interface2, '00:00:02:02:01:02', 100)

    ma1 = Dot1agMaConfig(upper=sys_entry, MdName='Ma1')
    dot1ag1 = Dot1agProtocolConfig(upper=port1)
    dot1ag2 = Dot1agProtocolConfig(upper=port2)

    mp1 = Dot1agMpConfig(upper=dot1ag1)
    mp2 = Dot1agMpConfig(upper=dot1ag2)

    if not mp1.set_relatives(relation_name='SelectMa', relation_obj=ma1, direction=EnumRelationDirection.TARGET):
        renix_error('mp1 select ma failed.')

    if not mp2.set_relatives(relation_name='SelectMa', relation_obj=ma1, direction=EnumRelationDirection.TARGET):
        renix_error('mp2 select ma failed.')

    mp1.get_relatives(relation_name='SelectMa', direction=EnumRelationDirection.TARGET)
    mp2.get_relatives(relation_name='SelectMa', direction=EnumRelationDirection.TARGET)

    select_interface_cmd1 = SelectInterfaceCommand(ProtocolList=[dot1ag1.handle], InterfaceList=[interface1.handle])
    select_interface_cmd1.execute()
    select_interface_cmd2 = SelectInterfaceCommand(ProtocolList=[dot1ag2.handle], InterfaceList=[interface2.handle])
    select_interface_cmd2.execute()

    start_all_cmd = StartAllProtocolCommand()
    start_all_cmd.execute()

    # start capture
    capture_cfgs = port1.get_relatives('lower', relative_name=CaptureConfig.cls_name())
    if not capture_cfgs or len(capture_cfgs) <= 0:
        raise Exception('No capture config on port: {}'.format(port1.handle))
    capture_cfg1 = capture_cfgs[0]

    capture_cfg1.edit(CaptureMode=EnumCaptureMode.CTRL_PLANE)
    start_capture_cmd = StartCaptureCommand(CaptureConfigs=[capture_cfg1.handle])
    start_capture_cmd.execute()

    time.sleep(5)

    dot1ag1.set_force_auto_sync(True)
    dot1ag2.set_force_auto_sync(True)
    while True:
        if dot1ag1.State == EnumDot1agState.RUNNING and dot1ag2.State == EnumDot1agState.RUNNING:
            break
        else:
            time.sleep(1)

    start_link_trace_cmd = Dot1agStartLinkTraceCommand(Dot1agConfigs=[dot1ag1.handle, dot1ag2.handle])
    start_link_trace_cmd.execute()

    time.sleep(5)

    # subscribe statistic
    result_view1 = ResultView(upper=sys_entry, DataClassName=Dot1agMpStats.cls_name())
    result_query1 = ResultQuery(upper=result_view1)

    subcribe_result_cmd = SubscribeResultCommand(ResultViewHandles=[result_view1.handle])
    subcribe_result_cmd.execute()

    time.sleep(20)

    # download capture
    stop_capture_cmd = StopCaptureCommand(CaptureConfigs=[capture_cfg1.handle])
    stop_capture_cmd.execute()
    pcap_dir = os.path.normpath(os.path.join(os.path.dirname(sys.argv[0]), 'logs'))
    download_capture_cmd = DownloadCaptureDataCommand(FileDir=pcap_dir, FileName='dot1ag_test.pcap',
                                                      CaptureConfigs=[capture_cfg1.handle])
    download_capture_cmd.execute()

    capture_cfg1.set_force_auto_sync(True)
    while True:
        if capture_cfg1.CaptureState == EnumCaptureState.IDLE:
            break
        else:
            time.sleep(1)

    result_query1.get()
    if len(result_query1.lower) > 0:
        for sta in result_query1.lower:
            sta.get()
    else:
        renix_error('cannot get dot1ag mp statistic.')
