import pymysql.cursors

from warnings import warn


class Connection:
    def __init__(self, host, user, password):
        self._connection = pymysql.connect(host, user, password)
        
        valid_dbs = self._get_dbs()
        self._dbs_available = valid_dbs
        self._dbs_selected = valid_dbs 

        self.errors = []
        
    def __enter__(self):
        return self
        
    def __exit__(self, *exception_data):
        self.close()
        
        return self
           
    @property
    def connection(self):
        """Returns the PyMYSQL Connection object."""
        return self._connection
    
    @property
    def host(self):
        """Returns the connection hostname."""
        return self.connection.host
        
    @property
    def user(self):
        """Returns the connection username."""
        return self.connection.user
        
    @property
    def dbs_available(self):
        """Returns a list of databases which can be queried on this connection.
        """
        return self._dbs_available

    @property
    def dbs_selected(self):
        """Returns a list of databases to be queried on query execution."""
        return self._dbs_selected
        
    @property
    def is_open(self):
        """Returns True if the connection is open."""
        return self.connection.open
        
    def select_dbs(self, dbs=None, fpred=None):
        """Selects the databases on which to execute a query.
        
        Args:
            dbs: An iterable of database names.
            fpred: Short for "filter predicate". A function which, when passed
                   a database name, returns a boolean indicating whether that 
                   db is to be selected.
            
        Returns:
            Nothing
            
        Raises:
            TypeError
        """
        if isinstance(dbs, str):
            dbs = [dbs]
            
        if dbs:
            for db in dbs:
                if db not in self.dbs_available:
                    raise ValueError('DB "{d}" not available on {h}'.format(
                        d=db, h=self.host))
            self._dbs_selected = dbs
            
        elif fpred:
            self._dbs_selected = [db for db in self.dbs_available if fpred(db)]

        else:
            raise TypeError('select_dbs() requires an argument.')
                
                

    def _db(self):
        """Returns the database name the connection is currently using."""
        return self.connection.db

    def use(self, database: str):
        """Sets the connection database.
        
        Args:
            database: A database name.
        """
        self.connection.select_db(database)
        
    def _get_dbs(self, exclude_metadata_dbs=True):
        """Retrieves a list of databases with from the server.
                  
        Returns:
            list
        """
        metadata_dbs = (
            'mysql',
            'information_schema',
            'performance_schema',
        )

        databases = []

        with self.connection.cursor() as cursor:
            cursor.execute('SHOW DATABASES')
            
            for row in cursor:
                db = row[0]
                
                if exclude_metadata_dbs and db not in metadata_dbs:
                    databases.append(db)
                    
                else:
                    databases.append(db)
                    
        return databases

    def execute(self, query, include_fields=False, max_errors=5):
        """Executes a query on all selected databases.
        
        Yields the result as a continuous steam of rows 
        with server/db metadata attached.
        
        Args:
            query: A string containing a valid database query.
            include_fields: A boolean that declares whether to include the
                            column names. If True, the column names will be the
                            first element in the result set.
            max_errors: An int that causes execution to abort after a specific
                        number of queries have thrown an error.
                        
        Returns:
            generator
            
        Raises:
            KeyboardInterrupt, RuntimeError
        """
        error_count = 0
        
        for idx, db in enumerate(self.dbs_selected):
            self.use(db)
            
            with self.connection.cursor() as cursor:
                try:
                    cursor.execute(query)
                    # We only want fields from the first query as headers
                    if include_fields == True and idx == 0:
                        fields = [l[0] for l in cursor.description]
                        yield ('host', 'db', *fields)
                        
                    for row in cursor:
                        yield (self.host, db, *row)
                        
                except KeyboardInterrupt as e:
                    print('^C received. Shutting down.')
                    raise
                    
                except pymysql.err.ProgrammingError as e:
                    msg = 'Query on {d} finished with errors. Call `errors` ' \
                        'instance method for details.'.format(d=db)
                    warn(msg)
                    
                    self.errors.append((self.host, db, e))
                    
                    error_count += 1
                    
                    if error_count > max_errors:
                        raise RuntimeError("Error count ({e}) exceeded max " \
                                           "({n}). Aborting.".format(
                                                e=error_count, n=max_errors))
                    
    def execute_multiple(self, queries, **kwargs):
        """Executes a list of queries on all selected databases.
        Returns the result as a nested list.
        
        Wraps `execute`.
        
        Args:
            queries: A list of queries to execute.
            
        Returns:
            list
        """
        results = []
        
        for query in queries:
            results.append([row for row in self.execute(query, **kwargs)])
            
        return results
        
    def close(self):
        """Closes the connection. If this class is used as a context manager,
        calling this method is unnecessary
        """
        if self.is_open:
            self.connection.close()
   
    def __repr__(self):
        return "<Connection host='{h}' open={s}>".format(
            h=self.connection.host, s=self.is_open)
        

class MultiConnection:
    def __init__(self, user, password, hosts=None):
        if hosts is None:
            hosts = valid_hosts
            
        if isinstance(hosts, str):
            hosts = [hosts]
            
        self._connections = {
            host: Connection(host, user, password) for host in hosts
        }
        
    def __enter__(self):
        return self
    
    def __exit__(self, *exception_data):
        self.close_all()
        return self
        
    @property
    def hosts(self):
        """Returns a list of hostnames available to this instance"""
        return list(self._connections)
        
    @property
    def dbs_selected(self):
        """Returns a dict of selected databases per host."""
        items = self._connections.items()
        
        return {host: conn.dbs_selected for host, conn in items}
    
    def select_dbs(self, host, dbs):
        """Selects the databases on which to execute a query.
        
        Args:
            host: The hostname to select dbs on.
            dbs: A list of database names.
            
        Returns:
            Nothing
        """
        self._connections[host].select_dbs(dbs)
        
    @property
    def dbs_available(self):
        """Returns a dict of available databases per host."""
        items = self._connections.items()
        
        return {host: conn.dbs_available for host, conn in items}
        
    def set_hosts(self, hosts, user: str, password: str):
        """Resets hosts and connections. Username and password required.
        Keeps existing open connections for efficiency.
        
        Args:
            hosts: An iterable of hostnames.
            user: A username string.
            password: A password string.
        """
        for host in hosts:
            conn = self._connections.get(host)
            
            if not conn:
                self.add(host, user, password)
                
            elif conn.is_open == False:
                self.remove(host)
                self.add(host, user, password)
            
        for host in self.hosts:
            conn = self._connections[host]
            
            if host not in hosts and conn.is_open:
                self.remove(host)
    
    def execute(self, query: str, **kwargs):
        """
        Executes a query on all selected databases in all
        selected hosts.
        
        Args:
            query: A string containing a valid database query.
            kwargs: Keywords for `Connection.execute`.
            
        Returns:
            generator
        """
        connections = self._connections.values()
        
        for connection in connections:
            for row in connection.execute(query, **kwargs):
                yield row
        
    def execute_multiple(self, queries, **kwargs):
        """Executes an iterable of queries on all hosts on all selected 
        databases.Returns the result as a nested list.
        
        Args:
            queries: An iterable of strings containing database queries.
            kwargs: Keywords for `MultiConnection.execute`.
        
        Returns:
            list
        """
        results = []
        
        for query in queries:
            results.append([row for row in self.execute(query, **kwargs)])
            
        return results
        
    def add(self, host: str, user: str, password: str):
        """Creates a connection and adds it to the list of connections.
        Username and password required.
        
        Args:
            host: A valid hostname.
            user: A valid username.
            password: A valid password.
        """
        if host not in self.hosts:
            self._connections[host] = Connection(host, user, password)
        
    def close(self, host: str):
        """Closes a connection.
        
        Args:
            host: A valid hostname.
        """
        self._connections[host].close()
    
    def remove(self, host: str):
        """Closes a connection and removes it from the connections
        registry.
        
        Args:
            host: A valid hostname
        """
        self.close(host)
        
        del self._connections[host]
        
    def close_all(self):
        """Closes all connections."""
        for host in self.hosts:
            self.close(host)
    
    def __repr__(self):
        hosts = '({h})'.format(
            h=', '.join("'" + host + "'" for host in sorted(self.hosts)))
        return "<MultiConnection hosts={h}>".format(h=hosts)