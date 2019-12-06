# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 18:22:21 2019

@author: dso-s.gao
"""

import pandas as pd

class Datacheck_V1():
    """
    データ概要を自動表示ツールです。
    これは試作です。（debugもしてません）
    エラーとか、こういう機能があったほうがいいとかがあったら
    利用者がパージョンUPをお願いします。
　　修正LOGを残してください。
    """
    
    def _get_attribute(self):
        self.length = len(self.data)
        self._columns = self.data.columns
        self._data_type = self.data.dtypes
    
    def _calc_null_rate(self):
        self._null_rate = ["{:.2%}".format(self.data[col].isnull().sum() / self.length) for col in self._columns]
        
    def _calc_zero_rate(self):
        self.zero_rate =  \
            ["{:.2%}".format(self.data[self.data[col]==0][col].count() / self.length) 
             if self._data_type[col] == "int64" else "0.00%" for col in self._columns]
        
    def _get_region(self):
        list_ = []
        
        for col in self._columns:
            dtype = self._data_type[col]
            
            if (dtype == "int64") or (dtype=="int32") or (dtype == "float64") or (dtype == "float64"):
                list_.append("最小値{:.2f}～最大値{:.2f}".format(min(self.data[col]), max(self.data[col])))
            
            elif dtype == "object":
                
                try:
                    pd.to_datetime(self.data[col])
                    list_.append("{0}～{1}".format(min(pd.to_datetime(self.data[col])), max(pd.to_datetime(self.data[col]))))
                    print(col + "はTimestampです。pd.to_datetimeを試してください")
                
                except (TypeError, ValueError) as e:
                    _seq = self.data[col].unique()
                    if len(_seq) > 5:
                        list_.append("{0},{1}とそのほか{2}個".format(_seq[0], _seq[1], len(_seq) - 2))  
                    else:
                        list_.append("{}".format(_seq)) 
            
            elif dtype == "datetime64[ns]":
                list_.append("{0}～{1}".format(min(pd.to_datetime(self.data[col])), max(pd.to_datetime(self.data[col]))))
                
            else:
                raise TypeError("見たことの型が入ったねと高が言ってた")                        
        self.list_ = list_
    
    def make_output(self, data):
        self.data = data
        self._get_attribute()
        self._calc_null_rate()
        self._calc_zero_rate()
        self._get_region()
        
        print("レコード数", self.length)
        return pd.DataFrame([self._data_type.values, 
                             self._null_rate,
                             self.zero_rate,
                             self.list_], 
                     columns= self._columns, 
                     index= ["型", "欠損率", "zeroが含む率", "データの範囲"]).T 
    
    @classmethod
    def export_output(cls, df):
        return cls().make_output(data=df)