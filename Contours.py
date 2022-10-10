import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline


# Чтение и первичная обработка изображения
def main(name):
    image = cv2.imread(name)
    height, weight = image.shape[:2]


    # Форматирование изображение
    # (Замена цвета таким образом, чтобы связанные с графиком объёкты стали чёрными, а всё остальное белым)

    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY)


    # Обнаружение всех контуров на изображении с последующей конвертацией в массив

    contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    contours = np.array(contours)


    # Цикл для сортировки исходных контуров по длинне

    for i in range(len(contours)):
        for j in range(len(contours)):
            if len(contours[i]) > len(contours[j]):
                contours[[i, j]] = contours[[j, i]]


    # Поиск необходимого контура с графиком

    Result = 0
    for i in range(len(contours) - 1):
        if abs(len(contours[i + 1]) - len(contours[i])) > 100 and (2 * (height + weight) - len(contours[i])) > 100:
            Result = i
            break


    # Удаление рамки изобржения и отсечение ненужных контуров на графике

    contours = list(contours)
    for i in range(Result + 1, len(contours), 1):
        contours.pop()

    for i in range(len(contours) - 1):
        if abs(len(contours[i]) - 2 * (height + weight)) < 20:
            contours.pop(i)


    # Приведение списка contours к двумерному массиву, где пары чисел будут представлять координаты графика

    TempArray = list()
    for i in range(len(contours)):
        for j in range(len(contours[i])):
            TempArray.append(contours[i][j][0])
    ResultArray = np.zeros((len(TempArray), 2))
    for i in range(len(TempArray)):
        ResultArray[i][0] = TempArray[i][0]
        ResultArray[i][1] = TempArray[i][1]


    # Поиск координатных осей с их последующим удалением

    TempList = list()
    for i in range(len(ResultArray)):
        for j in range(len(ResultArray)):
            if ((ResultArray[i][1] == ResultArray[j][1] and abs(ResultArray[i][0] - ResultArray[j][0]) < 5) or (ResultArray[i][0] == ResultArray[j][0] and abs(ResultArray[i][1] - ResultArray[j][1]) < 5)) and i > j:
                temp = list()
                temp.append((ResultArray[i][0] + ResultArray[j][0]) / 2)
                temp.append(ResultArray[i][1])
                TempList.append(temp)

    ResultArray = np.array(TempList)

    CoordCenter = list()
    for i in range(len(ResultArray) - 1):
        for j in range(len(ResultArray) - 1):
            if abs(ResultArray[i][0] - ResultArray[j][0]) < 3 and abs(ResultArray[i][1] - ResultArray[j][1]) < 3 and i > j:
                if i in CoordCenter:
                    continue
                else:
                    CoordCenter.append(i)

    for i in sorted(CoordCenter, reverse=True):
        del TempList[i]

    CoordCenter = list()
    for i in range(len(TempList) - 1):
        if abs(TempList[i][0] - TempList[i + 1][0]) > 5 or abs(TempList[i][1] - TempList[i + 1][1]) > 5:
            CoordCenter.append(i)

    for i in sorted(CoordCenter, reverse=True):
        del TempList[i]

    k = 0
    for i in sorted(range(len(TempList)), reverse=True):
        if k < 8:
            del TempList[i]
            k += 1
        else:
            break

    TempListSlice = list()
    for i in range(len(TempList)):
        TempListSlice.append(TempList[i][1])

    x_start = TempList[0][0]
    y_start = TempList[0][1]
    for i in range(len(TempList)):
        TempList[i][0] = TempList[i][0] - x_start
        TempList[i][1] = TempList[i][1] - y_start
        TempList[i][1] = 0 - TempList[i][1]

    # Занесение финального списка в csv файл

    ResultDataFrame = pd.DataFrame(TempList)
    ResultDataFrame.to_csv("Result.csv", index=False, header=False)

    # Вывод программы для оценки промежуточного результата

    ResultArray = np.array(TempList)
    image_copy = image.copy()
    cv2.drawContours(image_copy, contours, -1, (0, 255, 0), 3)
    cv2.imshow('None approximation', image_copy)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    plt.axis("equal")
    plt.plot(ResultArray[:, 0], ResultArray[:, 1])
    plt.show()
