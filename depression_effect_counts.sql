




CREATE TABLE IF NOT EXISTS depression_effect_counts as
SELECT side.side_effect, drg.medicinalproduct, COUNT(side.side_effect) AS side_effect_count
FROM (
	SELECT DISTINCT drg0.medicinalproduct, pat_drg0.patientid
	FROM drugs drg0
	JOIN patient_drugs pat_drg0
	ON drg0.drug_id = pat_drg0.drug_id
	WHERE drg0.medicinalproduct IN 
		("CITALOPRAM HYDROBROMIDE", "MIRTAZAPINE", "FLUOXETINE", "PAROXETINE HCL", "CITALOPRAM", "ESCITALOPRAM", "SERTRALINE HYDROCHLORIDE", "SERTRALINE", "BUPROPION HCL", "SEROQUEL", "VENLAFAXINE HCL", "VENLAFAXINE", "CYMBALTA", "ZOLOFT", "BUPROPION HYDROCHLORIDE")
	) AS drg
JOIN patient_side_effects pat_side
	ON drg.patientid = pat_side.patientid
JOIN side_effects side
	ON pat_side.side_effect_id = side.side_effect_id
GROUP BY side.side_effect, drg.medicinalproduct
ORDER BY side_effect_count DESC, side.side_effect




CREATE TABLE IF NOT EXISTS contraception_effect_counts as
SELECT side.side_effect, drg.medicinalproduct, COUNT(side.side_effect) AS side_effect_count
FROM (
	SELECT DISTINCT drg0.medicinalproduct, pat_drg0.patientid
	FROM drugs drg0
	JOIN patient_drugs pat_drg0
	ON drg0.drug_id = pat_drg0.drug_id
	WHERE drg0.medicinalproduct IN 
		('ORTHO EVRA', 'YAZ',  'YASMIN',  'DROSPIRENONE AND ETHINYL ESTRADIOL',  'ORTHO TRI-CYCLEN LO',  'ORTHO TRI-CYCLEN',  'OCELLA',  'BEYAZ',  'NUVARING',  'MIRENA',  'PLAN B',  'MICRONOR',  'DEPO-PROVERA',  'LOESTRIN 24 FE',  'LOESTRIN 1.5/30')
	) AS drg
JOIN patient_side_effects pat_side
	ON drg.patientid = pat_side.patientid
JOIN side_effects side
	ON pat_side.side_effect_id = side.side_effect_id
GROUP BY side.side_effect, drg.medicinalproduct
ORDER BY side_effect_count DESC, side.side_effect