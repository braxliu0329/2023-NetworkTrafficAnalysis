import { Link } from "react-router-dom";

function FrequencyAn() {
    return (
        <div className="container">
            <div className="options">
            <div className="options-column">
                <h1>Frequency Analysis</h1>
                <ul className="options-list">
                    <li><Link to="/frequencyanalysis/protocol">Protocol Frequency Analysis</Link></li>
                    <li><Link to="/frequencyanalysis/source">Source Frequency Analysis</Link></li>
                    <li><Link to="/frequencyanalysis/dest">Destination Frequency Analysis</Link></li>
                </ul>
            </div>
            </div>
        </div>
    );
}

export default FrequencyAn;