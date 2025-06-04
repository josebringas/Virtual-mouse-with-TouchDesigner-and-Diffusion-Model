# Gesture-Controlled Real-Time AI Animation
Exhibited at the Art Gallery of Ontario, March 2025

![ago-2](https://github.com/user-attachments/assets/6855c2f8-be48-4f7b-a03f-2973bc0dddc1)

## Project Overview
The Microscopic is a real-time generative AI system exhibited as a public video mapping installation. It merges multimodal user input with diffusion-based image generation to create immersive, reactive visuals. The project was designed to test how human gestures can condition and control AI imagery in live settings, using a custom pipeline that combines gesture recognition with a diffusion model conditioning.

![ago-3](https://github.com/user-attachments/assets/0373b508-839f-4453-a435-9c500e7eee41)

## Objectives
* Explore gesture-based control as a creative input for AI visual systems.
* Investigate image conditioning using predefined animations and structure-aware prompts.
* Demonstrate live integration between user input and Stable Diffusion using the [TouchDiffusion](https://github.com/olegchomp/TouchDiffusion) plugin for TouchDesigner.

## Gesture Control System
This system implements a rule-based classifier using `cvzone.HandTrackingModule`, `OpenCV`, and `autopy` to translate webcam-captured hand landmarks into real-time interaction modes:

## Modes Implemented:
1. Virtual Mouse – Controls the mouse using the index fingertip position.
2. Zoom Mode – Recognizes two-hand gestures to scale and reposition images.

![ago-2-ezgif com-optimize](https://github.com/user-attachments/assets/f737ca69-64a9-4ec8-9107-a144e522c43d)

## Key Libraries:
* [cvzone](https://github.com/cvzone/cvzone)
* OpenCV
* autopy
* socket (for UDP communication with TouchDesigner)

## Code Features:
* Smoothed pointer movement using interpolation.
* click recognition based on hand pose (index + middle finger clse together).
* Zoom level control by measuring distance between both hands.
* UDP data transmission of gestures states and zoom values to TouchDesigner.

See code example in `VirtualMouse_GestureControl_v02.py` (add this as a file to your repo).

## Diffusion Image Generation
We used [TouchDiffusion](https://github.com/olegchomp/TouchDiffusion), a real-time implementation of Stable Diffusion in TouchDesigner.

## Conditioning Strategy
* Noise Map: The default randomness input.
* Author-Controlled RGB Animation: A high contrast particle-based animation was used as a second conditioning map. This helped the model "preserve the structure" while allowing creative variation.
* Gesture Input: Gestures sent via UDp dynamically transformed or influenced the diffusion parameters during runtime.

![GIF_touchdesigner_01](https://github.com/user-attachments/assets/bed93029-cdb0-49a9-b77e-5a99084526bb)

This conditioning approach allowed the diffusion model to maintain coherence with the structured reference (e.g., particle animations) while introducing stylistic variation bassed on the noise.

![PXL_20250604_025615794 (1)](https://github.com/user-attachments/assets/8947c587-2d1f-42e7-8f1b-b48e33d15a3c)

## Future Possibilities
While The Microscopic was designed as a standalone installation, its architecture opens doors to future uses in:
* Theater and Live Performance (gesture-driven control of VFX, lighting, sound)
* Prototype testing for multimodal AI interaction
* Creative gaming and memory-based physical interaction systems
The combination of authored animations, structured prompts, and reactive gesture input makes this system ideal for immersive, performative applications!

## Acknowledgments
* [TouchDiffusion by @olegchomp](https://github.com/olegchomp/TouchDiffusion)
* [cvzone](https://github.com/cvzone/cvzone)
* OpenCV, autopy, and TouchDesigner community
* [Paketa12 on Youtube].(https://www.youtube.com/watch?v=w47xTWMNTFA&t)

## Considerations:
1. I'm running python version 3.8.0 because Mediapipe didn't seem to be running on later versions (at least for me).
2. I'm using TouchDiffusion main version. I've tried to install the portable version but it simply won't run. Don't get discourage if either versions don't work properly at first. Reinstalling the main version seemed to work for me.
