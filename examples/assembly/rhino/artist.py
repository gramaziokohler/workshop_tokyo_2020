import compas_rhino

class AssemblyArtist(object):
    """Rudimentary assembly artist for RhinoPython
    """

    def __init__(self, assembly, layer=None):
        self.assembly = assembly
        self.layer = layer

    def draw(self):
        from compas_rhino.artists import MeshArtist
        previous_layer = None

        if self.layer:
            if not compas_rhino.rs.IsLayer(self.layer):
                compas_rhino.create_layers_from_path(self.layer)
            previous_layer = compas_rhino.rs.CurrentLayer(self.layer)

        compas_rhino.rs.EnableRedraw(False)
        for vkey, element in self.assembly.elements():
            artist = MeshArtist(element.mesh)
            artist.draw_mesh()

        if self.layer and previous_layer:
            compas_rhino.rs.CurrentLayer(previous_layer)

        self.redraw()

    def redraw(self, timeout=None):
        if timeout:
            time.sleep(timeout)

        compas_rhino.rs.EnableRedraw(True)
        compas_rhino.rs.Redraw()

    def clear_layer(self):
        """Clear the main layer of the artist."""
        if self.layer:
            compas_rhino.clear_layer(self.layer)
        else:
            compas_rhino.clear_current_layer()
