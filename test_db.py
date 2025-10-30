import pyodbc

try:
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 18 for SQL Server};'
        'SERVER=localhost,1433;'
        'DATABASE=master;'
        'UID=sa;'
        'PWD=BibliotecaFort3!;'
        'TrustServerCertificate=yes;'
    )
    print("✅ Conectado com sucesso ao SQL Server!")
    conn.close()
except Exception as e:
    print("❌ Erro ao conectar:", e)
    