def delete_old_data_48h(conn):
    try:
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM weather
            WHERE loaded_at < NOW() - INTERVAL '48 hour';
        """)
        conn.commit()

    except Exception as e:
        conn.rollback()
        print(f"Error deleting data older than 48 hours: {e}")
    finally:
        cur.close()