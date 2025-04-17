import cv2


def run_analysis(p: int):
    cap = cv2.VideoCapture(p, cv2.CAP_DSHOW) 
    

    if not cap.isOpened():
        print("Error: Cannot open camera.")
        return
    
    while cap.isOpened():
        status, frame = cap.read()
        if status:
            cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break


    cap.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_analysis(0)
        


    