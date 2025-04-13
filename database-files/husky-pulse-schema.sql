drop database if exists HuskyPulse;
create database HuskyPulse;

use HuskyPulse;

create table if not exists student(
    NUID int PRIMARY KEY not null,
    first_name varchar(50) not null,
    last_name varchar(50) not null,
    email varchar(50) not null,
    # changed from 50 to 100
    major varchar(100) not null,
    cultural_background varchar(50),
    religion varchar(50),
    pre_professional varchar(50),
    year tinyint(1),
    UNIQUE INDEX idx_nuid (NUID),
    INDEX idx_email (email),
    INDEX idx_first_name (first_name),
    INDEX idx_last_name (last_name)
);

create table if not exists club(
    id int Primary key not null,
    name varchar(50) not null,
    type varchar(50) not null,
    subject varchar(50),
    size int not null,
    UNIQUE INDEX idx_id (id),
    INDEX idx_name (name)
);

create table if not exists student_club(
    NUID int,
    club_id int,
    when_joined DATETIME DEFAULT CURRENT_TIMESTAMP,
    primary key(nuid, club_id),
    constraint fk1 foreign key (NUID) references student(NUID) on delete cascade,
    constraint fk2 foreign key (club_id) references club(id) on delete cascade
);

create table if not exists location(
    id int primary key not null,
    capacity int not null,
    # changed building from 50 to 100
    building varchar(100) not null,
    room_num int,
    address varchar(100) not null,
    city varchar(100) not null,
    state varchar(2) not null,
    zip_code int(5) not null,
    UNIQUE INDEX idx_id (id)
);

create table if not exists event(
    id int primary key not null,
    name varchar(50) not null,
    start_date datetime not null,
    end_date datetime not null,
    location_id int not null,
    club_id int not null,
    constraint fk3 foreign key (location_id) references location(id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    constraint fk4 foreign key (club_id) references club(id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

create table if not exists student_event(
    event_id int not null,
    NUID int not null,
    when_rsvped DATETIME DEFAULT CURRENT_TIMESTAMP,
    primary key (event_id, NUID),
    constraint fk5 foreign key (event_id) references event(id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    constraint fk6 foreign key (NUID) references student(NUID)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

create table if not exists post(
    id int primary key not null,
    is_public tinyint(1) not null,
    created_at datetime not null DEFAULT CURRENT_TIMESTAMP,
    club_id int not null,
    event_id int,
    title varchar(50) not null,
    description varchar(200) not null,
    image_file varchar(200),
    constraint fk7 foreign key (club_id) references club(id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    constraint fk8 foreign key (event_id) references event(id)
        ON UPDATE CASCADE
);

create table if not exists comment(
    id int not null primary key,
    NUID int not null,
    date datetime not null,
    text varchar(500) not null,
    constraint fk9 foreign key (NUID) references student(NUID)
        ON UPDATE CASCADE ON DELETE CASCADE
);

create table if not exists post_comment(
    post_id int not null,
    comment_id int not null,
    primary key (post_id, comment_id),
    constraint fk10 foreign key (post_id) references post(id),
    constraint fk11 foreign key (comment_id) references comment(id)
);

create table if not exists system_admin(
    id int primary key not null,
    permission_level varchar(20) not null
);

CREATE TABLE IF NOT EXISTS feedback(
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    recipient_id INT NOT NULL,
    recipient_type VARCHAR(20) NOT NULL,
    sender_id INT NOT NULL,
    # increased varchar to 200 in case
    sender_type VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    date_submitted DATETIME NOT NULL,
    INDEX idx_recipient (recipient_id, recipient_type),
    INDEX idx_sender (sender_id, sender_type)
);

CREATE TABLE IF NOT EXISTS application(
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    status VARCHAR(25),
    club_id INT NOT NULL,
    applicant_id INT NOT NULL,
    CONSTRAINT FOREIGN KEY (club_id) REFERENCES club(id),
    CONSTRAINT FOREIGN KEY (applicant_id) REFERENCES student(NUID)
);

CREATE TABLE IF NOT EXISTS backup(
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    admin_id INT NOT NULL,
    content LONGTEXT,
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT FOREIGN KEY (admin_id) REFERENCES system_admin(id)
);

CREATE TABLE IF NOT EXISTS logs(
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    admin_id INT NOT NULL,
    content TEXT,
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT FOREIGN KEY (admin_id) REFERENCES system_admin(id)
);

CREATE TABLE IF NOT EXISTS role(
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    admin_id INT NOT NULL,
    role_name VARCHAR(50) NOT NULL,
    CONSTRAINT FOREIGN KEY (admin_id) REFERENCES system_admin(id)
);

CREATE TABLE IF NOT EXISTS compliance(
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    status VARCHAR(200),
    admin_id INT NOT NULL,
    club_id INT NOT NULL,
    CONSTRAINT FOREIGN KEY (admin_id) REFERENCES system_admin(id),
    CONSTRAINT FOREIGN KEY (club_id) REFERENCES club(id)
        ON UPDATE CASCADE
);

SHOW DATABASES;