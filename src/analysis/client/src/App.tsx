import { BrowserRouter, Route, Routes} from 'react-router-dom'
import Home from './pages/Home';
import PacketAn from './pages/PacketAn';
import IPv4An from './pages/IPv4An';
import AttackAn from './pages/AttackAn';


export const ENDPOINT = "http://localhost:4000";

function App() {
  return (
    <>
      <div>
      <BrowserRouter>
        <Routes>
            <Route path = "/" element={<Home />} />
            <Route path="/home" element={<Home />} />
            <Route path="/packetanalysis/ipv4" element={<IPv4An />} />
            <Route path="/packetanalysis" element={<PacketAn />} />
            <Route path="/attackanalysis" element={<AttackAn />} />
        </Routes>
      </BrowserRouter>
      </div>
    </>
  );
}

export default App;
