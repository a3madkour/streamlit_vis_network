import os
import json

import streamlit.components.v1 as components


import streamlit as st


_RELEASE = True

if not _RELEASE:
    _vis_network = components.declare_component(
        "vis_network",
        url="http://localhost:3001",
    )

else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _vis_network = components.declare_component("vis_network", path=build_dir)


class Config:
    def __init__(
        self,
        height=800,
        width=1000,
        directed=True,
        nodeLabelProperty="label",
        **kwargs,
    ):
        self.height = height
        self.width = width
        self.automaticRearrangeAfterDropNode = True
        self.directed = directed
        self.node = {"labelProperty": nodeLabelProperty}  # "highlightColor":"black",
        self.__dict__.update(kwargs)

    def to_dict(self):
        return self.__dict__


class Node:
    def __init__(
        self,
        id,
        abbrev="",
        size=25,
        borderWidth=1,
        borderWidthSelected=2,
        chosen=True,
        color="#AEAEAE",
        opacity=100,
        label=None,
        image="",
        shape="circularImage",
        symbolType="circle",
        strokeColor="",  # F7A7A6
        title="",  # F7A7A6
        widthConstraint=False,
        x=None,
        y=None,
        **kwargs,
    ):
        self.id = id
        self.size = size
        self.borderWidth = borderWidth
        self.borderWidthSelected = borderWidthSelected
        self.chosen = chosen
        self.abbrev = abbrev
        self.svgcolor = color
        self.opacity = opacity
        self.label = label
        self.image = image
        self.shape = shape
        self.symbolType = symbolType
        self.strokeColor = strokeColor
        self.title = title
        self.widthConstraint = widthConstraint
        self.x = x
        self.y = y
        self.__dict__.update(kwargs)

    def to_dict(self):
        return self.__dict__


class Edge:
    def __init__(
        self,
        source,
        target,
        color="#2B7CE9",
        id="",
        renderLabel=False,
        **kwargs,
    ):
        self.source = source
        self.target = target
        self.color = color  # labelPropertyF48B94 #F7A7A6 #
        self.renderLabel = renderLabel
        self.id = id
        self.__dict__["from"] = source
        self.__dict__["to"] = target
        self.__dict__.update(kwargs)

    def to_dict(self):
        return self.__dict__


def vis_network(nodes, edges, config, key=None):
    # layout = getattr(config, "graphviz_layout")
    # if layout:
    # config.d3 = {"disableLinkForce": True}
    # nodes, edges = _set_graphviz_layout(nodes, edges, config)

    nodes_data = [node.to_dict() for node in nodes]
    edges_data = [edge.to_dict() for edge in edges]

    # nodes_data = [{"id": f"{node}"} for node in nodes]
    # edges_data = [ {"source": f"{edge[0]}", "target": f"{edge[1]}"} for edge in edges]

    config_json = json.dumps(config.__dict__)
    # st.write(config_json)

    data = {"nodes": nodes_data, "edges": edges_data}
    # st.write(data)
    data_json = json.dumps(data)
    component_value = _vis_network(data=data_json, config=config_json, key=key)

    return component_value


# app: `$ streamlit run agraph/__init__.py`
if not _RELEASE:
    import json
    import streamlit as st

    st.subheader("Component with constant args")
    nodes = []
    edges = []
    nodes.append(
        Node(
            id="Spiderman",
            size=30,
            image="http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_spiderman.png",
            abbrev="S",
        )
    )  # ,
    nodes.append(
        Node(
            id="Captain_Marvel",
            size=30,
            image="http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_captainmarvel.png",
            abbrev="CM",
        )
    )
    edges.append(Edge(source="Captain_Marvel", target="Spiderman", type="CURVE_SMOOTH"))
    nodes.append(Node(id="Chris_Klose", size=30, abbrev="CK", color="#00000"))  #
    edges.append(
        Edge(source="Chris_Klose", target="Spiderman", type="CURVE_SMOOTH", id="omak")
    )
    # edges.append( Edge(source="Chris_Klose", target="Spiderman", type="CURVE_SMOOTH") )
    # edges.append(Edge(source="Chris_Klose", target="Captain_Marvel", type="CURVE_SMOOTH" )) # renderLabel=True, labelProperty="best_friend_of"
    # nodes = ["Harry","Sally","Peter","Chris"]
    # edges = [("Harry","Sally"),("Peter","Chris")]

    # myConfig = { "nodeHighlightBehavior": "true", "node": { "color": "lightgreen", "size": 120, "highlightStrokeColor": "blue",}, "link": { "highlightColor": "lightblue",}, }

    config = Config(width=1500, height=500, directed=True)
    return_value = vis_network(nodes=nodes, edges=edges, config=config)

    # st.write(return_value)
    # st.markdown("You've clicked %s times!" % int(num_clicks))

    # st.markdown("---")
