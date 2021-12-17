import json, os

_SWAPDB_INF = ["nsdb", 1]

class SwapDBException(Exception):
    pass

class Query:
    def __init__(self, type: str, db: dict, table: str):
        self.type = type
        self.table = table
        self.db = db
        self.q = []
    
    def where_equals(self, db_identifier: str, value: object) -> object:
        """
        Row, where column equals specified value.
        """
        self.q.append(["we", db_identifier, value])
        return self
    
    def get(self) -> object:
        """
        Complete the query.
        """
        if self.type == "select":
            rows = []
            for i in self.q:
                if i[0] == "we":
                    id = None
                    for i1 in range(len(self.db["tables"][self.table]["header"])):
                        if i[1] == self.db["tables"][self.table]["header"][i1]:
                            id = i1
                            break
                    if id == None:
                        raise SwapDBException("No column with such identifier.")
                    for i1 in self.db["tables"][self.table]["data"]:
                        if i1[id] == i[2]:
                            rows.append(i1)
                    for i1 in rows:
                        if i1[id] != i[2]:
                            rows.remove(i1)
            return rows
        else:
            raise SwapDBException("Unknown query type.")

def create(path):
    db = {
        "format": _SWAPDB_INF,
        "tables": {}
    }
    open(path, "w").write(json.dumps(db))

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
        if table not in self.db["tables"]:
            raise SwapDBException("Table already exists.")
        if len(self.db["tables"][table]["header"]) != len(data):
            raise SwapDBException("Head size and data size should be same!")
        self.db["tables"][table]["data"].append(data)
        self.__save()
        
    def select(self, table: str) -> Query:
        """
        Select something from db.
        Example:
        print(db.select().where_equals("id", 1).get())
        """
        return Query(type="select", db=self.db, table=table)

if __name__ == "__main__":
    db = SwapDB("test.json")
    print(', '.join(db.tables()))
    #db.create_table("MyTable", ["id", "name"])
    db.insert("MyTable", [3, "Peter"])
    print(db.select("MyTable").where_equals("id", 3).get())