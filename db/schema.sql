-- foreign key 설정
PRAGMA foreign_keys = ON;

-- TABLE contact
CREATE table contact (
id integer PRIMARY KEY AUTOINCREMENT,
name varchar(50) NOT NULL DEFAULT '',
profile_picture varchar(255) NOT NULL,
email varchar(50) NOT NULL,
phone_number varchar(20) NOT NULL UNIQUE,
company varchar(20) NOT NULL,
job_title varchar(20) NOT NULL,
description text NULL,
address varchar(250) NULL,
birth_date date NULL,
homepage_url varchar(50) NULL,
created_at datetime DEFAULT CURRENT_TIMESTAMP,
created_by varchar(150) NULL,
updated_at datetime DEFAULT CURRENT_TIMESTAMP,
updated_by varchar(150) NULL
);

-- TABLE label
CREATE TABLE label (
id integer PRIMARY KEY AUTOINCREMENT,
name varchar(100) NOT NULL,
created_at datetime DEFAULT CURRENT_TIMESTAMP,
created_by varchar(150) NULL,
updated_at datetime DEFAULT CURRENT_TIMESTAMP,
updated_by varchar(150) NULL
);

-- TABLE contact_label
CREATE TABLE contact_label (
contact_id integer NOT NULL,
label_id integer NOT NULL,
FOREIGN KEY (contact_id) REFERENCES contact(id),
FOREIGN KEY (label_id) REFERENCES label(id),
PRIMARY KEY (contact_id, label_id)
);
