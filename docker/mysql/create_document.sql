CREATE TABLE `document` (
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

ALTER TABLE document ADD INDEX idx_document_01(filer_name);

ALTER TABLE document ADD INDEX idx_document_02(sec_code, form_code, doc_type_code);


commit;
