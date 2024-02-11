function Home() {
    return (
      <div className="container">
        <div className="options">
          <div className="options-column">
            <h1>NTAnalyzer</h1>
            <ul className="options-list">
              <li>Protocol Analysis</li>
              <li>IPv4 Analysis</li>
              <li>IPv6 Analysis</li>
              <li>MAC Analysis</li>
              <li>Source Analysis</li>
              <li>Destination Analysis</li>
            </ul>
          </div>
        </div>
        <div className="description">
          <h2>What is NTAnalyzer?</h2>
          <p>NTAnalyzer is a lightweight tool designed for network engineers to analyze packet data efficiently.</p>
          <p>It provides various analysis options such as protocol, IPv4, IPv6, MAC, source, and destination analysis.</p>
          <p>Use NTAnalyzer to gain insights into your network traffic and troubleshoot issues effectively.</p>
        </div>
      </div>
    );
}
export default Home;