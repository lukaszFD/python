import pyautogui
import random
import time

def move_and_click():
    # Set a small delay between actions
    pyautogui.PAUSE = 1.0

    # Safety feature: move mouse to any corner to abort
    pyautogui.FAILSAFE = True

    print("Python automation started. Press Ctrl+C to stop or move mouse to corner.")

    try:
        while True:
            # Generate random coordinates within a typical screen range
            x = random.randint(200, 800)
            y = random.randint(200, 600)

            # Move mouse smoothly over 0.5 seconds
            pyautogui.moveTo(x, y, duration=0.5)

            # Perform a left click
            pyautogui.click()

            print(f"Clicked at: {x}, {y}")

            # Wait 3 seconds
            time.sleep(3)
    except KeyboardInterrupt:
        print("\nAutomation stopped by user.")

if __name__ == "__main__":
    move_and_click()