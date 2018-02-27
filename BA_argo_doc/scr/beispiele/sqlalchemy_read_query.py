from webapp import db

sql_template = "SELECT DISTINCT ON (f.id)
  f.identifier,
  l.longitude,
  l.latitude,
  p.timestamp
FROM argo_floats f
  JOIN measurements m
    ON f.id = m.argo_float_id
  JOIN profiles p
    ON m.id = p.measurement_id
  JOIN locations l
    ON l.id = m.location_id
ORDER BY f.id, p.cycle DESC;"

result = db.engine.execute(sql_template)
