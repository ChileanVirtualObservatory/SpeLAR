/*
-- Selecting by area in spatial coordinates
SELECT
  SpecLine.SpecLineID,
  SpecLine.wave,
  SpecLine.restWave,
  SpecLine.lineID,
  SpecLine.category,
  SpecLine.specobjID,
  SpecObj.ra,
  SpecObj.dec,
  SpecObj.objType,
  SpecObj.objTypeName
INTO mydb.SpecSample
FROM SpecLine
JOIN SpecObj
ON SpecLine.specobjID=SpecObj.SpecObjID
WHERE
  (SpecObj.ra > 145 AND SpecObj.ra < 155) AND
  (SpecObj.dec > 1.5 AND SpecObj.dec < 2.5)
*/

-- Selecting lines of galaxies with high flux magnitude
SELECT
  PhotoObj.objID,
  PhotoObj.petroMag_r,
  PhotoObj.extinction_r,
  SpecObj.SpecObjID,
  SpecObj.ra,
  SpecObj.dec,
  SpecObj.objType,
  SpecObj.objTypeName,
  SpecLine.SpecLineID,
  SpecLine.wave,
  SpecLine.restWave,
  SpecLine.lineID,
  SpecLine.category
INTO mydb.SpecSample
FROM SpecLine
JOIN SpecObj
ON SpecLine.specobjID = SpecObj.SpecObjID
JOIN PhotoObj
ON SpecObj.SpecObjID = PhotoObj.specObjID
WHERE
  PhotoObj.petroMag_r-PhotoObj.extinction_r < 15 AND
  PhotoObj.petroMag_r > -9000 AND
  SpecObj.objType = 0


-- Selecting galaxies with high flux magnitude
SELECT
  PhotoObj.objID,
  PhotoObj.petroMag_r,
  PhotoObj.extinction_r,
  SpecObj.objType,
  SpecObj.objTypeName
FROM SpecObj
JOIN PhotoObj
ON SpecObj.SpecObjID = PhotoObj.specObjID
INTO mydb.GalaxySample
WHERE
  PhotoObj.petroMag_r-PhotoObj.extinction_r < 18 AND
  SpecObj.objType = 0


--- Number of lines per magnitude
SELECT
  COUNT(*) as num_lines,
  objID,
  petroMag_r,
  extinction_r
INTO MyDB.LinesPerMag
FROM SpecSample
GROUP BY 
  objID,
  petroMag_r,
  extinction_r

--- Number of lines per magnitude (general)
SELECT
  PhotoObj.objID,
  PhotoObj.petroMag_r,
  PhotoObj.extinction_r,
  COUNT(SpecLine.SpecLineID) as num_lines
INTO mydb.LinesPerMag
FROM SpecLine
JOIN SpecObj
ON SpecLine.specobjID = SpecObj.SpecObjID
JOIN PhotoObj
ON SpecObj.SpecObjID = PhotoObj.specObjID
WHERE
  PhotoObj.petroMag_r-PhotoObj.extinction_r < 18 AND
  PhotoObj.petroMag_r > -9000 AND
  SpecObj.objType = 0
GROUP BY
  PhotoObj.objID,
  PhotoObj.petroMag_r,
  PhotoObj.extinction_r


--- Number of lines per magnitude of Stars(general)
SELECT
  PhotoObj.objID,
  PhotoObj.psfMag_u,
  COUNT(SpecLine.SpecLineID) as num_lines
INTO mydb.LinesPerMagStars
FROM SpecLine
JOIN PhotoObj
ON SpecLine.specobjID = PhotoObj.SpecObjID
WHERE
  PhotoObj.psfMag_u < 22 AND
  PhotoObj.psfMag_u > -9000 AND
  PhotoObj.type = 6
GROUP BY
  PhotoObj.objID,
  PhotoObj.psfMag_u


--- Selecting galaxies from catalog
  SELECT TOP 100
  PhotoObj.objID,
  PhotoObj.petroMag_r,
  PhotoObj.extinction_r,
  SpecObj.SpecObjID,
  SpecObj.ra,
  SpecObj.dec,
  SpecObj.objTypeName,
  SpecLineAll.SpecLineID,
  SpecLineAll.wave,
  SpecLineAll.restWave,
  SpecLineAll.lineID,
  SpecLineAll.category,
  SpecLineAll.height,
  SpecLineAll.heightErr,
  SpecLineAll.ew,
  SpecLineAll.ewErr
FROM SpecLineAll
JOIN SpecObj
ON SpecLineAll.specobjID = SpecObj.SpecObjID
JOIN PhotoObj
ON SpecObj.SpecObjID = PhotoObj.specObjID
WHERE
  PhotoObj.petroMag_r-PhotoObj.extinction_r < 18 AND
  PhotoObj.petroMag_r > -9000 AND
  SpecObj.objType = 0




--- Number of lines per galaxy magnitude
SELECT
  PhotoObj.objID,
  PhotoObj.petroMag_r,
  PhotoObj.extinction_r,
  COUNT(SpecLineAll.SpecLineID) as num_lines
INTO mydb.LinesPerMag
FROM SpecLineAll
JOIN SpecObj
ON SpecLineAll.specobjID = SpecObj.SpecObjID
JOIN PhotoObj
ON SpecObj.SpecObjID = PhotoObj.specObjID
WHERE
  PhotoObj.petroMag_r-PhotoObj.extinction_r < 18 AND
  PhotoObj.petroMag_r > -9000 AND
  SpecObj.objType = 0
GROUP BY
  PhotoObj.objID,
  PhotoObj.petroMag_r,
  PhotoObj.extinction_r



  --- Bright galaxies' emission lines (all)
SELECT
  PhotoObj.objID,
  PhotoObj.petroMag_r,
  PhotoObj.extinction_r,
  SpecObj.SpecObjID,
  SpecObj.ra,
  SpecObj.dec,
  SpecObj.objTypeName,
  SpecLineAll.SpecLineID,
  SpecLineAll.wave,
  SpecLineAll.restWave,
  SpecLineAll.lineID,
  SpecLineAll.category,
  SpecLineAll.height,
  SpecLineAll.heightErr,
  SpecLineAll.ew,
  SpecLineAll.ewErr
INTO GalaxyEmissionLines
FROM SpecLineAll
JOIN SpecObj
ON SpecLineAll.specobjID = SpecObj.SpecObjID
JOIN PhotoObj
ON SpecObj.SpecObjID = PhotoObj.specObjID
WHERE
  PhotoObj.petroMag_r-PhotoObj.extinction_r < 18 AND
  PhotoObj.petroMag_r > -9000 AND
  SpecObj.objType = 0 AND
  SpecLineAll.height > 0 AND 
  SpecLineAll.height / NULLIF(SpecLineAll.heightErr, 0) > 10


--- Emission lines of a selection of bright galaxies
SELECT
  Galaxy.objId,
  Galaxy.petroMag_r,
  Galaxy.extinction_r,
  Galaxy.SpecObjID,
  Galaxy.ra,
  Galaxy.dec,
  Galaxy.objTypeName,
  SpecLineAll.SpecLineID,
  SpecLineAll.wave,
  SpecLineAll.restWave,
  SpecLineAll.lineID,
  SpecLineAll.category,
  SpecLineAll.height,
  SpecLineAll.heightErr,
  SpecLineAll.ew,
  SpecLineAll.ewErr
INTO GalaxyEmissionLines
FROM
  (SELECT TOP 50000
    PhotoObj.objID,
    PhotoObj.petroMag_r,
    PhotoObj.extinction_r,
    SpecObj.SpecObjID,
    SpecObj.ra,
    SpecObj.dec,
    SpecObj.objTypeName
  FROM PhotoObj 
  JOIN SpecObj 
  ON PhotoObj.specobjID = SpecObj.SpecObjID
  WHERE
    PhotoObj.petroMag_r-PhotoObj.extinction_r < 18 AND
    PhotoObj.petroMag_r > -9000 AND
    SpecObj.objType = 0) Galaxy
JOIN
  SpecLineAll
ON
  SpecLineAll.specobjID = Galaxy.SpecObjID
WHERE
  SpecLineAll.height > 0 AND 
  SpecLineAll.height / NULLIF(SpecLineAll.heightErr, 0) > 10


--- Emission lines of a selection of bright galaxies, only identified lines
SELECT
  PhotoObj.objId,
  PhotoObj.psfMag_r,
  PhotoObj.psfMagErr_r,
  PhotoObj.specObjID,
  PhotoObj.ra,
  PhotoObj.dec,
  PhotoObj.type,
  SpecLineAll.SpecLineID,
  SpecLineAll.wave,
  SpecLineAll.restWave,
  SpecLineAll.lineID,
  SpecLineAll.category,
  SpecLineAll.height,
  SpecLineAll.heightErr,
  SpecLineAll.ew,
  SpecLineAll.ewErr,
  SpecLineAll.z AS SpecLineZ,
  SpecLineAll.zErr AS SpecLineZErr,
  SpecObj.z AS specObjZ,
  SpecObj.zErr AS specObjZErr,
  (SpecLineAll.wave / (1 + SpecObj.z)) AS calcRestWave,
  ABS((SpecLineAll.wave / (1 + SpecObj.z)) - SpecLineAll.restWave) AS calcRestWaveAcc
INTO StarEmissionLines
FROM
  (
    SELECT TOP 100000
      *
    FROM PhotoObj
    WHERE
      PhotoObj.psfMag_r < 18 AND
      PhotoObj.psfMag_r > -9000 AND
      PhotoObj.type = 6 AND
      PhotoObj.specObjID != 0
    ) PhotoObj
JOIN SpecLineAll
ON PhotoObj.specObjID = SpecLineAll.specobjID
JOIN SpecObj
ON PhotoObj.specObjID = SpecObj.SpecObjID
WHERE
  SpecLineAll.ew > 0 AND 
  SpecLineAll.ew / NULLIF(SpecLineAll.ewErr, 0) > 10 AND
  SpecLineAll.restWave > 0


--- Emission lines of a selection of bright galaxies, all lines with calculated rest wave length
SELECT
  PhotoObj.objId,
  PhotoObj.psfMag_r,
  PhotoObj.psfMagErr_r,
  PhotoObj.specObjID,
  PhotoObj.ra,
  PhotoObj.dec,
  PhotoObj.type,
  SpecLineAll.SpecLineID,
  SpecLineAll.wave,
  SpecLineAll.restWave,
  SpecLineAll.lineID,
  SpecLineAll.category,
  SpecLineAll.height,
  SpecLineAll.heightErr,
  SpecLineAll.ew,
  SpecLineAll.ewErr,
  SpecLineAll.z AS SpecLineZ,
  SpecLineAll.zErr AS SpecLineZErr,
  SpecObj.z AS specObjZ,
  SpecObj.zErr AS specObjZErr,
  SpecLineAll.wave / (1 + SpecObj.z) AS calcRestWave
INTO StarEmissionLinesAll
FROM
  (
    SELECT TOP 100000
      *
    FROM PhotoObj
    WHERE
      PhotoObj.psfMag_r < 18 AND
      PhotoObj.psfMag_r > -9000 AND
      PhotoObj.type = 6 AND
      PhotoObj.specObjID != 0

    ) PhotoObj
JOIN SpecLineAll
ON PhotoObj.specObjID = SpecLineAll.specobjID
JOIN SpecObj
ON PhotoObj.specObjID = SpecObj.SpecObjID
WHERE
  SpecLineAll.ew > 0 AND 
  ABS(SpecLineAll.ew) / NULLIF(SpecLineAll.ewErr, 0) > 5


  --- Absorption lines of a selection of bright galaxies, only identified lines
SELECT
  PhotoObj.objId,
  PhotoObj.psfMag_r,
  PhotoObj.psfMagErr_r,
  PhotoObj.specObjID,
  PhotoObj.ra,
  PhotoObj.dec,
  PhotoObj.type,
  SpecLineAll.SpecLineID,
  SpecLineAll.wave,
  SpecLineAll.restWave,
  SpecLineAll.lineID,
  SpecLineAll.category,
  SpecLineAll.height,
  SpecLineAll.heightErr,
  SpecLineAll.ew,
  SpecLineAll.ewErr,
  SpecLineAll.z AS SpecLineZ,
  SpecLineAll.zErr AS SpecLineZErr,
  SpecObj.z AS specObjZ,
  SpecObj.zErr AS specObjZErr,
  (SpecLineAll.wave / (1 + SpecObj.z)) AS calcRestWave,
  ABS((SpecLineAll.wave / (1 + SpecObj.z)) - SpecLineAll.restWave) AS calcRestWaveAcc
INTO StarAbsorptionLines
FROM
  (
    SELECT TOP 100000
      *
    FROM PhotoObj
    WHERE
      PhotoObj.psfMag_r < 18 AND
      PhotoObj.psfMag_r > -9000 AND
      PhotoObj.type = 6 AND
      PhotoObj.specObjID != 0
    ) PhotoObj
JOIN SpecLineAll
ON PhotoObj.specObjID = SpecLineAll.specobjID
JOIN SpecObj
ON PhotoObj.specObjID = SpecObj.SpecObjID
WHERE
  SpecLineAll.height < 0 AND 
  SpecLineAll.ew / ABS(NULLIF(SpecLineAll.ewErr, 0)) > 10 AND
  SpecLineAll.restWave > 0


  --- Absorption lines of a selection of bright galaxies, all lines with calculated rest wave length
SELECT
  PhotoObj.objId,
  PhotoObj.psfMag_r,
  PhotoObj.psfMagErr_r,
  PhotoObj.specObjID,
  PhotoObj.ra,
  PhotoObj.dec,
  PhotoObj.type,
  SpecLineAll.SpecLineID,
  SpecLineAll.wave,
  SpecLineAll.restWave,
  SpecLineAll.lineID,
  SpecLineAll.category,
  SpecLineAll.height,
  SpecLineAll.heightErr,
  SpecLineAll.ew,
  SpecLineAll.ewErr,
  SpecLineAll.z AS SpecLineZ,
  SpecLineAll.zErr AS SpecLineZErr,
  SpecObj.z AS specObjZ,
  SpecObj.zErr AS specObjZErr,
  SpecLineAll.wave / (1 + SpecObj.z) AS calcRestWave
INTO StarAbsorptionLinesAll
FROM
  (
    SELECT TOP 100000
      *
    FROM PhotoObj
    WHERE
      PhotoObj.psfMag_r < 18 AND
      PhotoObj.psfMag_r > -9000 AND
      PhotoObj.type = 6 AND
      PhotoObj.specObjID != 0
    ) PhotoObj
JOIN SpecLineAll
ON PhotoObj.specObjID = SpecLineAll.specobjID
JOIN SpecObj
ON PhotoObj.specObjID = SpecObj.SpecObjID
WHERE
  SpecLineAll.height < 0 AND 
  SpecLineAll.ew / NULLIF(SpecLineAll.ewErr, 0) > 10




SELECT
  PhotoObj.objID,
  PhotoObj.petroMag_r,
  PhotoObj.extinction_r,
  PhotoObj.psfMag_r,
  SpecObj.z AS specObjZ,
  SpecObj.zErr AS specObjZErr,
  SpecObj.zStatus,
  SpecObj.objTypeName,
  SpecObj.specClass
  ---SpecLineAll.z AS specLineZ,
  ---SpecLineAll.z AS specLineZErr
INTO StarObject
FROM PhotoObj
  JOIN SpecObj
  ON PhotoObj.specObjID = SpecObj.SpecObjID
  ---JOIN SpecLineAll
  ---ON PhotoObj.specObjID = SpecLineAll.specobjID
WHERE
  PhotoObj.psfMag_r < 18 AND
  PhotoObj.psfMag_r > -9000 AND
  (SpecObj.specClass = 6 OR SpecObj.specClass = 1) AND
  SpecObj.z < 0.002


SELECT
  SpecObjAll.z AS specObjZ,
  SpecObjAll.zErr AS specObjZErr,
  SpecObjAll.zStatus,
  SpecObjAll.objTypeName,
  SpecObjAll.specClass,
  SpecObjAll.mag_0,
  SpecObjAll.mag_1,
  SpecObjAll.mag_2
  ---SpecLineAll.z AS specLineZ,
  ---SpecLineAll.z AS specLineZErr
INTO StarObject
FROM SpecObjAll
  ---ON PhotoObjAll.specObjID = SpecObjAll.SpecObjID
  ---JOIN SpecLineAll
  ---ON PhotoObjAll.specObjID = SpecLineAll.specobjID
WHERE
  ---PhotoObjAll.psfMag_r < 18 AND
  ---PhotoObjAll.psfMag_r > -9000 AND
  (SpecObjAll.specClass = 6 OR SpecObjAll.specClass = 1) AND
  SpecObj.z < 0.002


--- Final star catalogue
SELECT
  SpecObjAll.specObjID,
  SpecObjAll.z AS specObjZ,
  SpecObjAll.zErr AS specObjZErr,
  SpecObjAll.zStatus,
  SpecObjAll.objTypeName,
  SpecObjAll.specClass,
  SpecObjAll.mag_0,
  SpecObjAll.mag_1,
  SpecObjAll.mag_2
INTO SpecObjStar
FROM SpecObjAll
WHERE
  (SpecObjAll.specClass = 6 OR SpecObjAll.specClass = 1) AND
  SpecObjAll.z < 0.002

--- Final star lines
SELECT
  SpecObj.specObjID,
  SpecObj.z AS specObjZ,
  SpecObj.zErr AS specObjZErr,
  SpecObj.zStatus,
  SpecObj.objTypeName,
  SpecObj.specClass,
  SpecObj.mag_0,
  SpecObj.mag_1,
  SpecObj.mag_2,
  SpecLineAll.SpecLineID,
  SpecLineAll.wave,
  SpecLineAll.waveErr,
  SpecLineAll.restWave,
  SpecLineAll.lineID,
  SpecLineAll.category,
  SpecLineAll.height,
  SpecLineAll.heightErr,
  SpecLineAll.ew,
  SpecLineAll.ewErr,
  SpecLineAll.z AS specLineZ,
  SpecLineAll.zErr AS specLineZErr,
  SpecObj.z AS specObjZ,
  SpecObj.zErr AS specObjZErr,
  (SpecLineAll.wave / (1 + SpecObj.z)) AS calcRestWave,
  ABS((SpecLineAll.wave / (1 + SpecObj.z)) - SpecLineAll.restWave) AS calcRestWaveAcc
INTO SpecObjStarLines
FROM SpecObj
  JOIN SpecLineAll
  ON SpecObj.SpecObjID = SpecLineAll.specobjID
WHERE
  (SpecObj.specClass = 6 OR SpecObj.specClass = 1) AND
  SpecObj.z < 0.002 AND
  ABS(SpecLineAll.ew) / NULLIF(SpecLineAll.ewErr, 0) > 5