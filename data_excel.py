import time
from datetime import datetime
import pandas as pd
import os
import glob
from styleframe import StyleFrame

dummy = 'null'
properties = str(open('C:/properties.txt', 'r').readline(14))
print(properties)


def data_excel(*list_excel):
    date_current = datetime.today().strftime('%Y %m %d %H %M %S')
    path_excel = properties + '\\dataTest' + str(date_current) + '.xlsx'
    print(path_excel)
    df = pd.DataFrame({
                       # 'Data ' + date_current: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
                       'Info Dryer': ['T inlet', 'P inlet', 'T pipe', 'moisture', 'temp cyclone 1', 'temp cyclone 2',
                                      'filling level bunker', 'dosing bunker', '', ''],
                       'Dryer': [list_excel[0][0], list_excel[0][1], list_excel[0][2],
                                 list_excel[0][3], list_excel[0][4], list_excel[0][5],
                                 list_excel[0][6], list_excel[0][7], '', ''],
                       'Info Refiner': ['preheater temp', 'preheater steam', 'difibrator pressure',
                                        'preheater hoist min', 'motor power SEC', 'production t/h',
                                        'blow valve %', '', '', ''],
                       'Refiner': [list_excel[1][0], list_excel[1][1], list_excel[1][2], list_excel[1][3],
                                   list_excel[1][4], list_excel[1][5], list_excel[1][6], '', '', ''],
                       'Info Glue': ['uf glue', 'muf glue', 'water', 'hardener', 'urea', 'emulsion', '', '', '', ''],
                       'Glue Kitchen': [list_excel[2][0], list_excel[2][1], list_excel[2][2],
                                        list_excel[2][3], list_excel[2][4], list_excel[2][5], '', '', '', ''],
                       'Info Dosing': ['1 silos', '2 silos', 'outdoor system', '', '', '', '', '', '', ''],
                       'Dosing Chips': [list_excel[3][0], list_excel[3][1], list_excel[3][2], '', '', '', '', '', '',
                                        ''],
                       'Info Matformer & Press': ['temp bunker', 'density calculate', 'weight on scale',
                                                  'heating plate 1', 'heating plate 2', 'heating plate 3',
                                                  'heating plate 4', ' heating plate 5', 'speed press',
                                                  'press facktor'],
                       'Matformer & Press': [list_excel[4][0], list_excel[4][1], list_excel[4][2], list_excel[5][0],
                                             list_excel[5][1],
                                             list_excel[5][2], list_excel[5][3], list_excel[5][4], list_excel[5][5],
                                             list_excel[5][6]],
                       'Info Product': ['recipe name', 'product code', 'thickness mm', 'width mm', 'length mm',
                                        'density kg/m3', '', '', '', ''],
                       'Product': [list_excel[6][0], list_excel[6][1], list_excel[7][0], list_excel[7][1],
                                   list_excel[7][2], list_excel[7][3], '', '', '', '']
                       })

    excel_writer = StyleFrame.ExcelWriter(path_excel)
    sf = StyleFrame(df)
    sf.set_column_width(
        columns=['Info Dryer', 'Dryer', 'Info Refiner', 'Refiner', 'Info Glue', 'Glue Kitchen',
                 'Info Dosing', 'Dosing Chips', 'Info Matformer & Press', 'Matformer & Press', 'Info Product',
                 'Product'], width=25.0)
    sf.to_excel(excel_writer=excel_writer, row_to_add_filters=0, columns_and_rows_to_freeze='B1')
    excel_writer.save()

    # df.to_excel(path_excel)

    # os.system('start "excel" "C:\\Users\\ASUTP\\PycharmProjects\\pythonProject\\%s"'%path_excel)

    dir_file = glob.glob(properties + "\\*.xlsx")
    print(dir_file)

    if len(dir_file) > 5:
        for i in range(5):
            os.remove(dir_file[i])

    time.sleep(2)
