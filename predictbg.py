# import streamlit as st
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
# # import seaborn as sns
# import plotly.express as px
# import plotly.graph_objects as go
from math import exp


list = []


class PredData:
    def __init__(self, vtime, value):
        self.vtime = vtime
        self.value = value


class GlucosePredict:
    def __init__(self, carbs, inscarbRatio,  correctionRatio, timetotarget, timetopeak, currentbg, targetbg, time,):
        self.carbs = carbs
        self.inscarbRatio = inscarbRatio
        self.correctionRatio = correctionRatio
        self.timetotarget = timetotarget
        self.timetopeak = timetopeak
        self.currentbg = currentbg
        self.targetbg = targetbg
        self.time = time

    def calculatebolus(self, currentbg, carbs):
        bolus = ((currentbg - self.targetbg) / self.correctionRatio) + \
            (carbs / self.inscarbRatio)

        return bolus

    def getcorrection(self, time):
        top = (-pow((exp(1)*time)/self.timetotarget, 2))/2
        self.correction = 1-exp(top)

        return self.correction

    def getfall(self, time, currentbg, carbs):
        self.fall = - \
            self.getcorrection(time)*self.correctionRatio * \
            self.calculatebolus(currentbg, carbs)

        return self.fall

    def getcarbs(self, time):
        bot = (-pow((exp(1)*time)/self.timetopeak, 2))/2
        self.carbs = 1 - exp(bot)

        return self.carbs

    def getrise(self, time, currentbg, carbs,):
        self.rise = self.getcarbs(time)*carbs * \
            self.correctionRatio/self.inscarbRatio

        return self.rise

    def getprediction(self, time, currentbg, carbs):
        self.prediction = self.getfall(
            time, currentbg, carbs) + self.getrise(time, currentbg, carbs)+currentbg

        return self.prediction

    def getpredictions(self, currentbg, carbs, time):
        self.predictions = []
        # self.predictions = {}
        for i in range(0, len(time)):
            self.predictions.append(
                self.getprediction(time[i], currentbg, carbs))
        # st.write(self.predictions.__len__())
        list.append(self.predictions)
        return self.predictions

    def getpredictionsdf(self, currentbg, carbs, time):
        self.predictionsdf = pd.DataFrame(
            self.getpredictions(time, currentbg, carbs))
        # st.write(self.predictionsdf)
        return self.predictionsdf

    def getpredictionsdfplot(self, currentbg, carbs):
        self.predictionsdfplot = self.getpredictionsdf(currentbg, carbs)
        # st.write(self.predictionsdfplot)
        return self.predictionsdfplot
