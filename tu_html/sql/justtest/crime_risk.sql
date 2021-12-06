with crimes as (select id,date,primary_type,st_geogpoint(longitude, latitude) as geom
from `musa-509-final.justtest.crime_2021-11-30`
WHERE date between DATE_SUB(current_date(), INTERVAL 30 DAY) and current_date()),

check as (SELECT N.pri_neigh,C.id,C.primary_type,C.date, N.the_geom as neigh_geom, C.geom as crime_geom, st_within(C.geom,N.the_geom) as test
FROM `musa-509-final.justtest.neighborhood_2021-12-01` AS N
CROSS JOIN crimes as C),

count as (SELECT cri.pri_neigh,nei.the_geom,cri.number
FROM `musa-509-final.justtest.neighborhood_2021-12-01` AS nei
right join 
(select pri_neigh,count(id) as number
from check
where test = TRUE 
group by pri_neigh) AS cri
ON nei.pri_neigh = cri.pri_neigh
Order by cri.pri_neigh)

select *, 
       Case 
        when number <50 then "1"
        when number >=50 and number < 200 then "2"
        when number >= 200 and number < 500 then "3"
        when number >= 500 and number < 1000 then "4"
        when number >= 1000 then "5"
  END 
        AS risk
from count