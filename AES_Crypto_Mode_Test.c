/**
*@autho stardust
*@time 2013-10-10
*@param 实现AES五种加密模式的测试
*/
#include <iostream>
using namespace std;

//加密编码过程函数,16位1和0
int dataLen = 16;   //需要加密数据的长度
int encLen = 4;     //加密分段的长度
int encTable[4] = {1,0,1,0};  //置换表
int data[16] = {1,0,0,1,0,0,0,1,1,1,1,1,0,0,0,0}; //明文
int ciphertext[16]; //密文

//切片加密函数
void encode(int arr[])
{
    for(int i=0;i<encLen;i++)
    {
        arr[i] = arr[i] ^ encTable[i];
    }
}

//电码本模式加密，4位分段
void ECB(int arr[])
{
    //数据明文切片
    int a[4][4];
    int dataCount = 0;  //位置变量
    for(int k=0;k<4;k++)
    {
        for(int t=0;t<4;t++)
        {
            a[k][t] = data[dataCount];
            dataCount++;
        }
    }
    dataCount = 0;//重置位置变量
    for(int i=0;i<dataLen;i=i+encLen)
    {
        int r = i/encLen;//行
        int l = 0;//列
        int encQue[4]; //编码片段
        for(int j=0;j<encLen;j++)
        {
            encQue[j] = a[r][l];
            l++;
        }
        encode(encQue); //切片加密
        //添加到密文表中
        for(int p=0;p<encLen;p++)
        {
            ciphertext[dataCount] = encQue[p];
            dataCount++;
        }
    }
    cout<<"ECB加密的密文为："<<endl;
    for(int t1=0;t1<dataLen;t1++) //输出密文
    {
        if(t1!=0 && t1%4==0)
            cout<<endl;
        cout<<ciphertext[t1]<<" ";
    }
    cout<<endl;
    cout<<"---------------------------------------------"<<endl;
}

//CBC
//密码分组链接模式，4位分段
void CCB(int arr[])
{
    //数据明文切片
    int a[4][4];
    int dataCount = 0;  //位置变量
    for(int k=0;k<4;k++)
    {
        for(int t=0;t<4;t++)
        {
            a[k][t] = data[dataCount];
            dataCount++;
        }
    }
    dataCount = 0;//重置位置变量

    int init[4] = {1,1,0,0};  //初始异或运算输入
    //初始异或运算
    for(int i=0;i<dataLen;i=i+encLen)
    {
        int r = i/encLen;//行
        int l = 0;//列
        int encQue[4]; //编码片段
        //初始化异或运算
        for(int k=0;k<encLen;k++)
        {
            a[r][k] = a[r][k] ^ init[k];
        }
         //与Key加密的单切片
        for(int j=0;j<encLen;j++)
        {
            encQue[j] = a[r][j];
        }
        encode(encQue); //切片加密
        //添加到密文表中
        for(int p=0;p<encLen;p++)
        {
            ciphertext[dataCount] = encQue[p];
            dataCount++;
        }
        //变换初始输入
        for(int t=0;t<encLen;t++)
        {
            init[t] = encQue[t];
        }
    }


    cout<<"CCB加密的密文为："<<endl;
    for(int t1=0;t1<dataLen;t1++) //输出密文
    {
        if(t1!=0 && t1%4==0)
            cout<<endl;
        cout<<ciphertext[t1]<<" ";
    }
    cout<<endl;
    cout<<"---------------------------------------------"<<endl;
}

//CTR
//计算器模式，4位分段
void CTR(int arr[])
{
    //数据明文切片
    int a[4][4];
    int dataCount = 0;  //位置变量
    for(int k=0;k<4;k++)
    {
        for(int t=0;t<4;t++)
        {
            a[k][t] = data[dataCount];
            dataCount++;
        }
    }
    dataCount = 0;//重置位置变量

    int init[4][4] = {{1,0,0,0},{0,0,0,1},{0,0,1,0},{0,1,0,0}};  //算子表
    int l = 0; //明文切片表列
    //初始异或运算
    for(int i=0;i<dataLen;i=i+encLen)
    {
        int r = i/encLen;//行
        int encQue[4]; //编码片段
        //将算子切片
        for(int t=0;t<encLen;t++)
        {
            encQue[t] = init[r][t];
        }
        encode(encQue); //算子与key加密
        //最后的异或运算
        for(int k=0;k<encLen;k++)
        {
            encQue[k] = encQue[k] ^ a[l][k];
        }
        l++;

        //添加到密文表中
        for(int p=0;p<encLen;p++)
        {
            ciphertext[dataCount] = encQue[p];
            dataCount++;
        }
    }


    cout<<"CTR加密的密文为："<<endl;
    for(int t1=0;t1<dataLen;t1++) //输出密文
    {
        if(t1!=0 && t1%4==0)
            cout<<endl;
        cout<<ciphertext[t1]<<" ";
    }
    cout<<endl;
    cout<<"---------------------------------------------"<<endl;
}

//CFB
//密码反馈模式，4位分段
void CFB(int arr[])
{
    //数据明文切片,切成2 * 8 片
    int a[8][2];
    int dataCount = 0;  //位置变量
    for(int k=0;k<8;k++)
    {
        for(int t=0;t<2;t++)
        {
            a[k][t] = data[dataCount];
            dataCount++;
        }
    }
    dataCount = 0;  //恢复初始化设置
    int lv[4] = {1,0,1,1};  //初始设置的位移变量
    int encQue[2]; //K的高两位
    int k[4]; //K

    for(int i=0;i<2 * encLen;i++) //外层加密循环
    {
        //产生K
        for(int vk=0;vk<encLen;vk++)
        {
            k[vk] = lv[vk];
        }
        encode(k);
        for(int k2=0;k2<2;k2++)
        {
            encQue[k2] = k[k2];
        }
        //K与数据明文异或产生密文
        for(int j=0;j<2;j++)
        {
            ciphertext[dataCount] = a[dataCount/2][j] ^ encQue[j];
            dataCount++;
        }
        //lv左移变换
        lv[0] = lv[2];
        lv[1] = lv[3];
        lv[2] = ciphertext[dataCount-2];
        lv[3] = ciphertext[dataCount-1];
    }

    cout<<"CFB加密的密文为："<<endl;
    for(int t1=0;t1<dataLen;t1++) //输出密文
    {
        if(t1!=0 && t1%4==0)
            cout<<endl;
        cout<<ciphertext[t1]<<" ";
    }
    cout<<endl;
    cout<<"---------------------------------------------"<<endl;
}

//OFB
//输出反馈模式，4位分段
void OFB(int arr[])
{
    //数据明文切片,切成2 * 8 片
    int a[8][2];
    int dataCount = 0;  //位置变量
    for(int k=0;k<8;k++)
    {
        for(int t=0;t<2;t++)
        {
            a[k][t] = data[dataCount];
            dataCount++;
        }
    }
    dataCount = 0;  //恢复初始化设置
    int lv[4] = {1,0,1,1};  //初始设置的位移变量
    int encQue[2]; //K的高两位
    int k[4]; //K

    for(int i=0;i<2 * encLen;i++) //外层加密循环
    {
        //产生K
        for(int vk=0;vk<encLen;vk++)
        {
            k[vk] = lv[vk];
        }
        encode(k);
        for(int k2=0;k2<2;k2++)
        {
            encQue[k2] = k[k2];
        }
        //K与数据明文异或产生密文
        for(int j=0;j<2;j++)
        {
            ciphertext[dataCount] = a[dataCount/2][j] ^ encQue[j];
            dataCount++;
        }
        //lv左移变换
        lv[0] = lv[2];
        lv[1] = lv[3];
        lv[2] = encQue[0];
        lv[3] = encQue[1];
    }

    cout<<"CFB加密的密文为："<<endl;
    for(int t1=0;t1<dataLen;t1++) //输出密文
    {
        if(t1!=0 && t1%4==0)
            cout<<endl;
        cout<<ciphertext[t1]<<" ";
    }
    cout<<endl;
    cout<<"---------------------------------------------"<<endl;
}


void printData()
{
    cout<<"以下示范AES五种加密模式的测试结果："<<endl;
    cout<<"---------------------------------------------"<<endl;
    cout<<"明文为："<<endl;
    for(int t1=0;t1<dataLen;t1++) //输出密文
    {
        if(t1!=0 && t1%4==0)
            cout<<endl;
        cout<<data[t1]<<" ";
    }
    cout<<endl;
    cout<<"---------------------------------------------"<<endl;
}
int main()
{
    printData();
    ECB(data);
    CCB(data);
    CTR(data);
    CFB(data);
    OFB(data);
    return 0;
}