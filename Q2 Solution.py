import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

# Game settings
width, height = 1280, 640
player_pos = [320, 440]
# enemy speed, size, and list initialization
enemy_speed=6
enemy_size=50
enemy_list=[]


# Initialize score
score=0


# Create random enemy
def create_enemy():
    x_coordinate=np.random.randint(0,width - enemy_size)
    return [x_coordinate,0]
    
# Move enemies down
def move_enemies(enemy_list):
    for enemy in enemy_list:
        enemy[1]+=enemy_speed
    
# Check if enemy is off-screen
def check_off_screen(enemy_list):
    global score
    for enemy in enemy_list[:] :
        if enemy[1] > height:
            score+=1
            enemy_list.remove(enemy)
                       
# Increment score for each enemy that goes off-screen
# Check for collisions
def check_collision(player_pos, enemy_list):
    pos_x, pos_y = player_pos
    for enemy in enemy_list:
        if (pos_x < enemy[0] + enemy_size and pos_x + enemy_size > enemy[0] and pos_y < enemy[1] + enemy_size and pos_y + enemy_size > enemy[1]):
            return True
    return False
    
# Initialize webcam
cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()
    
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame with MediaPipe
    processed = hands.process(rgb_frame)

            
    # Get coordinates of the index finger tip (landmark 8)
    if processed.multi_hand_landmarks:
        for hand_landmarks in processed.multi_hand_landmarks:
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            player_pos[0] = int(index_finger_tip.x * width)
            player_pos[1] = int(index_finger_tip.y * height)

            
    # Move player based on hand movement
    cv2.rectangle(frame,(player_pos[0],player_pos[1]),(player_pos[0]+50,player_pos[1]+50),(0,255,0),-1)
    # Add new enemies
    if np.random.randint(0,30)==7:
        enemy_list.append(create_enemy())

    
    # Move enemies
    move_enemies(enemy_list)
    
    # Check for collision
    if check_collision(player_pos,enemy_list)==True:
        print("Game Over")
        break

    
    # Draw game elements
    for enemy in enemy_list:
        cv2.rectangle(frame,(enemy[0],enemy[1]),(enemy[0]+enemy_size,enemy[1]+enemy_size),(0,0,255),-1)

    
    # Display score on the frame
    cv2.putText(frame, f'Score: {score}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Object Dodging Game", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
