import { NodeTooltipProps, ResponsiveNetwork } from '@nivo/network';

interface Node {
    id: any
    height: Number
    size: Number
    color: string
}

interface Link {
    source: string
    target: string
    distance: Number
}

interface NetworkGraphsProps {
    data: {
        nodes: Node[];
        links: Link[];
    }
}


const NetworkGraph: React.FC<NetworkGraphsProps> = ({data}) => {
    return (
        <ResponsiveNetwork
            data={data}
            margin={{ top: 0, right: 0, bottom: 0, left: 0 }}
            linkDistance={(e: any) => e.distance}
            linkColor="#62a0ea"
            centeringStrength={0.3}
            repulsivity={6}
            nodeSize={(n: any) =>n.size}
            activeNodeSize={(n: any)=>1.5*n.size}
            nodeColor="#613583"
            nodeBorderWidth={1}
            nodeBorderColor={{
                from: 'color',
                modifiers: [
                    [
                        'darker',
                        0.8
                    ]
                ]
            }}
            linkThickness={(n: any)=>2+2*n.target.data.height}
            nodeTooltip={({ node } :NodeTooltipProps<Node>) => <div>{node.id}</div>}
    />
    );
}
export default NetworkGraph;

