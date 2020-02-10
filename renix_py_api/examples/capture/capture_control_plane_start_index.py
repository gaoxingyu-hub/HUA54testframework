from renix_py_api.renix import *
import time
initialize(log_level=logging.INFO)


def create_interface(upper, work_layers, address_count):
    interface = Interface(upper=upper, Count=address_count)
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


def get_cap_data(cap_cfg, start_index=1, attemp_count=0):
    cap_cfg.StartingFrameIndex = start_index
    cap_cfg.AttemptDownloadPacketCount = attemp_count
    current_path, current_file_name_ext = os.path.split(os.path.abspath(sys.argv[0]))
    file_dir = os.path.join(current_path, 'logs')
    download_capture_cmd = DownloadCaptureDataCommand(FileDir=file_dir,
                                                      FileName='capture_control_plane_pppoe_ipcp1.pcap',
                                                      CaptureConfigs=[cap_cfg.handle])
    download_capture_cmd.execute()

    wait_download_finish(cap_cfg, 30)
    cap_cfg.set_force_auto_sync(True)

    cap_data = []
    for i in range(cap_cfg.DownloadedPacketCount):
        get_index_cmd = GetCaptureDataByIndexCommand(cap_cfg.handle, i + 1)
        get_index_cmd.execute()
        cap_data.append(get_index_cmd.Data)

    return cap_data


def wait_download_finish(cap_cfg, time_out=10):
    cap_cfg.set_force_auto_sync(True)
    while time_out:
        if cap_cfg.CaptureState == EnumCaptureState.IDLE:
            cap_cfg.set_force_auto_sync(False)
            break
        else:
            time.sleep(2)
            time_out -= 2
    else:
        raise Exception('Waiting for {} download finish timeout'.format(cap_cfg.handle))


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

    pppoe_connection_count = 10
    # create 2 interface with working layer
    work_layers1 = ['eth', 'pppoe', 'ipv4']
    interface1 = create_interface(port1, work_layers1, pppoe_connection_count)
    interface2 = create_interface(port2, work_layers1, pppoe_connection_count)
    client_mac = '00:00:02:02:01:02'
    set_pppoe_mac_address(interface2, client_mac)
    interface2.get()

    # create pppoe server
    pppoe_server = create_protocol(PppoeServerConfig.cls_name(), port1, interface1)
    pppoe_server.edit(Ipv4Count=pppoe_connection_count)
    pppoe_client = create_protocol(PppoeClientConfig.cls_name(), port2, interface2)

    # start capture
    capture_cfgs = port1.get_relatives('lower', relative_name=CaptureConfig.cls_name())
    if not capture_cfgs or len(capture_cfgs) <= 0:
        raise Exception('No capture config on port: {}'.format(port1.handle))
    capture_cfg1 = capture_cfgs[0]

    if capture_cfg1 is None:
        raise Exception('No capture config on port')

    capture_cfg1.edit(CaptureMode=EnumCaptureMode.CTRL_PLANE)

    start_all_capture_cmd = StartAllCaptureCommand()
    start_all_capture_cmd.execute()

    # start pppoe
    start_all_cmd = StartAllProtocolCommand()
    start_all_cmd.execute()

    wait_time = 30
    while wait_time:
        if pppoe_server.IpcpState == EnumPppoeCpState.CONNECTED and pppoe_client.IpcpState == EnumPppoeCpState.CONNECTED:
            renix_debug('pppoe connection established.')
            break
        else:
            wait_time = wait_time - 5
            time.sleep(5)
    else:
        renix_warn('Not all pppoe connection established')

    # download capture
    stop_all_capture_cmd = StopAllCaptureCommand()
    stop_all_capture_cmd.execute()
    capture_cfg1.get()

    if not capture_cfg1.CapturedPacketCount:
        raise Exception('Captured no packets.')

    all_data = get_cap_data(capture_cfg1)

    if len(all_data) != capture_cfg1.CapturedPacketCount:
        raise Exception('Download packet count is not equal to captured packet count when download all packets')

    cap_data1 = get_cap_data(capture_cfg1, capture_cfg1.CapturedPacketCount + 1)
    if len(cap_data1) > 0:
        raise Exception('Download packet count is not 0 when StartingFrameIndex > CapturedPacketCount')

    start_index = capture_cfg1.CapturedPacketCount // 2 + 1
    cap_data2 = get_cap_data(capture_cfg1, start_index)
    target_count = capture_cfg1.CapturedPacketCount - start_index + 1
    if len(cap_data2) != target_count:
        raise Exception(
            'Download packet count is {}, it should be {} when StartingFrame index is {} count is ALL'.format(
                capture_cfg1.DownloadedPacketCount, target_count, start_index))
    else:
        for i in range(target_count):
            if cap_data2[i] != all_data[start_index - 1 + i]:
                raise Exception('Packet not equal when index is {}'.format(start_index + i))

        renix_info('StartingFrameIndex ({}) and count(ALL) test successfully'.format(start_index))

    cap_data3 = get_cap_data(capture_cfg1, start_index, capture_cfg1.CapturedPacketCount + 100)
    if len(cap_data3) != target_count:
        raise Exception('Download packet count is not right if AttemptDownloadPacketCount > CapturedPacketCount')
    else:
        for i in range(target_count):
            if cap_data2[i] != cap_data3[i]:
                raise Exception(
                    'Packet not equal when index is {} when AttemptDownloadPacketCount > CapturedPacketCount'.format(
                        start_index + i))

        renix_info('StartingFrameIndex({}) and count(>CapturedPacketCount) test successfully'.format(start_index))

    renix_info('Capture pdu filter with pppoe ipcp in control plane mode successfully')
