"""Source-preview finish masks added only after native FBX export."""
def configure_studio(material,texture,bsdf,palette,rgba):
    nodes,links=material.node_tree.nodes,material.node_tree.links
    def math_node(operation,a,b):
        node=nodes.new('ShaderNodeMath')
        node.operation=operation
        for socket,value in zip(node.inputs,(a,b)):
            if isinstance(value,(float,int)):socket.default_value=value
            else:links.new(value,socket)
        return node.outputs[0]
    def mask(colours):
        total=0
        for colour in colours:
            distance=nodes.new('ShaderNodeVectorMath')
            distance.operation='DISTANCE'
            links.new(texture.outputs['Color'],distance.inputs[0])
            distance.inputs[1].default_value=rgba(palette[colour])[:3]
            selected=math_node('LESS_THAN',distance.outputs['Value'],.001)
            total=math_node('MAXIMUM',total,selected)
        return total
    metal=mask(('chrome','chromeDark','steel','silverLight'))
    cloth=mask(('rubber','seat','cream','pink','wine'))
    glass=mask(('glass',))
    paint=mask(('red','redLight','redDark'))
    links.new(math_node('ADD',.05,math_node('MULTIPLY',metal,.90)),bsdf.inputs['Metallic'])
    roughness=math_node('ADD',.32,math_node('MULTIPLY',metal,-.16))
    roughness=math_node('ADD',roughness,math_node('MULTIPLY',cloth,.50))
    links.new(math_node('ADD',roughness,math_node('MULTIPLY',glass,-.20)),bsdf.inputs['Roughness'])
    links.new(math_node('MULTIPLY',paint,.35),bsdf.inputs['Coat Weight'])
    bsdf.inputs['Coat Roughness'].default_value=.12
