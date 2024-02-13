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
        </Routes>
      </BrowserRouter>
      </div>
    </>
  );
}

export default App;
