import { Link } from "react-router-dom";

function PacketAn() {
    return (
        <div className="container">
            <div className="options">
            <div className="options-column">
                <h1>Packet Analysis</h1>
                <ul className="options-list">
                    <li><Link to="/packetanalysis/ipv4">IPv4 Analysis</Link></li>
                </ul>
            </div>
            </div>
        </div>
    );
}

export default PacketAn