import sqlite3, re

class Database():
    """Create a Database and manage it. In all table, an 'id' column will be create.
    
    # Args:
    - name (str): The name of the DB (without .db at the end)
    
    - rows (list): A list of dict, just like that : [{"name": "email", "type": "int NOT NULL"}]
    
    - path (str) (optionnal): The Path where the Database will me created, leave blank will create it in the same folder as your current file
    
    # Raises:
    - TypeError: This error is raised when you give an incorrect variable
    
    - ValueError: This error is raised when you put a wrong variable

    """
    def __init__(self, name: str, rows: list, path: str = ""):
        
        if not isinstance(name, str): raise TypeError("The name of the Database need to be a string.")
        if not isinstance(rows, list): raise TypeError("Rows of the Database need to be a list.")
        if not isinstance(path, str): raise TypeError("The path of the Database need to be a string.")
        
        self.name = name if ".db" in name else name + ".db"
        self.rows = rows
        self.path = self.name if not path else path + f"/{self.name}"
        
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()
        
        command = f"""CREATE TABLE IF NOT EXISTS {name.replace(".db", "")} (
            id INTEGER PRIMARY KEY AUTOINCREMENT
        """
        
        for row in rows:
            if not "name" in row: raise ValueError(f"You forgot to give the name of the column on this row:\n{row}")
            if not "type" in row: raise ValueError(f"You forgot to give the type of the column on this row:\n{row}")
            
            if not isinstance(row["name"], str): raise TypeError(f"The name of the column need to be a string.\nRow: {row}")
            if not isinstance(row["type"], str): raise TypeError(f"The type of the column need to be a string.\nRow: {row}")
            
            if not re.match(r"^[a-zA-Z0-9_]+$", row["name"]):
                raise ValueError(
                    f"Invalid column name '{row['name']}'. Use only letters, numbers and"
                    " underscores."
                )
            
            command += f",\n{row['name']} {row['type']}"
        
        command += ")"
        self.cursor.commit(command)
        
    def execute(self, command: str, params: tuple = ()) -> bool | str:
        """Execute a SQL Command on the Database.
        
        # Args:
        - command (str): The SQL Command to run
        
        - params (tuple) (optionnal): The parameters to add when the command is run
        
        # Returns:
        - bool: Return if the command has been run successfully or not
        
        - str: If the command didn't run correctly, return the error
        """
        
        
        