import { BrowserRouter, Route, Routes} from 'react-router-dom'
import Sidebar from './components/Sidebar';
import Home from './pages/Home';
import PacketAn from './pages/SourceDestAn';
import IPv4An from './pages/IPv4An';
import AttackAn from './pages/AttackAn';
import IPv6An from './pages/IPv6An';
import MACAn from './pages/MACAn';
import FrequencyAn from './pages/FrequencyAn';
import ProtocolFrequencyAn from './pages/ProtocolFrequencyAn';
import SourceFrequencyAn from './pages/SourceFrequencyAn';
import DestFrequencyAn from './pages/DestFrequencyAn';
import ArpPoision from './pages/ArpPoison';
import TCPSYNFlood from './pages/TCPSYNFlood';
import TCPScan from './pages/TCPScan';
import DOSDetect from './pages/DOSDetect';
import HTTPFlood from './pages/HTTPFlood';
import DNSFlood from './pages/DNSFlood';
import ICMPFlood from './pages/ICMPFlood';
import { Page } from './components/Sidebar';
import Shutdown from './pages/Shutdown';
import UDPFlood from './pages/UDPFlood';

// Define paths and titles for use in the sidebar
const pages: Page[] = [
  { title: 'Home', path: '/home' },
  { title: 'Source / Destination Analysis', path: '/sourcedestanalysis', children: [
    { title: 'IPv4 Analysis', path:'/sourcedestanalysis/ipv4'},
    { title: 'IPv6 Analysis', path:'/sourcedestanalysis/ipv6'},
    { title: 'MAC Analysis', path:'/sourcedestanalysis/mac'}
  ] },
  { title: 'Frequency Analysis', path: '/frequencyanalysis', children: [
    { title: 'Protocol Frequency', path: '/frequencyanalysis/protocol' },
    { title: 'Source Frequency', path: '/frequencyanalysis/source' },
    { title: 'Destination Frequency', path: '/frequencyanalysis/dest'}
  ] },
  { title: 'Attack Analysis', path: '/attackanalysis', children: [
    { title: 'ARP Poison', path: '/attackanalysis/arppoison' },
    { title: 'TCP SYN Flood', path: '/attackanalysis/tcpsynflood' },
    { title: 'TCP Connect Scanning', path: '/attackanalysis/tcpconnscan' },
    { title: 'DoS Detection', path: '/attackanalysis/dosdetect' },
    { title: 'HTTP Flooding', path: '/attackanalysis/httpflood' },
    { title: 'DNS Flooding', path: '/attackanalysis/dnsflood' },
    { title: 'ICMP Flooding', path: '/attackanalysis/icmpflood' },
    { title: 'UDP Flooding', path: '/attackanalysis/udpflood'}
  ] },
  { title: 'Shutdown', path: '/shutdown'}  
];

function App() {
  return (
    <>
      <div>
        <BrowserRouter>
          <Sidebar pages={pages} />
          <Routes>
              <Route path = "/" element={<Home />} />
              <Route path="/home" element={<Home />} />
              <Route path="/sourcedestanalysis" element={<PacketAn />} />
              <Route path="/sourcedestanalysis/ipv4" element={<IPv4An />} />
              <Route path="/sourcedestanalysis/ipv6" element={<IPv6An />} />
              <Route path="/sourcedestanalysis/mac" element={<MACAn />} />
              <Route path="/frequencyanalysis" element={<FrequencyAn />} />
              <Route path="/frequencyanalysis/protocol" element={<ProtocolFrequencyAn />} />
              <Route path="/frequencyanalysis/source" element={<SourceFrequencyAn />} />
              <Route path="/frequencyanalysis/dest" element={<DestFrequencyAn />} />
              <Route path="/attackanalysis" element={<AttackAn />} />
              <Route path="/attackanalysis/arppoison" element={<ArpPoision />} />
              <Route path="/attackanalysis/tcpsynflood" element={<TCPSYNFlood /> } />
              <Route path="/attackanalysis/tcpconnscan" element={<TCPScan />}/>
              <Route path="/attackanalysis/dosdetect" element={<DOSDetect />} />
              <Route path="/attackanalysis/httpflood" element={<HTTPFlood />} />
              <Route path="/attackanalysis/dnsflood" element={<DNSFlood />} />
              <Route path="/attackanalysis/icmpflood" element={<ICMPFlood />} />
              <Route path="/attackanalysis/udpflood" element={<UDPFlood />} />
              <Route path="/shutdown" element={<Shutdown />} />
          </Routes>
        </BrowserRouter>
      </div>
    </>
  );
}

export default App;
