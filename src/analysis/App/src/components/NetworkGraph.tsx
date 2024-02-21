import { NodeTooltipProps, ResponsiveNetwork } from '@nivo/network';


interface Nodes {
    id: any
    size: Number
};

interface Link {
    source: string
    target: string
    distance: Number
};

interface NetworkGraphsProps {
    data: {
        nodes: Nodes[];
        links: Link[];
    };
};

const NetworkGraph: React.FC<NetworkGraphsProps> = ({data}) => { 
    return (
        <ResponsiveNetwork
            data={data}
            margin={{ top: 0, right: 0, bottom: 0, left: 0 }}
            linkDistance={(e: any) => e.distance}
            linkColor="#62a0ea"
            centeringStrength={0.3}
            repulsivity={6}
            nodeSize={24}
            activeNodeSize={(n: any)=>1.5*n.size}
            nodeColor="#613583"
            nodeBorderWidth={3}
            nodeBorderColor={{
                from: 'color',
                modifiers: [
                    [
                        'brighter',
                        0.8
                    ]
                ]
            }}
            linkThickness={3}
            nodeTooltip={({ node } :NodeTooltipProps<Nodes>) => <div>{node.id}</div>}
    />
    );
}
export default NetworkGraph;

