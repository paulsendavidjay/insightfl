-- MySQL schemas
-- To import your schemas into your database, run:
-- `mysql -u username -p database < schema.sql`
-- where username is your MySQL username

CREATE DATABASE IF NOT EXISTS RxFx;

 USE RxFx;

CREATE TABLE IF NOT EXISTS main
(patientid INTEGER (8) NOT NULL AUTO_INCREMENT PRIMARY KEY,
safetyreportid	VARCHAR(30),
age FLOAT,
weight FLOAT,
sex INTEGER(1),
country VARCHAR(50),
receivedate DATE,
hospitalization INTEGER(1),
death INTEGER(1),
seriousness INTEGER(1),
seriousnessother INTEGER(1),
n_drugs INTEGER(3),
n_side_effects INTEGER(3));


CREATE TABLE IF NOT EXISTS side_effects
(side_effect_id INTEGER (8) NOT NULL AUTO_INCREMENT PRIMARY KEY,
side_effect VARCHAR(100));


CREATE TABLE IF NOT EXISTS patient_side_effects
(patientid INTEGER (8) NOT NULL,
side_effect_id INTEGER (8));


CREATE TABLE IF NOT EXISTS drugs
(drug_id INTEGER (8) NOT NULL AUTO_INCREMENT PRIMARY KEY,
medicinalproduct VARCHAR (200),
brand_name VARCHAR (200),
generic_name VARCHAR (200),
substance_name VARCHAR (200),
pharm_class_cs VARCHAR (200));


CREATE TABLE IF NOT EXISTS patient_drugs
(patientid INTEGER (8) NOT NULL,
drug_id INTEGER (8),
drugstartdate DATE,
drugenddate DATE);


CREATE TABLE IF NOT EXISTS indications
(patientid INTEGER (8) NOT NULL,
drugindication VARCHAR (100),
drug_id INTEGER (8));


CREATE TABLE IF NOT EXISTS queries
(queryid INTEGER (8) NOT NULL AUTO_INCREMENT PRIMARY KEY,
queryurl VARCHAR (300),
results_entered INTEGER (1));

