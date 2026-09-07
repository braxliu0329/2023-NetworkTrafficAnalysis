# 网络流量分析工具 (Network Traffic Analysis)

---
<p align="center">
  <a href="https://braxliu0329.github.io/2023-NetworkTrafficAnalysis/">
    <img alt="在线使用文档" src="https://img.shields.io/badge/%F0%9F%9A%80_%E5%9C%A8%E7%BA%BF%E6%96%87%E6%A1%A3-GitHub_Pages-2ea44f?style=for-the-badge">
  </a>
  &nbsp;
  <a href="README.md">
    <img alt="English Version" src="https://img.shields.io/badge/README-English-blue?style=for-the-badge&logo=readme&logoColor=white">
  </a>
</p>

---

## 目录

- [项目简介](#项目简介)
- [功能特性](#功能特性)
- [项目需求](#项目需求)
- [利益相关者](#利益相关者)
- [团队成员](#团队成员)
- [指导老师](#指导老师)
- [用户故事](#用户故事)
- [最小可行产品要求](#最小可行产品要求)
- [开发环境搭建](#开发环境搭建)
- [部署与使用说明](#部署与使用说明)
- [项目结构](#项目结构)
- [支持的攻击检测类型](#支持的攻击检测类型)
- [许可证](#许可证)

---

## 项目简介

本项目在去年网络流量分析项目的基础上进行了开发，对数据包嗅探的实现进行了优化。去年的项目已能够检测多种攻击方式，但随着其他攻击方式日益突出，本项目旨在扩展前一版本的检测范围。项目开发并优化了一套用于分析流量模式的数据包嗅探工具，支持检测的攻击类型包括但不限于：ARP欺骗、TCP SYN洪泛攻击、ICMP洪泛攻击以及拒绝服务（DoS）攻击等。

## 功能特性

- **实时数据包捕获与嗅探**：支持监控模式和混杂模式进行网络数据包抓取
- **多平台GUI界面**：基于PyQt5开发的交互式桌面应用，提供直观的数据包分析界面
- **Web可视化分析平台**：基于React + Go的Web端数据可视化，支持多种图表分析
- **命令行分析工具**：Go语言编写的高性能CLI工具，支持离线pcap文件分析
- **多种攻击检测算法**：涵盖目前主流的网络攻击检测方法
- **数据包过滤与搜索**：按协议、源地址、目的地址等条件进行过滤
- **数据包标记与忽略**：支持对可疑数据包进行标记，或忽略无关数据包
- **流量统计图表**：IP频率、协议分布、端口统计等多种可视化图表
- **协议流追踪**：基于Tshark的TCP/UDP流内容还原
- **配置灵活**：可自定义各攻击检测的阈值参数

## 项目需求

- 提供一个可运行、更优化的现有项目版本，用于监控网络中的数据流量
- 拦截并记录数据包
- 对数据进行分析，并考虑此前未实现的攻击检测方法
- 提供一个交互式、直观易用的图形用户界面

## 利益相关者

**Louis 与 Synoptix** — 作为本项目的委托方（客户）及主要用户。他们期望获得一套能够监控和分析指定网络数据包的系统，需要一个最终的、稳健的程序，使其能够通过定期扫描数据包来测试公司网络的安全性，发现公司未察觉的网络攻击。

## 团队成员

- Ani Boja
- Tony Liu
- Tomos Sherlock
- Joe Dobson

## 指导老师

- Oliver Gay

## 用户故事

- 作为 Synoptix 信息技术部门，我希望拥有一套自动化系统来监控和分析客户的专用网络，以便检查数据是否被窃取或滥用。我的首要目标是保护网络免受潜在的恶意攻击。
- 作为 Synoptix 的客户，我希望我的网络能够被仔细分析以发现潜在威胁，这样在程序检测到正在进行的攻击时，可以进一步加强安全措施并通知IT部门。我希望能够以被动方式在我们的测试网络上使用该程序，程序将被动监控网络以自动识别任何我们未察觉的网络攻击。
- 作为一名经验丰富的网络分析师，我希望能够以主动方式扫描测试网络，以便在我们怀疑存在某种正在进行的攻击时能够及时响应。
- 作为一名网络工程师，我需要一个有用的、具有直观GUI的网络分析工具，使我能够有效地使用界面来动态捕获、过滤和排序数据包。我的首要目标是能够监控和报告网络中的可疑数据包，以指导网络安全调查。

## 最小可行产品要求

- 保留现有解决方案的功能和特性
- 代码有良好的文档和注释
- 项目的GUI更加直观和有条理
- 使用不同的、更优化的语言重写现有产品（Go语言实现CLI工具和Web后端）

---

## 开发环境搭建

### 前置条件

克隆 GitHub 仓库：

```bash
git clone https://github.com/spe-uob/2023-NetworkTrafficAnalysis.git
```

---

### Windows 系统

1. **下载 Python**：访问 [Python官网](https://www.python.org/downloads/) 下载安装（推荐 Python < 3.9 版本）

2. **检查 Python 版本并安装依赖库**：

```bash
python --version
pip install Scapy
pip install Pyqt5
pip install matplotlib
pip install pandas
pip install networkx
```

或者通过 Scapy 官方链接安装：https://scapy.readthedocs.io/en/latest/installation.html

3. **下载 Npcap**：访问 https://npcap.com/#download 下载并安装

---

### macOS - Intel 芯片

1. **下载 Python**：访问 [Python官网](https://www.python.org/downloads/) 下载安装

2. **安装依赖库**：

```bash
pip install -r requirements.txt
```

---

### macOS - Arm64 (M1 / M2) 芯片

> 注意：Scapy 库在本机环境下目前不可直接使用，需要通过 Anaconda 创建虚拟环境。

1. **下载 Anaconda**：访问 https://www.anaconda.com/download/ 下载安装

2. **创建虚拟环境并安装依赖**：

```bash
conda create -n <环境名称> python=<版本号>
conda env list
activate <环境名称>
pip install -r requirements.txt
```

> 运行完程序后，别忘了使用 `deactivate` 命令退出虚拟环境。

---

### Tshark 安装

Tshark 是 Wireshark 的命令行版本，为程序中的"流追踪（Follow Stream）"功能提供支持。Linux 用户可直接安装 Tshark；Windows 用户需要同时安装 Wireshark 和 Tshark，并完成其他配置步骤。

> 版本要求：4.2 及以上版本。使用更早的版本将导致追踪流时无法使用 UTF-8 编码。

#### Windows

1. 从 [此处](https://www.wireshark.org/#download) 下载 Wireshark 安装程序
2. 在文件资源管理器中，找到 Wireshark 的安装路径
3. 在开始菜单中搜索"编辑账户的环境变量"
4. 编辑 Path 变量，添加 Wireshark 安装路径（应指向包含 Python 的路径）
5. 点击确定保存修改的 PATH 环境变量
6. 设置好 PATH 后，重启 cmd 窗口，运行 `TShark` 检查是否正常工作

#### Linux

下载 [Tshark 4.2.x](https://www.wireshark.org/download/src/wireshark-4.2.4.tar.xz) 源码包并编译安装：

```bash
wget https://www.wireshark.org/download/src/wireshark-4.2.4.tar.xz -O /tmp/wireshark-4.2.4.tar.xz
tar -xvf /tmp/wireshark-4.2.4.tar.xz
cd /tmp/wireshark-4.2.4

sudo apt update && sudo apt dist-upgrade
sudo apt install cmake libglib2.0-dev libgcrypt20-dev flex yacc bison byacc \
  libpcap-dev qtbase5-dev libssh-dev libsystemd-dev qtmultimedia5-dev \
  libqt5svg5-dev qttools5-dev
cmake .
make
sudo make install
```

请确保满足 Tshark 所需的所有依赖项。

#### macOS

1. **安装 Homebrew**：

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. **安装 Wireshark（包含 Tshark）**：

```bash
brew install wireshark
```

3. **验证 Tshark 安装**：

```bash
Tshark -v
```

---

## 部署与使用说明

### 构建与启动

1. **在项目根目录运行构建脚本**：

```bash
./build.sh
```

2. **运行启动脚本**：

```bash
./nta.sh
```

3. **查看使用帮助**：

```bash
./nta.sh --help
```

### nta.sh 启动参数

| 参数 | 说明 |
|------|------|
| `--analysis` | 启用 Web 分析平台（启动后端服务器并自动打开浏览器） |
| `--monitor` | 启用监控模式进行数据包捕获 |
| `--promiscuous` | 启用混杂模式进行数据包捕获 |
| `--help` / `-h` | 显示帮助信息 |
| `--version` / `-v` | 显示版本信息 |

> 注意：`--monitor` 和 `--promiscuous` 不可同时使用。

**使用示例**：

```bash
# 仅启动GUI，不启用分析平台，不使用特殊模式
./nta.sh

# 启动GUI + Web分析平台
./nta.sh --analysis

# 启动GUI + 混杂模式捕获
./nta.sh --promiscuous

# 启动GUI + Web分析平台 + 监控模式
./nta.sh --analysis --monitor
```

> macOS 用户：当提示配置 Python 解释器时，请选择 conda 解释器。

---

### CLI 文件分析工具使用

如需使用命令行 pcap 文件分析工具，进入 `src` 目录并运行：

```bash
cd src
./pcap_analysis
```

**CLI 使用格式**：

```bash
./pcap_analysis [检测类型] ["文件路径"]
```

**查看所有支持的检测类型**：

```bash
./pcap_analysis tests
```

**支持的检测类型编号**：

| 编号 | 检测类型 |
|------|----------|
| 0 | TCP SYN 洪泛攻击 (TCPFlood) |
| 1 | TCP 连接扫描 (TCPConnectScan) |
| 2 | ARP 欺骗攻击 (ARPPoison) |
| 3 | ICMP 洪泛攻击 (ICMPFlood) |
| 4 | HTTP 洪泛攻击 (HTTPFlood) |
| 5 | DNS 攻击检测 |
| all / * | 运行全部检测 |

**使用示例**：

```bash
# 对 test.pcap 运行所有检测
./pcap_analysis all test.pcap

# 对 http-flood.pcap 运行HTTP洪泛检测
./pcap_analysis 4 "test_pcaps/http-flood.pcap"
```

> 输入阈值时，可输入 `d` 使用默认配置。

---

### Web 分析平台使用指南

完整的使用指南请访问：
https://tomossherlock.github.io/NetworkTrafficAnalysis/#/README

---

## 项目结构

```
2023-NetworkTrafficAnalysis/
├── README.md                     # 英文说明文档
├── README_zh.md                  # 中文说明文档（本文件）
├── requirements.txt              # Python 依赖清单
├── build.sh                      # 项目构建脚本
├── nta.sh                        # 主启动脚本
├── help.txt                      # 帮助文本
├── config.txt                    # CLI工具配置文件
├── stream.yaml                   # 流配置文件
├── .github/                      # GitHub 配置（CI/CD、Issue模板等）
├── Meetings/                     # 会议记录
├── Research/                     # 攻击方法研究文档
│   ├── ARPPoisoning.md
│   ├── DOSAttacks.md
│   ├── HTTPFlood.md
│   ├── ICMPFloods.md
│   ├── TCP Connect Scanning.md
│   └── NewAttackMethods.md
├── docs/                         # 文档与Web指南
│   ├── Handover.md
│   └── webguide/                 # Web端使用指南
└── src/                          # 源代码目录
    ├── main.py                   # Python GUI 主入口
    ├── main.go                   # Go CLI 分析工具主入口
    ├── attack_analysis.go        # Go 攻击检测核心逻辑
    ├── attack_analysis_test.go   # Go 攻击检测测试
    ├── go.mod / go.sum           # Go 依赖管理
    ├── config.txt                # Go CLI 阈值配置
    ├── test_pcaps/               # 测试用 pcap 样本文件
    │   ├── SYN.pcap
    │   ├── arp-poisoning.pcap
    │   ├── dns.pcap
    │   ├── http-flood.pcap
    │   ├── icmp-ping.pcap
    │   ├── ssl_stripping.pcap
    │   ├── tcp-conn.pcap
    │   ├── udp_flood.pcap
    │   └── udp_flood2.pcap
    ├── tshark_wrapper/           # Tshark 封装
    │   └── tshark.py
    ├── pythonGUI/                # Python GUI 模块（PyQt5）
    │   ├── window.py / window.ui          # 主窗口
    │   ├── config.yml                       # 攻击检测阈值配置
    │   ├── attack_analysis_action.py        # 攻击分析动作
    │   ├── follow_stream.py                 # 流追踪功能
    │   ├── capture_analysis/                # 捕获分析核心
    │   │   ├── Packet_Capture.py            # 数据包捕获
    │   │   ├── GUI_actions.py               # GUI动作处理
    │   │   ├── attack_detection.py          # 攻击检测算法
    │   │   ├── dataframe_create.py          # DataFrame 创建
    │   │   └── plotting.py                  # 图表绘制
    │   ├── attack_pcap_file_generate/       # 攻击pcap样本生成
    │   ├── plotData/                        # 绘图数据JSON
    │   └── Icons/                           # GUI图标资源
    └── analysis/                  # Web 分析平台
        ├── App/                   # React 前端 (Vite + TypeScript)
        │   └── src/
        │       ├── pages/         # 各分析页面
        │       └── components/    # 图表组件
        └── backend/               # Go Web 后端
            ├── main.go            # 服务器主入口（端口8080）
            └── api/               # API 路由
                ├── api.go
                ├── attack.go      # 攻击分析API
                ├── frequency.go   # 频率分析API
                └── sourcedest.go  # 源目地址分析API
```

---

## 支持的攻击检测类型

| 攻击类型 | 检测方式 | GUI 页面 | CLI 支持 |
|----------|----------|----------|----------|
| **ARP 欺骗攻击** (ARP Poisoning) | 检测ARP响应中MAC-IP映射异常 | ✅ ArpPoison | ✅ 编号 2 |
| **TCP SYN 洪泛攻击** | 分析SYN/SYN-ACK数据包比例失衡 | ✅ TCPSYNFlood | ✅ 编号 0 |
| **TCP 连接扫描** | 检测短时间内向多端口发送SYN的行为 | ✅ TCPScan | ✅ 编号 1 |
| **ICMP 洪泛攻击** | 基于时间窗口的ICMP包频率阈值 | ✅ ICMPFlood | ✅ 编号 3 |
| **HTTP 洪泛攻击** | HTTP请求频率阈值检测 | ✅ HTTPFlood | ✅ 编号 4 |
| **DNS 攻击** | DNS请求/响应比例分析 | ✅ DNSFlood | ✅ 编号 5 |
| **UDP 洪泛攻击** | UDP数据包频率阈值检测 | ✅ UDPFlood | ❌ |
| **DoS 拒绝服务攻击** | 综合流量异常检测 | ✅ DOSDetect | ❌ |
| **SSL 剥离攻击** | 检测HTTP与HTTPS混合异常流量 | ✅ SSLStripping | ❌ |

### 分析功能页面

除攻击检测外，Web端和GUI还提供以下流量分析功能：

- **IPv4 地址分析** (IPv4An)
- **IPv6 地址分析** (IPv6An)
- **MAC 地址分析** (MACAn)
- **源地址频率分析** (SourceFrequencyAn)
- **目的地址频率分析** (DestFrequencyAn)
- **协议频率分析** (ProtocolFrequencyAn)
- **综合频率分析** (FrequencyAn)
- **源-目地址对分析** (SourceDestAn)
- **攻击综合分析** (AttackAn)
- **网络拓扑图** (NetworkGraph)

### 检测阈值配置

所有攻击检测的阈值均可通过 `src/pythonGUI/config.yml` 文件自定义：

```yaml
DNS_Flood_Detect_Threshold: 100
DoS_Detect_Threshold: 100
HTTP_Flood_Detect_Threshold: 100
ICMP_Flood_Detect_Threshold: 100
TCP_Scan_Detect_Threshold: 100
UDP_Flood_Detect_Threshold: 100
```

CLI 工具阈值配置位于 `src/config.txt`。

---

## 许可证

本项目采用 *公司许可证 (Company License)* 分发。
