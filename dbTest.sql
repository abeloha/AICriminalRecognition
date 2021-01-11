CREATE TABLE users (
    id           INTEGER  PRIMARY KEY AUTOINCREMENT
                            UNIQUE
                            NOT NULL,
    surname      STRING   NOT NULL,
    firstname    STRING,
    othername    STRING,
    biodata      STRING,
    date_created TEXT,
    is_deleted   INT      DEFAULT (0) 
);


CREATE TABLE offense (
    id             INTEGER         PRIMARY KEY AUTOINCREMENT
                                   UNIQUE
                                   NOT NULL,
    user_id        INTEGER          NOT NULL,
    date_committed DATE,
    details        VARCHAR (50000),
    date_created TEXT,
    is_deleted                     DEFAULT (0) 
);