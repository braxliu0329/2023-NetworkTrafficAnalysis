import { Link } from "react-router-dom";

  function Home() {
    return (
      <div className="container">
        <div className="options">
          <div className="options-column">
            <h1>NTAnalyser</h1>
            <ul className="options-list">
              <li><Link to="/sourcedestanalysis">Source/Destination Analysis</Link></li>
              <li><Link to="/frequencyanalysis">Frequency Analysis</Link></li>
              <li><Link to="/attackanalysis">Attack Analysis</Link></li>
            </ul>
          </div>
        </div>
        <div className="description">
          <h2>What is NTAnalyser?</h2>
          <p>NTAnalyser is a lightweight tool designed for network engineers to analyse packet data efficiently.</p>
          <p>It provides various analysis options such as protocol, IPv4, IPv6, MAC, source, and destination analysis.</p>
          <p>Use NTAnalyser to gain insights into your network traffic and troubleshoot issues effectively.</p>
        </div>
      </div>
    );
}
export default Home;