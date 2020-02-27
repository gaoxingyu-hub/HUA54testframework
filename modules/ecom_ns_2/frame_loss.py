from renix_py_api.renix import *
import logging, time
initialize(log_level=logging.INFO)
from renix_py_api.api_gen import *
from renix_py_api.core import EnumRelationDirection
from renix_py_api.rom_manager import *

sys_entry = get_sys_entry()

def add_statistic(stream, rxPort, mode=EnumRxPortSelectMode.ONE_TO_ONE):
    streamHandleList = stream.handle
    rxPortHandleList = rxPort.handle
    select_rxPort_cmd = SelectRxPortCommand(StreamList=streamHandleList, RxPortList=rxPortHandleList, Mode=mode)
    select_rxPort_cmd.execute()
    stream.get_relatives('RxPort', EnumRelationDirection.TARGET, 'Port')
    stream.get()

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

def create_stream(port, packet_length=128):
    renix_info('port({}) create streams'.format(port.Location))
    stream = StreamTemplate(upper=port)
    assert stream.handle
    create_stream_header_cmd = CreateHeaderCommand(stream.handle, ['Ethernet.ethernetII', 'IPv4.ipv4', 'UDP.udp'])
    create_stream_header_cmd.execute()
    if len(create_stream_header_cmd.HeaderNames) != 3:
        raise Exception('{} create EthernetII and IPv4 header failed'.format(stream.handle))
    stream.FixedLength = packet_length
    stream.get()
    return stream

def edit_stream(stream, parameter):
    update_header_cmd = UpdateHeaderCommand(Stream=stream.handle, Parameter=parameter)
    update_header_cmd.execute()
    stream.get()

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

errInfo = []
verdict = 'pass'
# reserve port
port_location = ('//192.168.1.23/2/1', '//192.168.1.23/2/2')
port1, port2 = create_ports(sys_entry, port_location)
stream_port_cfg = port1.get_children(StreamPortConfig.cls_name())[0]
inter_frame_gap_cfg = stream_port_cfg.get_children(InterFrameGapProfile.cls_name())[0]
inter_frame_gap_cfg.edit(Rate=100)

# create stream
stream1_2 = create_stream(port1)
stream2_1 = create_stream(port2)


edit_stream(stream1_2, 'ethernetII_1.sourceMacAdd=00:00:00:11:11:11 ethernetII_1.destMacAdd=00:00:00:22:22:22')
edit_stream(stream2_1, 'ethernetII_1.sourceMacAdd=00:00:00:22:22:22 ethernetII_1.destMacAdd=00:00:00:11:11:11')


# add rx port for specified stream
add_statistic(stream1_2, port2)
add_statistic(stream2_1, port1)


# create result view
resultView_create = CreateResultViewCommand(DataClassName=StreamBlockStats.cls_name())
resultView_create.execute()
resultView_stream = ROMManager.get_object(resultView_create.ResultViewHandle)
subscribe_result_cmd = SubscribeResultCommand(ResultViewHandles=resultView_stream.handle)
subscribe_result_cmd.execute()
sys_entry.get()
page_result_view = sys_entry.get_children(PageResultView.cls_name())[0]

# Pre-Start stream
startallstream = StartAllStreamCommand()
startallstream.execute()
time.sleep(2)
stopallstream = StopAllStreamCommand()
stopallstream.execute()

# Clear statistic
result_clear_cmd = ClearResultCommand(ResultViewHandles=page_result_view.handle)
result_clear_cmd.execute()

# Start stream
startallstream = StartAllStreamCommand()
startallstream.execute()
time.sleep(10)
stopallstream = StopAllStreamCommand()
stopallstream.execute()

# get stream statistic
time.sleep(3)
result_query = page_result_view.get_children()[0]
stream1_2_stats = result_query.get_children('StreamBlockStats')[0]
stream2_1_stats = result_query.get_children('StreamBlockStats')[1]


# check rx equal to tx
if stream1_2_stats.TxStreamFrames != stream1_2_stats.RxStreamFrames:
    verdict = 'fail'
    errInfo.append('[Test Fail] Stream1_2 tx packet ({}) is NOT equal to rx packets ({})'.format(stream1_2_stats.TxStreamFrames, stream1_2_stats.RxStreamFrames))
else:
    print('[Test Pass] Stream1_2 tx packet ({}) is equal to rx packets ({})'.format(stream1_2_stats.TxStreamFrames, stream1_2_stats.RxStreamFrames))

if stream2_1_stats.TxStreamFrames != stream2_1_stats.RxStreamFrames:
    verdict = 'fail'
    errInfo.append('[Test Fail] stream2_1 tx packet ({}) is NOT equal to rx packets ({})'.format(stream2_1_stats.TxStreamFrames, stream2_1_stats.RxStreamFrames))
else:
    print('[Test Pass] stream2_1 tx packet ({}) is equal to rx packets ({})'.format(stream2_1_stats.TxStreamFrames, stream2_1_stats.RxStreamFrames))


# check no loss packet
if stream1_2_stats.RxLossStreamFrames != 0:
    verdict = 'fail'
    errInfo.append('[Test Fail] Stream1_2 realtime loss packet ({}) is NOT equal to 0'.format(stream1_2_stats.RxLossStreamFrames))
else:
    print('[Test Pass] Stream1_2 realtime loss packet ({}) is equal to 0'.format(stream1_2_stats.RxLossStreamFrames))
	
if stream2_1_stats.RxLossStreamFrames != 0:
    verdict = 'fail'
    errInfo.append('[Test Fail] stream2_1 realtime loss packet ({}) is NOT equal to 0'.format(stream2_1_stats.RxLossStreamFrames))
else:
    print('[Test Pass] stream2_1 realtime loss packet ({}) is equal to 0'.format(stream2_1_stats.RxLossStreamFrames))


# check no sequence error
if stream1_2_stats.RxSeqErr != 0:
    verdict = 'fail'
    errInfo.append('[Test Fail] Stream1_2 sequence error packet ({}) is NOT equal to 0'.format(stream1_2_stats.RxSeqErr))
else:
    print('[Test Pass] Stream1_2 sequence error packet ({}) is equal to 0'.format(stream1_2_stats.RxSeqErr))

if stream2_1_stats.RxSeqErr != 0:
    verdict = 'fail'
    errInfo.append('[Test Fail] stream2_1 sequence error packet ({}) is NOT equal to 0'.format(stream2_1_stats.RxSeqErr))
else:
    print('[Test Pass] stream2_1 sequence error packet ({}) is equal to 0'.format(stream2_1_stats.RxSeqErr))



print('verdict:', verdict)
print('errInfo:')
if verdict == 'fail':
    for i in errInfo:
        print(i)