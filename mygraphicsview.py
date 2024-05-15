from pyqtgraph import QtCore, getConfigOption, QtWidgets
from pyqtgraph import GraphicsView


class MyGraphicsView(GraphicsView):
    # User defined
    sigMouseMoved = QtCore.Signal(object)

    def __init__(self, parent=None, useOpenGL=None, background='default'):
        super().__init__(parent=parent, useOpenGL=useOpenGL, background=background)
        self.centralLayout.setSpacing(0)


    def setMouseTracking(self, m=False):
        b = getConfigOption('useOpenGL')
        if b:
            HAVE_OPENGL = hasattr(QtWidgets, 'QOpenGLWidget')
            if not HAVE_OPENGL:
                raise Exception("Requested to use OpenGL with QGraphicsView, but QOpenGLWidget is not available.")

            v = QtWidgets.QOpenGLWidget()
        else:
            v = QtWidgets.QWidget()

        v.setMouseTracking(m)

        self.setViewport(v)

    def mouseMoveEvent(self, ev):
        pos = ev.position() if hasattr(ev, 'position') else ev.localPos()

        # 左键没有按下，说明只是移动，没有拖拽
        if ev.buttons() is not QtCore.Qt.MouseButton.LeftButton:
            self.sigMouseMoved.emit(pos)
            return
        
        super().mouseMoveEvent(ev)
