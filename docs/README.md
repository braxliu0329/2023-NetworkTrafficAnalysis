# 网络流量分析工具 (Network Traffic Analysis)

> 本页面是 **2023 Network Traffic Analysis** 项目的在线使用指南。
> 项目仓库：[github.com/braxliu0329/2023-NetworkTrafficAnalysis](https://github.com/braxliu0329/2023-NetworkTrafficAnalysis)

---

## 项目简介

本项目在 2022 年版 Network Traffic Analysis 的基础上进行了优化和扩展，提供了一套完整的网络流量嗅探与攻击检测解决方案。项目提供三种交互形式：

- **桌面 GUI 程序**（Python + PyQt5）- 实时抓包、pcap 分析、攻击检测、可视化图表
- **命令行离线分析工具**（Go）- 高性能批量处理 pcap 文件
- **Web 可视化平台**（React + Vite + Go）- 浏览器端的多维度数据可视化界面

支持检测的攻击类型包括但不限于：ARP 欺骗、TCP SYN 洪泛、ICMP 洪泛、HTTP/DNS/UDP 洪泛、TCP 端口扫描、DoS 拒绝服务、SSL 剥离等。

---

## 📚 指南目录

请在左侧边栏或下方链接中选择对应的章节：

- [环境搭建指南 (Setup)](Guide/setup.md)
- [PCAP 文件与数据包操作 (Pcap)](Guide/pcap.md)
- [攻击检测与分析 (Attack Analysis)](Guide/attack_analysis.md)

---

## 💡 快速开始

```bash
# 1. 克隆项目
git clone https://github.com/braxliu0329/2023-NetworkTrafficAnalysis.git
cd 2023-NetworkTrafficAnalysis

# 2. 安装 Python 依赖
pip install -r requirements.txt

# 3. 安装并确认 Tshark（4.2+）
tshark -v

# 4. 构建并启动
./build.sh
./nta.sh --analysis
```

更多详细说明请参考 [环境搭建指南 (Setup)](Guide/setup.md)。
