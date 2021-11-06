import pandas as pd
import numpy as np

class PVMAnalysis:
    
    # Dataframe elements navigation
    __name_dictionary = {
                  'margin_pr':None,
                  'margin_ac':None,
                  
                  'quantity_pr':None,
                  'quantity_ac':None,
                  
                  'hierarchy':[]  
                 }
    
    __agg_dictionary = {}
    
    __data = None
    __data_multi_level = []
    __markers_set = False
    
    def __init__(self, data=None):
        '''
        Used for initialisation and basic error handling of the analysis.
        Parameters - Class reference, non-empty pandas dataset
        Return - None, creates a class instance
        '''
        
        if isinstance(data, pd.DataFrame):
            if data.shape == (0,0):
                raise ValueError('Empty dataframe passed for analysis.')
        else:
            raise ValueError('Pandas dataframe not passed for the analysis.')
        
        self.__data = data
        self.__data_multi_level.append(data)
    
    def setMarkers(\
                    self,
                    margin_pr=None,
                    margin_ac=None,
                    quantity_pr=None,
                    quantity_ac=None,
                    hierarchy=[]):
        '''
        Used to set pandas dataframe column names
        Parameters - Margin & Quantity column names, Dimension heirarchy from highest to lowest
        Return - None
        '''
        
        if margin_pr == None:
            raise ValueError('Previous Period Margin column not set!')
        if margin_ac == None:
            raise ValueError('Current Period Margin column not set!')
            
        if quantity_pr == None:
            raise ValueError('Previous Period Quantity column not set!')
        if quantity_ac == None:
            raise ValueError('Current Period Quantity column not set!')
            
        if len(hierarchy) == 0:
            raise ValueError('Hierarchy not specified!')
        
        self.__name_dictionary['margin_pr'] = margin_pr
        self.__name_dictionary['margin_ac'] = margin_ac
        self.__name_dictionary['quantity_pr'] = quantity_pr
        self.__name_dictionary['quantity_ac'] = quantity_ac
        self.__name_dictionary['hierarchy'] = hierarchy
        
        self.__markers_set = True
        self.__agg_dictionary = {
            margin_pr:'sum',
            margin_ac:'sum',
            quantity_pr:'sum',
            quantity_ac:'sum'
        }
    
    def __process_aggregated_result(self, key):
        '''
        Used to group latest df to desired aggregate level
        Parameters - key: List of columns of heirarchy being processed.
        Return - None
        '''
        
        self.__data_multi_level[-1] = self.__data_multi_level[-1]\
                                .groupby(key, dropna=False)\
                                .agg(self.__agg_dictionary)\
                                .reset_index()
    
    @staticmethod
    def __mark_other(self):
        '''
        Used for marking other category
        Parameters - None
        Returns - None
        '''
        
        def pd_flagger_function(m=None, q=None):
            return 1 if m!=0 and q==0 else 0
        
        self.__data_multi_level[-1]['Flag'] = self.__data_multi_level[-1].apply(\
                                                                               lambda r:\
                                                                               pd_flagger_function(\
                                                                                                          m=r[self.__name_dictionary['margin_pr']],
                                                                                                          q=r[self.__name_dictionary['quantity_pr']])
                                                                                or\
                                                                               pd_flagger_function(\
                                                                                                          m=r[self.__name_dictionary['margin_ac']],
                                                                                                          q=r[self.__name_dictionary['quantity_ac']]), 
                                                                               axis = 1)
        
    
    @staticmethod
    def __calculateOtherEffect(self):
        '''
        Used for marking other category
        Parameters - None
        Returns - None
        '''
        self.__data_multi_level[-1]['Other Effect'] = self.__data_multi_level[-1].apply(\
                                                                                        lambda r: (r[self.__name_dictionary['margin_ac']] - r[self.__name_dictionary['margin_pr']]) if r['Flag'] else 0
                                                                                        , axis = 1)
    @staticmethod    
    def __calculatePriceEffect(self):
        '''
        Used for calculation of price effect
        Parameters - None
        Returns - None
        '''
        
        def pd_price_effect(\
                            margin_pr=None
                           , margin_ac=None
                           , quantity_pr=None
                           , quantity_ac=None
                           , other=None):
            if other:
                return 0
            
            q_pr = 0 if quantity_pr in ([np.nan, None, np.inf, -np.inf]) else quantity_pr
            q_ac = 0 if quantity_ac in ([np.nan, None, np.inf, -np.inf]) else quantity_ac
            
            if(q_pr*q_ac==0):
                return 0
            return((margin_ac/quantity_ac - margin_pr/quantity_pr)*quantity_ac)
        
        self.__data_multi_level[-1]['Price Effect'] = self.__data_multi_level[-1].apply(\
                                                                                        lambda r: pd_price_effect(\
                                                                                                                 margin_pr=r[self.__name_dictionary['margin_pr']],
                                                                                                                 margin_ac=r[self.__name_dictionary['margin_ac']],
                                                                                                                 quantity_pr=r[self.__name_dictionary['quantity_pr']],
                                                                                                                 quantity_ac=r[self.__name_dictionary['quantity_ac']],
                                                                                                                 other=r['Flag'])
                                                                                        , axis = 1)
    
    @staticmethod    
    def __calculateVolumeEffect(self):
        '''
        Used for volume effect calculation
        Parameters - None
        Returns - None
        '''
        
        def pd_volume_effect(\
                            margin_pr=None
                           , margin_ac=None
                           , quantity_pr=None
                           , quantity_ac=None
                           , other=None):
            if other:
                return 0
            
            u_m_pr = margin_pr/quantity_pr if quantity_pr!= 0 else 0
            u_m_ac = margin_ac/quantity_ac if quantity_ac!= 0 else 0
            
            return((u_m_pr if u_m_pr!=0 else u_m_ac)*(quantity_ac-quantity_pr))
        
        self.__data_multi_level[-1]['Volume Effect'] = self.__data_multi_level[-1].apply(\
                                                                                        lambda r: pd_volume_effect(\
                                                                                                                 margin_pr=r[self.__name_dictionary['margin_pr']],
                                                                                                                 margin_ac=r[self.__name_dictionary['margin_ac']],
                                                                                                                 quantity_pr=r[self.__name_dictionary['quantity_pr']],
                                                                                                                 quantity_ac=r[self.__name_dictionary['quantity_ac']],
                                                                                                                 other=r['Flag'])
                                                                                        , axis = 1)
    @staticmethod
    def __calculateMixEffect(self, key):
        '''
        Used for mix effect calculation
        Parameters - None
        Returns - None
        '''
        
        current_col = key[-1]
        if len(key)==1:
            self.__data_multi_level[-1]['q_totals_pr'] =  self.__data_multi_level[-1][self.__name_dictionary['quantity_pr']].sum()
            self.__data_multi_level[-1]['q_totals_ac'] =  self.__data_multi_level[-1][self.__name_dictionary['quantity_ac']].sum()
        
        else:
            self.__data_multi_level[-1] = pd.merge(\
                                                      self.__data_multi_level[-1]\
                                                    , self.__data_multi_level[-1]\
                                                                            .groupby(key[:-1], dropna=False).agg(q_totals_pr=(self.__name_dictionary['quantity_pr'], 'sum'),
                                                                                                                 q_totals_ac=(self.__name_dictionary['quantity_ac'], 'sum'))\
                                                                            .reset_index()\
                                                    , left_on=key[:-1]
                                                    , right_on=key[:-1])
            
        def pd_mix_effect(\
                             margin_pr=None
                           , margin_ac=None
                           , quantity_pr=None
                           , quantity_ac=None
                           , quantity_pr_t=None
                           , quantity_ac_t=None
                           , other=None):
            
            if other:
                return 0
            
            if(quantity_pr_t==0 or quantity_ac_t==0):
                return 0
            
            if(quantity_pr==0 or quantity_ac==0):
                return (margin_ac-margin_pr)
            
            unit_margin_py = margin_pr/quantity_pr if quantity_pr!=0 else 0
            unit_margin_ac = margin_ac/quantity_ac if quantity_ac!=0 else 0
            
            return (unit_margin_py if unit_margin_py!=0 else unit_margin_ac)*((quantity_ac/quantity_ac_t*quantity_ac_t)-(quantity_pr/quantity_pr_t*quantity_ac_t))
        
        
        self.__data_multi_level[-1]['{} Mix Effect'.format(current_col)] = self.__data_multi_level[-1].apply(\
                                                                                        lambda r: pd_mix_effect(\
                                                                                                                 margin_pr=r[self.__name_dictionary['margin_pr']],
                                                                                                                 margin_ac=r[self.__name_dictionary['margin_ac']],
                                                                                                                 quantity_pr=r[self.__name_dictionary['quantity_pr']],
                                                                                                                 quantity_ac=r[self.__name_dictionary['quantity_ac']],
                                                                                                                 quantity_pr_t=r['q_totals_pr'],
                                                                                                                 quantity_ac_t=r['q_totals_ac'],
                                                                                                                 other=r['Flag'])
                                                                                        , axis = 1)
        
        self.__agg_dictionary['{} Mix Effect'.format(current_col)] = 'sum'
        
    @staticmethod
    def __adjustVolumeEffect(self, key):
        current_col = key[-1]
        self.__data_multi_level[-1]['Volume Effect'] = self.__data_multi_level[-1]['Volume Effect'] - self.__data_multi_level[-1]['{} Mix Effect'.format(current_col)]
        
    @staticmethod
    def __adjustOtherEffect(self):
        self.__data_multi_level[-1]['Total Mix Effect'] = 0
        
        for key in self.__agg_dictionary:
            try:
                if ' '.join(key.split(' ')[-2:]) == 'Mix Effect':
                    self.__data_multi_level[-1]['Total Mix Effect'] += self.__data_multi_level[-1]['{}'.format(key)]
            except:
                continue
            
        self.__data_multi_level[-1]['Other Effect'] =   self.__data_multi_level[-1][self.__name_dictionary['margin_ac']]\
                                                      - (   self.__data_multi_level[-1]['Other Effect']\
                                                          + self.__data_multi_level[-1]['Total Mix Effect']\
                                                          + self.__data_multi_level[-1]['Price Effect']\
                                                          + self.__data_multi_level[-1]['Volume Effect']
                                                          + self.__data_multi_level[-1][self.__name_dictionary['margin_pr']]
                                                        )
        
    
    def __calculateBridgeElements(self, key):
        '''
        Calculates layered metrics, handles metrics creation also.
        Parameters - None
        Return - None
        '''
        # Mark a flag for other condition
        self.__mark_other(self)
        
        # Check if it's the base level metrics
        if(key==self.__name_dictionary['hierarchy']):
    
            # Other Effect
            PVMAnalysis.__calculateOtherEffect(self)
            
            # Calculate Price Effect
            PVMAnalysis.__calculatePriceEffect(self)
            
            # Volume Effect
            PVMAnalysis.__calculateVolumeEffect(self)
            
            # Append to aggregation dictonary
            self.__agg_dictionary['Other Effect'] = 'sum'
            self.__agg_dictionary['Price Effect'] = 'sum'
            self.__agg_dictionary['Volume Effect'] = 'sum'
            
        # Mix Effect
        PVMAnalysis.__calculateMixEffect(self, key)
        
        # Effect Alteration
        PVMAnalysis.__adjustVolumeEffect(self, key)
        PVMAnalysis.__adjustOtherEffect(self)
        
    def calculateMarginBridge(self):
        '''
        Center point function for calculating the bridge.
        Parameters - None
        Return - None
        '''
        
        if self.__markers_set == False:
            raise ValueError('Please set the markers to the dataframe using the setMarkers() method!')
        
        key = self.__name_dictionary['hierarchy']
        
        while(len(key)!=0):
            # Perform aggregation on key
            self.__process_aggregated_result(key)
            
            # Calculate metrics
            self.__calculateBridgeElements(key)
            
            # Move to higher level
            key.pop()
    
    def __find_labels(self):
        labels = [self.__name_dictionary['margin_pr'], 'Price Effect', 'Other Effect']
        for key in self.__agg_dictionary:
            try:
                if ' '.join(key.split(' ')[-2:]) == 'Mix Effect':
                    labels.append(key)
            except:
                pass
        labels.append('Volume Effect')
        labels.append(self.__name_dictionary['margin_ac'])
        return labels
    
    def __find_values(self, labels=None):
        values = []
        for label in labels[:-1]:
            values.append(self.__data_multi_level[-1][label].sum())
        values.append(0)
        return values
    
    def plotPVMBridge(self, t='PVM Analysis Margin Bridge'):
        '''
        Used to plot margin bridge.
        Parameters - t: Title for analysis
        Return - None
        '''
        
        import plotly.graph_objects as go

        labels = self.__find_labels()
        values = self.__find_values(labels)
        
        fig = go.Figure(go.Waterfall(
        orientation = "v",
        measure = ["relative"]*(len(labels)-1) + ["total"],
        x = labels,
        y = values,
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
        ))

        fig.update_layout(
                title = t,
                showlegend = False
        )

        fig.show()
        self.__find_labels()
    
    
    def exportMarginBridgeFile(self):
        '''
        Exports all the processing files at different levels.
        Parameters - None
        Return - None
        '''

        self.__data_multi_level[-1].to_csv('Bridge_Export.csv')