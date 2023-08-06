# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 10:24:45 2017

@author: Amine

EDA analysis
"""

import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import FormatStrFormatter

"""Config sns """
sns.set(style='white')
sns.axes_style('white')
sns.set_palette(sns.husl_palette(10,h=.4083,s=1,l=0.421))

""" utils """
def write_pdf(fname, figures):
    doc = PdfPages(fname)
    for fig in figures:
        fig.savefig(doc, format='pdf')
    doc.close()
    

class UnivariateEda() :
    
    """ Constructor """
    def __init__(self,data,cont_vars=[],cat_vars=[],id_var=None,threshol_mod = 8):
        self.df = data
        self._cont_vars = cont_vars
        self._cat_vars = cat_vars
        self._id_var = id_var
        self.variables = {}
        self.variables['Continuous'] = self._cont_vars
        self.variables['Categorical'] = self._cat_vars
        self.variables['Id'] = self._id_var
        self._fill_small_big_variables()
        self.ncount = len(self.df)
        self.threshol_mod = threshol_mod
        
        
        
    """ Methods """
    def _fill_small_big_variables(self):    
        
        self.variables['Categorical_small']=[]
        self.variables['Categorical_big']=[]
        # Fill Categorical_small and categorical_big
        for cat_var in self.variables['Categorical']:
            nb_modalities = len(self.df[cat_var].unique())
            if nb_modalities > self.threshol_mod:
                self.variables['Categorical_big'].append(cat_var)
            else :
                self.variables['Categorical_small'].append(cat_var)
    
    ##################################
    

    def analyze_na(self,show_graph=True):
        """Gives the status of na values in the dataset """
        all_variables = self.variables['Categorical'] + self.variables['Continuous']
        reports = []
        
        for var in all_variables :
            df_na = self.df[self.df[var].isnull()]
            nb_na = df_na.shape[0] 
            perc_na = nb_na/self.df.shape[0]
            report = {
                    'variable' : var,
                    'nb_missing' : nb_na,
                    'perct_missing':perc_na,
                    'type_variable' : 'X'
                        }
            reports.append(report)
            
        reports = sorted(reports,key= lambda x : x['perct_missing'],reverse=True)
       
       # Draw graph
        if show_graph :
            report_df = pd.DataFrame(reports)
            report_df = report_df[report_df.nb_missing > 0]
            if len(report_df) == 0:
                print('no missing values in this dataset')
                return
            ax = sns.barplot(x='variable',y='nb_missing',data=report_df)
            ax2=ax.twinx()
            ax2.yaxis.tick_left()
            ax.yaxis.tick_right()
            ax.yaxis.set_label_position('right')
            ax2.yaxis.set_label_position('left')
            ax2.set_ylabel('Frequency [%]')
            for p in ax.patches:
                x=p.get_bbox().get_points()[:,0]
                y=p.get_bbox().get_points()[1,1]
                ax.annotate('{:.0f}%'.format(100.*y/self.ncount), (x.mean(), y), 
                        ha='center', va='bottom') # set the alignment of the text
            ax.yaxis.set_major_locator(ticker.LinearLocator(11))
            ax2.set_ylabel('Frequency [%]')
            ax2.set_ylim(0,100)
            ax.set_ylim(0,self.ncount)
            #ax2.yaxis.set_major_locator(ticker.MultipleLocator(10))
            ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
            ax.set_title('Variables with missing values')
            plt.show()
       
       # Write report
        for report in reports :
            txt = "Variable {0} - Missing values {1:.0f} ({2:.1f}%)".format(report['variable'],report['nb_missing'],report['perct_missing']*100)
            print(txt)
           
    ##################################        
    def anlyse_cont_variable(self,var,show_graph=True):
        print('analyzing '+var+'...')
        if not(var in self.variables['Continuous']):
            raise Exception('analyse_cont_variables must take as input a continuous variable of the dataset')
        fig, axs = plt.subplots(2,sharex = True)
        sns.boxplot(self.df[var],ax=axs[1])
        sns.distplot(self.df[var].dropna(),label='all',ax=axs[0])
        plt.setp(axs[0].get_xticklabels(),fontsize=9,visible=True)
        txt = "mean : {0:.1f}\nstd : {1:.1f}\nmin : {2:.1f}\nmax : {3:.1f}".format(self.df[var].mean(),self.df[var].std(),self.df[var].min(),self.df[var].max())
        props = dict(boxstyle='round', facecolor='white', alpha=0.5)
        axs[0].text(0.05, 0.95, txt, transform=axs[0].transAxes, fontsize=10,
                verticalalignment='top', bbox=props)     
        axs[0].set_title(var + ' - distribution')
        if not show_graph :
            plt.close()
        return fig

        
    ################################## 
    def analyse_cat_small_variable(self,var,show_graph=True):
         if not(var in self.variables['Categorical_small']):
            raise Exception('analyse_cont_variables must take as input a continuous variable of the dataset')
    
         print('analyzing '+var+'...')
         self.df[var].fillna('missing',inplace=True)
         plt.figure()
         ax = sns.countplot(x=var,data=self.df)
         # Make twin axis
         ax2=ax.twinx()
         # Switch so count axis is on right, frequency on left
         ax2.yaxis.tick_left()
         ax.yaxis.tick_right()
         # Also switch the labels over
         ax.yaxis.set_label_position('right')
         ax2.yaxis.set_label_position('left')
         ax2.set_ylabel('Frequency [%]')
        
         for p in ax.patches:
             x=p.get_bbox().get_points()[:,0]
             y=p.get_bbox().get_points()[1,1]
             ax.annotate('{:.0f}%'.format(100.*y/self.ncount), (x.mean(), y), 
                    ha='center', va='bottom') # set the alignment of the text
                
        # Use a LinearLocator to ensure the correct number of ticks
         ax.yaxis.set_major_locator(ticker.LinearLocator(11))
        
        # Fix the frequency range to 0-100
         ax2.set_ylim(0,100)
         ax.set_ylim(0,self.ncount)
        
        # And use a MultipleLocator to ensure a tick spacing of 10
         ax2.yaxis.set_major_locator(ticker.MultipleLocator(10))
    
        # Need to turn the grid on ax2 off, otherwise the gridlines end up on top of the bars
        # ax2.grid(None)
        # ax.grid(None)
        
         ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))        
         ax.set_title(var)
         if not show_graph :
             plt.close()
         return ax.get_figure()

        
    ##################################
    def analyse_cat_big_variable(self,var,show_graph=True):        
        print('analyzing '+var+'...')
        # We should group the main variables
        df_grp = pd.DataFrame()
        if not(self.variables['Id'] is None):
            df_grp[self.variables['Id']] = self.df[self.variables['Id']]
        newvar = var+'_grp'    
        df_grp[newvar] = self.df[var]
        df_grp[newvar].replace(np.nan,'NA',inplace=True)
        # count the occurences of each modality
        df_grp = df_grp.groupby([newvar])[newvar].count()
        df_grp = df_grp.to_frame()
        nb_modalities = df_grp.shape[0]
        df_grp.rename(columns={newvar : 'count'},inplace=True)
        df_grp.reset_index(inplace=True)
        df_grp.sort_values('count',ascending=False,inplace=True)
        df_grp_up = df_grp.iloc[0:self.threshol_mod]
        df_grp_down = df_grp.iloc[self.threshol_mod:]
        sum_others = df_grp_down['count'].sum()
        if df_grp_down.shape[0] > 1 :    
            interm = pd.DataFrame({
                                    newvar :'others',
                                    'count':sum_others
                                    },index=[self.threshol_mod])
        else :
            interm = df_grp_down
        df_grp = df_grp_up.append(interm)
        df_grp.rename(columns={newvar : var},inplace=True)
        del df_grp_up,df_grp_down,interm
        
        # draw the graph
        
        plt.figure()
        ax = sns.barplot(x=var,y='count',data=df_grp)
        ax.set_ylabel('count')
        # Make twin axis
        ax2=ax.twinx()
        # Switch so count axis is on right, frequency on left
        ax2.yaxis.tick_left()
        ax.yaxis.tick_right()
        # Also switch the labels over
        ax.yaxis.set_label_position('right')
        ax2.yaxis.set_label_position('left')
        ax2.set_ylabel('Frequency [%]')
        
        for p in ax.patches:
            x=p.get_bbox().get_points()[:,0]
            y=p.get_bbox().get_points()[1,1]
            ax.annotate('{:.0f}%'.format(100.*y/self.ncount), (x.mean(), y), 
                    ha='center', va='bottom') # set the alignment of the text
                
        # Use a LinearLocator to ensure the correct number of ticks
        ax.yaxis.set_major_locator(ticker.LinearLocator(11))
        
        # Fix the frequency range to 0-100
        ax2.set_ylim(0,100)
        ax.set_ylim(0,self.ncount)
        
        # And use a MultipleLocator to ensure a tick spacing of 10
        ax2.yaxis.set_major_locator(ticker.MultipleLocator(10))
        
        # Need to turn the grid on ax2 off, otherwise the gridlines end up on top of the bars
        # ax2.grid(None)
        # ax.grid(None)
        
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
        
        title = var + ' -- {0} modalities'.format(nb_modalities)    
        plt.title(title)    

        if not show_graph :
             plt.close()
        return ax.get_figure()
        
    ### analyse dataset ###
    def analyse_univariate(self,link_export_pdf=''):
        print("")
        print("Begin univariate analysis of the data")
        graphs = []
        for var in self.variables['Continuous']:
            graphs.append(self.anlyse_cont_variable(var,show_graph=False))
        for var in self.variables['Categorical_small']:
            graphs.append(self.analyse_cat_small_variable(var,show_graph=False))
        for var in self.variables['Categorical_big']:
            graphs.append(self.analyse_cat_big_variable(var,show_graph=False))
        
        if link_export_pdf != '':
            write_pdf(link_export_pdf,graphs)
        print("End of univariate analysis of the data")
        return graphs
        
""" TEST """

#directory = 'C:/Users/Amine/Documents/Repos/Kaggle/Titanic/data/'
#file = 'train.csv'
#
#id_var = 'PassengerId'
#cont_vars = ['Age','Fare']
#cat_vars = ['Survived', 'Pclass', 'Sex','SibSp','Parch','Ticket','Cabin','Embarked']
#                
#                
#data = pd.read_csv(directory+file)
#sample = data[0:1000]
#data = data[data.Fare <= 200]
#eda = UnivariateEda(data,cont_vars,cat_vars,id_var)
#eda.variables
#eda.analyze_na(show_graph=False)
#
#eda.analyse_univariate()

#for var in eda.variables['Continuous']:
#    graph.append(eda.anlyse_cont_variable(var))

#for var in eda.variables['Categorical_small']:
#    graph.append(eda.analyse_cat_small_variable(var,False))

#for var in eda.variables['Categorical_big']:
#    graph.append(eda.analyse_cat_big_variable(var,False))



