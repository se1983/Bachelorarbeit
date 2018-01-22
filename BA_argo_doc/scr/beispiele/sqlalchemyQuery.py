for p in session.query(Profile).all():
    for r in p.records:
        print(f"Zu Zeitpunkt {p.timestamp} wurde {r.data_type} mit {r.value} gemessen.")
        
# Zu Zeitpunkt 2018-01-20 wurde Temperature mit 15.0 gemessen.
# Zu Zeitpunkt 2018-01-17 wurde Temperature mit 25.0 gemessen.
# Zu Zeitpunkt 2018-01-17 wurde Pressure mit 55.0 gemessen.
