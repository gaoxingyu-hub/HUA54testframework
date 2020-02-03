from renix_py_api.renix import *
import time
initialize(log_level=logging.INFO)


def create_interface(upper, work_layers):
    interface = Interface(upper=upper)
    build_interface_cmd = BuildInterfaceCommand(InterfaceList=[interface.handle], NetworkLayers=work_layers)
    build_interface_cmd.execute()
    interface.get()

    return interface


def set_pppoe_mac_address(interface, mac):
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


if __name__ == '__main__':
    sys_entry = get_sys_entry()
    # create 2 port
    port1 = Port(upper=sys_entry, Location='//10.1.5.11/2/3')
    port2 = Port(upper=sys_entry, Location='//10.1.5.11/2/4')
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
    set_pppoe_mac_address(interface2, '00:00:02:02:01:02')
    interface2.get()

    # create pppoe server
    pppoe_server = create_protocol(PppoeServerConfig.cls_name(), port1, interface1)
    pppoe_client = create_protocol(PppoeClientConfig.cls_name(), port2, interface2)

    ret = pppoe_client.get('PadiTimeout', 'PadrTimeout')
    if ret:
        print(pppoe_client.PadiTimeout, pppoe_client.PadrTimeout)

    # start capture
    capture_cfgs = port1.get_relatives('lower', relative_name=CaptureConfig.cls_name())
    if not capture_cfgs or len(capture_cfgs) <= 0:
        raise Exception('No capture config on port: {}'.format(port1.handle))
    capture_cfg1 = capture_cfgs[0]

    capture_cfg1.edit(CaptureMode=EnumCaptureMode.CTRL_PLANE)
    start_capture_cmd = StartCaptureCommand(CaptureConfigs=[capture_cfg1.handle])
    start_capture_cmd.execute()

    # start pppoe
    start_all_cmd = StartAllProtocolCommand()
    start_all_cmd.execute()

    # subscribe statistic
    result_view1 = ResultView(upper=sys_entry, DataClassName=PppoeClientBlockStatistic.cls_name())
    result_query1 = ResultQuery(upper=result_view1)
    result_view2 = ResultView(upper=sys_entry, DataClassName=PppoeServerBlockStatistic.cls_name())
    result_query2 = ResultQuery(upper=result_view2)

    subcribe_result_cmd = SubscribeResultCommand(ResultViewHandles=[result_view1.handle, result_view2.handle])
    subcribe_result_cmd.execute()

    while True:
        if pppoe_server.IpcpState == EnumPppoeCpState.CONNECTED and pppoe_client.IpcpState == EnumPppoeCpState.CONNECTED:
            renix_debug('pppoe connection established.')
            break
        else:
            time.sleep(1)

    # download capture
    stop_capture_cmd = StopCaptureCommand(CaptureConfigs=[capture_cfg1.handle])
    stop_capture_cmd.execute()
    pcap_dir = os.path.normpath(os.path.join(os.path.dirname(sys.argv[0]), 'logs'))
    download_capture_cmd = DownloadCaptureDataCommand(FileDir=pcap_dir, FileName='pppoe_test.pcap', CaptureConfigs=[capture_cfg1.handle])
    download_capture_cmd.execute()

    capture_cfg1.set_force_auto_sync(True)
    while True:
        if capture_cfg1.CaptureState == EnumCaptureState.IDLE:
            break
        else:
            time.sleep(1)

    statistics = result_query1.get_relatives('lower', PppoeClientBlockStatistic.cls_name())
    if len(statistics) > 0:
        statistic = statistics[0]
        statistic.get()
        print(statistic.IpcpState)
    else:
        renix_error('cannot get pppoe client block statistic.')

    get_index_cmd = GetCaptureDataByIndexCommand(capture_cfg1.handle, 1)
    get_index_cmd.execute()
    print(get_index_cmd.Length)
