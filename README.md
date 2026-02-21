# Red Light Green Light - Computer Vision Game

## Project Overview

This project implements the **Red Light Green Light game** using computer vision.
The system uses a webcam to detect player motion and enforce the rules of the game.

The game alternates between **GREEN** and **RED** phases. During GREEN, the player must move. During RED, the player must remain still. Motion is detected using frame-to-frame image differences.

---

## Technologies Used

* Python
* OpenCV
* NumPy
* Webcam motion detection

---

## Game Rules

* Game starts in **GREEN** state.
* Player must move during GREEN.
* System switches to **RED** after a random duration.
* During RED, the player must remain still.
* Movement during RED beyond a threshold causes **death**.
* If the player survives RED, the game continues.

Additional rule:

* If the player does not move during GREEN for too long, a **WARNING** is shown.
* Continued inactivity results in **DEAD**.

---

## Motion Detection Algorithm

Motion is computed using frame-to-frame differences.

Steps:

1. Capture webcam frame.
2. Resize frame to width 640.
3. Convert frame to grayscale.
4. Apply Gaussian blur to reduce noise.
5. Compute difference between current and previous frame.

Motion score:

motion_score = mean(abs(current_gray - previous_gray)) / 255

Higher values indicate more movement.

---

## State Machine Design

The game operates using a state machine with four states:

GREEN
RED
WARNING
DEAD

### GREEN

* Player must move.
* Idle timer starts if motion is below threshold.

### WARNING

* Triggered when idle timer exceeds warning limit.

### RED

* Player must remain still.
* Movement beyond threshold causes death.

### DEAD

* Game over state.

---

## Parameters Used

green_move_threshold = 0.004

red_move_threshold_base = 0.005

red_move_threshold = red_move_threshold_base + (level - 1) * 0.003 for level increase

red_grace_ms = 650

idle_warning_ms = 1800

idle_death_ms = 3600

green_duration = 2600–4200 ms

red_duration = 1700–2900 ms

---

## Demo Video

Unlisted YouTube link:

(Add your video link here)

---

## How to Run

1. Install dependencies:

```
pip install -r requirements.txt
```

2. Run the game:

```
python rlgl_game.py
```

Press **R** to restart.

Press **Q** to quit.

---

## Prepared by

Josep Melvin L. ARguelles
