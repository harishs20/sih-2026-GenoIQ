from db import verify_connection, close

try:
    verify_connection()
finally:
    close()