# coding:utf-8  
  
import rpyc  
import sys  
from Tkinter import Tcl


def build_cmd(*args):

    cmd = ''

    for arg in args:

        cmd = cmd + arg + ' '

    return cmd

 

class StcService(object):



    def __init__(self):
        self.tclsh = Tcl()

        self.tclsh.eval("source {C:\Program Files\Spirent Communications\Spirent TestCenter 3.60\Spirent TestCenter Application\SpirentTestCenter.tcl}")

        print "Initiallized"
 

    # ���ڷ������˵�� ֻ����" "��ͷ�ķ������ܱ��ͻ��˵��ã�����Ҫ�ṩ���ͻ��˵ķ������ü�" "  

    def  test(self, num):  
        return 1+num  

    def  getVersion(self):  
        return "STC 3.60"  
        
    def  init(self, *args):

        cmd =build_cmd('stc::init', *args)

        return self.tclsh.eval(cmd)


    def  connect(self,*args):

        cmd =build_cmd('stc::connect', *args)

        return self.tclsh.eval(cmd)

 

 

    def  disconnect(self,*args):

        cmd =build_cmd('stc::disconnect', *args)

        return self.tclsh.eval(cmd)

 

 

    def  create(self,*args):

        cmd =build_cmd('stc::create', *args)

        return self.tclsh.eval(cmd)

 

 

    def  delete(self,*args):

        cmd =build_cmd('stc::delete', *args)

        return self.tclsh.eval(cmd)

 

 

    def  config(self,*args):

        cmd =build_cmd('stc::config', *args)

        return self.tclsh.eval(cmd)

 

 

    def  get(self, *args):

        cmd = build_cmd('stc::get', *args)

        return self.tclsh.eval(cmd)

 

 

    def  perform(self,*args):

        cmd =build_cmd('stc::perform', *args)

        return self.tclsh.eval(cmd)

 
    def  apply(self,*args):

        cmd =build_cmd('stc::apply', *args)

        return self.tclsh.eval(cmd)
 

    def  reserve(self,*args):

        cmd =build_cmd('stc::reserve', *args)

        return self.tclsh.eval(cmd)

 

    def  release(self,*args):

        cmd =build_cmd('stc::release', *args)

        return self.tclsh.eval(cmd)

 

 

    def  subscribe(self,*args):

        cmd = build_cmd('stc::subscribe',*args)

        return self.tclsh.eval(cmd)

 

    def  unsubscribe(self,*args):

        cmd =build_cmd('stc::unsubscribe', *args)

        return self.tclsh.eval(cmd)

 
    def  sleep(self,*args):

        cmd =build_cmd('stc::sleep', *args)

        return self.tclsh.eval(cmd)        
        
 

    def  help(self, *args):

        cmd = build_cmd('stc::help',*args)

        return self.tclsh.eval(cmd)


    
def test():
    cResult =conn.test(11)  
    print cResult 

    cResult =conn.getVersion()  
    print cResult 

    cResult =conn.help('commands')  
    print cResult  
        
    print "Starting connect to chassis"
#    cResult =conn.connect('172.16.66.12')  
#    print cResult 

def connect():
    print "Starting connect to chassis"
    cResult =conn.connect('172.16.66.12')  
    print cResult 
 
def config():
    chassisAddress = "172.16.66.12"

    slotPort1 = "7/7"

    slotPort2 = "7/8"

    #����һ����Ŀ    
    ProjectA  = conn.create("project")
    print  ProjectA   

    #����ĿProjextA �´���һ�����Ͷ˿� ��һ�����ն˿�
    TxPort = conn.create( "port","-under" , ProjectA)
    print TxPort
    RxPort = conn.create( "port","-under" , ProjectA)
    print RxPort
    portReturn = conn.config( TxPort, " -location " , "//" + chassisAddress + '/' + slotPort1)
    print portReturn
    portReturn = conn.config( RxPort , " -location " , "//" + chassisAddress + '/' + slotPort2)
    print portReturn   
    

    
    #���ö˿����ͣ�����ʵ�ʶ˿�����ѡ�������Ethernet10GigFiber��Ethernet100GigFiber��Ethernet40GigFiber��Ethernet10GigCopper��EthernetCopper�ȣ�
    EthernetCopper = [" "," "]
    EthernetCopper[0] = conn.create( "EthernetCopper" ,"-under",TxPort, "-Name" ,"ethernetCopper_1")

    EthernetCopper[1] = conn.create( "EthernetCopper" ,"-under",RxPort, "-Name" ,"ethernetCopper_2")   
    
    # Switch to the loopback mode to capture transmitted packets.
    print "Switch to the loopback mode to capture transmitted packets.   "
    portReturn = conn.config( EthernetCopper[0], "-DataPathMode", "LOCAL_LOOPBACK")
    print portReturn 
    
    #�ڷ��Ͷ˿��´���StreamBlock(1)
    StreamBlock = [" ", " "]
    StreamBlock[0] = conn.create(  "StreamBlock" ,
                                        "-under" , 
                                        TxPort,
                                        "-FrameLengthMode" , 
                                        "FIXED",
                                        "-FixedFrameLength" ,
                                        "222" ,
                                        "-name",
                                        "StreamBlock_1")

    #��StreamBlock(1)�����EthIIͷ
    StrEthII = conn.create( "ethernet:EthernetII",
                                 "-under",
                                 StreamBlock[0],
                                 "-name",
                                 "eht_1",
                                 "-srcMac",
                                 "11:11:11:11:11:11" ,
                                 "-dstMac" ,
                                 "22:22:22:22:22:22" )

    #���IPv4ͷ 
    strIPv4 = conn.create( "ipv4:IPv4",
                                "-under",
                                StreamBlock[0],
                                "-name",
                                "Ipv4_1", 
                                "-sourceAddr",
                                "10.10.10.10",
                                "-destAddr",
                                "20.20.20.20")

    #���TCPͷ
    strTcp = conn.create( "tcp:Tcp",
                                "-under ",
                                StreamBlock[0],
                                "-name",
                                "tcp1",
                                "-sourcePort",
                                "10",
                                "-destPort ",
                                "20 ")    

    #����Streamblock2
    StreamBlock[1] = conn.create( "StreamBlock" ,
                                       "-under",
                                       TxPort,
                                       "-FrameLengthMode ",
                                       "FIXED",
                                       "-FixedFrameLength",
                                       "222",
                                       "-name",
                                       "StreamBlock_2")

   #��StreamBlock(1)�����EthIIͷ
    StrEthII = conn.create( "ethernet:EthernetII",
                                 "-under",
                                 StreamBlock[1],
                                 "-name",
                                 "eht_2",
                                 "-srcMac",
                                 "31:11:11:11:11:11",
                                 "-dstMac",
                                 "42:22:22:22:22:22")
    #���IPv4ͷ 

    strIPv4 = conn.create( "ipv4:IPv4",
                                "-under",
                                StreamBlock[1] ,
                                "-name" ,
                                "Ipv4_2" ,
                                "-sourceAddr" ,
                                "40.40.40.40" ,
                                "-destAddr" ,
                                "50.50.50.50")

    #���TCPͷ

    strTcp = conn.create(  "udp:Udp" ,
                                "-under" ,
                                StreamBlock[1] ,
                                "-name" ,
                                "tcp_2" ,
                                "-sourcePort" ,
                                "40" ,
                                "-destPort" ,
                                "50" )

    #����StreamBlock(1)��modifier ����ѡ�� RangeModifer ��RandomModifier ��TableModifier

    #StreamBlock1 ԴIp ���

    RandomModifier1 = conn.create(  "RandomModifier",
                                         "-under" ,
                                         StreamBlock[0],
                                         "-Mask" ,
                                         "{0.0.0.255}"  ,
                                         "-RecycleCount" ,
                                         "10" ,
                                         "-EnableStream" ,
                                         "FALSE" ,
                                         "-OffsetReference" ,
                                         "{Ipv4_1.sourceAddr}")

    #StreamBlock2 Ŀ��Ip ����

    RangeModifier2 = conn.create(  "RangeModifier" ,
                                        "-under" ,
                                        StreamBlock[1] ,
                                        "-ModifierMode" ,
                                        "INCR" ,
                                        "-Mask" ,
                                        "{0.0.255.0}" ,
                                        "-StepValue" ,
                                        "{0.0.1.0}" ,
                                        "-RecycleCount" ,
                                        "10" ,
                                        "-RepeatCount" ,
                                        "0",
                                        "-Data" ,
                                        "{0.0.50.0}" ,
                                        "-EnableStream" ,
                                        "FALSE" ,
                                        "-OffsetReference" ,
                                        "{Ipv4_2.destAddr}" ,
                                        "-Active",
                                        "true")
                                
    #�ڷ��Ͷ˿ڴ��� generator

    generator1 = conn.get( TxPort, "-children-Generator") 

    conn.config(generator1, "-Name", "Generator_1")

    #���� generator1 ,

    generatorConfig1 = conn.get(generator1, "-children-GeneratorConfig")
    print generatorConfig1
    #-------------------------------����˵��--------------------------------------------
    #SchedulingModes���ԣ���ѡ������PORT_BASED ��RATE_BASED ��PRIORITY_BASED ��MANUAL_BASED
    #DurationMode���ԣ���ѡ������CONTINUOUS ��BURSTS ��SECONDS �ȣ�
    #LoadUnit���ԣ���ѡ������PERCENT_LINE_RATE ��FRAMES_PER_SECOND ��BITS_PER_SECOND ��
    #                  KILOBITS_PER_SECOND ��MEGABITS_PER_SECOND ��INTER_BURST_GAP
    #---------------------------------------------------------------------------------

    conn.config( generatorConfig1,
                      "-SchedulingMode",
                      "PORT_BASED" ,
                      "-LoadMode",
                      "FIXED",
                      "-FixedLoad",
                      "10",
                      "-LoadUnit",
                      "PERCENT_LINE_RATE")
                      
                      

    #�ڽ��ն˿ڴ���analyzer   
    analyzer1 = conn.get( RxPort, "-children-Analyzer")
    print analyzer1
    #����analyzer

    conn.config( analyzer1, "-Name", "Analyzer_1")

    analyzerConfig1 = conn.get( analyzer1 , "-children-AnalyzerConfig")
    print analyzerConfig1

    #-------------------------------����˵��--------------------------------------------
    #TimestampLatchMode ���� ����ѡ������START_OF_FRAME ��END_OF_FRAME
    #
    #---------------------------------------------------------------------------------

    conn.config(  analyzerConfig1, 
                       "-TimestampLatchMode" ,
                       "END_OF_FRAME" ,
                       "-JumboFrameThreshold" ,
                       "1500" ,
                       "-OversizeFrameThreshold" ,
                       "2000" ,
                       "-UndersizeFrameThreshold" ,
                       "64" ,
                       "-AdvSeqCheckerLateThreshold" ,
                       "1000" ,
                       "-Name" ,
                       "AnalyzerConfig_1")

    #����ʵʱ�����ȡ
    #��������� ��ű���ͬ·���£�����ļ���Ϊ result

    generatorResult = conn.subscribe( "-Parent" ,
                                           ProjectA ,
                                           "-ResultParent" ,
                                           TxPort ,
                                           "-ConfigType",
                                           "Generator",
                                           "-resulttype",
                                           "GeneratorPortResults",
                                           "-filenameprefix",
                                           "result")

    analyzerResult = conn.subscribe( "-Parent",
                                          ProjectA,
                                          "-ResultParent",
                                          RxPort ,
                                          "-ConfigType",
                                          "Analyzer" ,
                                          "-resulttype",
                                          "AnalyzerPortResults",
                                          "-filenameprefix",
                                          "result" )

    #���ӻ���

    resultReturn = conn.connect(chassisAddress)

    #ռ�ö˿�

    resultReturn = conn.reserve( "//" + chassisAddress + "/" + slotPort1)

    resultReturn = conn.reserve( "//" + chassisAddress + "/" + slotPort2)

    #����ץ���˿�

    captureRx = conn.get(RxPort, "-children-capture")
    print captureRx
    captureTx = conn.get(TxPort, "-children-capture")
    print captureTx

    
    

    #-----------------------------------����˵��-------------------------------------
    #
    #mode ���ԣ���ѡ������REGULAR_MODE��ץ���б��ģ� SIG_MODE��ץ��signature�ı��ġ�
    #Buffermode ���ԣ� ��ѡ������WRAP ��������д��ʱ���ع�������ץ����   STOP_ON_FULL ����������д��ʱ��ֹͣ
    #srcMode ���ԣ���ѡ������ TX_MODE �� RX_MODE �� TX_RX_MODE
    #
    #-----------------------------------------------------------------------------

    conn.config(captureRx, "-mode" ,"REGULAR_MODE", "-BufferMode", "WRAP" ,"-srcMode" ,"RX_MODE" )
    conn.config(captureTx, "-mode" ,"REGULAR_MODE", "-BufferMode", "WRAP" ,"-srcMode" ,"TX_RX_MODE" )
    #conn.perform StreamBlockUpdate -streamBlock "$StreamBlock(1)"

    #conn.perform StreamBlockUpdate -streamBlock "$StreamBlock(2)"

    #�����߼��˿�������˿ڵ�ӳ��

    resultReturn = conn.perform( "setupPortMappings")

    #ִ��apply
    print "ִ��apply"
    resultReturn = conn.apply()
    print resultReturn
    #-------------------------------------------------------------------------------
    #                                     �������
    #-------------------------------------------------------------------------------

    #��ʼanalyzer
    print "��ʼanalyzer"
    analyzerCurrent = conn.get(RxPort ,"-children-analyzer")

    conn.perform ("analyzerStart" ,"-analyzerList" ,analyzerCurrent)

    #����ץ��
    print "����ץ��"
    conn.perform( "CaptureStart", "-captureProxyId" ,captureRx)
    conn.perform( "CaptureStart", "-captureProxyId" ,captureTx)
    #��ʼ����
    print "��ʼ����"
    generatorCurrent = conn.get(TxPort, "-children-generator")

    conn.perform("generatorStart", "-generatorList", generatorCurrent)

    #�ȴ�ִ�н���
    print "�ȴ�ִ�н���"
    conn.sleep( "20")

    # ֹͣ����

    conn.perform( "generatorStop", "-generatorList" ,generatorCurrent)

    #ֹͣץ��
    conn.perform( "CaptureStop" ,"-captureProxyId" ,captureRx)
    conn.perform( "CaptureStop" ,"-captureProxyId" ,captureTx)

    #����ץ�����
    print "����ץ�����"
    conn.perform( "CaptureDataSave", "-captureProxyId", captureRx ,"-FileName" ,"test_stc_rx.pcap" ,"-FileNameFormat" ,"PCAP")
    conn.perform( "CaptureDataSave", "-captureProxyId", captureTx ,"-FileName" ,"test_stc_tx.pcap" ,"-FileNameFormat" ,"PCAP")

    #ֹͣanalyzer

    conn.perform( "analyzerStop","-analyzerList" ,analyzerCurrent)

    #�ͷŶ˿�

    conn.release( conn.get(TxPort, "-location"))

    conn.release( conn.get(RxPort, "-location"))

    #�����Ͽ�����

    conn.disconnect( chassisAddress)

    #ɾ�� project
    print "ɾ�� project"
    conn.delete( ProjectA)

    conn.perform( "ResetConfig" ,"-config", "system1")
        



# ������Ҫ��host, port  
conn = StcService() 
# test�Ƿ���˵��Ǹ���" "��ͷ�ķ���   


cResult = conn.config("automationoptions -logTo \"aTemplateLog.txt\" -logLevel DEBUG")  
print cResult

while True:
    cmd = raw_input('cmd: ')
    #print(cmd)
    if cmd == 'test':
        test()
    elif cmd == 'conn':
        connect()
    elif cmd == 'config':
        config()
    elif cmd == 'exit':
        sys.exit(1) 
    
 
 
#print cResult  