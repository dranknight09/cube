import cv2
import numpy as np

# Lists in the format [B, G, R]
color_map = {'red': [26, 6, 164],
             'green': [43, 92, 11],
             'blue': [117, 45, 0],
             'orange': [8, 50, 180],
             'yellow': [3, 125, 166],
             'white': [186, 188, 182]}


def avg_color(img):
    average_color_per_row = np.average(img, axis=0)
    average_color = np.average(average_color_per_row, axis=0)
    return average_color


def identify_color(c):
    diff_min = np.inf
    color = ''

    for i in color_map:
        diff = sum([abs(a - b) for a, b in zip(c, color_map[i])])
        if diff < diff_min:
            diff_min = diff
            color = i

    return color


def video_main():
    cube = {}
    cap = cv2.VideoCapture(0)
    order = 'FLBRUD'
    txt = 'Align face in Squares. Press Enter to capture.'
    for face in order:
        while True:
            ret, frame = cap.read()
            frame_display = frame.copy()                                # Separate the display and processing Frames

            p = int(min(frame.shape[0], frame.shape[1]) / 50)           # size of cubie regions
            r = int(min(frame.shape[0], frame.shape[1]) / 10)           # distance b/w points
            x, y = int(frame.shape[1]/2), int(frame.shape[0]/2)         # Center

            # Define and mark capture regions for the face
            res = []
            for yi in [y-r, y, y+r]:
                for xi in [x-r, x, x+r]:
                    frame_display = cv2.rectangle(frame_display, (xi-p, yi-p), (xi+p, yi+p), (255, 0, 0), 2)
                    block = frame[yi-p:yi+p, xi-p:xi+p]
                    res.append(identify_color(avg_color(block)))

            res = [res[0:3], res[3:6], res[6:9]]                        # Convert result to 3x3 matrix

            # Display Captured Faces
            face_size = 20
            for i in range(3):
                for j in range(3):
                    frame_display = cv2.rectangle(frame_display,
                                                  (face_size*(j+1), face_size*(i+1)),
                                                  (face_size*(j+2), face_size*(i+2)),
                                                  color_map[res[i][j]], -1)

            # Flip and display image
            frame_display = cv2.flip(frame_display, 1)
            # Add text prompt at the bottom left
            frame_display = cv2.putText(frame_display, txt, (0, int(frame.shape[0])-5),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))

            cv2.imshow('Frame', frame_display)
            if cv2.waitKey(1) == 13:                    # Identify Enter Key
                break

        cv2.imwrite('cam.jpg', frame)
        cube[face] = res
        txt = face + ' has been captured.'

    cap.release()
    cv2.destroyAllWindows()

    return cube


def img_debug():
    frame = cv2.imread('cam.jpg')
    frame_display = cv2.flip(frame, 1)                          # Separate the display and processing Frames

    p = int(min(frame.shape[0], frame.shape[1]) / 50)           # size of cubie regions
    r = int(min(frame.shape[0], frame.shape[1]) / 10)           # distance b/w points
    x, y = int(frame.shape[1]/2), int(frame.shape[0]/2)         # Center

    res = []
    for yi in [y-r, y, y+r]:
        for xi in [x-r, x, x+r]:
            frame_display = cv2.rectangle(frame_display, (xi-p, yi-p), (xi+p, yi+p), (255, 0, 0), 2)
            block = frame[yi-p:yi+p, xi-p:xi+p]
            res.append(avg_color(block))
    res = [res[0:3], res[3:6], res[6:9]]
    print(*res, sep='\n')


if __name__ == '__main__':
    video_main()
