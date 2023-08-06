import os

class RecursiveDep(object):

    """
    Map all dependencies for a database/schema, to advise changes.
        args:
            host: the hostname to use to connect to
            database: the database to check against
            form: the form to return the result
            """

    def __init__(self, host="localhost", database="mysql",
                 table="user", form="tree"):
        """create assertion object."""
        self.host = host
        self.database = database
        self.table = table
        self.form = form
        self.storage = set()  # set of lists for result

    def _run_mysql(self, command):
        """Run the mysql query and get the result as a list."""
        cmd = ["mysql",  "-h", self.host, self.database,
               "-sss", "-e", "\"{command};\"".format(command=command)]
        return os.subprocess.check_output(cmd).splitlines()

    def find(self):
        """Find, store, and show all dependencies."""
        # get tables in db
        table_query = "select TABLE_NAME from information_schema.TABLES \
        where TABLE_SCHEMA='{db}'".format(db=self.database)
        tables = self._run_mysql(table_query)
        # call _find_deps for all and store
        for table in tables:
            self._store(table, self._find_deps(table))
        # call the appropriate result function

    def _store(self, from_table, to_table):
        """Store the result to internal variable."""
        self.storage.add([from_table, to_table])

    def _find_deps(self, tablename):
        """Find dependencies for a given table, given by name."""
        dep_query = """select TABLE_NAME from information_schema.KEY_COLUMN_USAGE
        where TABLE_SCHEMA = "{db}" and REFERENCED_TABLE_NAME = "{table}"
        and referenced_column_name is not NULL;""".format(db=self.database,
                                                          table=tablename)
        return self._run_mysql(dep_query)

    def _connect_deps(self, tablename, maxdep=5):
        """Get the tree of dependencies for a table, up to maxdep times.
            input:
                tablename(str) - which table to start with.
                maxdep(int) - (optional) how many layers deep to go
            output:
                """
        connecting = True  # while condition set
        # for each iteration
        working = []  # list of tables to work through
        working2 = [] # list of tables to add next iteration
        result = []
        pos = 0  # position for result, and for maxdep
        working.append(tablename)
        while connecting:
            for table in working:
                # remove from working
                working.remove(table)
                # all tables with relevant depenency
                midres = [x[1] for x in self.storage if x[0]==table]
                #add to working
                working2.extend(midres)
            # prepare for next level deep
            working = list(set(working2))
            working2 = []
            # check if we should continue
            result[pos] = working  # save the result
            pos = pos + 1
            if (not midres) or (pos >= maxdep):
                    continue = False  # end the loop

    def _graph_result(self):
        """The result display function for the graph output."""
        pass

    def _text_result(self):
        """The result displa function for text or command line output."""
        pass
