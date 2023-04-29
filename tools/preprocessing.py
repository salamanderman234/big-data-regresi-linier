import pandas
import datetime
from math import ceil


class Preprocessor :
    def __init__(self, file_name : str, attributes: list, date_attribute: str) -> None:
        self.file_name = file_name
        self.attributes = attributes
        self.date_attribute = date_attribute
    
    def __read(self):
        data = pandas.read_excel("sample/" + self.file_name)
        self.file = data
    
    def __clean(self):
        datas = []
        for data in self.file.iloc :
            datas.append({ attribute : data[attribute] for attribute in self.attributes})
        self.cleaned_data = datas
    
    def __cluster_data(self):
        transaction_totals = {}
        bruto_totals = {}
        qty_totals = {}
        for data in self.cleaned_data:
            date = data[self.date_attribute]
            week = str(int(date.strftime("%V")) - 4)

            transaction_totals[week] = transaction_totals.get(week, 0)  + 1
            bruto_totals[week] = bruto_totals.get(week, 0) + data["Bruto"]
            qty_totals[week] = qty_totals.get(week, 0) + data["Qty"]

        clustered_data = []
        for transc in transaction_totals:
            clustered_data.append({
                "Minggu" : int(transc),
                "Total Transaksi" : int(transaction_totals[transc]),
                "Total Penjualan" : int(bruto_totals[transc]),
                "Total Produk Terjual" : int(qty_totals[transc])
            })
        self.clustered_data = clustered_data

    def __set_result(self):
        file_location = "sample/clean/"+self.file_name
        new = pandas.DataFrame(self.clustered_data)
        new.to_excel(file_location, index=False)

    def process(self):
        self.__read()
        self.__clean()
        self.__cluster_data()
        self.__set_result()

preprocessor = Preprocessor("data-penjualan-toko.xlsx", ["Tanggal", "Qty", "Harga", "Bruto"], "Tanggal")
preprocessor.process()