CREATE TABLE `company` (
  `date` date
  , `seq_number` int
  , `edinet_code` varchar(10)
  , `sec_code` varchar(10)
  , `form_code` varchar(10)
  , `doc_type_code` varchar(10)
  , `filer_name` varchar(200)
  , `doc_id` varchar(20) UNIQUE

  , PRIMARY KEY(date, seq_number)
);

ALTER TABLE company ADD INDEX idx_company_01(filer_name);

ALTER TABLE company ADD INDEX idx_company_02(sec_code, form_code, doc_type_code);


commit;
