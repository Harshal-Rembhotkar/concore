import concore
import concore2
from osparc_control import PairedTransmitter
print("funcall 0mq")

concore.delay = 0.07
concore2.delay = 0.07
concore2.inpath = concore.inpath
concore2.outpath = concore.outpath
concore2.simtime = 0
concore.default_maxtime(100)
init_simtime_u = "[0.0, 0.0, 0.0]"
init_simtime_ym = "[0.0, 0.0, 0.0]"

u = concore.initval(init_simtime_u)
ym = concore2.initval(init_simtime_ym)
while(concore2.simtime<concore.maxtime):
    while concore.unchanged():
        u = concore.read(concore.iport['U'],"u",init_simtime_u)
    print(u)
    #concore.write(concore.oport['U1'],"u",u)
    #old2 = concore2.simtime
    #while concore2.unchanged() or concore2.simtime <= old2:
    #    ym = concore2.read(concore.iport['Y1'],"ym",init_simtime_ym)
    paired_transmitter = PairedTransmitter(
        remote_host="localhost", exposed_commands=[],  
        #remote_host="193.136.132.10", exposed_commands=[],  
        remote_port=2345, listen_port=2346,)
    paired_transmitter.start_background_sync() 
    ym = paired_transmitter.request_with_immediate_reply(
        "fun", timeout=10.0, params={"u": [concore.simtime]+u})
    concore2.simtime = ym[0]
    ym = ym[1:]
    paired_transmitter.stop_background_sync()
    #print(ym)
    concore2.write(concore.oport['Y'],"ym",ym)
    print("funcall 0mq u="+str(u)+" ym="+str(ym)+" time="+str(concore2.simtime))
print("retry="+str(concore.retrycount))
