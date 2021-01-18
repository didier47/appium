import os

import xlsxwriter

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class OperateReport:
    def __init__(self, wd):
        self.wd = wd

    def init(self, worksheet, data, devices):

        worksheet.set_column("A:A", 15)
        worksheet.set_column("B:B", 20)
        worksheet.set_column("C:C", 20)
        worksheet.set_column("D:D", 20)
        worksheet.set_column("E:E", 20)

        worksheet.set_row(1, 30)
        worksheet.set_row(2, 30)
        worksheet.set_row(3, 30)
        worksheet.set_row(4, 30)
        worksheet.set_row(5, 30)
        worksheet.set_row(6, 30)
        worksheet.set_row(7, 30)
        worksheet.set_row(8, 30)

        define_format_H1 = get_format(self.wd, {'bold': True, 'font_size': 18})
        define_format_H2 = get_format(self.wd, {'bold': True, 'font_size': 14})
        define_format_H1.set_border(1)

        define_format_H2.set_border(1)
        define_format_H1.set_align("center")
        define_format_H2.set_align("center")
        define_format_H2.set_bg_color("blue")
        define_format_H2.set_color("#ffffff")

        worksheet.merge_range('A1:E1', 'Descripción general del informe de prueba', define_format_H1)
        worksheet.merge_range('A2:E2', 'Resumen de la prueba de conocimientos de WebLink', define_format_H2)

        _write_center(worksheet, "A3", 'versionCode', self.wd)
        _write_center(worksheet, "A4", 'versionName', self.wd)
        _write_center(worksheet, "A5", 'packingTime', self.wd)
        _write_center(worksheet, "A6", 'Fecha de la prueba', self.wd)

        _write_center(worksheet, "B3", data['versionCode'], self.wd)
        _write_center(worksheet, "B4", data['versionName'], self.wd)
        _write_center(worksheet, "B5", data['packingTime'], self.wd)
        _write_center(worksheet, "B6", data['testDate'], self.wd)

        _write_center(worksheet, "C3", "Número total de casos de uso", self.wd)
        _write_center(worksheet, "C4", "Número total de pases", self.wd)
        _write_center(worksheet, "C5", "Número total de fallas", self.wd)
        _write_center(worksheet, "C6", "Pruebas que requieren mucho tiempo", self.wd)

        _write_center(worksheet, "D3", data['sum'], self.wd)
        _write_center(worksheet, "D4", data['pass'], self.wd)
        _write_center(worksheet, "D5", data['fail'], self.wd)
        _write_center(worksheet, "D6", data['testSumDate'], self.wd)

        _write_center(worksheet, "E3", "Lenguaje de escritura", self.wd)

        worksheet.merge_range('E4:E6', 'appium1.7+python3', get_format_center(self.wd))
        _write_center(worksheet, "A8", 'Estado', self.wd)
        _write_center(worksheet, "B8", 'Exitoso', self.wd)
        _write_center(worksheet, "C8", 'Fallido', self.wd)

        temp = 9
        for item in devices:
            _write_center(worksheet, "A%s" % temp, item["phone_name"], self.wd)
            _write_center(worksheet, "B%s" % temp, item["pass"], self.wd)
            _write_center(worksheet, "C%s" % temp, item["fail"], self.wd)
            temp = temp + 1

        pie(self.wd, worksheet)

    def detail(self, worksheet, info):

        worksheet.set_column("A:A", 30)
        worksheet.set_column("B:B", 20)
        worksheet.set_column("C:C", 20)
        worksheet.set_column("D:D", 20)
        worksheet.set_column("E:E", 20)
        worksheet.set_column("F:F", 20)
        worksheet.set_column("G:G", 20)
        worksheet.set_column("H:H", 20)
        worksheet.set_column("I:I", 20)
        worksheet.set_column("J:J", 20)

        worksheet.set_row(1, 30)
        worksheet.set_row(2, 30)
        worksheet.set_row(3, 30)
        worksheet.set_row(4, 30)
        worksheet.set_row(5, 30)
        worksheet.set_row(6, 30)
        worksheet.set_row(7, 30)
        worksheet.set_row(8, 30)
        worksheet.set_row(9, 30)
        worksheet.set_row(10, 30)

        worksheet.merge_range('A1:J1', 'Detalles de la prueba',
                              get_format(self.wd, {'bold': True, 'font_size': 18, 'align': 'center',
                                                   'valign': 'vcenter', 'bg_color': 'blue',
                                                   'font_color': '#ffffff'}))
        _write_center(worksheet, "A2", 'modelo', self.wd)
        _write_center(worksheet, "B2", 'ID de caso de uso', self.wd)
        _write_center(worksheet, "C2", 'introducción al caso de uso', self.wd)
        _write_center(worksheet, "D2", 'Función de caso de uso', self.wd)
        _write_center(worksheet, "E2", 'Precondición', self.wd)
        _write_center(worksheet, "F2", 'pasos de operación ', self.wd)
        _write_center(worksheet, "G2", 'Punto de control ', self.wd)
        _write_center(worksheet, "H2", 'Resultado de la prueba ', self.wd)
        _write_center(worksheet, "I2", 'Comentarios ', self.wd)
        _write_center(worksheet, "J2", 'captura de pantalla', self.wd)

        temp = 3
        for item in info:

            _write_center(worksheet, "A" + str(temp), item["phoneName"], self.wd)
            _write_center(worksheet, "B" + str(temp), item["id"], self.wd)
            _write_center(worksheet, "C" + str(temp), item["title"], self.wd)
            _write_center(worksheet, "D" + str(temp), item["caseName"], self.wd)
            _write_center(worksheet, "E" + str(temp), item["info"], self.wd)
            _write_center(worksheet, "F" + str(temp), item["step"], self.wd)
            _write_center(worksheet, "G" + str(temp), item["checkStep"], self.wd)
            _write_center(worksheet, "H" + str(temp), item["result"], self.wd)
            _write_center(worksheet, "I" + str(temp), item.get("msg", ""), self.wd)
            if item.get("img", "false") == "false":
                _write_center(worksheet, "J" + str(temp), "", self.wd)
                worksheet.set_row(temp, 30)
            else:
                worksheet.insert_image('J' + str(temp), item["img"],
                                       {'x_scale': 0.1, 'y_scale': 0.1, 'border': 1})
                worksheet.set_row(temp - 1, 110)
            temp = temp + 1

    def close(self):
        self.wd.close()


def get_format(wd, option={}):
    return wd.add_format(option)


def get_format_center(wd, num=1):
    return wd.add_format({'align': 'center', 'valign': 'vcenter', 'border': num})


def set_border_(wd, num=1):
    return wd.add_format({}).set_border(num)


def _write_center(worksheet, cl, data, wd):
    return worksheet.write(cl, data, get_format_center(wd))


def set_row(worksheet, num, height):
    worksheet.set_row(num, height)


def pie(workbook, worksheet):
    chart1 = workbook.add_chart({'type': 'pie'})
    chart1.add_series({
        'name': 'Estadísticas de prueba automatizadas',
        'categories': '=Resumen de la prueba!$C$4:$C$5',
        'values': '=Resumen de la prueba!$D$4:$D$5',
    })
    chart1.set_title({'name': 'Estadísticas de prueba'})
    chart1.set_style(10)
    worksheet.insert_chart('A9', chart1, {'x_offset': 25, 'y_offset': 10})


if __name__ == '__main__':
    sum = {'testSumDate': '25segundo', 'sum': 10, 'pass': 5, 'testDate': '2017-06-05 15:26:49', 'fail': 5,
           'appVersion': '17051515', 'appSize': '14M', 'appName': "'Libro breve'"}
    info = [
        {"id": 1, "title": "Abierto por primera vez", "caseName": "testf01", "result": "por", "phoneName": "Samsung"},
        {"id": 1, "title": "Abierto por primera vez",
         "caseName": "testf01", "result": "por", "img": "d:\\1.PNG", "phoneName": "Huawei"}]
    workbook = xlsxwriter.Workbook('Report.xlsx')
    worksheet = workbook.add_worksheet("Resumen de la prueba")
    worksheet2 = workbook.add_worksheet("Detalles de la prueba")
    bc = OperateReport(wd=workbook)
    bc.init(worksheet, sum)
    bc.detail(worksheet2, info)
    bc.close()
