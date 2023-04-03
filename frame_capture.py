import time
import threading,queue
import numpy as np
import cv2

# ------------------------------
# Camera Tread
# ------------------------------

class Camera_Thread:

    # IMPORTANT: a queue is much more efficient than a deque
    # the queue version runs at 35% of 1 processor
    # the deque version ran at 108% of 1 processor

    # ------------------------------
    # User Instructions
    # ------------------------------

    # Using the user variables (see below):
    # Set the camera source number (default is camera 0).
    # Set the camera pixel width and height (default is 640x480).
    # Set the target (max) frame rate (default is 30).
    # Set the number of frames to keep in the buffer (default is 4).
    # Set buffer_all variable: True = no frame loss, for reading files, don't read another frame until buffer allows
    #                          False = allows frame loss, for reading camera, just keep most recent frame reads

    # Start camera thread using self.start().

    # Get next frame in using self.next(black=True,wait=1).
    #    If black, the default frame value is a black frame.
    #    If not black, the default frame value is None.
    #    If timeout, wait up to timeout seconds for a frame to load into the buffer.
    #    If no frame is in the buffer, return the default frame value.

    # Stop the camera using self.stop()

    # ------------------------------
    # User Variables
    # ------------------------------

    # camera setup
    camera_source = 0
    camera_width = 640
    camera_height = 480
    camera_frame_rate = 30
    camera_fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    # 2nd main option: camera_fourcc = cv2.VideoWriter_fourcc(*"YUYV")

    # buffer setup
    buffer_length = 5
    buffer_all = False

    # ------------------------------
    # System Variables
    # ------------------------------

    # camera
    camera = None
    camera_init = 0.5

    # buffer
    buffer = None

    # control states
    frame_grab_run = False
    frame_grab_on = False

    # counts and amounts
    frame_count = 0
    frames_returned = 0
    current_frame_rate = 0
    loop_start_time = 0

    # ------------------------------
    # Functions
    # ------------------------------

    def start(self):

        # buffer
        if self.buffer_all:
            self.buffer = queue.Queue(self.buffer_length)
        else:
            # last frame only
            self.buffer = queue.Queue(1)

        # camera setup
        self.camera = cv2.VideoCapture(self.camera_source)
        self.camera.set(3,self.camera_width)
        self.camera.set(4,self.camera_height)
        self.camera.set(5,self.camera_frame_rate)
        self.camera.set(6,self.camera_fourcc)
        time.sleep(self.camera_init)

        # camera image vars
        self.camera_width  = int(self.camera.get(3))
        self.camera_height = int(self.camera.get(4))
        self.camera_frame_rate = int(self.camera.get(5))
        self.camera_mode = int(self.camera.get(6))
        self.camera_area = self.camera_width*self.camera_height

        # black frame (filler)
        self.black_frame = np.zeros((self.camera_height,self.camera_width,3),np.uint8)

        # set run state
        self.frame_grab_run = True
        
        # start thread
        self.thread = threading.Thread(target=self.loop)
        self.thread.start()

    def stop(self):

        # set loop kill state
        self.frame_grab_run = False
        
        # let loop stop
        while self.frame_grab_on:
            time.sleep(0.1)

        # stop camera if not already stopped
        if self.camera:
            try:
                self.camera.release()
            except:
                pass
        self.camera = None

        # drop buffer
        self.buffer = None

    def loop(self):

        # load start frame
        frame = self.black_frame
        if not self.buffer.full():
            self.buffer.put(frame,False)

        # status
        self.frame_grab_on = True
        self.loop_start_time = time.time()

        # frame rate
        fc = 0
        t1 = time.time()

        # loop
        while 1:

            # external shut down
            if not self.frame_grab_run:
                break

            # true buffered mode (for files, no loss)
            if self.buffer_all:

                # buffer is full, pause and loop
                if self.buffer.full():
                    time.sleep(1/self.camera_frame_rate)

                # or load buffer with next frame
                else:
                    
                    grabbed,frame = self.camera.read()

                    if not grabbed:
                        break

                    self.buffer.put(frame,False)
                    self.frame_count += 1
                    fc += 1

            # false buffered mode (for camera, loss allowed)
            else:

                grabbed,frame = self.camera.read()
                if not grabbed:
                    break

                # open a spot in the buffer
                if self.buffer.full():
                    self.buffer.get()

                self.buffer.put(frame,False)
                self.frame_count += 1
                fc += 1

            # update frame read rate
            if fc >= 10:
                self.current_frame_rate = round(fc/(time.time()-t1),2)
                fc = 0
                t1 = time.time()

        # shut down
        self.loop_start_time = 0
        self.frame_grab_on = False
        self.stop()

    def next(self,black=True,wait=0):

        # black frame default
        if black:
            frame = self.black_frame

        # no frame default
        else:
            frame = None

        # get from buffer (fail if empty)
        try:
            frame = self.buffer.get(timeout=wait)
            self.frames_returned += 1
        except queue.Empty:
            #print('Queue Empty!')
            #print(traceback.format_exc())
            pass

        # done
        return frame
