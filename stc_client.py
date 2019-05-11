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
 

    # 对于服务端来说， 只有以" "打头的方法才能被客户端调用，所以要提供给客户端的方法都得加" "  

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

    #创建一个项目    
    ProjectA  = conn.create("project")
    print  ProjectA   

    #在项目ProjextA 下创建一个发送端口 和一个接收端口
    TxPort = conn.create( "port","-under" , ProjectA)
    print TxPort
    RxPort = conn.create( "port","-under" , ProjectA)
    print RxPort
    portReturn = conn.config( TxPort, " -location " , "//" + chassisAddress + '/' + slotPort1)
    print portReturn
    portReturn = conn.config( RxPort , " -location " , "//" + chassisAddress + '/' + slotPort2)
    print portReturn   
    

    
    #配置端口类型，根据实际端口类型选择参数：Ethernet10GigFiber、Ethernet100GigFiber、Ethernet40GigFiber、Ethernet10GigCopper、EthernetCopper等；
    EthernetCopper = [" "," "]
    EthernetCopper[0] = conn.create( "EthernetCopper" ,"-under",TxPort, "-Name" ,"ethernetCopper_1")

    EthernetCopper[1] = conn.create( "EthernetCopper" ,"-under",RxPort, "-Name" ,"ethernetCopper_2")   
    
    # Switch to the loopback mode to capture transmitted packets.
    print "Switch to the loopback mode to capture transmitted packets.   "
    portReturn = conn.config( EthernetCopper[0], "-DataPathMode", "LOCAL_LOOPBACK")
    print portReturn 
    
    #在发送端口下创建StreamBlock(1)
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

    #在StreamBlock(1)中添加EthII头
    StrEthII = conn.create( "ethernet:EthernetII",
                                 "-under",
                                 StreamBlock[0],
                                 "-name",
                                 "eht_1",
                                 "-srcMac",
                                 "11:11:11:11:11:11" ,
                                 "-dstMac" ,
                                 "22:22:22:22:22:22" )

    #添加IPv4头 
    strIPv4 = conn.create( "ipv4:IPv4",
                                "-under",
                                StreamBlock[0],
                                "-name",
                                "Ipv4_1", 
                                "-sourceAddr",
                                "10.10.10.10",
                                "-destAddr",
                                "20.20.20.20")

    #添加TCP头
    strTcp = conn.create( "tcp:Tcp",
                                "-under ",
                                StreamBlock[0],
                                "-name",
                                "tcp1",
                                "-sourcePort",
                                "10",
                                "-destPort ",
                                "20 ")    

    #创建Streamblock2
    StreamBlock[1] = conn.create( "StreamBlock" ,
                                       "-under",
                                       TxPort,
                                       "-FrameLengthMode ",
                                       "FIXED",
                                       "-FixedFrameLength",
                                       "222",
                                       "-name",
                                       "StreamBlock_2")

   #在StreamBlock(1)中添加EthII头
    StrEthII = conn.create( "ethernet:EthernetII",
                                 "-under",
                                 StreamBlock[1],
                                 "-name",
                                 "eht_2",
                                 "-srcMac",
                                 "31:11:11:11:11:11",
                                 "-dstMac",
                                 "42:22:22:22:22:22")
    #添加IPv4头 

    strIPv4 = conn.create( "ipv4:IPv4",
                                "-under",
                                StreamBlock[1] ,
                                "-name" ,
                                "Ipv4_2" ,
                                "-sourceAddr" ,
                                "40.40.40.40" ,
                                "-destAddr" ,
                                "50.50.50.50")

    #添加TCP头

    strTcp = conn.create(  "udp:Udp" ,
                                "-under" ,
                                StreamBlock[1] ,
                                "-name" ,
                                "tcp_2" ,
                                "-sourcePort" ,
                                "40" ,
                                "-destPort" ,
                                "50" )

    #配置StreamBlock(1)的modifier 可以选择 RangeModifer 、RandomModifier 、TableModifier

    #StreamBlock1 源Ip 随机

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

    #StreamBlock2 目的Ip 递增

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
                                
    #在发送端口创建 generator

    generator1 = conn.get( TxPort, "-children-Generator") 

    conn.config(generator1, "-Name", "Generator_1")

    #配置 generator1 ,

    generatorConfig1 = conn.get(generator1, "-children-GeneratorConfig")
    print generatorConfig1
    #-------------------------------配置说明--------------------------------------------
    #SchedulingModes属性，可选参数：PORT_BASED 、RATE_BASED 、PRIORITY_BASED 、MANUAL_BASED
    #DurationMode属性，可选参数：CONTINUOUS 、BURSTS 、SECONDS 等，
    #LoadUnit属性，可选参数：PERCENT_LINE_RATE 、FRAMES_PER_SECOND 、BITS_PER_SECOND 、
    #                  KILOBITS_PER_SECOND 、MEGABITS_PER_SECOND 、INTER_BURST_GAP
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
                      
                      

    #在接收端口创建analyzer   
    analyzer1 = conn.get( RxPort, "-children-Analyzer")
    print analyzer1
    #配置analyzer

    conn.config( analyzer1, "-Name", "Analyzer_1")

    analyzerConfig1 = conn.get( analyzer1 , "-children-AnalyzerConfig")
    print analyzerConfig1

    #-------------------------------配置说明--------------------------------------------
    #TimestampLatchMode 属性 ，可选参数：START_OF_FRAME 、END_OF_FRAME
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

    #配置实时结果获取
    #结果保存在 与脚本相同路径下，结果文件名为 result

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

    #连接机框

    resultReturn = conn.connect(chassisAddress)

    #占用端口

    resultReturn = conn.reserve( "//" + chassisAddress + "/" + slotPort1)

    resultReturn = conn.reserve( "//" + chassisAddress + "/" + slotPort2)

    #配置抓包端口

    captureRx = conn.get(RxPort, "-children-capture")
    print captureRx
    captureTx = conn.get(TxPort, "-children-capture")
    print captureTx

    
    

    #-----------------------------------配置说明-------------------------------------
    #
    #mode 属性，可选参数：REGULAR_MODE，抓所有报文； SIG_MODE：抓有signature的报文。
    #Buffermode 属性， 可选参数：WRAP 当缓冲区写满时，回滚，继续抓包，   STOP_ON_FULL ：当缓冲区写满时，停止
    #srcMode 属性，可选参数： TX_MODE 、 RX_MODE 、 TX_RX_MODE
    #
    #-----------------------------------------------------------------------------

    conn.config(captureRx, "-mode" ,"REGULAR_MODE", "-BufferMode", "WRAP" ,"-srcMode" ,"RX_MODE" )
    conn.config(captureTx, "-mode" ,"REGULAR_MODE", "-BufferMode", "WRAP" ,"-srcMode" ,"TX_RX_MODE" )
    #conn.perform StreamBlockUpdate -streamBlock "$StreamBlock(1)"

    #conn.perform StreamBlockUpdate -streamBlock "$StreamBlock(2)"

    #建立逻辑端口与物理端口的映射

    resultReturn = conn.perform( "setupPortMappings")

    #执行apply
    print "执行apply"
    resultReturn = conn.apply()
    print resultReturn
    #-------------------------------------------------------------------------------
    #                                     配置完成
    #-------------------------------------------------------------------------------

    #开始analyzer
    print "开始analyzer"
    analyzerCurrent = conn.get(RxPort ,"-children-analyzer")

    conn.perform ("analyzerStart" ,"-analyzerList" ,analyzerCurrent)

    #开启抓包
    print "开启抓包"
    conn.perform( "CaptureStart", "-captureProxyId" ,captureRx)
    conn.perform( "CaptureStart", "-captureProxyId" ,captureTx)
    #开始发包
    print "开始发包"
    generatorCurrent = conn.get(TxPort, "-children-generator")

    conn.perform("generatorStart", "-generatorList", generatorCurrent)

    #等待执行结束
    print "等待执行结束"
    conn.sleep( "20")

    # 停止发包

    conn.perform( "generatorStop", "-generatorList" ,generatorCurrent)

    #停止抓包
    conn.perform( "CaptureStop" ,"-captureProxyId" ,captureRx)
    conn.perform( "CaptureStop" ,"-captureProxyId" ,captureTx)

    #保存抓包结果
    print "保存抓包结果"
    conn.perform( "CaptureDataSave", "-captureProxyId", captureRx ,"-FileName" ,"test_stc_rx.pcap" ,"-FileNameFormat" ,"PCAP")
    conn.perform( "CaptureDataSave", "-captureProxyId", captureTx ,"-FileName" ,"test_stc_tx.pcap" ,"-FileNameFormat" ,"PCAP")

    #停止analyzer

    conn.perform( "analyzerStop","-analyzerList" ,analyzerCurrent)

    #释放端口

    conn.release( conn.get(TxPort, "-location"))

    conn.release( conn.get(RxPort, "-location"))

    #与机框断开连接

    conn.disconnect( chassisAddress)

    #删除 project
    print "删除 project"
    conn.delete( ProjectA)

    conn.perform( "ResetConfig" ,"-config", "system1")
        



# 参数主要是host, port  
conn = StcService() 
# test是服务端的那个以" "开头的方法   


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