CREATE TABLE hatenabookmark(
id BIGINT(7) NOT NULL AUTO_INCREMENT,
bookmarkdate DATE, --         ホットエントリーの日付
timestamp DATETIME, --        作成日時？
url VARCHAR(2083), --         URL
domain VARCHAR(255), --       ドメイン
title VARCHAR(1000), --       はてブに登録されているタイトル
hatebu INT(5), --             はてブの数
htnurl VARCHAR(2083), --      はてなブックマークのURL
comment_count INT(5), --      はてブのコメント数
category VARCHAR(30), --      はてなブックマークのカテゴリー
linkerror VARCHAR(16),--      リンクエラー時の内容
errorcontent VARCHAR(255), -- リンクエラーの詳細
nowtitle VARCHAR(1000), --    現在のタイトル
created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY(id));

ALTER TABLE hatenabookmark CHANGE domain domain VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE hatenabookmark CHANGE title title VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE hatenabookmark CHANGE category category VARCHAR(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE hatenabookmark CHANGE nowtitle nowtitle VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
