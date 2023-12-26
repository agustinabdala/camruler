# camruler
cam ruler with openCV to measure metal plate cutouts.

# Explanation of Changes:

    ## Save Presets:
        save_presets(filename): This function retrieves the current positions of all trackbars and saves them to a JSON file. It is triggered by pressing the 's' key.

    ## Load Presets:
        load_presets(filename): This function reads the slider values from a JSON file and sets the sliders to these values. It is called at the start of the main function.

    ## Trackbar Initialization:
        create_trackbar_window(): Initializes the trackbars for all the adjustable parameters.

    ## Trigger Save and Load:
        In the main loop, pressing 's' saves the current slider settings to a file.

# How to Use:

    Run the script. Adjust the sliders as needed.
    Press 's' to save the current settings to presets.json.
    The next time you run the script, it will load the saved presets automatically.

This setup allows you to easily save and load your preferred configurations, making it convenient to switch between different setups.











Source idea/initial code: https://www.youtube.com/watch?v=1CVmjTcSpIw
Another source: https://github.com/alexyev/ObjectSizeEstimation
                https://www.youtube.com/watch?v=2oTUd2cN37k&t=25s   ==> demo video
                https://medium.com/@alexanderyevchenko/building-a-virtual-ruler-82694d821d61  ==> Explanation

COLOR COUNT: https://github.com/codegiovanni/Counting_by_color


#OpenCV package proposed to use in this project: 
-   pip install opencv-contrib-python

#para listar cams en linux 
-   ls -la /dev/

#use gopro with openCV
-   https://youtu.be/Wi6aMYFSwcA
-   pip install goprocam
-   https://pypi.org/project/goprocam/
-   https://github.com/KonradIT/gopro-py-api/blob/master/docs/docs.md

#Mas info
-   https://pyimagesearch.com/2016/03/28/measuring-size-of-objects-in-an-image-with-opencv/
-   TEXT DETECTION https://pyimagesearch.com/2018/08/20/opencv-text-detection-east-text-detector/
-   TEXT DETECTION https://pyimagesearch.com/2018/09/17/opencv-ocr-and-text-recognition-with-tesseract/
-   TEXT DETECTION https://www.geeksforgeeks.org/text-detection-and-extraction-using-opencv-and-ocr/



#PROCEDIMIENTO
- leer codigo
- traer espesor db
- tomar foto
