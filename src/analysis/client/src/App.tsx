import { BrowserRouter, Route, Routes} from 'react-router-dom'
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


export const ENDPOINT = "http://localhost:4000";

function App() {
  return (
    <>
      <div>
      <BrowserRouter>
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
        </Routes>
      </BrowserRouter>
      </div>
    </>
  );
}

export default App;
