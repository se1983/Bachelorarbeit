SELECT *
FROM argo_floats
  JOIN measurements ON argo_floats.id = measurements.argo_float_id
  JOIN locations ON measurements.location_id = locations.id
  JOIN profiles ON measurements.id = profiles.measurement_id
WHERE identifier = '%s';