# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 15:28:23 2018

@author: asdftoger
"""
import matplotlib.pyplot as plt
import numpy as np
import sys

from matplotlib import patches
import matplotlib.animation as animation

def calc_th_b(a,b,c,d,th_a,mode='open',show_angle=False):
    '''
    Calculates theta b using Freuedenstein equations
    '''
    K1 = d/a
    K4 = d/b
    K5 = (-a**2-b**2+c**2-d**2)/(2*a*b)
    D = np.cos(th_a) - K1 + K4*np.cos(th_a) + K5
    E = -2*np.sin(th_a)
    F = K1 + (K4-1)*np.cos(th_a) + K5
    disc = (E**2)-4*D*F 
    #Checks if non-grashoff, and extracts the valid angles
    if not(np.greater_equal(disc,0).all()):
        #This extracts the th_a elements with discriminants > 0 and reruns the function.
        condition = np.greater_equal(disc,0)
        th_a = np.extract(condition, th_a)
#        condition = np.less_equal(th_a, np.pi)
#        th_a= np.extract(condition,th_a)
        th_a=np.append(th_a,th_a[-2::-1])
        _,th_b=calc_th_d(a,b,c,d,th_a)
    else:
        th_b=2*np.arctan((-E - np.sqrt(disc) )/(2*D)) if mode=='open' else 2*np.arctan((-E + np.sqrt(disc) )/(2*D))
    if show_angle:
        plt.plot(th_a,th_b)
        plt.show()    
    return th_a,th_b    

def calc_th_d(a,b,c,d,th_a,mode='open',show_angle=False):
    '''
    Calculates theta d using Freuedenstein equations
    '''
    K1 = d/a
    K2 = d/c
    K3 = (a**2-b**2+c**2+d**2)/(2*a*c)
    A = np.cos(th_a) - K1 - K2*np.cos(th_a) + K3
    B = -2*np.sin(th_a)
    C = K1 - (K2+1)*np.cos(th_a) + K3
    #Grashoff condition
    disc = (B**2)-4*A*C 
    #Checks if non-grashoff, and extracts the valid angles
    if not(np.greater_equal(disc,0).all()):#Checks grashoff?
        #This extracts the th_a elements with discriminants > 0 and reruns the function.
        condition = np.greater_equal(disc,0)
        th_a = np.extract(condition, th_a)
#        condition = np.less_equal(th_a, np.pi)
#        th_a= np.extract(condition,th_a)
        th_a=np.append(th_a,th_a[-2::-1])#Full range of non-grashoff motion
        _,th_d=calc_th_d(a,b,c,d,th_a)
    else:
        th_d=2*np.arctan((-B - np.sqrt(disc) )/(2*A)) if mode=='open' else 2*np.arctan((-B + np.sqrt(disc) )/(2*A))#Final formula for other fixed angle
    if show_angle:
        plt.plot(th_a,th_d)
        plt.show()
    return th_a,th_d
    
def generate_th_a(rotation='cw',step=0.1):
    return np.arange(2*np.pi,0,-step*np.pi) if rotation=='cw' else np.arange(0,2*np.pi+0.0001,step*np.pi)

def calc_joint_position(a,b,c,d,th_a):
    '''
    Calculates the position of the joints 
    '''
    th_a,th_d=calc_th_d(a,b,c,d,th_a)
#    print(th_a)
#    print(th_d)
    x1,x4 = 0,d
    y1,y4 = 0,0
    x2,x3 = a*np.cos(th_a), d + c*np.cos(th_d)
    y2,y3 = a*np.sin(th_a), c*np.sin(th_d)
    
    return x1,x2,x3,x4,y1,y2,y3,y4
def animate_linkage_motion(x1,x2,x3,x4,y1,y2,y3,y4,save_animation=False,animation_name='FourBarLinkage'):
    def animate(i,x1,x2,x3,x4,y1,y2,y3,y4):
        #This uses global angles in degrees
#        global th_a_d,patch1
#        global th_b_d,patch2
#        global th_d_d,patch4
#        
#        global arrow1,arrow2,arrow3,len_arrow
        #This draws the linkages
        thisx = [x1, x2[i],x3[i],x4]
        thisy = [y1, y2[i],y3[i],y4]
        line.set_data(thisx, thisy)
        '''
        #This draws the angles
        ax.patches.remove(patch1)
        patch1= patches.Arc((x1,y1),100,100,0,0,th_a_d[i],color='r')
        ax.add_patch(patch1)
        
        ax.patches.remove(patch2)
        patch2= patches.Arc((x2[i],y2[i]),100,100,0,0,th_b_d[i],color='g')
        ax.add_patch(patch2)
        
        ax.patches.remove(patch4)
        patch4 = patches.Arc((x4,y4),100,100,0,0,th_d_d[i],color = 'b')
        ax.add_patch(patch4)
        
        #Draws tangential component
    #    ax.patches.remove(arrow1)
    #    arrow1 = patches.Arrow(x3[i],y3[i]
    #                           ,len_arrow*v_b[i]*(np.cos(th_d[i]-th_b[i])*
    #np.cos(np.pi + th_b[i] - th_d[i]) + np.sin(th_d[i]-th_b[i])*np.sin(np.pi + th_b[i] - th_d[i]))
    #                           ,len_arrow*v_b[i]*(np.sin(th_d[i]-th_b[i])*
    #np.cos(np.pi + th_b[i] - th_d[i]) - np.cos(th_d[i]-th_b[i])*np.sin(np.pi + th_b[i] - 
    #th_d[i]))
    #                           ,width = 20,color = 'y')
    #    ax.add_patch(arrow1)
        #Draws radial component
        
        ax.patches.remove(arrow3)
        arrow3 = patches.Arrow(x3[i],y3[i],
                               len_arrow*np.cos(th_b[i])*v_b[i]*np.cos(np.pi + th_b[i]- th_d[i])
                               ,len_arrow*np.sin(th_b[i])*v_b[i]*np.cos(np.pi + th_b[i]- th_d[i])
                               ,width = 20,color = 'y')
        ax.add_patch(arrow3)
        
        #Draws actual component
        ax.patches.remove(arrow2)
        arrow2 = patches.Arrow(x3[i],y3[i],
                               len_arrow*np.cos(th_b[i])*v_b[i]
                               ,len_arrow*np.sin(th_b[i])*v_b[i]
                               ,width = 20,color = 'y')
        ax.add_patch(arrow2)
        
        #This displays the angles
    #    ax.text(x1,y1)
        text = \
        'Angle1 (red): ' + str(round(th_a_d[i],2)) + '\n' + \
        'Angle2 (green): ' + str(round(th_b_d[i],2)) + '\n' + \
        'Angle4 (blue): ' + str(round(th_d_d[i],2)) + '\n' + \
        'Speed(yellow): ' + str(round(v_b[i],2)) + '\n'
        ang_text.set_text(text)
        '''
        return line,#patch1,patch2,patch4,ang_text,arrow2,#arrow3,arrow1

    #Defining xandylims of the plot
    temp = x1,x2,x3,x4
    xmin = np.amin([np.amin(mini) for mini in temp])
    xmax = np.amax([np.amax(mini) for mini in temp])
    temp = y1,y2,y3,y4
    ymin = np.amin([np.amin(mini) for mini in temp])
    ymax = np.amax([np.amax(mini) for mini in temp])
    #xmin,xmax
    
    fig = plt.figure()
    fig.set_size_inches(6,4.8,True)
    plt.axis('off')
    plt.tight_layout()
    bord = 200 #FBL an offset
    ax = fig.add_subplot(111, autoscale_on=True,
                         xlim=(xmin-bord, xmax+bord), ylim=(ymin-bord, ymax+bord))
    ax.grid()
    #Draw linkages
    line, = ax.plot([], [], marker = 'o',c = 'k',lw = 6,ms = 10)
    '''
    len_arrow = 300
    #Max and min angles, radians
    a_min = np.amin(th_d)
    a_max = np.amax(th_d)
    #draw arrows
    ax.arrow(x4,y4,
             len_arrow * np.cos(a_min), len_arrow * np.sin(a_min),
             fc='b', ec='b')
    ax.arrow(x4,y4,
             len_arrow * np.cos(a_max), len_arrow * np.sin(a_max)
             ,fc='b', ec='b')
    #Max and min angles, degrees
    a_min = np.amin(th_d_d)
    a_max = np.amax(th_d_d)
    #Draw angle between the arrows
    ang_radius = 200 #for both drawing and writing
    ang_subtended = a_max - a_min #angle subtended
    ang_patch = patches.Arc((x4,y4),ang_radius,ang_radius,a_min,0,ang_subtended)
    ax.add_patch(ang_patch)
    
    #Write angle
    #x,y = (x4 + ang_radius*np.cos(a_min),y4 + ang_radius*np.sin(a_min))
    #s = str(round(ang_subtended,2) )
    #ang_text = ax.text(x,y,'')
    #ang_text.set_text(s)
    
    #Initialize an arc patch
    #patch1 -> angle of point1 etc.
    patch1 = patches.Arc((x1,y1),100,100,0,0,0,color='r')
    patch2 = patches.Arc((x2[0],y2[0]),100,100,0,0,0,color='g')
    patch4 = patches.Arc((x4,y4),100,100,0,0,0,color = 'b')
    
    #Transmisson angle
    len_arrow = 100
    #arrow direction: use 0[i] - 0[i-1]/dt
    v_b = (np.roll(th_d,1) - np.roll(th_d,-1))*30
    
    arrow1 = patches.Arrow(x3[0],y3[0],0,0)
    arrow2 = patches.Arrow(x3[0],y3[0],0,0)
    arrow3 = patches.Arrow(x3[0],y3[0],0,0)
    ang_text = ax.text(0.5, 0.1, '', transform=ax.transAxes)
    '''
    #Initialize lines and patches
    
    #Animate the FBL
    ani = animation.FuncAnimation(fig, animate, frames=len(y2),fargs=(x1,x2,x3,x4,y1,y2,y3,y4),
                              interval=30, blit=True)
    if save_animation:
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps = 30,extra_args=['-vcodec', 'libx264'],bitrate = 3000)
        dpi = 100
        ani.save('{}.mp4'.format(animation_name), writer = writer,dpi = dpi)
    return ani

#Linkage notation
#      . 
#     / \  
#    b    \
#   / thb   \ thc
#  .----      c----
#   \           \
#    a            \
#     \  tha        \ thd
#      .______d_______.----
if __name__=='__main__':
    case='g'
    if case=='ng':
        #Non-grashoff
        a,b,c,d = 300,500,200,200
        th_a=generate_th_a(step=0.1E-1)
        x1,x2,x3,x4,y1,y2,y3,y4=calc_joint_position(a,b,c,d,th_a)
        anim1=animate_linkage_motion(x1,x2,x3,x4,y1,y2,y3,y4)#save_animation=True,animation_name='non-grashoff_FBL')
        plt.show()
    elif case=='g':
        #Grashoff
        a,b,c,d = 50,60,200,200
        th_a=generate_th_a(step=1E-2)
        x1,x2,x3,x4,y1,y2,y3,y4=calc_joint_position(a,b,c,d,th_a)
        anim2=animate_linkage_motion(x1,x2,x3,x4,y1,y2,y3,y4,save_animation=True,animation_name='grashoff_FBL')
        plt.show()