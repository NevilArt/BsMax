import pygame
from pygame.locals import *
import sys
import random
from math import sqrt, fabs, pow
from lines import X, Y
import itertools
import pygame
from pygame import draw, Color
import padlib
from roots_detailed import cubicRoots


def add_points(*points):
    X,Y = 0,0
    for (x,y) in points:
        X += x
        Y += y
    return (X,Y)

def diff_points(p2, p1):
    return (X(p2)-X(p1), Y(p2)-Y(p1));

def scale_point(factor, p):
    return (factor * X(p), factor*Y(p))

def between(v0, v, v1):
    if v0 > v1: v0, v1 = v1, v0
    return v >= v0 and v <= v1


# the point is guaranteed to be on the right line
def pointOnLineSegment(l1, l2, point):
    return between(X(l1), X(point), X(l2)) and between(Y(l1), Y(point), Y(l2))


def rotate(x, y, R1, R2, R3, R4):
    return (x*R1 + y*R2, x*R3 + y * R4);

def findIntersections(p0, p1, m0, m1, l1, l2):
    # We're solving the equation of one segment of Kochanek-Bartels
    # spline intersecting with a line segment
    # The spline is described at http://en.wikipedia.org/wiki/Cubic_Hermite_spline 
    # The discussion on the adopted solution can be found at https://stackoverflow.com/questions/1813719/intersection-between-bezier-curve-and-a-line-segment
    # 
    # The equation we're solving is 
    #
    # h00(t) p0 + h10(t) m0 + h01(t) p1 + h11(t) m1 = u + v t1
    #
    # where 
    #
    # h00(t) = 2t^3 - 3t^2 + 1
    # h10(t) = t^3 - 2t^2 + t
    # h01(t) = -2t^3 + 3t^2
    # h11(t) = t^3 - t^2
    # u = l1
    # v = l2-l1

    u = l1
    v = diff_points(l2, l1);

    # The first thing we do is to move u to the other side:
    #
    # h00(t) p0 + h10(t) m0 + h01(t) p1 + h11(t) m1 - u = v t1
    #
    # Then we're looking for matrix R that would turn (v t1) into
    # ({|v|, 0} t1). This is rotation of coordinate system matrix,
    # described at http://mathworld.wolfram.com/RotationMatrix.html
    #
    # R(h00(t) p0 + h10(t) m0 + h01(t) p1 + h11(t) m1 - u) = R(v t1) = {|v|, 0}t1
    #
    # We only care about R[1,0] and R[1,1] because it lets us solve
    # the equation for y coordinate where y == 0 (intersecting the
    # spline segment with the x axis of rotated coordinate
    # system). I'll call R[1,0] = R3 and R[1,1] = R4 . 

    v_abs = sqrt(v[0] ** 2 + v[1] ** 2)
    R1 =  X(v) / v_abs
    R2 =  Y(v) / v_abs
    R3 = -Y(v) / v_abs
    R4 =  X(v) / v_abs


    # The letters x and y are denoting x and y components of vectors
    # p0, p1, m0, m1, and u.

    p0x = p0[0]; p0y = p0[1]
    p1x = p1[0]; p1y = p1[1]
    m0x = m0[0]; m0y = m0[1]
    m1x = m1[0]; m1y = m1[1]
    ux = X(u); uy = Y(u)

    #
    #
    #   R3(h00(t) p0x + h10(t) m0x + h01(t) p1x + h11(t) m1x - ux) +
    # + R4(h00(t) p0y + h10(t) m0y + h01(t) p1y + h11(t) m1y - uy) = 0
    #
    # Opening all parentheses and simplifying for hxx we get:
    #
    #   h00(t) p0x R3 + h10(t) m0x R3 + h01(t) p1x R3 + h11(t) m1x R3 - ux R3 +
    # + h00(t) p0y R4 + h10(t) m0y R4 + h01(t) p1y R4 + h11(t) m1y R4 - uy R4 = 0
    # 
    #   h00(t) p0x R3 + h10(t) m0x R3 + h01(t) p1x R3 + h11(t) m1x R3 - ux R3 + 
    # + h00(t) p0y R4 + h10(t) m0y R4 + h01(t) p1y R4 + h11(t) m1y R4 - uy R4 = 0
    # 
    #   (1)
    #   h00(t) (p0x R3 + p0y R4) + h10(t) (m0x R3 + m0y R4) + 
    #   h01(t) (p1x R3 + p1y R4) + h11(t) (m1x R3 + m1y R4) - (ux R3 + uy R4) = 0
    #
    # We now introduce new substitution

    K00 = p0x * R3 + p0y * R4
    K10 = m0x * R3 + m0y * R4
    K01 = p1x * R3 + p1y * R4
    K11 = m1x * R3 + m1y * R4
    U = ux * R3 + uy * R4

    # Expressed in those terms, equation (1) above becomes
    #
    # h00(t) K00 + h10(t) K10 + h01(t) K01 + h11(t) K11 - U = 0
    #
    # We will now substitute the expressions for hxx(t) functions
    #
    # (2t^3 - 3t^2 + 1) K00 + (t^3 - 2t^2 + t) K10 + (-2t^3 + 3t^2) K01 + (t^3 - t^2) K11 - U = 0
    # 
    #   2 K00 t^3 - 3 K00 t^2 + K00 + 
    # + K10 t^3 - 2 K10 t^2 + K10 t - 
    # - 2 K01 t^3 + 3 K01 t^2 + 
    # + K11 t^3  - K11 t^2 - U = 0
    # 
    #   2 K00 t^3 - 3 K00 t^2 +    0t +  K00 
    # + K10   t^3 - 2 K10 t^2 + K10 t
    # - 2 K01 t^3 + 3 K01 t^2 
    # +   K11 t^3 -   K11 t^2 +    0t -   U = 0
    # 
    #  (2 K00 + K10 - 2K01 + K11) t^3 
    # +(-3 K00 - 2K10 + 3 K01 - K11) t^2
    # + K10 t
    # + K00 - U = 0
    # 
    # 
    # (2 K00 + K10 - 2K01 + K11) t^3 + (-3 K00 - 2K10 + 3 K01 - K11) t^2 + K10 t + K00 - U = 0
    #
    # All we need now is to solwe a cubic equation
    valuesOfT = cubicRoots((2 * K00 + K10 - 2 * K01 + K11),
                           (-3 * K00 - 2 * K10 + 3 * K01 - K11),
                           (K10),
                           K00 - U)
    # We can then put the values of it into our original spline segment
    # formula to find the potential intersection points.  Any point
    # that's on original line segment is an intersection

    def h00(t): return 2 * t**3 - 3 * t**2 + 1
    def h10(t): return t**3 - 2 * t**2 + t
    def h01(t): return -2 * t**3 + 3 * t**2
    def h11(t): return t**3 - t**2

    intersections = []
    for t in valuesOfT:
        if t < 0 or t > 1.0: continue
        # point = h00(t) * p0 + h10(t) * m0 + h01(t) * p1 + h11(t) * m1
        point = add_points(
            scale_point(h00(t), p0),
            scale_point(h10(t), m0),
            scale_point(h01(t), p1),
            scale_point(h11(t), m1)
            )

        if pointOnLineSegment(l1, l2, point): intersections.append(point)


    return intersections

def findIntersectionsManyCurves(p0_array, p1_array, m0_array, m1_array, u, v):
    result = [];
    for (p0, p1, m0, m1) in itertools.izip(p0_array, p1_array, m0_array, m1_array):
        result.extend(findIntersections(p0, p1, m0, m1, u, v))
    return result


def findIntersectionsManyCurvesManyLines(p0, p1, m0, m1, points):
    result = [];

    for (u,v) in itertools.izip(*[iter(points)]*2):
        result.extend(findIntersectionsManyCurves(p0, p1, m0, m1, u, v))

    return result

class EventsEmitter(object):
    def __init__(self):
        self.consumers = []

    def emit(self, eventName, *params):
        for method in self.consumers:
            funcName = method.im_func.func_name if hasattr(method, "im_func") else method.func_name
            if funcName == eventName:
                method(*params)
    def register(self, method):
        self.consumers.append(method)

    def unregister(self, method):
        self.consumers.remove(method)



class BunchOfPointsModel(EventsEmitter):
    def __init__(self):
        EventsEmitter.__init__(self)
        self.pts = []


    def points(self):
        return self.pts.__iter__()

    def pointsSequence(self):
        return tuple(self.pts)

    def have(self, point):
        return point in self.pts

    def addPoint(self,p):
        self.pts.append(p)
        self.emit("pointsChanged", p)

    def replacePoint(self, oldP, newP):
        idx = self.pts.index(oldP)
        self.pts[idx] = newP
        self.emit("pointsChanged", newP)


    def removePoint(self, p):
        self.point.remove(p)
        self.emit("pointsChanged", p)


class BunchOfPointsCompositeModel(object):
    def __init__(self, m1, m2):
        self.m1 = m1
        self.m2 = m2

    def points(self):
        return itertools.chain(self.m1.points(), self.m2.points())

    def have(self, point):
        return self.m1.have(point) or self.m2.have(point)


    def replacePoint(self, oldP, newP):
        if self.m1.have(oldP):
            self.m1.replacePoint(oldP, newP)
        else:
            self.m2.replacePoint(oldP, newP)

    def removePoint(self, p):
        if self.m1.have(p):
            self.m1.removePoint(p)
        else:
            self.m2.removePoint(p)

    def register(self, method):
        self.m1.register(method)
        self.m2.register(method)

    def unregister(self, method):
        self.m1.unregister(method)
        self.m2.unregister(method)

class BunchOfPointsDragController(EventsEmitter):
    def __init__(self, model):
        EventsEmitter.__init__(self)
        self.model = model
        self.draggedPoint = None

    def mouseMovedTo(self, x,y):
        if self.draggedPoint != None:
            newPoint = (x,y)
            draggedPoint = self.draggedPoint
            self.draggedPoint = newPoint
            self.model.replacePoint(draggedPoint, newPoint)
    def buttonDown(self, x,y):
        if self.draggedPoint == None:
            closePoint = self.getCloseEnoughPoint(x,y)
            if closePoint != None:
                self.draggedPoint = closePoint
                self.emit("dragPointChanged",closePoint)

    def buttonUp(self, x,y):
        self.mouseMovedTo(x,y)
        self.draggedPoint = None
        self.emit("dragPointChanged", None)

    def getCloseEnoughPoint(self, x,y):
        minSquareDistance = 25
        closestPoint = None
        for point in self.model.points():
            dx = X(point) - x
            dy = Y(point) - y
            distance = dx*dx + dy*dy
            if minSquareDistance > distance:
                closestPoint = point
                minSquareDistance = distance
        return closestPoint

    def isDraggedPoint(self, p):
        return p is self.draggedPoint

# class CurvesLinesViewPointsView(object):
#     def __init__(self, screen, modelCurves, modelLines, model, controller):
#         self.screen = screen
#         self.modelLines = modelLines
#         self.modelCurves = modelCurves
#         self.controller = controller
#         controller.register(self.dragPointChanged)
#         model.register(self.pointsChanged)

#     def draw(self):
#         self.screen.fill(Color("black"))
#         pygame.draw.lines(self.screen, Color("cyan"), 0, self.modelLines.pointsSequence(), 3)
#         (p0, p1, m0, m1) =  padlib.BezierCurve(screen,modelCurves.pointsSequence(),3,100,Color("magenta"))

#         self.drawPointSet(self.modelCurves.points(),
#                           lambda(p):self.controller.isDraggedPoint(p),
#                           Color("white"), Color("red"))
#         self.drawPointSet(self.modelLines.points(),
#                           lambda(p):self.controller.isDraggedPoint(p),
#                           Color("lightgray"), Color("red"))


#         self.drawSimplePointSet(findIntersectionsManyCurvesManyLines(p0, p1, m0, m1,self.modelLines.points()),
#                           Color("blue"))




#     def drawSimplePointSet(self, points, normalColor):
#         self.drawPointSet(points, lambda(p):True, None, normalColor);

#     def drawPointSet(self, points, specialPoint, normalColor, specialColor):
#         for p in points:
#             if specialPoint(p):
#                 draw.circle(self.screen, specialColor, p, 6)
#             else:
#                 draw.circle(self.screen, normalColor, p, 2)
#         pygame.display.update()

#     def dragPointChanged(self, p): self.draw()
#     def pointsChanged(self, p): self.draw()


# class PygameEventsDistributor(EventsEmitter):
#     def __init__(self):
#         EventsEmitter.__init__(self)
#     def processEvent(self, e):
#         if e.type == MOUSEMOTION:
#             self.emit("mouseMovedTo", e.pos[0], e.pos[1])
#         elif e.type == MOUSEBUTTONDOWN:
#             self.emit("buttonDown", e.pos[0], e.pos[1])
#         elif e.type == MOUSEBUTTONUP:
#             self.emit("buttonUp", e.pos[0], e.pos[1])


# modelLines = BunchOfPointsModel()
# modelCurves = BunchOfPointsModel()
# model = BunchOfPointsCompositeModel(modelLines, modelCurves);
# controller = BunchOfPointsDragController(model)

# distributor = PygameEventsDistributor()
# distributor.register(controller.mouseMovedTo)
# distributor.register(controller.buttonUp)
# distributor.register(controller.buttonDown)

# pygame.init()
# screen = pygame.display.set_mode((640, 480))

# modelCurves.addPoint((29,34))
# modelCurves.addPoint((98,56))
# modelCurves.addPoint((200, 293))
# modelCurves.addPoint((350, 293))

# modelLines.addPoint((23,123))
# modelLines.addPoint((78,212))

# view = CurvesLinesViewPointsView(screen, modelCurves, modelLines, model, controller)


# keepGoing = True

# try:
#     while (keepGoing):
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 keepGoing = False
#                 break
#             distributor.processEvent(event)
#         pass
# finally:
#     pygame.quit()


def cubicRoots(a,b,c,d):
    A, B, C = b/a, c/a, d/a;
    
    S, T, Im
 
    Q = (3*B - A**2)/9;
    R = (9*A*B - 27*C - 2*A**3)/54;
    D = Q**3 + R**2 #polynomial discriminant
 
    t = []]
 
    if D >= 0: # complex or duplicate roots
        S = sgn(R + sqrt(D))*Math.pow(Math.abs(R + Math.sqrt(D)),(1/3));
        T = sgn(R - Math.sqrt(D))*Math.pow(Math.abs(R - Math.sqrt(D)),(1/3));
 
        t[0] = -A/3 + (S + T);                    // real root
        t[1] = -A/3 - (S + T)/2;                  // real part of complex root
        t[2] = -A/3 - (S + T)/2;                  // real part of complex root
        Im = Math.abs(Math.sqrt(3)*(S - T)/2);    // complex part of root pair   
 
        /*discard complex roots*/
        if (Im!=0)
        {
            t[1]=-1;
            t[2]=-1;
        }
 
    }
    else                                          // distinct real roots
    {
        var th = Math.acos(R/Math.sqrt(-Math.pow(Q, 3)));
 
        t[0] = 2*Math.sqrt(-Q)*Math.cos(th/3) - A/3;
        t[1] = 2*Math.sqrt(-Q)*Math.cos((th + 2*Math.PI)/3) - A/3;
        t[2] = 2*Math.sqrt(-Q)*Math.cos((th + 4*Math.PI)/3) - A/3;
        Im = 0.0;
    }
 
    /*discard out of spec roots*/
    for (var i=0;i<3;i++) 
        if (t[i]<0 || t[i]>1.0) t[i]=-1;
 
    /*sort but place -1 at the end*/
    t=sortSpecial(t);
 
    console.log(t[0]+" "+t[1]+" "+t[2]);
    return t;
}