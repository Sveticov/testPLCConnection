import threading
import time

from snap7.exceptions import Snap7Exception

from ClientCreate import clientCreate
from Client_destroy import client_destroy
from DataFromPLC import DataFromPLC
from LisDataFromPLC import listDataFromPLC
from Status_conection import status_connection
from data_excel import data_excel
from tkinter import *

rdf_plc = 0
connect = False

root = Tk()
root['bg'] = '#fafafa'
root.title('Laboratory Report')
root.wm_attributes('-alpha', 0.9)
root.geometry('400x400')

canvas = Canvas(root, height=400, width=400)
canvas.pack()

frame = Frame(root, bg='#333333')
frame.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)


def simulate_test_report():
    global rdf_plc
    rdf_plc = 1


btnTest = Button(frame, text='Test Report', command=simulate_test_report)
btnTest.pack()


def impulse_read_plc(param, param_2):
    if param == 1 and param_2 == 0:
        return 1
    if param == 0:
        return 0


def connect_plc():
    global connect
    while True:
        time.sleep(1)
        if not connect:
            try:
                clientDryer, connectDryer = clientCreate('172.20.2.1', 0, 2)
                clientRefiner, connectRefiner = clientCreate('172.20.2.5', 0, 3)
                clientClueKitchen, connectGlueKitchen = clientCreate('172.20.3.1', 0, 2)
                clientMatformer, connectMatformer = clientCreate('172.20.4.4', 0, 2)
                clientPress, connectPress = clientCreate('172.20.4.3', 0, 3)
                time.sleep(0.5)

                connect = status_connection(connectDryer, connectRefiner, connectGlueKitchen, connectMatformer,
                                            connectPress)
                print('plc connect ', connect)
            except Snap7Exception as e:
                connect = False
                continue
        else:
            try:
                rdf_plc = 1  # impulse_read_plc(clientDryer.db_read(100, 0, 1)[0], rdf_plc)

                if rdf_plc == 1:
                    rdf_plc = 2
                    listDryer = listDataFromPLC(connect,
                                                DataFromPLC(clientDryer, 400, 1180, 4),  # temp inlet 2420 te9360
                                                DataFromPLC(clientDryer, 400, 1196, 4),  # pressure inlet 2420 pt9365
                                                DataFromPLC(clientDryer, 400, 24, 4),  # temp pipe 2420 te1360
                                                DataFromPLC(clientDryer, 400, 44, 4),  # moisture 2425 y0101
                                                DataFromPLC(clientDryer, 400, 0, 4),  # temp cyclone 1
                                                DataFromPLC(clientDryer, 400, 4, 4),  # temp cyclone 2
                                                DataFromPLC(clientDryer, 23, 8, 4),  # filling level bunker
                                                DataFromPLC(clientDryer, 23, 4, 4),  # dosing bunker
                                                )
                    print(listDryer)

                    listRefiner = listDataFromPLC(connect,
                                                  DataFromPLC(clientRefiner, 60, 160, 4),  # preheater temp
                                                  DataFromPLC(clientRefiner, 60, 150, 4),  # preheater steam
                                                  DataFromPLC(clientRefiner, 60, 260, 4),  # difibrator pressure
                                                  DataFromPLC(clientRefiner, 60, 110, 4),  # preheater hoist min
                                                  DataFromPLC(clientRefiner, 60, 210, 4),  # motor power SEC
                                                  DataFromPLC(clientRefiner, 45, 66, 4),  # production t/h
                                                  DataFromPLC(clientRefiner, 60, 400, 4),  # blow valve %

                                                  )
                    print(listRefiner)

                    listGlueKitchen = listDataFromPLC(connect,
                                                      DataFromPLC(clientClueKitchen, 620, 168, 4),  # fm uf glue
                                                      DataFromPLC(clientClueKitchen, 620, 172, 4),  # fm muf glue
                                                      DataFromPLC(clientClueKitchen, 620, 176, 4),  # fm water
                                                      DataFromPLC(clientClueKitchen, 620, 180, 4),  # fm hardener
                                                      DataFromPLC(clientClueKitchen, 620, 184, 4),  # fm urea
                                                      DataFromPLC(clientClueKitchen, 620, 188, 4),  # fm emulsion
                                                      )
                    print(listGlueKitchen)

                    listChipDosing = listDataFromPLC(connect,
                                                     DataFromPLC(clientRefiner, 45, 426, 4),  # dosing chips 1 silos
                                                     DataFromPLC(clientRefiner, 45, 430, 4),  # dosing chips 2 silos
                                                     DataFromPLC(clientRefiner, 715, 44, 4)
                                                     # dosing chips outdoor system
                                                     )
                    listMatformer = listDataFromPLC(connect,
                                                    DataFromPLC(clientMatformer, 51, 52, 4),  # temp bunker
                                                    DataFromPLC(clientMatformer, 402, 18, 4),  # density calculate
                                                    DataFromPLC(clientMatformer, 402, 4, 4),  # weight on scale
                                                    )
                    listPress = listDataFromPLC(connect,
                                                DataFromPLC(clientPress, 1002, 76, 4),  # heating plate 1
                                                DataFromPLC(clientPress, 1002, 112, 4),  # heating plate 2
                                                DataFromPLC(clientPress, 1002, 152, 4),  # heating plate 3
                                                DataFromPLC(clientPress, 1002, 192, 4),  # heating plate 4
                                                DataFromPLC(clientPress, 1002, 232, 4),  # heating plate 5
                                                DataFromPLC(clientPress, 12, 36, 4),  # speed press
                                                DataFromPLC(clientPress, 1002, 496, 4),  # press faktor
                                                )
                    listDataProduct2 = listDataFromPLC(connect,
                                                       DataFromPLC(clientPress, 1870, 0, 4),  # thickness mm
                                                       DataFromPLC(clientPress, 1870, 4, 4),  # width mm
                                                       DataFromPLC(clientPress, 1870, 8, 4),  # length mm
                                                       DataFromPLC(clientPress, 1870, 12, 4)  # density kg/m3
                                                       )
                    listDataProduct1 = [str(clientPress.db_read(587, 120, 22))[17:],  # recipe name
                                        str(clientPress.db_read(587, 160, 10))[18:]  # product code
                                        ]

                    print('press', str(clientPress.db_read(587, 120, 22))[17:])
                    print('press code', str(clientPress.db_read(587, 160, 10))[18:])

                    data_excel(listDryer, listRefiner, listGlueKitchen, listChipDosing,
                               listMatformer, listPress, listDataProduct1, listDataProduct2)


            except Snap7Exception as e:
                client_destroy(clientDryer, clientRefiner)
                print('error ', e)
                connect = False
                continue


def btn_run():
    thread_plc = threading.Thread(target=connect_plc, daemon=True)
    thread_plc.start()


def hide_btn(event):
    time.sleep(2)
    event.widget.pack_forget()


btnRun = Button(frame, text='Run Program', command=btn_run)
# btnRun.bind('<Button-1>', hide_btn)
btnRun.pack()

root.mainloop()

# def impulse_read_plc(param, param_2):
#     if param == 1 and param_2 == 0:
#         return 1
#     if param == 0:
#         return 0

#
# while True:
#
#     if not connect:
#         try:
#             clientDryer, connectDryer = clientCreate('172.20.2.1', 0, 2)
#             clientRefiner, connectRefiner = clientCreate('172.20.2.5', 0, 3)
#             clientClueKitchen, connectGlueKitchen = clientCreate('172.20.3.1', 0, 2)
#             clientMatformer, connectMatformer = clientCreate('172.20.4.4', 0, 2)
#             clientPress, connectPress = clientCreate('172.20.4.3', 0, 3)
#             time.sleep(0.5)
#
#             connect = status_connection(connectDryer, connectRefiner, connectGlueKitchen, connectMatformer,
#                                         connectPress)
#             print('plc connect ', connect)
#         except Snap7Exception as e:
#             connect = False
#             continue
#     else:
#         try:
#             rdf_plc = 1  # impulse_read_plc(clientDryer.db_read(100, 0, 1)[0], rdf_plc)
#
#             if rdf_plc == 1:
#                 rdf_plc = 2
#                 listDryer = listDataFromPLC(connect,
#                                             DataFromPLC(clientDryer, 400, 1180, 4),  # temp inlet 2420 te9360
#                                             DataFromPLC(clientDryer, 400, 1196, 4),  # pressure inlet 2420 pt9365
#                                             DataFromPLC(clientDryer, 400, 24, 4),  # temp pipe 2420 te1360
#                                             DataFromPLC(clientDryer, 400, 44, 4),  # moisture 2425 y0101
#                                             DataFromPLC(clientDryer, 400, 0, 4),  # temp cyclone 1
#                                             DataFromPLC(clientDryer, 400, 4, 4),  # temp cyclone 2
#                                             DataFromPLC(clientDryer, 23, 8, 4),  # filling level bunker
#                                             DataFromPLC(clientDryer, 23, 4, 4),  # dosing bunker
#                                             )
#                 print(listDryer)
#
#                 listRefiner = listDataFromPLC(connect,
#                                               DataFromPLC(clientRefiner, 60, 160, 4),  # preheater temp
#                                               DataFromPLC(clientRefiner, 60, 150, 4),  # preheater steam
#                                               DataFromPLC(clientRefiner, 60, 260, 4),  # difibrator pressure
#                                               DataFromPLC(clientRefiner, 60, 110, 4),  # preheater hoist min
#                                               DataFromPLC(clientRefiner, 60, 210, 4),  # motor power SEC
#                                               DataFromPLC(clientRefiner, 45, 66, 4),  # production t/h
#                                               DataFromPLC(clientRefiner, 60, 400, 4),  # blow valve %
#
#                                               )
#                 print(listRefiner)
#
#                 listGlueKitchen = listDataFromPLC(connect,
#                                                   DataFromPLC(clientClueKitchen, 620, 168, 4),  # fm uf glue
#                                                   DataFromPLC(clientClueKitchen, 620, 172, 4),  # fm muf glue
#                                                   DataFromPLC(clientClueKitchen, 620, 176, 4),  # fm water
#                                                   DataFromPLC(clientClueKitchen, 620, 180, 4),  # fm hardener
#                                                   DataFromPLC(clientClueKitchen, 620, 184, 4),  # fm urea
#                                                   DataFromPLC(clientClueKitchen, 620, 188, 4),  # fm emulsion
#                                                   )
#                 print(listGlueKitchen)
#
#                 listChipDosing = listDataFromPLC(connect,
#                                                  DataFromPLC(clientRefiner, 45, 426, 4),  # dosing chips 1 silos
#                                                  DataFromPLC(clientRefiner, 45, 430, 4),  # dosing chips 2 silos
#                                                  DataFromPLC(clientRefiner, 715, 44, 4)  # dosing chips outdoor system
#                                                  )
#                 listMatformer = listDataFromPLC(connect,
#                                                 DataFromPLC(clientMatformer, 51, 52, 4),  # temp bunker
#                                                 DataFromPLC(clientMatformer, 402, 18, 4),  # density calculate
#                                                 DataFromPLC(clientMatformer, 402, 4, 4),  # weight on scale
#                                                 )
#                 listPress = listDataFromPLC(connect,
#                                             DataFromPLC(clientPress, 1002, 76, 4),  # heating plate 1
#                                             DataFromPLC(clientPress, 1002, 112, 4),  # heating plate 2
#                                             DataFromPLC(clientPress, 1002, 152, 4),  # heating plate 3
#                                             DataFromPLC(clientPress, 1002, 192, 4),  # heating plate 4
#                                             DataFromPLC(clientPress, 1002, 232, 4),  # heating plate 5
#                                             DataFromPLC(clientPress, 12, 36, 4),  # speed press
#                                             DataFromPLC(clientPress, 1002, 496, 4),  # press faktor
#                                             )
#                 listDataProduct2 = listDataFromPLC(connect,
#                                                    DataFromPLC(clientPress, 1870, 0, 4),  # thickness mm
#                                                    DataFromPLC(clientPress, 1870, 4, 4),  # width mm
#                                                    DataFromPLC(clientPress, 1870, 8, 4),  # length mm
#                                                    DataFromPLC(clientPress, 1870, 12, 4)  # density kg/m3
#                                                    )
#                 listDataProduct1 = [str(clientPress.db_read(587, 120, 22))[17:],  # recipe name
#                                     str(clientPress.db_read(587, 160, 10))[17:]  # product code
#                                     ]
#
#                 print('press', str(clientPress.db_read(587, 120, 22)))
#                 print('press code', str(clientPress.db_read(587, 160, 10)))
#
#                 data_excel(listDryer, listRefiner, listGlueKitchen, listChipDosing,
#                            listMatformer, listPress, listDataProduct1, listDataProduct2)
#
#
#         except Snap7Exception as e:
#             client_destroy(clientDryer, clientRefiner)
#             print('error ', e)
#             connect = False
#             continue
