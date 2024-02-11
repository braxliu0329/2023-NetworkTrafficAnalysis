import { BrowserRouter, Route, Routes} from 'react-router-dom'
import './App.css';
import Home from './pages/Home';
import IPv4 from './pages/IPv4Analysis';


export const ENDPOINT = "http://localhost:4000";

function App() {
  return (
    <>
      <div>
      <BrowserRouter>
        <Routes>
            <Route index element={<Home />} />
            <Route path="/home" element={<Home />} />
            <Route path="/ipv4" element={<IPv4 />} />
        </Routes>
      </BrowserRouter>
      </div>
    </>
  );
}

export default App;
