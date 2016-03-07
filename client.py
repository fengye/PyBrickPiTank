import sys
import ctypes
from sdl2 import *
from socket import *
import sys


HOST, PORT = 'dex', 9999
def main():
    print("Start")
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_JOYSTICK)
    window = SDL_CreateWindow(b"PyBrickPiTank Client",
                              SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
                              592, 460, SDL_WINDOW_SHOWN)
    windowsurface = SDL_GetWindowSurface(window)

    SDL_GameControllerAddMappingsFromFile("gamecontrollerdb.txt")

    gamepad = SDL_JoystickOpen(0)
    print(gamepad)

    sock = socket(AF_INET, SOCK_DGRAM)

    l_axis = 0 + 128
    r_axis = 0 + 128

    running = True
    event = SDL_Event()
    while running:

        while SDL_PollEvent(ctypes.byref(event)) != 0:
            # print(event.type)
            if event.type == SDL_QUIT:
                running = False
                break

            if event.type == SDL_JOYAXISMOTION:
                # if event.jaxis.value >= 3200 or event.jaxis.value <= -3200:
                if event.jaxis.axis == 1:
                    l_axis = event.jaxis.value >> 8
                    l_axis = l_axis + 128
                    data = bytearray()

                    data.append(l_axis)
                    data.append(r_axis)
                    
                    try:
                        sock.sendto(data, (HOST, PORT))
                    except:
                        pass
                    print("Gamepad Left Y: %d, %d" % (event.jaxis.axis, event.jaxis.value))
                if event.jaxis.axis == 3:
                    r_axis = event.jaxis.value >> 8
                    r_axis = r_axis + 128
                    data = bytearray()

                    data.append(l_axis)
                    data.append(r_axis)
                    
                    try:
                        sock.sendto(data, (HOST, PORT))
                    except:
                        pass
                    print("Gamepad Right Y: %d, %d" % (event.jaxis.axis, event.jaxis.value))
                break




    SDL_JoystickClose(gamepad)
    SDL_DestroyWindow(window)
    SDL_Quit()
    return 0

if __name__ == "__main__":
    sys.exit(main())