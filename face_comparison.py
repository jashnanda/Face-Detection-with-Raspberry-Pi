from picarx import Picarx
from vilib import Vilib
import face_recognition
import cv2
import os
from time import sleep, time, strftime, localtime
from robot_hat import Music, TTS

# Initialize Picarx
px = Picarx()
music = Music()
tts = TTS()

# Set up paths
KNOWN_FACES_DIR = "known_faces"
PHOTOS_DIR = "photos"

# Make sure photos folder exists
if not os.path.exists(PHOTOS_DIR):
    os.makedirs(PHOTOS_DIR)

# Helper function: Clamp angle
def clamp_number(num, a, b):
    return max(min(num, max(a, b)), min(a, b))

# Helper function: Take photo
def take_photo():
    _time = strftime('%Y-%m-%d-%H-%M-%S', localtime(time()))
    name = f'photo_{_time}'
    path = PHOTOS_DIR + "/"
    Vilib.take_photo(name, path)
    full_path = os.path.join(path, name + ".jpg")
    print(f'Photo saved as {full_path}')
    return full_path

# Load known faces
def load_known_faces():
    known_faces = []
    known_names = []
    for filename in os.listdir(KNOWN_FACES_DIR):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(KNOWN_FACES_DIR, filename)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if len(encodings) > 0:
                encoding = encodings[0]
                known_faces.append(encoding)
                name = filename.split("_")[0]  # Extract name from filename (e.g., "alice_1.jpg" -> "alice")
                known_names.append(name)
            else:
                print(f"Warning: No faces found in {filename}!")
    print(f"Loaded {len(known_faces)} known face encodings.")
    return known_faces, known_names

# Main program
def main():
    # Initialize camera
    Vilib.camera_start()
    Vilib.display()
    Vilib.face_detect_switch(True)

    x_angle = 0
    y_angle = 0
    tts.lang("en-US")
    music.music_set_volume(20)

    # Load known faces
    known_faces, known_names = load_known_faces()
    print("starting face detection")
    while True:
        print("Checking for faces...")
        print("Detected faces:", Vilib.detect_obj_parameter['human_n'])
        if Vilib.detect_obj_parameter['human_n'] != 0:
            print("Face detected!")
            photo_path = take_photo()
            img = cv2.imread(photo_path)
            human_x = Vilib.detect_obj_parameter.get('human_x', 0)
            human_y = Vilib.detect_obj_parameter.get('human_y', 0)
            human_w = Vilib.detect_obj_parameter.get('human_w', 0)
            human_h = Vilib.detect_obj_parameter.get('human_h', 0)

            
            #cropped_img = img[int(human_y - human_h): int(human_y + human_h), int(human_x - human_w): int(human_x + human_w)]
            #cv2.imwrite("cropped_photos/cropped_img.jpg", cropped_img)

            # Convert BGR to RGB before face encoding
            #cropped_img_rgb = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)

            # Load captured photo
            unknown_image = face_recognition.load_image_file(photo_path)
            
            unknown_encodings = face_recognition.face_encodings(unknown_image)
            print(unknown_encodings)
            print("Before for loop")
            if unknown_encodings:
                unknown_encoding = unknown_encodings[0]  # Just take the first face found

                matches = face_recognition.compare_faces(known_faces, unknown_encoding)
                name = "Unknown"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_names[first_match_index]

                new_photo_path = photo_path.replace("photo_", f"{name}_")
                os.rename(photo_path, new_photo_path)
                print(f"Detected: {name}")

                if name == "Unknown":
                    music.sound_play('../picar-x/sounds/IntruderSound.wav')
                    sleep(1)
                    word = "Welcome"
                    tts.say(word)
                    sleep(1)
                    print("Unknown face detected! Take action here.")
                else:
                    print("Recognized ", name)
                    #tts.say(f"Hello {name}")
                    #music.sound_play('../picar-x/sounds/car-start-engine.wav')
                    words = f"Hello {name}"
                    tts.say(words)
            else:
                print("No faces found in photo.")

            # You can break or continue checking
            break

        else:
            sleep(0.05)

# Entry point
if __name__ == "__main__":
    try:
        main()
    finally:
        px.stop()
        Vilib.camera_close()
        print("Stop and exit.")
        sleep(0.1)
