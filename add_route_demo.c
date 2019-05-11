/*参考ppp-2.4.4的代码写了一个简单的。
用法是addroute interface Destination gateway。
其中interface是网卡，Destination是网段(就是route -n看到的第一个参数，0.0.0.0表示要添加默认的路由)，
gateway当然是网关地址了。比如：./addroute eth0 0.0.0.0 192.168.1.1
***********addroute.c*****************/
 
#include "addroute.h"
 
/****************
 raphia_wu 2007.10.26
 function:add a route for one interface
 argv[1]:interface
 argv[2]:destination
 argv[3]:gateway
 ****************/
 int
 main (int argc, char *argv[])
 {
     static int sock_fd = -1;        /* socket for doing interface ioctls */
     struct rtentry rt;
     FILE *db_fd = (FILE *) 0;
     char ifname[32];
     u_int32_t dstaddr, gateway;

     if (argc != 4){
       printf("usage:addroute interface dstaddr gw\n");
         return -1;
     }
     
    strcpy(ifname, argv[1]);
     dstaddr = inet_addr(argv[2]);
     gateway = inet_addr(argv[3]);
 
    /* Get an internet socket for doing socket ioctls. */
     sock_fd = socket(AF_INET, SOCK_DGRAM, 0);
     
    /*open for debug*/
     db_fd = fopen("/tmp/addrt_db.txt","a+");
     fprintf(db_fd, "ifname=%s ouraddr=%x gateway=%x\n", ifname, dstaddr, gateway);
     
    memset (&rt, 0, sizeof (rt));
     /*set Destination addr*/
     SET_SA_FAMILY (rt.rt_dst, AF_INET);
     SIN_ADDR(rt.rt_dst) = dstaddr;
    
     /*set gw addr*/
     SET_SA_FAMILY (rt.rt_gateway, AF_INET);
     SIN_ADDR(rt.rt_gateway) = gateway;
     fprintf(db_fd,"mygateway=%x\n", SIN_ADDR(rt.rt_gateway));
        
    /*set genmask addr*/
     SET_SA_FAMILY (rt.rt_genmask, AF_INET); 
    SIN_ADDR(rt.rt_genmask) = 0L;
    
     rt.rt_dev = ifname;
 
    rt.rt_flags = RTF_GATEWAY;
 
    if (ioctl(sock_fd, SIOCADDRT, &rt) < 0) {
       fprintf(db_fd,"route add err num=%m\n",errno);
       return 0;
     }
         
     fprintf(db_fd,"route add success route=%x\n", SIN_ADDR(rt.rt_gateway));
     fclose(db_fd);
         
     return 0;
 }
 
/**************addroute.h***********************/
 #include <sys/ioctl.h>
 #include <sys/types.h>
 #include <sys/socket.h>
 #include <asm/types.h>                /* glibc 2 conflicts with linux/types.h */
 #include <net/if.h>
 #include <net/if_arp.h>
 #include <net/route.h>
 #include <netinet/if_ether.h>
 #include <sys/errno.h>
 #include <stdio.h>
 /*
 * SET_SA_FAMILY - set the sa_family field of a struct sockaddr,
 * if it exists.
 */
 
#define SET_SA_FAMILY(addr, family)                        \
     memset ((char *) &(addr), '\0', sizeof(addr));        \
     addr.sa_family = (family);
 
#define SIN_ADDR(x)        (((struct sockaddr_in *) (&(x)))->sin_addr.s_addr)