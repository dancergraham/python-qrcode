import Rhino.Geometry as rg
import Rhino
import scriptcontext as sc
import qrcode.image.base


class RhinoImage(qrcode.image.base.BaseImage):
    """
    Rhino QRCode image output class.
    """
    kind = "Rhino"
    allowed_kinds = ("Rhino", )

    def __init__(self, *args, **kwargs):
        super(RhinoImage, self).__init__(*args, **kwargs)

    def drawrect(self, row, col):
        """
        Draw a single rectangle of the QR code.
        """
        square = rg.Rectangle3d(rg.Plane.WorldXY, 1.,1.)
        surf = rg.Brep.CreatePlanarBreps(square.ToNurbsCurve())[0]
        surf.Transform(rg.Transform.Translation(col, -row, 0))
        self._img.append(surf)
        
    def show(self):
        for brep in self._img:
            sc.doc.Objects.AddBrep(brep)

    def save(self, stream, kind=None):
        """
        Save the image file.
        """
        pass

    def pixel_box(self, row, col):
        """
        A helper method for pixel-based image generators that specifies the
        four pixel coordinates for a single rect.
        """
        x = (col + self.border) * self.box_size
        y = (row + self.border) * self.box_size
        return [(x, y), (x + self.box_size - 1, y + self.box_size - 1)]

    def new_image(self, **kwargs):
        """
        Build the image class. Subclasses should return the class created.
        """
        return []

    def get_image(self, **kwargs):
        """
        Return the image class for further processing.
        """
        return self._img

