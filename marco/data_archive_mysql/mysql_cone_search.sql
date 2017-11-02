
SELECT X(astro), Y(astro), distance 
  FROM ( 
         SELECT astro, r,
                units * vincenty(decpoint, rapoint, X(astro), Y(astro))
                                        AS distance 
           FROM astrogrid
           JOIN ( 
                  SELECT 90.0 AS decpoint, 100.0 AS rapoint, 
                         5.0 AS r, 1.0 AS units 
                ) AS p ON (1=1) 
          WHERE MbrContains(ST_GEOMFROMTEXT( 
                        CONCAT(
                          'LINESTRING(', decpoint-(r/units),' ', rapoint-(r /(units*COS(RADIANS(decpoint-(r/units))))), ',', 
                                         decpoint-(r/units),' ', rapoint+(r /(units*COS(RADIANS(decpoint-(r/units))))), ',', 
                                         decpoint+(r/units),' ', rapoint-(r /(units*COS(RADIANS(decpoint+(r/units))))), ',', 
                                         decpoint+(r/units),' ', rapoint+(r /(units*COS(RADIANS(decpoint+(r/units))))), ')')),
                        astro) 
       ) AS d 
 WHERE distance <= r
 ORDER BY distance;




SELECT declination, ra, distance 
  FROM ( 
         SELECT declination, ra, vincenty(42.81, 30.81, declination, ra) AS distance FROM tgas ) as d
 WHERE distance <= 100.0
 ORDER BY distance;

