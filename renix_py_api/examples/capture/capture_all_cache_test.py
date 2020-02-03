from renix_py_api.renix import *
import time
initialize(log_level=logging.INFO)


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


def create_ports(sys_entry, locations):
    renix_info('Create ports with locations: '.format(locations))
    port1 = Port(upper=sys_entry, Location=locations[0])
    port2 = Port(upper=sys_entry, Location=locations[1])

    assert port1.handle
    assert port2.handle

    bring_port_online_cmd = BringPortsOnlineCommand(PortList=[port1.handle, port2.handle])
    bring_port_online_cmd.execute()
    if not wait_port_online(port1):
        raise Exception('bring online port({}) failed'.format(port1.handle))
    if not wait_port_online(port2):
        raise Exception('bring online port({}) failed'.format(port2.handle))

    return port1, port2


def create_streams(port1, port2, packet_length=128):
    renix_info('port({}) port({}) create streams'.format(port1.Location, port2.Location))
    stream1 = StreamTemplate(upper=port1)
    stream2 = StreamTemplate(upper=port2)
    assert stream1.handle
    assert stream2.handle

    create_stream_header_cmd1 = CreateHeaderCommand(stream1.handle, ['Ethernet.ethernetII', 'IPv4.ipv4'])
    create_stream_header_cmd1.execute()
    if len(create_stream_header_cmd1.HeaderNames) != 2:
        raise Exception('{} create EthernetII and IPv4 header failed'.format(stream1.handle))
    create_stream_header_cmd2 = CreateHeaderCommand(stream2.handle, ['Ethernet.ethernetII', 'IPv4.ipv4'])
    create_stream_header_cmd2.execute()
    if len(create_stream_header_cmd2.HeaderNames) != 2:
        raise Exception('{} create EthernetII and IPv4 header failed'.format(stream2.handle))

    stream1.FixedLength = packet_length
    stream2.FixedLength = packet_length

    return stream1, stream2


def get_captures(port1, port2):
    renix_info('port({}) port({}) get captures'.format(port1.Location, port2.Location))
    capture_cfgs = port1.get_relatives('lower', relative_name=CaptureConfig.cls_name())
    if not capture_cfgs or len(capture_cfgs) <= 0:
        raise Exception('No capture config on port: {}'.format(port1.handle))
    capture_cfg1 = capture_cfgs[0]

    capture_cfgs = port2.get_relatives('lower', relative_name=CaptureConfig.cls_name())
    if not capture_cfgs or len(capture_cfgs) <= 0:
        raise Exception('No capture config on port: {}'.format(port2.handle))
    capture_cfg2 = capture_cfgs[0]

    return capture_cfg1, capture_cfg2


def wait_buff_full(cache):
    print('waiting for cache({}) full...'.format(cache))
    if cache == EnumCacheCapacity.Cache_32KB or cache == EnumCacheCapacity.Cache_64KB or cache == EnumCacheCapacity.Cache_128KB or cache == EnumCacheCapacity.Cache_256KB:
        time.sleep(10)
    elif cache == EnumCacheCapacity.Cache_512KB or cache == EnumCacheCapacity.Cache_1MB or cache == EnumCacheCapacity.Cache_2MB:
        time.sleep(20)
    elif cache == EnumCacheCapacity.Cache_4MB or cache == EnumCacheCapacity.Cache_8MB:
        time.sleep(30)
    elif cache == EnumCacheCapacity.Cache_16MB or cache == EnumCacheCapacity.Cache_32MB:
        time.sleep(40)
    elif cache == EnumCacheCapacity.Cache_64MB:
        time.sleep(60)
    elif cache == EnumCacheCapacity.Cache_128MB or cache == EnumCacheCapacity.Cache_256MB:
        time.sleep(80)
    elif cache == EnumCacheCapacity.Cache_512MB:
        time.sleep(100)
    elif cache == EnumCacheCapacity.Cache_1GB:
        time.sleep(200)


def get_v6_v8_v82_x6_x8_theoretical_capture_count(cache_size, packet_length=128):
    cache_str = str(cache_size)
    cache_str = cache_str.replace(EnumCacheCapacity.__name__, '')  # remove enum class name
    cache_str = cache_str.replace('.Cache_', '')  # remove '.Cache_'
    cache = 0
    if 'KB' in cache_str:
        cache = int(cache_str.replace('KB', '')) * 1024
    elif 'MB' in cache_str:
        cache = int(cache_str.replace('MB', '')) * 1024 * 1024
    elif 'GB' in cache_str:
        cache = int(cache_str.replace('GB', '')) * 1024 * 1024 * 1024
    else:
        raise Exception('Unknown cache size: {}'.format(cache_size))

    if packet_length % 8 != 0:
        packet_length = (packet_length // 8 + 1) * 8

    return cache * 7 // 8 // (packet_length + 8)


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
    all_cache_capacities = (EnumCacheCapacity.Cache_32KB, EnumCacheCapacity.Cache_64KB, EnumCacheCapacity.Cache_128KB,
                            EnumCacheCapacity.Cache_256KB, EnumCacheCapacity.Cache_512KB, EnumCacheCapacity.Cache_1MB,
                            EnumCacheCapacity.Cache_2MB, EnumCacheCapacity.Cache_4MB, EnumCacheCapacity.Cache_8MB,
                            EnumCacheCapacity.Cache_16MB, EnumCacheCapacity.Cache_32MB, EnumCacheCapacity.Cache_64MB,
                            EnumCacheCapacity.Cache_128MB, EnumCacheCapacity.Cache_256MB, EnumCacheCapacity.Cache_512MB,
                            EnumCacheCapacity.Cache_1GB)

    # v6004c port
    # port_location = ('//10.1.5.16/1/1', '//10.1.5.16/1/2')
    # cache_capacity = all_cache_capacities

    # v6008c v6008m v6016c port
    # port_location = ('//10.1.6.149/1/5', '//10.1.6.149/1/6')
    # cache_capacity = all_cache_capacities[:-1]

    # v8004f v8008f port
    port_location = ('//10.1.5.10/2/1', '//10.1.5.10/2/2')
    cache_capacity = all_cache_capacities

    # v8008M v8008c port
    # port_location = ('//10.1.5.15/1/1', '//10.1.5.15/1/2')
    # cache_capacity = all_cache_capacities

    # v2-10G port
    # port_location = ('//10.1.6.199/2/1', '//10.1.6.199/2/2')
    # cache_capacity = all_cache_capacities

    # x8 port
    # port_location = ('//10.1.5.12/2/1', '//10.1.5.12/2/2')
    # cache_capacity = all_cache_capacities

    # # x6 port
    # port_location = ('//10.1.5.12/1/1', '//10.1.5.12/1/2')
    # cache_capacity = all_cache_capacities

    # create ports
    sys_entry = get_sys_entry()
    port1, port2 = create_ports(sys_entry, port_location)

    if is_v98_port(port1) or is_v98_port(port2):
        renix_warn('This test is not available for v98 ports, test finish')
    else:
        # create streams
        packet_length = 128
        stream1, stream2 = create_streams(port1, port2, packet_length)

        start_all_stream_cmd = StartAllStreamCommand()
        start_all_stream_cmd.execute()

        # get capture
        cap_cfg1, cap_cfg2 = get_captures(port1, port2)

        all_buff_full_action = (EnumBufferFullAction.STOP, EnumBufferFullAction.WRAP)
        for action in all_buff_full_action:
            renix_info('Set capture buffer full action to : {}'.format(action))
            cap_cfg1.BufferFullAction = action
            cap_cfg2.BufferFullAction = action
            for cache in cache_capacity:
                renix_info('Set capture cache to: {}'.format(cache))
                print('Cache : {}, action: {} test begin.'.format(cache, action))
                cap_cfg1.CacheCapacity = cache
                cap_cfg2.CacheCapacity = cache

                start_all_capture_cmd = StartAllCaptureCommand()
                start_all_capture_cmd.execute()
                wait_buff_full(cache)

                stop_all_capture_cmd = StopAllCaptureCommand()
                stop_all_capture_cmd.execute()
                cap_cfg1.get()
                cap_cfg2.get()

                theoretical_capture_count = get_v6_v8_v82_x6_x8_theoretical_capture_count(cache, packet_length)
                if action == EnumBufferFullAction.STOP:
                    if cap_cfg1.BufferFull != EnumBuffFullState.FULL or cap_cfg2.BufferFull != EnumBuffFullState.FULL:
                        raise Exception('Capture buffer full state is not full with cache({}) in {}'.format(cache, action))
                    if cap_cfg1.CapturedPacketCount != theoretical_capture_count:
                        raise Exception(
                            'Capture in port({}) packet count is {}, it should be {} with cache({}) in {}'.format(
                                port1.Location, cap_cfg1.CapturedPacketCount, theoretical_capture_count, cache, action))
                    if cap_cfg2.CapturedPacketCount != theoretical_capture_count:
                        raise Exception(
                            'Capture in port({}) packet count is {}, it should be {} with cache({}) in {}'.format(
                                port2.Location, cap_cfg2.CapturedPacketCount, theoretical_capture_count, cache, action))
                else:
                    if cap_cfg1.CapturedPacketCount != theoretical_capture_count and cap_cfg1.CapturedPacketCount != theoretical_capture_count - 1:
                        raise Exception(
                            'Capture in port({}) packet count is {}, it should be {} or {} with cache({}) in {}'.format(
                                port1.Location, cap_cfg1.CapturedPacketCount, theoretical_capture_count,
                                theoretical_capture_count - 1, cache, action))
                    if cap_cfg2.CapturedPacketCount != theoretical_capture_count and cap_cfg2.CapturedPacketCount != theoretical_capture_count - 1:
                        raise Exception(
                            'Capture in port({}) packet count is {}, it should be {} or {} with cache({}) in {}'.format(
                                port2.Location, cap_cfg2.CapturedPacketCount, theoretical_capture_count,
                                theoretical_capture_count - 1, cache, action))

                renix_info('Capture ALL mode with cache({}) action({}) success'.format(cache, action))
                print('Cache : {}, action: {} test finish.'.format(cache, action))

        stop_all_stream_cmd = StopAllStreamCommand([stream1.handle, stream2.handle])
        stop_all_stream_cmd.execute()
        renix_info('Capture Cache Capacity in ALL Mode test success')
    print('Capture Cache Capacity in ALL Mode test finish!')
