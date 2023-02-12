import csv
import sys


class CSVReader:

    def __init__(self, file):
        self.cell_dictionary = {}
        self.read_file = []
        self.column = []
        self.error = False
        self.reading_a_file(file)

    def reading_a_file(self, file: str):
        with open(file, encoding='utf-8') as file:
            reader_f = csv.reader(file, delimiter=',')
            for row in reader_f:
                self.read_file.append(row)
                self.column.append(row[0])
            if not self.creating_dictionary():
                return
            self.overwriting_cells()

    def creating_dictionary(self):
        """
        Создание словаря.
        Ключ словаря - название ячейки таблицы. Значение - данные ячейки.
        """

        def Error(text):
            print(text)
            self.error = True

        try:
            for f_row in range(1, len(self.read_file)):
                for f_column in range(1, len(self.read_file[0])):
                    if str(str(self.read_file[0][f_column]) + str(self.column[f_row])) in self.cell_dictionary.keys():
                        Error('Неверный формат ячеек.')
                        return False
                    if str(self.read_file[0][f_column]).isdigit() or not str(self.column[f_row]).isdigit():
                        Error('Неверный формат ячеек.')
                        return False
                    else:
                        self.cell_dictionary[str(self.read_file[0][f_column]) + str(self.column[f_row])] = \
                            self.read_file[f_row][f_column]
            return True
        except IndexError:
            Error('Неверный формат таблицы.')
            return False

    def overwriting_cells(self):
        for f_row in range(1, len(self.read_file)):
            for f_column in range(1, len(self.read_file[0])):
                if '=' in self.read_file[f_row][f_column][0]:
                    self.read_file[f_row][f_column] = self.counting_cell_values(self.read_file[f_row][f_column])
                elif '=' in self.read_file[f_row][f_column]:
                    self.read_file[f_row][f_column] = 'Error'
                self.cell_dictionary[str(self.read_file[0][f_column]) + str(self.column[f_row])] = \
                    self.read_file[f_row][f_column]

    def counting_cell_values(self, string):

        def original_string_conversion(input_line: str):
            """
            Преобразование строки. Замена символов '+','-','*','/' на '&'.
            Возвращает: преобразованную строку, список символов в исходной последовательности.
            :param input_line: str;
            :return: out_line: str;
            :return: symbol_lst: list;
            """
            symbol_lst = []
            out_line = ""
            input_line = list(input_line)
            for index in range(len(input_line)):
                if input_line[index] in '*/+-':
                    symbol_lst.append(input_line[index])
                    input_line[index] = '&'
                out_line += input_line[index]
            return out_line, symbol_lst

        def reverse_string_conversion(input_line: str, symbol_lst: list):
            """
            Обратное преобразование строки.
            Возвращает строку с исходными арифметическими знаками.
            :param input_line: str;
            :param symbol_lst: list;
            :return: out_line: str;
            """
            input_line = list(input_line)
            out_line = ""
            for index in range(len(input_line)):
                if input_line[index] in '&':
                    input_line[index] = symbol_lst.pop(0)
                out_line += input_line[index]
            return out_line

        try:
            if isinstance(string, (int, float, bool)):
                return string

            # Преобразование строки (замена математических знаков на символ &)
            if '+' in string or '-' in string or '/' in string or '*' in string:
                result_string, symbol_list = original_string_conversion(string)
                lst_component = result_string.split('&')
            else:
                if string[0] == '=':
                    lst_component = [string]
                else:
                    return str(string)

            # Преобразование элементов ячейки к числовым значениям
            for i in range(len(lst_component)):
                if str(lst_component[i])[0] == '=':
                    lst_component[i] = lst_component[i][1:]

                if not str(lst_component[i]).isdigit():
                    try:
                        lst_component[i] = self.counting_cell_values(self.cell_dictionary[lst_component[i]])
                    except KeyError:
                        return 'Error'
            out_string = '&'.join(str(component) for component in lst_component)

            # Вычисление результата значения ячейки
            try:
                out_string = reverse_string_conversion(out_string, symbol_list)
                result = eval(out_string)
            except ZeroDivisionError:
                return "Error"
            except NameError:
                return "Error"
            except TypeError:
                return "Error"
        except IndexError:
            return 'Error'

        return result

    def print_result_in_console(self):
        """
        Вывод полученной таблицы в консоль.
        """
        if not self.error:
            for f_row in self.read_file:
                print(*f_row, sep=',')


def console_initialization():
    a = sys.argv
    try:
        if '.csv' in a[1]:
            ex = CSVReader(a[1])
            ex.print_result_in_console()
        else:
            print('Неверный формат файла (файл должен иметь формат .csv)!')
    except FileNotFoundError:
        print('Указан неправильный путь или имя файла!')
    except IndexError:
        print("Укажите csv файл для чтения. -csvreader.exe ['file.csv']")


if __name__ == '__main__':
    console_initialization()
    # f = CSVReader("CSVFiles/file.csv")
    # f.print_result_in_console()
