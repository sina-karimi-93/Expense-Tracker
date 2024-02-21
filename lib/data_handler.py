

from typing import Generator
from datetime import datetime
from collections import defaultdict
from .interface.utils import load_json
from .interface.utils import write_json
from .constants import TABLE_HEADERS
from .constants import DATE_FORMAT

class DataHandler:
    """
    This class is for loading the expenses
    from the file and aggregate on it and
    return the desired expenses based on the
    given criteria.
    """
    def __init__(self,
                 data_path: str,
                 expenses_count: int) -> None:
        """
        ---------------------------------
        -> Params
            data_path: str
                json file that contains the epenses
        """
        self.data_path = data_path
        self.expenses_count = expenses_count
        self.expenses = self.load_expenses(self.data_path)
    
    def load_expenses(self, data_path: str) -> list:
        """
        Load data from the json file
        ---------------------------------
        -> Params
            data_path: str
        <- Return
            list of dicts
        """
        try:
            data = load_json(data_path)
            return data[:self.expenses_count]
        except FileNotFoundError:
            return list()
    
    def _filter_dates(self,
                     expense_date: datetime,
                     from_date: datetime,
                     to_date: datetime) -> bool:
        """
        Checks whether the expense is in the
        desired timeframe or not.
        ------------------------------------
        -> Params
            expense: dict
            from_date: datetime object
            to_date: datetime object
        <- Return
            bool
        """
        if from_date <= expense_date <= to_date:
            return True
        return False

    def _filter_expense(self,
                       expense: dict,
                       from_date: datetime,
                       to_date: datetime,
                       filters: dict) -> bool:
        """
        Checks whether the expense meets the desired
        criteria or not.
        --------------------------------------------
        -> Params
            expense: dict,
            from_date: datetime object
            to_date: datetime object
            filters: dict
        <- Return
            bool
        """
        if not self._filter_dates(expense["date"], from_date, to_date):
            return False
        for filter_name, value in filters.items():
            if not expense[filter_name].lower().startswith(value.lower()):
                return False
        return True

    def filter_data(self, filters: dict) -> list:
        """
        Filter the data based on the given filters.
        -------------------------------------------
        -> Params
            filters: dict
        <- Return
            list of expenses
        """
        from_date = filters.pop("from_date")                 
        to_date = filters.pop("to_date")                   
        data = filter(
            lambda expense: self._filter_expense(expense,
                                                 from_date,
                                                 to_date,
                                                 filters),
            self.expenses)
        return list(data)

    def get_all(self) -> list:
        """
        Returns the expenses.
        """
        return self.expenses
    
    def get_total_price(self, expenses: list) -> float:
        """
        Loops through the expenses and sum the
        overall price and return it.
        --------------------------------------
        -> Params
            expenses: list
        <- Return
            float
        """
        return sum(expense["overall_price"] for expense in expenses)

    def group_expenses_by_date(self,
                               expenses: list) -> dict:
        """
        Create new data strcture to group expenses
        based on day.
        ------------------------------------------
        -> Params
            expenses: list
        <- Return
            dict
        """
        grouped = defaultdict(list)
        for expense in expenses:
            grouped[expense["date"]].append(expense)
        return grouped
    
    def add_expense(self, expense: dict) -> None:
        """
        Add expense to the current expenses and
        save to file.
        ---------------------------------------
        -> Params
            expense: dict
        """
        self.expenses.append(expense)
        self.expenses = sorted(self.expenses,
                               key=lambda expense: expense["date"])
        self.expenses.reverse()
        write_json(self.data_path, self.expenses)
    
    def get_all_as_table(self) -> Generator:
        """
        Convert the expenses from list of dicts
        to list of tuples(values) for saving
        in csv and excel or sql.
        """
        yield TABLE_HEADERS
        for expense in self.expenses:
            row = list(expense.values())
            row[-1] = row[-1].strftime(DATE_FORMAT)
            yield row