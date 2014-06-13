-- MySQL schemas
-- To import your schemas into your database, run:
-- `mysql -u username -p database < schema.sql`
-- where username is your MySQL username

 
CREATE TABLE IF NOT EXISTS world_index (
  id INT NOT NULL AUTO_INCREMENT,
  country CHAR(50) NULL,
  median_age DECIMAL(3, 1) NULL,
  gdp INT NULL,
  edu_index DECIMAL(4, 3) NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB;

