import { Link } from "react-router-dom";

function SourceDestAn() {
    return (
        <div className="container">
            <div className="options">
            <div className="options-column">
                <h1>Source/Destination Analysis</h1>
                <ul className="options-list">
                    <li><Link to="/sourcedestanalysis/ipv4">IPv4 Analysis</Link></li>
                    <li><Link to="/sourcedestanalysis/ipv6">IPv6 Analysis</Link></li>
                    <li><Link to="/sourcedestanalysis/mac">MAC Analysis</Link></li>
                </ul>
            </div>
            </div>
        </div>
    );
}

export default SourceDestAn;