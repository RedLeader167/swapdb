import json, os

_SWAPDB_INF = ["nsdb", 1]

class SwapDBException(Exception):
    pass

class Condition:
    def __init__(self):
        raise SwapDBException("Do not use Condition, instead use other classes (see docs).")

class Equal(Condition):
    def __init__(self, first, second):

class selector:
    def __init__(self):
        self.c = []
    def where(self, condition):
        if isinstance("")
class SwapDB:
    def __init__(self, path: str):
        if not os.path.isfile(path):
            raise SwapDBException("Database not exists. Use 'swapdb.create(path)'.")
        try:
            f = open(path).read()
            f = json.loads(f)
            if f["format"][0] != _SWAPDB_INF[0]:
                raise SwapDBException("Incorrect format.")
            if f["format"][1] > _SWAPDB_INF[1]:
                raise SwapDBException("Version of loaded database is lower than current SwapDB version. Consider updating via pip.")
            self.db = f
            self.path = path
        except Exception as e:
            raise SwapDBException("Exception occured while reading: " + str(e))
    
    def __save(self) -> None:
        open(self.path, "w").write(json.dumps(self.db))
    
    def tables(self) -> list:
        """
        List all table names in current database.
        """
        for i in self.db["tables"]:
            yield i
    
    def create_table(self, name: str, head: list) -> None:
        """
        Create new table with specified name and head.
        Example:
        db.create_table("MyTable", ["id", "name"])
        """
        if name in self.db["tables"]:
            raise SwapDBException("Table already exists.")
        if not isinstance(head, list):
            raise SwapDBException(str(type(head)) + " passed in head parameter, should be list.")
        for i in head:
            if not isinstance(i, str):
                raise SwapDBException("head parameter takes list with strings only!")
        self.db["tables"][name] = {"header": head, "data": []}
        self.__save()
    
    def insert(self, table: str, data: list) -> None:
        """
        Inserts new row with given data (should follow table head)
        Example:
        db.insert("MyTable", [1, "John"])
        """
        pass

if __name__ == "__main__":
    db = SwapDB("test.json")
    print(', '.join(db.tables()))
    db.create_table("MyTable", ["id", "name"])