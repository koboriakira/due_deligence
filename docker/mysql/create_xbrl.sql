CREATE TABLE `xbrl` (
  `doc_id` varchar(20) PRIMARY KEY
  , `date` date
  , `seq_number` int
  , `edinet_code` varchar(10)
  , `sec_code` varchar(10)
  , `form_code` varchar(10)
  , `doc_type_code` varchar(10)
  , `filer_name` varchar(200)
  , `value_per_share` int
  , `capital_ratio` int
);

ALTER TABLE xbrl ADD INDEX idx_xbrl_01(date);

ALTER TABLE xbrl ADD INDEX idx_xbrl_02(sec_code, form_code, doc_type_code);

commit;
