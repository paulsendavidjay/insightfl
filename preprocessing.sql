CREATE TABLE drugs_by_indication AS
SELECT i.drugindication, COUNT(ds.`drug_short_name`) AS drug_count, ds.`drug_short_name`
FROM indications i
JOIN drugs d
ON d.drug_id = i.drug_id
JOIN drugs_short ds
ON d.`drug_short_id` = ds.`drug_short_id`
WHERE i.drugindication IN 
	(SELECT indication FROM top_indications)
GROUP BY i.drugindication, ds.drug_short_name


CREATE TABLE drugs_by_indication_short AS
SELECT drugindication, drug_count, drug_short_name
FROM drugs_by_indication
WHERE drug_count > 300



CREATE TABLE IF NOT EXISTS unique_med_patient
--		UNIQUE COMBINATION OF MEDICINE AND PATIENT		
SELECT DISTINCT drg1.drug_short_name, pat_drg0.patientid
--		CONTAINS NAMES FOR DRUG ID
FROM drugs_short drg1
JOIN drugs drg0
	ON drg0.drug_short_id = drg1.drug_short_id
--		PAIRS PATIENT ID WITH DRUG
JOIN patient_drugs pat_drg0
	ON drg0.drug_id = pat_drg0.drug_id
--		ALLOWS SELECTION OF PATIENTS WITH FEWER THAN N DRUGS
JOIN main
	ON main.patientid = pat_drg0.patientid
GROUP BY pat_drg0.patientid, drg1.drug_short_name
ORDER BY pat_drg0.patientid

CREATE TABLE IF NOT EXISTS patient_drug_counts
SELECT patientid, COUNT(patientid) AS drug_count
FROM unique_med_patient
GROUP BY patientid

-- ACTUALLY DID BY HAND EXPORTING AND IMPORTING
CREATE TABLE IF NOT EXISTS patient_drug_count_short
SELECT *
FROM patient_drug_counts
WHERE drug_count < 4)



CREATE TABLE IF NOT EXISTS unique_med_patient_short
SELECT patientid, drug_short_name
FROM unique_med_patient
WHERE patientid IN 
	(SELECT patientid FROM patient_drug_count_short)








