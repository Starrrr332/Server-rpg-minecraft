import pymysql

def test_conn():
    try:
        conn = pymysql.connect(
            host='38.97.61.71',
            port=3306,
            user='u63121_YEHsFXzBrp',
            password='U^TN^^AotPQeST0hg+Vc0KfF',
            database='s63121_mc_accounts',
            connect_timeout=10
        )
        print("[OK] Conexion exitosa a la base de datos MySQL de Holy Hosting!")
        with conn.cursor() as cur:
            cur.execute("SELECT VERSION();")
            ver = cur.fetchone()
            print("MySQL Version:", ver[0])
        conn.close()
        return True
    except Exception as e:
        print("[!] Error conectando a MySQL:", e)
        return False

if __name__ == '__main__':
    test_conn()
