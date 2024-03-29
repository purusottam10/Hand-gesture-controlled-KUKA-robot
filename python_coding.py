import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(static_image_mode=False,max_num_hands=2,min_detection_confidence=0.5,min_tracking_confidence=0.5)

mp_drawing = mp.solutions.drawing_utils

while True:
    ret,frame = cap.read()
    
    if not ret:
        break
        
    image_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    
    results = hands.process(image_rgb)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame,hand_landmarks,mp_hands.HAND_CONNECTIONS)


            index_finger_tip_x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
            index_finger_mcp_x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x

            index_finger_horz_diff = index_finger_tip_x-index_finger_mcp_x
            # print(index_finger_horz_diff)
            
            index_finger_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
            index_finger_mcp_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y

            index_finger_vert_diff = index_finger_tip_y-index_finger_mcp_y
            #print(index_finger_vert_diff)


            if index_finger_vert_diff <= -0.25:
                hand_gesture = "move"
                print("MOVE UPWARD")

            if index_finger_vert_diff >= 0.25:
                hand_gesture = "pointing down"
                print("MOVE DOWNWORD")

            if index_finger_horz_diff <= -0.2:
                print("MOVE RIGHT")

            if index_finger_horz_diff >= 0.2:
                print("MOVE LEFT")

            else:
                hand_gesture = "other"
                

            
            # if hand_gesture == "pointing up":
            #     print("Pointing up")
            
            # elif hand_gesture == "pointing down":
            #     print("Pointing Down")

    
    cv2.imshow("Hand Gesture",frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()