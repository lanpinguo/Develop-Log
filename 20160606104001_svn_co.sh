#! /bin/bash
n=$#
url_ritp=https://192.168.31.251/svn/ritp-plat/trunk/product_ritp
url_ros=https://192.168.31.251/svn/soft-plat/trunk/ros

mkdir product_ritp
mkdir ros

echo "svn co $url_ritp"
svn co --depth=immediates $url_ritp product_ritp

echo "svn co $url_ros"
svn co --depth=immediates $url_ros ros

echo "svn up product_ritp/ ros/"
svn update --set-depth=infinity product_ritp/ ros/

