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


def create_stream(port):
    renix_info('port({}) create streams'.format(port.Location))
    stream = StreamTemplate(upper=port)
    assert stream.handle

    return stream


def get_capture(port):
    renix_info('port({}) get captures'.format(port.Location))
    capture_cfgs = port.get_relatives('lower', relative_name=CaptureConfig.cls_name())
    if not capture_cfgs or len(capture_cfgs) <= 0:
        raise Exception('No capture config on port: {}'.format(port.handle))
    return capture_cfgs[0]


def wait_buff_full(cache):
    renix_info('waiting for cache({}) full...'.format(cache))
    if cache == EnumCacheCapacity.Cache_32KB or cache == EnumCacheCapacity.Cache_64KB or cache == EnumCacheCapacity.Cache_128KB or cache == EnumCacheCapacity.Cache_256KB:
        time.sleep(10)
    elif cache == EnumCacheCapacity.Cache_512KB or cache == EnumCacheCapacity.Cache_1MB or cache == EnumCacheCapacity.Cache_2MB:
        time.sleep(20)
    elif cache == EnumCacheCapacity.Cache_4MB or cache == EnumCacheCapacity.Cache_8MB:
        time.sleep(30)
    else:
        time.sleep(200)


if __name__ == '__main__':
    renix_info('Capture all mode download test begin')

    # v6004c port
    # port_location = ('//10.1.5.16/1/1', '//10.1.5.16/1/2')

    # v6008c v6008m v6016c port
    # port_location = ('//10.1.5.10/1/5', '//10.1.5.10/1/6')

    # v8004f v8008f port
    port_location = ('//10.1.5.10/2/1', '//10.1.5.10/2/2')

    # v8008M v8008c port
    # port_location = ('//10.1.5.15/1/1', '//10.1.5.15/1/2')

    # v2-10G port
    # port_location = ('//10.1.6.199/2/1', '//10.1.6.199/2/2')

    # v98-100G port
    # port_location = ('//10.1.6.149/2/1', '//10.1.6.149/2/2')

    # x8 port
    # port_location = ('//10.1.5.12/2/1', '//10.1.5.12/2/2')

    # x6 port
    # port_location = ('//10.1.5.12/1/1', '//10.1.5.12/1/2')

    # create ports
    sys_entry = get_sys_entry()
    port1, port2 = create_ports(sys_entry, port_location)

    # create streams
    min_length = 128
    max_length = 512
    stream1 = create_stream(port1)
    stream2 = create_stream(port2)

    # get capture
    cap_cfg1 = get_capture(port1)
    cap_cfg1.BufferFullAction = EnumBufferFullAction.STOP
    cap_cfg2 = get_capture(port2)
    cap_cfg2.BufferFullAction = EnumBufferFullAction.WRAP

    cache_capacity = (EnumCacheCapacity.Cache_32KB, EnumCacheCapacity.Cache_64KB, EnumCacheCapacity.Cache_128KB,
                      EnumCacheCapacity.Cache_256KB, EnumCacheCapacity.Cache_512KB, EnumCacheCapacity.Cache_1MB,
                      EnumCacheCapacity.Cache_2MB, EnumCacheCapacity.Cache_4MB, EnumCacheCapacity.Cache_8MB)

    stream_length_types = (
    EnumFrameLengthType.INCREMENT, EnumFrameLengthType.RANDOM, EnumFrameLengthType.FIXED, EnumFrameLengthType.AUTO)

    for length_type in stream_length_types:
        if length_type == EnumFrameLengthType.INCREMENT or length_type == EnumFrameLengthType.RANDOM:
            stream1.edit(FrameLengthType=length_type, MinLength=min_length, MaxLength=max_length)
            stream2.edit(FrameLengthType=length_type, MinLength=min_length, MaxLength=max_length)
            renix_info(
                'run stream({} packet length from {} to {})...'.format(length_type, min_length, max_length))
        elif length_type == EnumFrameLengthType.FIXED:
            stream1.edit(FrameLengthType=length_type, FixedLength=min_length)
            stream2.edit(FrameLengthType=length_type, FixedLength=min_length)
            renix_info('run stream(fixed packet length is {})...'.format(min_length))
        elif length_type == EnumFrameLengthType.AUTO:
            stream1.edit(FrameLengthType=length_type)
            stream2.edit(FrameLengthType=length_type)
            renix_info('run stream(auto packet length )...')
        else:
            raise Exception('Unknown stream length type: {}'.format(length_type))

        # run stream
        start_all_stream_cmd = StartAllStreamCommand()
        start_all_stream_cmd.execute()
        time.sleep(30)

        hard_ports = port1.get_relatives('HardwareLogical', direction=EnumRelationDirection.SOURCE,
                                         relative_name=HardwarePort.cls_name())
        if len(hard_ports) < 0:
            raise Exception('Port({}) cannot get hard port'.format(port1.Location))
        hard_port1 = hard_ports[0]

        hard_card = hard_port1.get_parent()

        if hard_card.PartNumber and 'V2-100G' in hard_card.PartNumber:
            cache_capacity = (EnumCacheCapacity.Cache_32KB,)

        for cache in cache_capacity:
            renix_info('{} test begin ...'.format(cache))
            cap_cfg1.CacheCapacity = cache
            cap_cfg2.CacheCapacity = cache

            # start capture and stream
            start_all_capture_cmd = StartAllCaptureCommand()
            start_all_capture_cmd.execute()

            wait_buff_full(cache)

            stop_all_capture_cmd = StopAllCaptureCommand()
            stop_all_capture_cmd.execute()

            # download capture
            cap_cfg1.get()
            if cap_cfg1.CapturedPacketCount == 0:
                raise Exception('Capture({}) packet count is 0'.format(cap_cfg1.handle))

            cap_cfg2.get()
            if cap_cfg2.CapturedPacketCount == 0:
                raise Exception('Capture({}) packet count is 0'.format(cap_cfg2.handle))

            pcap_dir = os.path.normpath(os.path.join(os.path.dirname(sys.argv[0]), 'logs'))
            download_capture_cmd1 = DownloadCaptureDataCommand(FileDir=pcap_dir,
                                                               FileName='CaptureAllModeDownloadStop.pcap'.format(
                                                                   cap_cfg1.handle),
                                                               CaptureConfigs=[cap_cfg1.handle])
            download_capture_cmd1.execute()

            download_capture_cmd2 = DownloadCaptureDataCommand(FileDir=pcap_dir,
                                                               FileName='CaptureAllModeDownloadWrap.pcap'.format(
                                                                   cap_cfg2.handle),
                                                               CaptureConfigs=[cap_cfg2.handle])
            download_capture_cmd2.execute()

            # waiting for download finish
            renix_info('Downloading packets...')
            cap_cfg1.set_force_auto_sync(True)
            download_delay = 180
            while download_delay:
                if cap_cfg1.CaptureState == EnumCaptureState.IDLE and cap_cfg1.DownloadedPacketCount != 0:
                    renix_info(
                        'Download packets finish, downloaded count: {}'.format(cap_cfg1.DownloadedPacketCount))
                    break
                else:
                    time.sleep(5)
                    download_delay -= 5
            else:
                raise Exception('{} download timeout in {}'.format(cap_cfg1.handle, cache))

            cap_cfg2.set_force_auto_sync(True)
            download_delay = 180
            while download_delay:
                if cap_cfg2.CaptureState == EnumCaptureState.IDLE and cap_cfg2.DownloadedPacketCount != 0:
                    renix_info(
                        'Download packets finish, downloaded count: {}'.format(cap_cfg2.DownloadedPacketCount))
                    break
                else:
                    time.sleep(5)
                    download_delay -= 5
            else:
                raise Exception('{} download timeout in {}'.format(cap_cfg2.handle, cache))

            if cap_cfg1.DownloadedPacketCount != cap_cfg1.CapturedPacketCount:
                raise Exception('Captured count: {} ,download count: {} in stop mode when cache is {}'.format(
                    cap_cfg1.CapturedPacketCount, cap_cfg1.DownloadedPacketCount, cache))

            if cap_cfg2.DownloadedPacketCount != cap_cfg2.CapturedPacketCount:
                raise Exception('Captured count: {} ,download count: {} in wrap mode when cache is {}'.format(
                    cap_cfg2.CapturedPacketCount, cap_cfg2.DownloadedPacketCount, cache))

            renix_info('{} test success'.format(cache))

        # stop stream
        stop_all_stream_cmd = StopAllStreamCommand()
        stop_all_stream_cmd.execute()

    renix_info('Capture all mode download test success')
