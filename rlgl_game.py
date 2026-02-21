import cv2
import numpy as np
import time
import random

cap = cv2.VideoCapture(0)

previous_gray = None

motion_history = []

# -----------------------------
# Game Parameters (from spec)
# -----------------------------

level = 1
cycle = 1
green_move_threshold = 0.004
red_move_threshold_base = 0.005
red_move_threshold = red_move_threshold_base + (level - 1) * 0.003

red_grace_ms = 650
idle_warning_ms = 1800
idle_death_ms = 3600

green_range = (2600, 4200)
red_range = (1700, 2900)

# -----------------------------
# Game State
# -----------------------------

state = "GREEN"

green_duration = random.randint(*green_range)
red_duration = random.randint(*red_range)

state_start_time = time.time()
idle_start_time = None

# -----------------------------
# Main Loop
# -----------------------------

while True:

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640,480))

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(5,5),0)

    motion_score = 0

    if previous_gray is not None:
        diff = cv2.absdiff(gray, previous_gray)
        motion_score = np.mean(diff) / 255.0

        motion_history.append(motion_score)

        if len(motion_history) > 5:
            motion_history.pop(0)

        motion_score = sum(motion_history) / len(motion_history)
    
    previous_gray = gray

    now = time.time()
    elapsed_ms = (now - state_start_time)*1000

    # -----------------------------
    # GREEN STATE
    # -----------------------------

    if state == "GREEN":

        if motion_score < green_move_threshold:

            if idle_start_time is None:
                idle_start_time = now

            idle_time = (now - idle_start_time)*1000

            if idle_time > idle_death_ms:
                state = "DEAD"

            elif idle_time > idle_warning_ms:
                state = "WARNING"

        else:
            idle_start_time = None

        if elapsed_ms > green_duration:
            state = "RED"
            state_start_time = now
            red_duration = random.randint(*red_range)
            idle_start_time = None

    # -----------------------------
    # WARNING STATE
    # -----------------------------

    elif state == "WARNING":

        if motion_score >= green_move_threshold:
            state = "GREEN"
            idle_start_time = None

        else:
            idle_time = (now - idle_start_time)*1000
            if idle_time > idle_death_ms:
                state = "DEAD"

    # -----------------------------
    # RED STATE
    # -----------------------------

    elif state == "RED":

        if elapsed_ms > red_grace_ms:

            if motion_score > red_move_threshold:
                state = "DEAD"

        if elapsed_ms > red_duration:
            state = "GREEN"
            state_start_time = now
            green_duration = random.randint(*green_range)
            idle_start_time = None

            cycle += 1
            if cycle % 3 == 0:
                level += 1
    # -----------------------------
    # Display
    # -----------------------------

    if state == "GREEN":
        state_color = (0,255,0)   # Green

    elif state == "RED":
        state_color = (0,0,255)   # Red

    elif state == "WARNING":
        state_color = (0,255,255) # Yellow

    else:
        state_color = (255,255,255) # Default white

    cv2.putText(frame, f"State: {state}", (20,40),
                cv2.FONT_HERSHEY_SIMPLEX, 1,(state_color),2)

    cv2.putText(frame, f"Motion: {motion_score:.4f}", (20,80),
                cv2.FONT_HERSHEY_SIMPLEX, 1,(state_color),2)

    # Motion bar settings
    bar_x = 20
    bar_y = 120
    bar_width = 200
    bar_height = 20

    # Scale motion score to bar width
    motion_bar = int(motion_score * 400)

    motion_bar = min(motion_bar, bar_width)

    motion_norm = min(motion_score / 0.02, 1.0)
    # Draw background bar
    cv2.rectangle(frame, (bar_x, bar_y),
              (bar_x + bar_width, bar_y + bar_height),
              (50,50,50), -1)

    # Draw motion level
    fill_width = int(bar_width * motion_norm)

    cv2.rectangle(frame,
              (bar_x, bar_y),
              (bar_x + fill_width, bar_y + bar_height),
              (0,255,0),
              -1)

    cv2.putText(frame, "Motion",
            (bar_x, bar_y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,0.6, (255,255,255), 2)

    # Phase timer calculation
    if state == "GREEN":
        duration = green_duration
    elif state == "RED":
        duration = red_duration
    else:
        duration = green_duration

    remaining = max(0, duration - elapsed_ms)

    timer_ratio = remaining / duration

    timer_bar_width = int(timer_ratio * 200)

    # Draw timer bar background
    cv2.rectangle(frame, (20,180),(220,200),(50,50,50), -1)

    # Draw remaining time
    cv2.rectangle(frame, (20,180),
              (20 + timer_bar_width,200),(255,200,0), -1)

    cv2.putText(frame, "Phase Timer",
            (20,170),
            cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
    
    cv2.putText(frame,
            f"Level: {level}",
            (20,230),
            cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)

    cv2.putText(frame,
            f"Cycle: {cycle}",
            (20,260),
            cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)

    if state == "DEAD":

        overlay = frame.copy()

        cv2.rectangle(overlay, (0,0), (640,480), (0,0,0), -1)

        alpha = 0.6
        frame = cv2.addWeighted(overlay, alpha, frame, 1-alpha, 0)

        cv2.putText(frame,
                "YOU DIED",
                (160,240),
                cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),5)

        cv2.putText(frame,
                "Press R to Restart",
                (170,300),
                cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)

    cv2.imshow("Red Light Green Light", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

    if key == ord('r') and state == "DEAD":

        state = "GREEN"
        state_start_time = now
        green_duration = random.randint(*green_range)

        idle_start_time = None
        cycle = 1
        level = 1

cap.release()
cv2.destroyAllWindows()