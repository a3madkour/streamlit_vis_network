
import React, { ReactNode, createRef, useEffect, useContext } from 'react';
import { Network } from "vis-network/standalone/esm/vis-network"
/* import { IGraph } from './util/graph'; */
import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection
} from "streamlit-component-lib";

interface State {
  network: any
}
interface Props {
  /* graph: IGraph, */
  args: any
  /* width?: number,
   * height?: number,
   * updateParent?: () => void,
   * manipulate: boolean
   * letter: Letter */
}

class GraphComponent extends StreamlitComponentBase<State> {

  public state = { network: {}, myRef: createRef<HTMLDivElement>() }


  public componentDidMount() {
    const processGraph = (graph: any) => {

      var nodes: Array<any> = []
      var edges: Array<any> = []
      var data = { nodes: nodes, edges: edges }

      for (var i = 0; i < graph.nodes.length; i++) {
        var node: any = Object.assign({}, graph.nodes[i]);
        if (node.image === ""){
          var svg =
            '<svg xmlns="http://www.w3.org/2000/svg" width="75" height="75">' +
            '<circle cx="37.5" cy="37.5" r="35" fill="' + node.svgcolor + '" />' +
            '<text x="50%" y="50%" text-anchor="middle" fill="white" font-size="x-large" font-family="Arial" dy=".3em">' + graph.nodes[i].abbrev + '</text>' +
            'Sorry, your browser does not support inline SVG.' +
            "</svg>";

          var url = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(svg);
          node.image = url;
        }
        
        data.nodes.push(node)
      }
      data.edges = graph.edges

      return data
    }


    const python_data = JSON.parse(this.props.args["data"])
    const python_config = JSON.parse(this.props.args["config"])
    const options = {
      interaction: { hover: true },
      /* width: python_config.width,
* height: python_config.height, */
      edges: {
        arrows: { to: true }
      },
      manipulation: {
        enabled: false
      },

    }
    var data = processGraph(python_data)
    var divElement = this.state.myRef.current
    if (divElement) {
      var network = new Network(divElement, data, options)
    }


    this.forceUpdate();
  }
  public render = (): ReactNode => {

    return (
      <div className="graph-container" ref={this.state.myRef} >
      </div>
    )

  }
}

export default withStreamlitConnection(GraphComponent)
