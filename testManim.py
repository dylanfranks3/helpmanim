from manim import *
from collections.abc import Iterable



def coord(x,y,z=0):
    return np.array([x,y,z])

def play_timeline(scene, timeline):
    previous_t = 0
    ending_time = 0
    for t, anims in sorted(timeline.items()):
        to_wait = t - previous_t
        if to_wait > 0:
            scene.wait(to_wait)
        previous_t = t
        if not isinstance(anims, Iterable):
            anims = [anims]
        for anim in anims:
            turn_animation_into_updater(anim)
            scene.add(anim.mobject)
            ending_time = max(ending_time, t + anim.run_time)
    if ending_time > t:
        scene.wait(ending_time-t)

# Abstract class:
class PathScene(Scene):
    def __init__(self):
        super().__init__()
        self.x_coords = [0,  1, 3,  -2, -3]
        self.y_coords = [3, -2, 1, 2.5, -1]
    
    """
    The setup method it is executed before the construct method, 
    so whatever they write in the setup method will be executed 
    before the construct method
    """
    def setup(self):
        self.tuples = list(zip(self.x_coords,self.y_coords))
        dots = self.get_dots(self.tuples)
        self.add(dots)

    def get_dots(self,coords):
        # This is called list comprehension, learn to use it here:
        # https://www.youtube.com/watch?v=AhSvKGTh28Q
        dots = VGroup(*[Dot(coord(x,y)) for x,y in coords])
        return dots




    def get_all_mobs(self):
        dots = self.get_dots(self.tuples)
        return dots

class ShowPoints(PathScene):
    pass



def play_timeline(scene, timeline):
    previous_t = 0
    ending_time = 0
    for t, anims in sorted(timeline.items()):
        to_wait = t - previous_t
        if to_wait > 0:
            scene.wait(to_wait)
        previous_t = t
        if not isinstance(anims, Iterable):
            anims = [anims]
        for anim in anims:
            turn_animation_into_updater(anim)
            scene.add(anim.mobject)
            ending_time = max(ending_time, t + anim.run_time)
    if ending_time > t:
        scene.wait(ending_time-t)
class DotMovingScene(Scene):
    def construct(self):
        patha = VMobject()
        pathb = VMobject()
        pathc = VMobject()
        pathd = VMobject()
        

        # Define paths
        
        patha.set_points_smoothly([2*LEFT + UP, 2*LEFT + DOWN])
        pathb.set_points_smoothly([2*RIGHT + UP, 2*RIGHT + DOWN])
        patha.set_opacity(0)
        pathb.set_opacity(0)
        
        
        def update_path_c(dot1,dot2):
            def updater(mob,dt):
                mob.set_points_smoothly([dot1.get_center(), dot2.get_center()])
            return updater
        # Add paths to the scene
        self.add(patha, pathb)
        # Create dots
        a = Dot(2*LEFT + UP)
        b = Dot(2*RIGHT + UP)
        self.add(a,b)
        pathc.set_points_smoothly([a.get_center(),b.get_center()])
        pathd.set_points_smoothly([b.get_center(),a.get_center()])
        pathc.set_opacity(0)
        pathd.set_opacity(0)

        pathc.add_updater(update_path_c(a,b))
        pathd.add_updater(update_path_c(b,a))
        vt = ValueTracker(0)
        vtd = ValueTracker(0)
        c = Dot().set_color(RED)
        d = Dot().set_color(RED)
        d.set_opacity(0)
        c.set_opacity(0)
        self.add(c,pathc,d,pathd)
        
        d.add_updater(lambda mob: mob.move_to(pathd.point_from_proportion(vtd.get_value()) ))# Using RED for visibility
        c.add_updater(lambda mob: mob.move_to(pathc.point_from_proportion(vt.get_value()) ))# Using RED for visibility
        # # Move dots along the paths
        
        anim0d = AnimationGroup(d.animate(run_time=0).set_opacity(1).build())
        anim1d = AnimationGroup(vtd.animate(run_time=2).set_value(1).build())
        anim3d = AnimationGroup(d.animate(run_time=0).set_opacity(0).build())

        anim0 = AnimationGroup(c.animate(run_time=0).set_opacity(1).build())
        anim1 = AnimationGroup(vt.animate(run_time=2).set_value(1).build())
        anim3 = AnimationGroup(c.animate(run_time=0).set_opacity(0).build())
        
        anim2 = AnimationGroup(MoveAlongPath(a, patha), MoveAlongPath(b, pathb), run_time=5, rate_func=linear)

        timeline = {
            
            1 : anim2,
            1.1 : [anim0d,anim1d],
            3.1 : anim3d,
            2 : [anim1,anim0],
            4: anim3
            
       }
        play_timeline(self,timeline)

        self.wait()

        
