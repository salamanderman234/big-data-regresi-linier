import pandas
from math import ceil

class Processor :
    def __init__(self, file_name : str, independent : str, dependent : str) -> None:
        self.file_name = file_name
        self.dependent = dependent
        self.independent = independent
    
    def __read(self):
        data = pandas.read_excel("sample/clean/" + self.file_name)
        self.file = data
    
    def __search_formula(self):
        datas = self.file.iloc
        
        x = 0
        y = 0
        sqX = 0
        sqY = 0
        xy = 0
        n = 0

        for data in datas :
            x += data[self.independent]
            y += data[self.dependent]
            sqX += data[self.independent]*data[self.independent]
            sqY += data[self.dependent]*data[self.dependent]
            xy += data[self.independent] * data[self.dependent]
            n += 1
        
        b = ((n * xy) - (x * y)) / ((n * sqX) - (x*x))
        a = (y/n) - (b * (x / n))

        self.formula = {
           "A" : a,
           "B" : b
        }

    def __evaluate(self):
        datas = self.file.iloc
        total_ape = 0
        new_datas = []
        for data in datas:
            new = {}
            if self.dependent in data :
                prediction = ceil(self.formula["A"] + self.formula["B"] * data[self.independent])
                error = data[self.dependent] - prediction
                abs_err = abs(error)
                ape = abs_err / data[self.dependent] * 100
                total_ape += ape

                new[self.independent] = data[self.independent]
                new[self.dependent] = data[self.dependent]
                new["Prediksi"] = prediction
                new["Error"] = error
                new["Error^2"] = error * error
                new["ABS(Error)"] = abs_err
                new["APE"] = ape

                new_datas.append(new)

            elif "Prediksi" in data:
                new[self.independent] = data[self.independent]
                new["Prediksi"] = data["Prediksi"]

                new_datas.append(new)
        
        # new_datas.append()
        self.result = new_datas
        self.result_error_sum = {self.independent : "MAPE",self.dependent : total_ape / len(new_datas), "Prediksi" : "%"}
    
    def __set_result(self):
        file_location = "sample/result/"+self.dependent+"-"+self.independent+"-"+self.file_name
        new = pandas.DataFrame(self.result)
        new.to_excel(file_location, index=False)
    
    def __predict(self):
        last_index = self.file.iloc[-1][self.independent]
        predicted_value = []

        for i in range(0,5):
            last_index += 1
            predicted_value.append({
                self.independent : last_index,
                "Prediksi" : ceil(self.formula["A"] + self.formula["B"] * last_index)
            })

        for i in predicted_value:
            self.result.append(i)
        self.result.append(self.result_error_sum)
            
    def process(self):
        self.__read()
        self.__search_formula()
        self.__evaluate()
        self.__predict()
        self.__set_result()

processor = Processor("data-penjualan-toko.xlsx", "Minggu" ,"Total Penjualan")
processor.process()