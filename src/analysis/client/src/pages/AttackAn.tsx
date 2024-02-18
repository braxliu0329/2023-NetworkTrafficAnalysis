import { Link } from "react-router-dom";

function AttackAn() {
    return (
        <div className="container">
            <div className="options">
            <div className="options-column">
                <h1>Attack Analysis</h1>
                <ul className="options-list">
                    <li><Link to="/attackanalysis/arppoison">Arp Poisoning</Link></li>
                    <li><Link to="/attackanalysis/tcpsynflood">TCP SYN Flooding</Link></li>
                </ul>
            </div>
            </div>
        </div>
    );
}

export default AttackAn;