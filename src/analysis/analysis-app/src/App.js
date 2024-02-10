import './App.css';
import {
  BrowserRouter,
  Routes,
  Route
} from 'react-router-dom';
import Home from './pages/Home';
import IPv4 from './pages/IPV4Analysis';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route index element={<Home />} />
          <Route path="/home" element={<Home />} />
          <Route path="/ipv4analysis" element={<IPv4 />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
