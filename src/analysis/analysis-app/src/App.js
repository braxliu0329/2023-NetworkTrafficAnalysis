import './App.css';

function App() {
  return (
    <div className="container">
      <h1>Packet Analyzer</h1>
      <div className="options">
        <div className="option">Protocol Analysis</div>
        <div className="option">IPv4 Analysis</div>
        <div className="option">IPv6 Analysis</div>
        <div className="option">MAC Analysis</div>
        <div className="option">Source Analysis</div>
        <div className="option">Destination Analysis</div>
      </div>
    </div>
  );
}

export default App;
