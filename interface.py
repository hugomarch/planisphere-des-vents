import pygame, math
from pygame.locals import *

from wind_reader import get_day_wind_data
from interpolation import get_wind_at_coord

greenwich_x_frac = 0.5

def mercator(lon, lat, w, h):
    return int(((greenwich_x_frac + lon/360)%1)*w), int(h*(lat+90)/180)

def main():

    #loading the winds
    #conn = create_connection("wind.db")
    #wind = get_wind(conn)
     
    # initialize the pygame module
    pygame.init()
    pygame.key.set_repeat(10)

    W, H = 1280,960

     
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((W, H))
    world = pygame.image.load("world-map.jpg")
    world_copy = pygame.image.load("world-map.jpg")

    double_world = pygame.Surface((world.get_width(), world.get_height()))
    double_world.blit(world_copy, (0,0))
    double_world.blit(world_copy, (world.get_width(),0))

    x, y = 0, 0

    dx = world.get_width()//144
    dy = world.get_height()//72
    dscale = 0.01
    min_scale,max_scale = 0.5,10
     
    # define a variable to control the main loop
    running = True

    drag = False
    scale = 1

    def get_coords_after_scale(cur_coords,scale_center,cur_scale,incr_scal):
        cur_x,cur_y = cur_coords
        center_x,center_y = scale_center
        ratio = 1+incr_scale/cur_scale
        new_x = center_x + ratio * (cur_x - center_x)
        new_y = center_y + ratio * (cur_y - center_y)
        return (new_x,new_y)
     
    # main loop
    while running:

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == K_LEFT:
                    x += 1
                if event.key == K_RIGHT:
                    x -= 1
                if event.key == K_UP:
                    y += 1
                if event.key == K_DOWN:
                    y -= 1


                 # scale
                incr_scale = 0
                if event.key == K_PLUS or event.key == K_KP_PLUS:
                    incr_scale = dscale
                if event.key == K_MINUS or event.key == K_KP_MINUS:
                    incr_scale = -dscale
                elif event.type == pygame.MOUSEWHEEL:
                    scroll = event.y
                    incr_scale = scroll*dscale
                mouse_x,mouse_y = pygame.mouse.get_pos()
                new_scale = max(min_scale,min(scale+incr_scale,max_scale))
                x,y = get_coords_after_scale((x,y),(mouse_x,mouse_y),scale,new_scale-scale)
                scale = new_scale


            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:            
                    drag = True
                    mouse_x, mouse_y = event.pos
                    offset_x = x - mouse_x
                    offset_y = y - mouse_y
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:            
                    drag = False
            elif event.type == pygame.MOUSEMOTION:
                if drag:
                    mouse_x, mouse_y = event.pos
                    x = mouse_x + offset_x
                    y = mouse_y + offset_y
           
        #unzoomed world manipulation drawbord
        world = world_copy.copy()
        _w, _h = world.get_width(), world.get_height()
        pygame.draw.line(world, (0, 0, 255), mercator(0, 90, _w, _h), mercator(0, -90, _w, _h))

        
        #logic

        (-x, -y)
        W/scale
        H/scale

        small_window = world.subsurface((-x, -y, int(W/scale)+1), int())

        world = pygame.transform.scale(world, (int(scale*_w),int(scale*_h)))
        x %= world.get_width()
        y = max(-world.get_height()+H, min(y, 0))


        #render
        screen.blit(world, (x, y))
        screen.blit(world, (x - world.get_width(), y))
        pygame.draw.circle(screen, (0,0,0), (x, y), 10)
        pygame.draw.circle(screen, (255,0,0), (x - world.get_width(), y), 10)

        step = 100
        


        pygame.display.flip()
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
