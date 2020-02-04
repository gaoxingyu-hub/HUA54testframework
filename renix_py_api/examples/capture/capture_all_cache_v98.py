from renix_py_api.renix import *
import time
initialize(log_level=logging.INFO)


def wait_port_online(port, times=20):
    port.set_force_auto_sync(True)
    while times:
        if port.Online:
            port.set_force_auto_sync(False)
            return True
        else:
            times -= 1
            time.sleep(1)
    else:
        port.set_force_auto_sync(False)
        return False


def get_capture(port):
    renix_info('port({}) get captures'.format(port.Location))
    capture_cfgs = port.get_relatives('lower', relative_name=CaptureConfig.cls_name())
    if not capture_cfgs or len(capture_cfgs) <= 0:
        raise Exception('No capture config on port: {}'.format(port.Location))
    return capture_cfgs[0]


def get_port_speed(port):
    renix_info('port({}) get speed'.format(port.Location))
    medias = port.get_relatives(relation_name='SelectMedia')
    if not medias or len(medias) <= 0:
        raise Exception('Cannot get media on port: {}'.format(port.Location))

    media = medias[0]
    media.get()
    return media.LineSpeed


def get_v98_theoretical_capture_count(speed, full_action, stream_length=128):
    threshold = 0
    if full_action == EnumBufferFullAction.STOP:
        if speed == EnumLineSpeed.SPEED_100G:
            threshold = 4 * 64
        else:
            threshold = 4 * 16

    return (32 * 1024 - threshold) // stream_length


def change_ports_speed(v98_port1, v98_port2, v98_speed):
    if v98_speed != get_port_speed(v98_port1) or v98_speed != get_port_speed(v98_port2):
        renix_info('Change v98_speed to {}, waiting...'.format(v98_speed))
        config_ports_cmd = ConfigurePortsCommand(PortList=[v98_port1.handle, v98_port2.handle], LineSpeed=v98_speed)
        config_ports_cmd.execute()
        time.sleep(60)  # waiting for change v98_speed finish

        bring_port_online_cmd = BringPortsOnlineCommand(PortList=[v98_port1.handle, v98_port2.handle])
        bring_port_online_cmd.execute()
        if not wait_port_online(v98_port1):
            raise Exception('bring online port({}) failed'.format(v98_port1.handle))
        if not wait_port_online(v98_port2):
            raise Exception('bring online port({}) failed'.format(v98_port2.handle))

        if v98_speed != get_port_speed(v98_port1) or v98_speed != get_port_speed(v98_port2):
            raise Exception('V98 change v98_speed to {} failed.'.format(v98_speed))


def do_cache_test(v98_port1, v98_port2, v98_speed, stream_length=128):
    # get capture
    cap_cfg1 = get_capture(v98_port1)
    cap_cfg1.BufferFullAction = EnumBufferFullAction.STOP
    cap_cfg2 = get_capture(v98_port2)
    cap_cfg2.BufferFullAction = EnumBufferFullAction.WRAP

    renix_info('V98 with speed ({}) running'.format(v98_speed))
    start_all_capture_cmd = StartAllCaptureCommand()
    start_all_capture_cmd.execute()
    start_all_stream_cmd = StartAllStreamCommand()
    start_all_stream_cmd.execute()

    time.sleep(20)
    stop_all_stream_cmd = StopAllStreamCommand()
    stop_all_stream_cmd.execute()
    stop_all_capture_cmd = StopAllCaptureCommand()
    stop_all_capture_cmd.execute()

    cap_cfg1.get()
    cap_cfg2.get()

    cap_cfg1_theoretical_count = get_v98_theoretical_capture_count(v98_speed, cap_cfg1.BufferFullAction, stream_length)
    if cap_cfg1.CapturedPacketCount != cap_cfg1_theoretical_count:
        renix_error(
            'V98 Stop mode in v98_speed({}) capture count is {}, it should be {}'.format(v98_speed,
                                                                                     cap_cfg1.CapturedPacketCount,
                                                                                     cap_cfg1_theoretical_count))

    cap_cfg2_theoretical_count = get_v98_theoretical_capture_count(v98_speed, cap_cfg2.BufferFullAction, stream_length)

    if cap_cfg2.CapturedPacketCount != cap_cfg2_theoretical_count and cap_cfg2.CapturedPacketCount != cap_cfg2_theoretical_count - 1:
        raise Exception('V98 wrap mode in v98_speed({}) capture count is {}, theoretical value is {}'.format(v98_speed,
                                                                                                         cap_cfg2.CapturedPacketCount,
                                                                                                         cap_cfg2_theoretical_count))

    renix_info('V98 with v98_speed({}) capture cache test successfully'.format(v98_speed))


def is_v98_port(port):
    hard_ports = port.get_relatives('HardwareLogical', direction=EnumRelationDirection.SOURCE,
                                     relative_name=HardwarePort.cls_name())
    if len(hard_ports) < 0:
        raise Exception('Port({}) cannot get hard port'.format(port.Location))
    hard_port1 = hard_ports[0]

    hard_card = hard_port1.get_parent()

    if hard_card.PartNumber and 'V2-100G' in hard_card.PartNumber:
        return True

    return False


if __name__ == '__main__':
    renix_info('V98 capture all cache test begin')

    sys_entry = get_sys_entry()
    # create ports
    locations_100G_40G = ('//10.1.6.149/2/1', '//10.1.6.149/2/2')
    port1 = Port(upper=sys_entry, Location=locations_100G_40G[0])
    port2 = Port(upper=sys_entry, Location=locations_100G_40G[1])

    bring_port_online_cmd = BringPortsOnlineCommand(PortList=[port1.handle, port2.handle])
    bring_port_online_cmd.execute()
    if not wait_port_online(port1):
        raise Exception('bring online port({}) failed'.format(port1.handle))
    if not wait_port_online(port2):
        raise Exception('bring online port({}) failed'.format(port2.handle))

    if is_v98_port(port1) and is_v98_port(port2):
        orign_speed = get_port_speed(port1)

        # create streams
        fixed_stream_length = 128
        stream1 = StreamTemplate(upper=port1, FixedLength=fixed_stream_length)
        stream2 = StreamTemplate(upper=port2, FixedLength=fixed_stream_length)

        for speed in (EnumLineSpeed.SPEED_100G, EnumLineSpeed.SPEED_40G):
            change_ports_speed(port1, port2, speed)
            do_cache_test(port1, port2, speed, fixed_stream_length)

        change_ports_speed(port1, port2, EnumLineSpeed.SPEED_25G)
        # create ports
        locations_25G_10G = ('//10.1.6.149/2/1', '//10.1.6.149/2/5')
        port3 = Port(upper=sys_entry, Location=locations_25G_10G[1])
        bring_port_online_cmd = BringPortsOnlineCommand(PortList=[port3.handle])
        bring_port_online_cmd.execute()
        if not wait_port_online(port3):
            raise Exception('bring online port({}) failed'.format(port3.handle))

        stream3 = StreamTemplate(upper=port3, FixedLength=fixed_stream_length)
        for speed in (EnumLineSpeed.SPEED_25G, EnumLineSpeed.SPEED_10G):
            change_ports_speed(port1, port3, speed)
            do_cache_test(port1, port3, speed, fixed_stream_length)

        renix_info('V98 cache test successfully')

        renix_info('Reset V98 speed to {}'.format(orign_speed))
        config_ports_cmd = ConfigurePortsCommand(PortList=[port1.handle], LineSpeed=orign_speed)
        config_ports_cmd.execute()
        time.sleep(60)

        renix_info('V98 capture ALL mode cache test finish')
    else:
        renix_warn('This test case only available for v98 ports, test finish')
