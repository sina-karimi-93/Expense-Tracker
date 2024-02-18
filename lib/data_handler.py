
from datetime import datetime
from .interface.utils import load_json
from .interface.utils import write_json
from .constants import DATE_FORMAT

class DataHandler:
    """
    This class is for loading the expenses
    from the file and aggregate on it and
    return the desired expenses based on the
    given criteria.
    """
    def __init__(self,
                 data_path: str) -> None:
        """
        ---------------------------------
        -> Params
            data_path: str
                json file that contains the epenses
        """
        self.data_path = data_path
        self.expenses = self._load_expenses(data_path)
    
    def _load_expenses(self, path: str) -> list:
        """
        Open the expenses file and load the
        data.
        ---------------------------------------
        -> Params
            path: str
                expenses file path
        <- Return
            list of dicts
        """
        try:
            data = load_json(path)
            return data
        except FileNotFoundError:
            return list()
    
    def _filter_dates(self,
                     expense: dict,
                     from_date: str,
                     to_date: str) -> bool:
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
        expense_date = datetime.strptime(expense["date"], DATE_FORMAT)
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
        if not self._filter_dates(expense, from_date, to_date):
            return False
        for filter_name, value in filters.items():
            if expense[filter_name].lower() != value.lower():
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
        from_date = datetime.strptime(filters.pop("from_date"),
                                      DATE_FORMAT)
        to_date = datetime.strptime(filters.pop("to_date"),
                                    DATE_FORMAT)
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
    
    def add_expense(self, expense: dict) -> None:
        """
        Add expense to the current expenses and
        save to file.
        ---------------------------------------
        -> Params
            expense: dict
        """
        self.expenses.append(expense)
        write_json(self.data_path, expense)