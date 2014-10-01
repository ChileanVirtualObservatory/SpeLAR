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