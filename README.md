# Color Tester Tool
## Description
This interactive tool allows you to detect specific colors in real time using your computer's camera. It uses the LAB (Luminosity, A-axis, B-axis) color space which offers better results for color detection than traditional RGB, especially under different lighting conditions.

## Main Features
- 🎚️ LAB threshold control via trackbars
- 🎨 4 predefined colors (Blue, Red, Green, Yellow)
- 🖱️ Interactive interface with buttons for presets
- 🎥 Real-time preview of:
  - Original image
  - Detection mask
  - Applied result
- 🟦 Display of the current detected color
- ⚙️ Morphological operations to improve detection

## Requirements
- Python 3.6+
- OpenCV (`opencv-python`)
- NumPy

````bash
pip install opencv-python numpy
````

## Usage
1. Run the script:
````bash
python color_tester4.py
````

2. The interface contains:
   - **Top panel**: Trackbars to set L, A, B
   - Center buttons**: Color presets (Blue, Red, Green, Yellow)
   - Right frame**: Displays the current detected color.
   - Bottom thumbnails**:
     - Original: Live camera feed
     - Mask: Detection areas (white=detected)
     - Result: Detected objects are highlighted.


3. Controls:
   - Click colored buttons to load presets.
   - Adjust trackbars to refine detection.
   - Press ‘Q’ to exit

## Customization
To add/modify predefined colors, edit the `predefined_colors` dictionary:

````python
predefined_colors = {
 "Orange": {"low": [40, 150, 100], "high": [100, 255, 200]},
 "Purple": {"low": [30, 100, 50], "high": [150, 180, 180]}
}
````

## Adjustable Parameters
| Parameter | Description | Range |
| ----------- | ------------- | -------|
| L (Brightness) | Light Intensity | 0-255 |
| A (Green-Red Axis) | Green (-) to Red (+) | 0-255 |
| B (Blue-Yellow Axis) | Blue (-) to Yellow (+) | 0-255 | | 0-255 |

## Tips for Better Detection
1. Start with a preset close to the target color.
2. Set channel A (green-red) first.
3. Then adjust channel B (blue-yellow).
4. Finally adjust L (brightness) for different light conditions.
5. Use uniform objects for initial calibration

## Troubleshooting
- If no video is detected: Verify camera is available (change `0` to `1` in `VideoCapture` if using external camera).
- Inconsistent detection: Reduce kernel size in morphological operations.
- Illumination changes: Recalibrate L values.

## Flowchart: Color Detection Tool

````mermaid
graph TD
 A[Start] --> B[Initialize LAB parameters]
 B --> C[Define predefined colors]
 C --> D[Create control window]
 D --> E[Configure trackbars]
 E --> F[Start video capture]
 F --> G[Configure mouse callback]
    
    G --> H{Main loop}
    H --> I[Capture camera frame]
 I --> J[Convert to LAB]
 J --> K[Get trackbars values]
 K --> L[Create mask with LAB thresholds]
 L --> M[Apply morphological operations]
 M --> N[Apply mask to frame] M --> N --> N[Apply mask to frame]
    
    N --> O[Build control panel]
 O --> P[Draw trackbars section]
 P --> Q[Draw preset buttons]
 Q --> R[Calculate detected color]
 R --> S[Show color chart]
 S --> T[Show video thumbnails]
    
    T --> U --> U[Show full panel]
 U --> V --> V{Key pressed?}
    V --> | 'q'| W[Release resources]
 V --> | Other key| H
 W --> X[End]
    
    click G callback_mouse
 click Q buttons_presets
    
    subgraph Mouse Callback
 callback_mouse[Click event] --> C1{Click on button?}
        C1 --> |Yes| C2[Load preset]
 C1 --> |No| C3[Ignore]
 end
    
    subgraph Buttons Presets
 buttons_presets[Draw buttons] --> D1[For each color]
 D1 --> D2[Draw rectangle]
 D2 --> D3[Add text]
 end
``` end ```