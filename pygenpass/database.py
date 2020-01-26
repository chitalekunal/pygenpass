"""
Copyright (c) 2019 paint-it

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sqlite3  # library for database

class DatabaseConnection:
    """ Class of database entries for user's information."""

    def __create_table__(self,structure):
        """
        Create table structure
        {
            "tablename":"passwords",
            field_name1:
            {
                "datatype": "<INTEGER,REAL,TEXT,BLOB<NONE>",
                "nullablity" : "true",
                "unique_index" : "true",
                "primary_key" : "true",

            },
            field_name2:
            {
                "datatype": "<INTEGER,REAL,TEXT,BLOB<NONE>",
                "nullablity" : "true",
                "unique_index" : "true",
                "primary_key" : "true",
            },
            .
            .
            .
        }
        """
        create_sql = "CREATE TABLE IF NOT EXISTS "
        for key_level1 in structure:
            if key_level1 == 'tablename':
                create_sql = create_sql+structure["tablename"]+"(\n"
            else:
                for key_level2 in structure[key_level1]:
                    #Add more constrains as per requirements
                    if [key_level2] == "nullablity":
                        create_sql=create_sql+" NOT NULL "
                    elif [key_level2] == "unique_index":
                        create_sql=create_sql+" UNIQUE "
                    elif [key_level2] == "primary_key":
                        create_sql=create_sql+" PRIMARY KEY "
                create_sql=create_sql+",\n"
        create_sql=create_sql+");"

        """self.cursor_obj.execute(
            CREATE TABLE IF NOT EXISTS passwords
    		  (id integer PRIMARY KEY,portal_name text NOT NULL UNIQUE, password varchar,
    		  creation_date varchar, email varchar, portal_url varchar)
    		
        )"""
        self.cursor_obj.execute(create_sql)
        self.con.commit()


    def __init__(self,structure):
        """Used to create database and then to connect with generated databse file
        Checked for table is created? if not then created as per required values """
        self.con = sqlite3.connect("generated_password.db")
        self.cursor_obj = self.con.cursor()
        self.__create_table__(structure)

    def insert_data(self, structure): 
        """Adding values into database
        A dict structure is accepted as input parameter having format as below
        {
            "tablename" : "passwords",
            "field_name" : "value",
            .
            .
            .
        }
        """

        insert_data_string="INSERT INTO "+structure["tablename"]+"( "+','.join([key for key in structure if key != "tablename" ])+") VALUES ("+','.join([structure[key] for key in structure if key != "tablename" ])+")"
        self.cursor_obj.execute(insert_data_string)
        self.con.commit()

    def delete_data(self, structure):
        """
        Deleting values from database
        A dict structure is accepted as input parameter having format as below
        {
            "tablename":"passwords",
            "field_name":"value_to_delete",
            .
            .
            .
        }
        """
        delete_data_string="DELETE from "+structure["tablename"]+" where "+' and '.join([key+"="structure[key] for key in structure if key != "tablename"])
        self.cursor_obj.execute(delete_data_string)
        self.con.commit()

    def update_data(self, portal_name, password):
        """
        Updating values in database
        A dict structure is accepted as input parameter having format as below
        {
            "tablename":"passwords",
            "change_value":{
                "field_name":"value_to_set",
                "field_name1":"value_to_set1",
                .
                .
                .
\            }
            "condition":{
                "field_name":"value_to_delete",
                .
                .
                .
            }
        }

        """
        delete_data_string="UPDATE "+structure["tablename"]+" SET "+','.join([key+"="structure[key] for key in structure["change_value"] ])
        self.cursor_obj.execute(delete_data_string)
        
        self.portal_name = portal_name
        self.password = password
        self.cursor_obj.execute(
            """UPDATE passwords SET password =? WHERE portal_name =?""",
            (self.password, self.portal_name),
        )
        self.con.commit()

    def show_data(self, portal_name):
        """All inserted data will showed"""
        self.portal_name = portal_name
        self.cursor_obj.execute(
            """SELECT password FROM passwords WHERE portal_name=?""", (self.portal_name,),
        )
        rows = self.cursor_obj.fetchall()

        for row in rows:
            return row[0]

        self.con.commit()

    def show_all_data(self):
        """Showing all data saved in database"""
        self.cursor_obj.execute("""SELECT * FROM passwords""")
        rows = self.cursor_obj.fetchall()
        return rows
        self.con.commit()
