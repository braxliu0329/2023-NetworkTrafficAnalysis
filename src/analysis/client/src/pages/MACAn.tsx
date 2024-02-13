import NetworkGraph from '../components/NetworkGraph'
import data from '../../../../pythonGUI/plotData/mac.json'

function MACAn() {
    return (
        <div className="Analysis">
            <h1>MAC Analysis</h1>
            <div style={{height:400}}>
                <NetworkGraph data={data}/>
            </div>
        </div>
    );
}

export default MACAn;