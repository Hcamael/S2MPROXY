# Single to Multi thread Proxy

单线程转换为多线程的代理，运用场景可以见我[blog](https://nobb.site/2021/12/07/0x6F/)。

目前只有简单的python版本，也只实现了UDP代理，按我设想，应该是可以实现TCP代理的，客户端和服务端之间进行通行也可以转换，另外还想着用C或者Golang再写一般，测测性能如何。

# 不知道什么使用再做的TODO

* 实现TCP协议。
* 开发C/Golang版本。
* 优化一下结构，目前的版本只是随便写的，只是为了快速实现我想要的功能。
* ......