"""
This module is about working with an excel file.
"""
from os.path import exists
from win32com.client import Dispatch
from typing import Generator
from typing import Any

__version__ = "1.0"
__all__ = ["ExcelHandler"]


class ExcelHandlerBaseException(Exception):
    """
    Custom base class for the exceptions
    """
    def __init__(self, message: str = None):
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return f"{self.message}"

    def __len__(self) -> int:
        return len(self.message)

    @property
    def error_message(self) -> str:
        """
        Return exception error_message
        """
        return self.message

    def to_dict(self) -> dict:
        """
        return error message as dictionary.
        make it easier for the to pass error
        in RestApi
        """
        return {"error": self.message,
                "type": self.__class__.__name__}


class NotFoundExcelFileError(ExcelHandlerBaseException):
    """
    Raises when couldn't find the desired file.
    """
    
class NotFoundSheetError(ExcelHandlerBaseException):
    """
    Raises when couldn't find the desired sheet.
    """

class ExcelHandler:
    """
    This class contains all the tools to open
    an excel file, fetch its data and update
    them.

    @methods
        open_excel
        create_new
        set_sheet
        get_columns_count
        get_rows_count
        fetch_all
        fetch_range
        get_as_dict
        update_cell
        save
        save_as
        close
    
    @note
        better to use this class as context manager.
    """
    EMPTY_ROWS_TOLERANCE = 5
    def __init__(self,
                 dev: bool = False) -> None:
        self.excel_app = Dispatch("Excel.Application")
        self.rows_count = 0
        if dev:
            self.excel_app.Visible = 1

    def __enter__(self)-> object:
        return self
    
    def __exit__(self, *args) -> object:
        self.close()
    
    def open_excel(self, 
                   file_path: str,
                   sheet_name: str = None) -> None:
        """
        Open an excel file if the path provided
        or create new one of file path is empty.
        """
        if not exists(file_path):
            raise NotFoundExcelFileError("Couldn't find the desired excel file.")
        self.excel_app.Workbooks.open(file_path)
        self.work_book = self.excel_app.WorkBooks(1)
        self.set_sheet(sheet_name)

    def create_new(self)-> None:
        """
        Create new excel file
        """
        self.excel_app.Workbooks.Add()
        self.work_book = self.excel_app.WorkBooks(1)
        self.set_sheet()

    def set_sheet(self, sheet_name: str = None) -> None:
        """
        Set the sheet file in an excel file.
        ------------------------------------
        -> Params
            sheet_name: str
        """
        if not sheet_name:
            self.sheet = self.work_book.Sheets(1)
            return
        total_sheets_count = self.work_book.Sheets.Count
        for sheet_number in range(1, total_sheets_count + 1):
            self.sheet = self.work_book.Sheets(sheet_number)
            if self.sheet.name == sheet_name:
                break
        raise NotFoundSheetError("Desired sheet is not in the file.")

    def get_columns_count(self) -> int:
        """
        Loop through the first row and count
        the number of columns until it faces
        empty column and stops. Then return
        the counter as number of columns.
        so line order null
        """
        column_count = 0
        while True:
            if self.sheet.Cells(1, column_count + 1).value:
                column_count += 1
                continue
            break
        return column_count
    
    def _calculate_rows_count(self,
                             columns_count: int,
                             rows_count: int = 1,
                             stride: int = 1000) -> None:
        """
        Recursive method to find the last row in
        the file.
        ----------------------------------------
        -> Params
            columns_count: int
            rows_count: int
            stride: int
        """
        if stride == 0:
            self.rows_count = rows_count - 1
            return
        row_data = self.sheet.Range(
                            self.sheet.Cells(rows_count, 1),
                            self.sheet.Cells(rows_count, columns_count))
        row_data = row_data.value[0]
        if any(row_data):
            rows_count += stride       
        else:
            stride //= 2
            rows_count -= stride
        self._calculate_rows_count(columns_count, rows_count, stride)

    def check_empty_rows(self, columns_count: int) -> int:
        """
        In some of files, there are spaces between
        rows. This method checks them whether is 
        there any row after the last calculated
        row or not. If yes then tries to find the
        last rows and returns the new number of rows
        count.
        --------------------------------------------
        -> Params
            columns_count: int
        """
        empty_rows_faced_coount = 1
        rows_count = self.rows_count + 1
        while empty_rows_faced_coount < self.EMPTY_ROWS_TOLERANCE:
            rows_count += 1
            row_data = self.sheet.Range(
                            self.sheet.Cells(rows_count, 1),
                            self.sheet.Cells(rows_count, columns_count))
            row_data = row_data.value[0]
            if any(row_data):
                empty_rows_faced_coount = 0
                continue
            empty_rows_faced_coount += 1
        rows_count -= self.EMPTY_ROWS_TOLERANCE
        return rows_count
    
    def calculate_rows_count(self, columns_count: int) -> int:
        """
        Returns the number of valid rows(end of the file)
        count.
        -------------------------------------------------
        -> Params
            columns_count: int
        <- Return
            rows_count: int
        """
        self._calculate_rows_count(columns_count)
        rows_count = self.check_empty_rows(columns_count)
        return rows_count

    def fetch_all(self, 
                  rows_count: int = None,
                  columns_count: int = None) -> Generator:
        """
        Fetch all data in the data.
        ------------------------------------
        -> Params
            rows_count : int
            columns_count: int
        <- Return
            Generator
        @note
            As the end of the sheet is not specified
            and we have to find it by ourselve, user
            can specify the end last row and column
            to ignore the steps finding the last row
            and column.
        """
        self.rows_count = rows_count
        if not all((rows_count, columns_count)):
            columns_count = self.get_columns_count()
            rows_count = self.calculate_rows_count(columns_count)
        yield from self.fetch_range((1, 1), 
                                    (rows_count, columns_count))

    def fetch_range(self, start: tuple, end: tuple) -> Generator:
        """
        Fetch data from sepcific positions range
        in the file.
        ----------------------------------------
        -> Params
            start: tuple → (1, 1)
            end: tuple → (14556, 3)
        """
        range_object = self.sheet.Range(self.sheet.Cells(*start),
                                        self.sheet.Cells(*end))
        yield from range_object.value

    def get_as_dict(self, 
                    headers: tuple,
                    data: Generator) -> Generator:
        """
        Returns the data as a dicts
        """
        for row in data:
            yield dict(zip(headers, row))

    def update_cell(self,
                    cell_position: tuple,
                    value: Any) -> None:
        """
        Update a cell in the active sheet
        with new value.
        ------------------------------------------
        -> Params
            cell_positions: tuple → (5, 6)
            value: anything → int, float, datetime, string
        """
        self.sheet.Cells(*cell_position).value = value

    def save(self) -> None:
        """
        Save current open file.
        """
        self.work_book.Save()
    
    def save_as(self, file_path: str) -> None:
        """
        Save current work book to new file.
        """
        self.work_book.SaveAs(file_path)

    def close(self)-> None:
        """
        Close the app
        """
        if self.excel_app.ActiveWorkbook:
            self.excel_app.ActiveWorkbook.Close()
        del self.excel_app

if __name__ == "__main__":
    import time
    from os import getcwd
    root = getcwd()
    with ExcelHandler() as handler:
        handler.open_excel(f"{root}\data\order analyzer data excel.xlsx")
        now = time.time()
        data = list(handler.fetch_all())
        end = time.time() - now
        print(data[0])
        print("==========================")
        print(len(data))
        print(end, " Seconds")