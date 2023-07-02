import cv2
import psycopg2
from config import host, user, password, db_name
from datetime import datetime


camera_id = 0  # Index of Camera
delay = 1  # 0 - Photo, 1 - Video
window_name = 'QR Code Detector by Fila'

qcd = cv2.QRCodeDetector()  # QR Code Detector
cap = cv2.VideoCapture(camera_id)  # Video Capture

while True:
    ret, frame = cap.read()  # проверяется целостность каждого кадра

    if ret:
        ret_qr, decoded_info, points, _ = qcd.detectAndDecodeMulti(frame)  # ret-qr - выводит true если находит qr. А по дефолту false
        if ret_qr:  # if true, then
            for s, p in zip(decoded_info, points):  # zip группирует значение points с decoded_info. То есть чекает каждый квадрат и выводит значение
                if s:
                    print(s)
                    try:
                        # connect to exist database
                        connection = psycopg2.connect(
                            host=host,
                            user=user,
                            password=password,
                            database=db_name
                        )
                        connection.autocommit = True

                        # the cursor for performing database connection
                        with connection.cursor() as cursor:
                            cursor.execute(
                                "SELECT decoded_info FROM qrlist;"
                            )

                            data_from_db = decoded_info



                        if data_from_db == s:
                            current_datetime = datetime.now()
                            print("Маршрут ", code_number)
                            print(f"Госномер ", govnumber)
                            print(current_datetime)
                            print("90 тенге")

                    except Exception as _ex:
                        print("[INFO] Error while working with PostgreSQL", _ex)

                    finally:
                        if connection:
                            connection.close()
                            print("[INFO] PostgreSQL connection closed")
                else:
                    color = (0, 0, 255)  # red
                frame = cv2.polylines(frame, [p.astype(int)], True, color, 8)  # тут qr обводится квадратом. Если он распознал код, то обводится зеленым. По дефолту красный

        cv2.imshow(window_name, frame)

    if cv2.waitKey(delay) & 0xFF == ord('q'):  # если нажал на q, то цикл выключается. Почему-то если delay = 0, при нажатии он просто обновляет кадр
        break

cv2.destroyWindow(window_name)  # камера закрывается
