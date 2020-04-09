CREATE TABLE `report` (
  `doc_id` varchar(20) PRIMARY KEY
  , `value_per_share` int -- 1株あたりの価値
  , `capital_ratio` int -- 自己資本比率
  , `current_year_operating_income` int -- 当期営業利益
  , `prior_1year_operating_income` int -- 前期営業利益
  , `current_year_current_assets` int -- 当期流動資産合計
  , `current_year_investments_and_other_assets` int -- 当期その他の資産合計
  , `current_year_current_liabilities` int -- 当期流動負債合計
  , `current_year_noncurrent_liabilities` int -- 当期固定負債合計
  , `current_year_net_assets` int -- 当期純資産合計
  , `current_year_total_number_of_issued_shares` bigint -- 当期発行済株式総数
  , `updated_at` timestamp -- 更新日時
);

ALTER TABLE report ADD INDEX idx_report_01(capital_ratio);

ALTER TABLE report ADD INDEX idx_report_02(updated_at);

commit;
