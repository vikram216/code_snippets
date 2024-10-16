import ibm_db

# Define the database connection parameters
dsn_hostname = "your_hostname"  # e.g., 'db2host.domain.com'
dsn_port = "50000"              # The port number
dsn_database = "your_db_name"    # The name of the database
dsn_uid = "your_username"        # Your DB2 username
dsn_pwd = "your_password"        # Your DB2 password
dsn_driver = "{IBM DB2 ODBC DRIVER}"  # The ODBC driver name
dsn_protocol = "TCPIP"           # Connection protocol
dsn_security = "SSL"             # If SSL is required (use 'None' if not)

# Build the DSN string
dsn = (
    f"DATABASE={dsn_database};"
    f"HOSTNAME={dsn_hostname};"
    f"PORT={dsn_port};"
    f"PROTOCOL={dsn_protocol};"
    f"UID={dsn_uid};"
    f"PWD={dsn_pwd};"
)

try:
    # Establish the connection
    conn = ibm_db.connect(dsn, "", "")
    print("Connected to the database successfully!")

except Exception as e:
    print(f"Unable to connect: {e}")
finally:
    # Close the connection when done
    if conn:
        ibm_db.close(conn)
