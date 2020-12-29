# -*- coding: utf-8 -*-
"""
Created on 27 December 2020
Last version on 29 December 2020
@author: Amaia Gonzalez-Garrido
Available for informational purpose and personal use only
"""
# IMPORTAMOS LIBRERÍAS PYTHON
# pip install numpy matplotlib pandas PyQt5
# pip install auto-py-to-exe

import numpy as np
import math
from PyQt5 import uic, QtWidgets
from PyQt5 import QtWidgets
import pyqtgraph as pg
import sys
import os
import pandas as pd
from pyqtgraph import PlotWidget
import matplotlib.pyplot as plt
from typing import List

'''*********************************************************************************'''

def resource_path(relative_path):
    #Get absolute path to resource, works for dev and for PyInstaller
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

'''*********************************************************************************'''

qtCreatorFile = resource_path("./GUI_Scooter.ui")
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

'''*********************************************************************************'''

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        # Conectamos los eventos con sus acciones
        self.tripdistanceValue.textChanged.connect(self.Travel_features)
        self.tripsValue.textChanged.connect(self.Travel_features)
        self.remainingdistanceValue.textChanged.connect(self.Travel_features)
        self.monthusageValue.textChanged.connect(self.Travel_features)
        self.HorizontValue.textChanged.connect(self.Travel_features)

        self.ScooterconsumptionValue.textChanged.connect(self.Scooter_features)
        self.ScooterefficiencyValue.textChanged.connect(self.Scooter_features)
        self.ScooteremissionsValue.textChanged.connect(self.Scooter_features)

        self.BusconsumptionValue.textChanged.connect(self.Bus_features)
        self.BusemissionsValue.textChanged.connect(self.Bus_features)
        self.BusoccupanceValue.textChanged.connect(self.Bus_features)

        self.CarconsumptionValue.textChanged.connect(self.Car_features)
        self.CaremissionsValue.textChanged.connect(self.Car_features)
        self.CaroccupanceValue.textChanged.connect(self.Car_features)

        self.ElectricconsumptionValue.textChanged.connect(self.Electric_features)
        self.ElectricemissionsValue.textChanged.connect(self.Electric_features)
        self.ElectricoccupanceValue.textChanged.connect(self.Electric_features)

        self.CalculateButton.clicked.connect(self.Calculate)
        self.ClearplotButton.clicked.connect(self.ClearPlot)

        self.busButton.setChecked(True)
        self.busButton.toggled.connect(self.Bus_state)
        self.carButton.toggled.connect(self.Car_state)
        self.electricButton.toggled.connect(self.Electric_state)

        self.graphWidget.setBackground('w')
        #self.graphWidget.setTitle("Cost comparison", color="k", size="10pt", italic=False)
        self.graphWidget.setLabel('left', 'Accumulative cost (€)')
        self.graphWidget.setLabel('bottom', "Time (month)")
        self.graphWidget.showGrid(x=True, y=True, alpha=0.2)


    def Travel_features(self):

        #float(self.tripdistanceValue.text())
        #float(self.tripsValue.text())
        #float(self.remainingdistanceValue.text())
        #float(self.monthusageValue.text())
        #float(self.HorizontValue.text())

        currentdistance=float(self.tripdistanceValue.text())*float(self.tripsValue.text())
        currentdistance=round(currentdistance,2)
        print("Current distance: " + str(currentdistance))
        self.currentdistanceCheck.setText(str(currentdistance))

        monthlydistance=(currentdistance+float(self.remainingdistanceValue.text())) / float(self.monthusageValue.text())
        monthlydistance=round(monthlydistance,2)
        print("Monthly distance: " + str(monthlydistance))
        self.monthlydistanceCheck.setText(str(monthlydistance))

        Horizon=float(self.HorizontValue.text())
        print("Evaluation horizon: " + str(Horizon))


    def Scooter_features(self):

        #float(self.ScooterconsumptionValue.text())
        #float(self.ScooterefficiencyValue.text())
        #float(self.ScooteremissionsValue.text())

        Netemissionskm=float(self.ScooterconsumptionValue.text())*float(self.ScooteremissionsValue.text())
        Emissionskm=Netemissionskm/(float(self.ScooterefficiencyValue.text())/100)
        Emissionskm=round(Emissionskm,4)

        print("GHG emissions per distance: " + str(Emissionskm))
        self.ScooteremissionskmCheck.setText(str(Emissionskm))

    def Bus_features(self):

        #float(self.BusconsumptionValue.text())
        #float(self.BusemissionsValue.text())
        #float(self.BusoccupanceValue.text())

        Netemissionskm=float(self.BusconsumptionValue.text())*float(self.BusemissionsValue.text())
        Emissionskm=Netemissionskm/float(self.BusoccupanceValue.text())
        Emissionskm=round(Emissionskm,4)

        print("GHG emissions per distance: " + str(Emissionskm))
        self.BusemissionskmCheck.setText(str(Emissionskm))

    def Car_features(self):

        #float(self.CarconsumptionValue.text())
        #float(self.CaremissionsValue.text())
        #float(self.CaroccupanceValue.text())

        Netemissionskm=float(self.CarconsumptionValue.text())*float(self.CaremissionsValue.text())
        Emissionskm=Netemissionskm/float(self.CaroccupanceValue.text())
        Emissionskm=round(Emissionskm,4)

        print("GHG emissions per distance: " + str(Emissionskm))
        self.CaremissionskmCheck.setText(str(Emissionskm))

    def Electric_features(self):

        #float(self.ElectricconsumptionValue.text())
        #float(self.ElectricemissionsValue.text())
        #float(self.ElectricoccupanceValue.text())

        Netemissionskm=float(self.ElectricconsumptionValue.text())*float(self.ElectricemissionsValue.text())
        Emissionskm=Netemissionskm/float(self.ElectricoccupanceValue.text())
        Emissionskm=round(Emissionskm,4)

        print("GHG emissions per distance: " + str(Emissionskm))
        self.ElectricemissionskmValue.setText(str(Emissionskm))

    def Bus_state(self):

         if self.busButton.isChecked() == True:
              print("Bus is selected")
              self.tabWidget.setCurrentWidget(self.Bus_tab)

    def Car_state(self):
        if self.carButton.isChecked() == True:
           print("Car is selected")
           self.tabWidget.setCurrentWidget(self.Car_tab)

    def Electric_state(self):
        if self.electricButton.isChecked() == True:
           print("Electric car is selected")
           self.tabWidget.setCurrentWidget(self.Electric_tab)

    def Calculate(self):
        global Trip, Scooter, Results

        Trip = {'Distance': float(self.monthlydistanceCheck.text()),'Months': int(self.monthusageValue.text()),
                'Horizon': int(self.HorizontValue.text())}

        Scooter = {'Capital_cost': float(self.ScootercapitalValue.text()), 'Maintenance': float(self.ScootermaintenanceValue.text()),
                   'Electricity_cost': float(self.ScootercostValue.text()), 'Capacity': float(self.ScootercapacityValue.text()),
                   'Consumption_perkm': float(self.ScooterconsumptionValue.text()), 'Efficiency': float(self.ScooterefficiencyValue.text()),
                   'GHG_perkwh': float(self.ScooteremissionsValue.text()) }

        # Calculate again GHG per km from final inputs and without rounding
        Netemissionskm=float(self.ScooterconsumptionValue.text())*float(self.ScooteremissionsValue.text())
        Scooter["GHG_perkm"]=Netemissionskm/(float(self.ScooterefficiencyValue.text())/100)

        # Calculate scooter results
        # DEMAND RESULTS
        Demand_monthly = [0 for i in range(0, int(Trip["Horizon"]) + 1)]
        for i in range(1, int(Trip["Horizon"]) + 1):
            Demand_monthly[i]=Scooter["Consumption_perkm"]/(Scooter["Efficiency"]/100)*Trip["Distance"]*i

        Results = {'Demand_monthly': Demand_monthly, 'Demand_now': Demand_monthly[Trip["Months"]],
                   'Demand_total': Demand_monthly[Trip["Horizon"]]}

        self.ResultsdemandValue.setText(str(round(Results["Demand_now"],2)))
        self.ResultsTOTALdemandValue.setText(str(round(Results["Demand_total"],2)))

        # COST RESULTS
        Results["Electcost_now"] = Results["Demand_now"] * Scooter["Electricity_cost"]
        self.ResultscostValue.setText(str(round(Results["Electcost_now"], 2)))


        Cost_monthly = [0 for i in range(0, int(Trip["Horizon"]) + 1)]
        for i in range(0, int(Trip["Horizon"]) + 1):
            Cost_monthly[i]=Demand_monthly[i]*Scooter["Electricity_cost"]+Scooter["Capital_cost"]+Scooter["Maintenance"]

        Results["Cost_monthly"]=Cost_monthly
        Results["Allcost_now"]=Cost_monthly[Trip["Months"]]
        Results["Allcost_total"]=Cost_monthly[Trip["Horizon"]]

        # FEC RESULTS
        Results["FEC_now"] = (Results["Demand_now"]*Scooter["Efficiency"]/100)/(Scooter["Capacity"]/1000)
        self.ResultsFECValue.setText(str(round(Results["FEC_now"], 2)))
        Results["FEC_total"] =Results["FEC_now"]/Trip["Months"]*Trip["Horizon"]
        self.ResultsTOTALFECValue.setText(str(round(Results["FEC_total"], 2)))

        # Cost of a completed charge
        Results["Chargecost"] = Results["Electcost_now"]/Results["FEC_now"]
        self.ResultschargecostValue.setText(str(round(Results["Chargecost"], 3)))

        # GHG RESULTS
        Results["GHG_now"]=Results["Demand_now"]*Scooter["GHG_perkwh"]
        Results["GHG_total"]=Results["Demand_now"]/Trip["Months"]*Trip["Horizon"]*Scooter["GHG_perkwh"]
        #Results["GHG_now"]=Trip["Distance"]*Trip["Months"]*Scooter["GHG_perkm"]
        self.ResultsghgValue.setText(str(round(Results["GHG_now"],2)))


        # Calculate results of Base Case
        if self.busButton.isChecked() == True:
            Results["BCdemand_now"]=float(self.BusconsumptionValue.text())/float(self.BusoccupanceValue.text())*Trip["Distance"]*Trip["Months"]
            Results["BCdemand_total"]=float(self.BusconsumptionValue.text())/float(self.BusoccupanceValue.text())*Trip["Distance"]*Trip["Horizon"]
            self.ResultsBCdemandValue.setText(str(round(Results["BCdemand_now"], 2)))
            self.ResultsBCdemandLabel.setText("Base Case demand (litre)")

            BCCost_monthly = [0 for i in range(0, int(Trip["Horizon"]) + 1)]
            for i in range(0, int(Trip["Horizon"]) + 1):
                BCCost_monthly[i] = float(self.tripsValue.text())/Trip["Months"]*float(self.BusticketValue.text())*i

            Results["BCcost_monthly"]=BCCost_monthly
            Results["BCcost_now"]=BCCost_monthly[Trip["Months"]]
            self.ResultsBCcostValue.setText(str(round(Results["BCcost_now"], 2)))
            Results["BCcost_total"]=BCCost_monthly[Trip["Horizon"]]

            Emissionskm = float(self.BusemissionsValue.text()) * float(self.BusconsumptionValue.text())  / float(self.BusoccupanceValue.text())
            Results["BCghg_now"]=Emissionskm*Trip["Distance"]*Trip["Months"]
            self.ResultsBCghgValue.setText(str(round(Results["BCghg_now"],2)))
            Results["BCghg_total"]=Emissionskm*Trip["Distance"]*Trip["Horizon"]

        elif self.carButton.isChecked() == True:
            Results["BCdemand_now"] = float(self.CarconsumptionValue.text())/float(self.CaroccupanceValue.text()) * Trip["Distance"] * Trip["Months"]
            Results["BCdemand_total"] = float(self.CarconsumptionValue.text())/float(self.CaroccupanceValue.text()) * Trip["Distance"] * Trip["Horizon"]
            self.ResultsBCdemandValue.setText(str(round(Results["BCdemand_now"], 2)))
            self.ResultsBCdemandLabel.setText("Base Case demand (litre)")

            BCCost_monthly = [0 for i in range(0, int(Trip["Horizon"]) + 1)]
            for i in range(0, int(Trip["Horizon"]) + 1):
                BCCost_monthly[i] = (float(self.CarcostValue.text())*float(self.CarconsumptionValue.text())+float(self.CarcostkmValue.text()))/float(self.CaroccupanceValue.text()) * Trip["Distance"]  * i

            Results["BCcost_monthly"] = BCCost_monthly
            Results["BCcost_now"] = BCCost_monthly[Trip["Months"]]
            self.ResultsBCcostValue.setText(str(round(Results["BCcost_now"], 2)))
            Results["BCcost_total"] = BCCost_monthly[Trip["Horizon"]]

            Emissionskm = float(self.CaremissionsValue.text()) * float(self.CarconsumptionValue.text()) / float(self.CaroccupanceValue.text())
            Results["BCghg_now"] = Emissionskm * Trip["Distance"] * Trip["Months"]
            self.ResultsBCghgValue.setText(str(round(Results["BCghg_now"], 2)))
            Results["BCghg_total"] = Emissionskm * Trip["Distance"] * Trip["Horizon"]

        elif self.electricButton.isChecked() == True:
            Results["BCdemand_now"] = float(self.ElectricconsumptionValue.text())/float(self.ElectricoccupanceValue.text()) * Trip["Distance"] * Trip["Months"]
            Results["BCdemand_total"] = float(self.ElectricconsumptionValue.text())/float(self.ElectricoccupanceValue.text()) * Trip["Distance"] * Trip["Horizon"]
            self.ResultsBCdemandValue.setText(str(round(Results["BCdemand_now"], 2)))
            self.ResultsBCdemandLabel.setText("Base Case demand (kWh)")

            BCCost_monthly = [0 for i in range(0, int(Trip["Horizon"]) + 1)]
            for i in range(0, int(Trip["Horizon"]) + 1):
                BCCost_monthly[i] = (float(self.ElectriccostValue.text())*float(self.ElectricconsumptionValue.text())+float(self.ElectriccoskmValue.text()))/float(self.ElectricoccupanceValue.text()) * Trip["Distance"]  * i

            Results["BCcost_monthly"] = BCCost_monthly
            Results["BCcost_now"] = BCCost_monthly[Trip["Months"]]
            self.ResultsBCcostValue.setText(str(round(Results["BCcost_now"], 2)))
            Results["BCcost_total"] = BCCost_monthly[Trip["Horizon"]]

            Emissionskm = float(self.ElectricemissionsValue.text()) * float(self.ElectricconsumptionValue.text()) / float(self.ElectricoccupanceValue.text())
            Results["BCghg_now"] = Emissionskm * Trip["Distance"] * Trip["Months"]
            self.ResultsBCghgValue.setText(str(round(Results["BCghg_now"], 2)))
            Results["BCghg_total"] = Emissionskm * Trip["Distance"] * Trip["Horizon"]

        # COMPARISON

        Results["Cost_saving_now"] = Results["BCcost_now"]- Results["Allcost_now"]
        self.ResultscostsavingsValue.setText(str(round(Results["Cost_saving_now"],2)))
        Results["Cost_saving_total"] = Results["BCcost_total"] - Results["Allcost_total"]
        self.ResultsTOTALcostsavingsValue.setText(str(round(Results["Cost_saving_total"],2)))

        # Payback
        savings = [0 for i in range(0, int(Trip["Horizon"]) + 1)]
        for i in range(0, int(Trip["Horizon"]) + 1):
            savings[i]=float(Results["BCcost_monthly"][i])-float(Results["Cost_monthly"][i])

        # Savings
        for i in range(0, int(Trip["Horizon"]) + 1):
            if savings[i]<0:
                #savings[i]=savings[int(Trip["Horizon"])]+1
                savings[i]= float("nan")

        array_savings=np.array(savings)
        saving_sum=np.nansum(array_savings)
        if saving_sum == 0:
            Results["Payback"] = "None"
        else:
            Results["Payback"]=[savings.index(min(i for i in savings if not math.isnan(i)))]

        self.ResultsPaybackValue.setText(str(Results["Payback"]))

        Results["GHG_saving_now"] = Results["BCghg_now"]- Results["GHG_now"]
        self.ResultsghgsavingsValue.setText(str(round(Results["GHG_saving_now"],2)))
        Results["GHG_saving_total"] = Results["BCghg_total"] - Results["GHG_total"]
        self.ResultsTOTALghgsavingsValue.setText(str(round(Results["GHG_saving_total"],2)))

        # Graph
        # https://www.learnpyqt.com/tutorials/embed-pyqtgraph-custom-widgets-qt-app/
        xaxes = [i for i in range(0, int(Trip["Horizon"]) + 1)]
        y1axes = np.array(Results["Cost_monthly"])
        y2axes = np.array(Results["BCcost_monthly"])
        color = pg.mkPen(color=(0, 255, 0))
        self.graphWidget.plot(xaxes,y1axes,label='Scooter',pen=color)
        if self.busButton.isChecked() == True:
            color = pg.mkPen(color=(0, 0, 255))
            self.graphWidget.plot(xaxes,y2axes,label='Bus',pen=color)
        elif self.carButton.isChecked() == True:
            color = pg.mkPen(color=(255, 0, 0))
            self.graphWidget.plot(xaxes,y2axes,label='Car',pen=color)
        elif self.electricButton.isChecked() == True:
            color = pg.mkPen(color=(200, 0, 200))
            self.graphWidget.plot(xaxes,y2axes,label='e-Car',pen=color)

    def ClearPlot(self):
        self.graphWidget.clear()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

