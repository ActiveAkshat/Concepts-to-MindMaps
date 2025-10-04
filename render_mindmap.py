import json
import streamlit.components.v1 as components

def render_enhanced_mindmap(dataset):
    """Render an enhanced, student-friendly mind map with emojis and better styling"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <script src="https://unpkg.com/gojs/release/go.js"></script>
      <style>
        body {{
          margin: 0;
          padding: 0;
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        #mindmap {{
          width: 100%;
          height: 700px;
          background: white;
          border-radius: 10px;
          box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        .tooltip {{
          position: absolute;
          background: rgba(0,0,0,0.85);
          color: white;
          padding: 10px 15px;
          border-radius: 8px;
          font-size: 13px;
          pointer-events: none;
          z-index: 1000;
          max-width: 250px;
          display: none;
          box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }}
      </style>
      <script>
        function init() {{
          var $ = go.GraphObject.make;

          var diagram = $(go.Diagram, "mindmap", {{
            layout: $(go.TreeLayout, {{ 
              angle: 0, 
              layerSpacing: 80,
              nodeSpacing: 40,
              arrangement: go.TreeLayout.ArrangementHorizontal
            }}),
            "undoManager.isEnabled": true,
            initialAutoScale: go.Diagram.Uniform,
            contentAlignment: go.Spot.Center,
            padding: 30
          }});

          // Enhanced node template with emoji and better styling
          diagram.nodeTemplate =
            $(go.Node, "Auto",
              {{
                selectionAdorned: true,
                shadowVisible: true,
                shadowColor: "#00000033",
                shadowOffset: new go.Point(0, 3),
                shadowBlur: 8,
                mouseEnter: function(e, obj) {{
                  var node = obj.part;
                  var desc = node.data.description || "";
                  if (desc) {{
                    var tooltip = document.getElementById('tooltip');
                    tooltip.innerHTML = desc;
                    tooltip.style.display = 'block';
                  }}
                }},
                mouseLeave: function(e, obj) {{
                  document.getElementById('tooltip').style.display = 'none';
                }}
              }},
              $(go.Shape, "RoundedRectangle",
                {{
                  strokeWidth: 0,
                  fill: "lightblue",
                  portId: "",
                  cursor: "pointer"
                }},
                new go.Binding("fill", "color")
              ),
              $(go.Panel, "Horizontal",
                {{ margin: 12 }},
                $(go.TextBlock,
                  {{
                    font: "bold 20px sans-serif",
                    margin: new go.Margin(0, 8, 0, 0),
                    stroke: "white"
                  }},
                  new go.Binding("text", "emoji")
                ),
                $(go.TextBlock,
                  {{
                    font: "bold 14px 'Segoe UI', sans-serif",
                    stroke: "white",
                    maxSize: new go.Size(180, NaN),
                    wrap: go.TextBlock.WrapFit,
                    textAlign: "center"
                  }},
                  new go.Binding("text", "text")
                )
              )
            );

          // Enhanced link template
          diagram.linkTemplate =
            $(go.Link,
              {{
                routing: go.Link.Orthogonal,
                corner: 10,
                curve: go.Link.JumpOver
              }},
              $(go.Shape,
                {{ strokeWidth: 3, stroke: "#a0a0a0" }}
              )
            );

          // Load the data
          diagram.model = new go.GraphLinksModel(
            {json.dumps(dataset.get("nodes", []))},
            {json.dumps(dataset.get("links", []))}
          );

          // Track mouse for tooltip positioning
          diagram.div.addEventListener('mousemove', function(e) {{
            var tooltip = document.getElementById('tooltip');
            if (tooltip.style.display === 'block') {{
              tooltip.style.left = (e.pageX + 15) + 'px';
              tooltip.style.top = (e.pageY + 15) + 'px';
            }}
          }});
        }}

        window.addEventListener('DOMContentLoaded', init);
      </script>
    </head>
    <body>
      <div id="mindmap"></div>
      <div id="tooltip" class="tooltip"></div>
    </body>
    </html>
    """
    components.html(html, height=750, scrolling=False)
