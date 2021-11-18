from math import pi, sin, cos  
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor  
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3  
from panda3d.core import ClockObject

keyMap = {
    "up": False,
    "down": False,
    "left": False,
    "right": False,
    "rotate": False
}
def updateKeyMap(key, state):
    keyMap[key] = state


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)  

        self.disableMouse()

        self.scene = self.loader.loadModel("models/environment")
        self.scene.reparentTo(self.render)
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        self.Panda = Actor("models/panda-model",
                           {"walk": "models/panda-walk4"})
        self.Panda.setScale(0.005, 0.005, 0.005)
        self.Panda.reparentTo(self.render)

        self.Panda.loop("walk")

        self.accept("arrow_left", updateKeyMap, ["left", True])
        self.accept("arrow_left-up", updateKeyMap, ["left", False])

        self.accept("arrow_right", updateKeyMap, ["right", True])
        self.accept("arrow_right-up", updateKeyMap, ["right", False])

        self.accept("arrow_up", updateKeyMap, ["up", True])
        self.accept("arrow_up-up", updateKeyMap, ["up", False])

        self.accept("arrow_down", updateKeyMap, ["down", True])
        self.accept("arrow_down-up", updateKeyMap, ["down", False])

        self.accept("space", updateKeyMap, ["rotate", True])
        self.accept("space-up", updateKeyMap, ["rotate", False])

        self.speed=6
        self.angle=0  

        self.taskMgr.add(self.update, "update")

    def spinCameraTask(self, task):
        angleDegrees=task.time * 6.0
        angleRadians=angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

    def update(self, task):

        globalClock = ClockObject.getGlobalClock()

        dt = globalClock.getDt()

        pos = self.Panda.getPos()

        if keyMap["left"]:
            pos.x -= self.speed * dt
        if keyMap["right"]:
            pos.x += self.speed * dt
        if keyMap["up"]:
            pos.z += self.speed * dt
        if keyMap["down"]:
            pos.z -= self.speed * dt
        if keyMap["rotate"]:
            self.angle += 1  
            self.Panda.setH(self.angle)

        self.Panda.setPos(pos)

        return task.cont


app=MyApp()
mySound=app.loader.loadSfx("grasswalk.mp3")
mySound.play()
mySound.setLoop(True)
mySound.setVolume(13)
app.run()