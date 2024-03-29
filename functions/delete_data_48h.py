def delete_old_data_48h(conn):
    try:
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM weather
            WHERE loaded_at < NOW() - INTERVAL '5minutes';
        """)
        conn.commit()

    except Exception as e:
        conn.rollback()
        print(f"Error deleting data older than 24 hours: {e}")
    finally:
        cur.close()