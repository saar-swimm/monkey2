import React from 'react';
import Graph from 'react-graph-vis';

class GraphWrapper extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {
    let newOptions = null;
    if(this.props.options !== undefined){
      newOptions = this.props.options;
    }
    return (
      <div className={'net-graph-wrapper'}>
        <Graph graph={this.props.graph} options={newOptions} events={this.props.events}/>
      </div>
    )
  }
}

let ReactiveGraph = GraphWrapper;
export {ReactiveGraph};
