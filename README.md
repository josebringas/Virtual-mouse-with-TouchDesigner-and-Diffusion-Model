# Virtual-mouse-with-TouchDesigner-and-Diffusion-Model
Simulate virtual mouse clicks to interact with Touchdesigner while running a diffusion model plugin to re-generate existing animations.  

Py file are ready to use, I've added notes inbetween the code explaining what is happening in case you wonder. (Else you can always ask your preferred AI chatbot about it ;)  

It's strongly recommended to follow a TouchDiffusion online tutorial to have it working inside TouchDesigner properly. I followed this one: https://www.youtube.com/watch?v=3WqUrWfCX1A&t  

Make sure to install all packages inside py to run successfully the scripts on your preferred IDE. You can double-check those libraries in the py scripts provided.  

Maybe I haven't explain what TouchDesigner is, in case you're new to it, it's a realtime software that allows to create graphics that can be driven by data from multiple input sources (webcam, audio, sensors, etc). making it extremely flexible for content creation.

![GIF_touchdesigner_01](https://github.com/user-attachments/assets/bed93029-cdb0-49a9-b77e-5a99084526bb)
Stable Diffusion Plugin installed and working properly inside Touchdesigner


https://github.com/user-attachments/assets/9470fa3b-da98-45b8-9b50-abdd193724f6
early testings using OpenCV to enable gesture-driven features like mouse moving or clicking modes.


# Considerations:
1. I'm running python version 3.8.0 because Mediapipe didn't seem to be running on later versions (at least for me).
2. I'm using TouchDiffusion main version. I've tried to install the portable version but it simply won't run. Don't get discourage if either versions don't work properly at first. Reinstalling the main version seemed to work for me.
3. In the -Mouse In- node inside TouchDesigner, you have to adapt the mouse screen values according to the extension of your screen. Check the min/max values for up/down and left/right edges and adjust acccordingly.
