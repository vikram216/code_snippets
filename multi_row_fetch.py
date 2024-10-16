def fetch_rows_in_chunks(conn, base_query, chunk_size):
    offset = 0  # Starting point for pagination
    while True:
        # Modify the query to fetch the next chunk
        paginated_query = f"{base_query} LIMIT {chunk_size} OFFSET {offset}"
        
        # Prepare and execute the query
        stmt = ibm_db.exec_immediate(conn, paginated_query)
        
        rows = []
        row = ibm_db.fetch_assoc(stmt)
        
        # Fetch and store all rows in the current chunk
        while row:
            rows.append(row)
            row = ibm_db.fetch_assoc(stmt)
        
        # If no more rows, break the loop
        if not rows:
            break
        
        # Process the current chunk of rows
        print(f"Processing {len(rows)} rows starting from offset {offset}")
        for r in rows:
            print(r)
        
        # Increment the offset for the next chunk
        offset += chunk_size

# Establish the connection
try:
    conn = ibm_db.connect(dsn, "", "")
    print("Connected to the database successfully!")

    # Base SQL query to fetch rows (without LIMIT and OFFSET)
    base_query = "SELECT * FROM your_table_name"

    # Define the chunk size (number of rows per fetch)
    chunk_size = 100  # Adjust the chunk size as needed

    # Fetch rows in chunks
    fetch_rows_in_chunks(conn, base_query, chunk_size)

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the connection when done
    if conn:
        ibm_db.close(conn)
