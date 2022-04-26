create table sanic_spider.auth_group
(
	id int auto_increment
		primary key,
	name varchar(150) not null,
	constraint name
		unique (name)
);

create table sanic_spider.auth_permission
(
	id int auto_increment
		primary key,
	name varchar(255) not null,
	codename varchar(100) not null
);

create table sanic_spider.auth_group_permissions
(
	id int auto_increment
		primary key,
	group_id int not null,
	permission_id int not null,
	constraint auth_group_permissions_ibfk_1
		foreign key (group_id) references sanic_spider.auth_group (id),
	constraint auth_group_permissions_ibfk_2
		foreign key (permission_id) references sanic_spider.auth_permission (id)
);

create index group_id
	on sanic_spider.auth_group_permissions (group_id);

create index ix_auth_group_permissions_permission_id
	on sanic_spider.auth_group_permissions (permission_id);

create table sanic_spider.auth_user
(
	id int auto_increment
		primary key,
	password varchar(128) not null,
	last_login datetime(6) null,
	is_superuser tinyint(1) not null,
	username varchar(150) not null,
	first_name varchar(30) not null,
	last_name varchar(150) not null,
	email varchar(254) not null,
	is_staff tinyint(1) not null,
	is_active tinyint(1) not null,
	date_joined datetime(6) not null,
	constraint username
		unique (username)
);

create table sanic_spider.auth_user_groups
(
	id int auto_increment
		primary key,
	user_id int not null,
	group_id int not null,
	constraint auth_user_groups_ibfk_1
		foreign key (user_id) references sanic_spider.auth_user (id),
	constraint auth_user_groups_ibfk_2
		foreign key (group_id) references sanic_spider.auth_group (id)
);

create index ix_auth_user_groups_group_id
	on sanic_spider.auth_user_groups (group_id);

create index user_id
	on sanic_spider.auth_user_groups (user_id);

create table sanic_spider.auth_user_user_permissions
(
	id int auto_increment
		primary key,
	user_id int not null,
	permission_id int not null,
	constraint auth_user_user_permissions_ibfk_1
		foreign key (user_id) references sanic_spider.auth_user (id),
	constraint auth_user_user_permissions_ibfk_2
		foreign key (permission_id) references sanic_spider.auth_permission (id)
);

create index ix_auth_user_user_permissions_permission_id
	on sanic_spider.auth_user_user_permissions (permission_id);

create index user_id
	on sanic_spider.auth_user_user_permissions (user_id);

create table sanic_spider.scrapy_server
(
	create_datetime datetime null,
	update_datetime datetime null,
	id int auto_increment
		primary key,
	host varchar(50) not null,
	port varchar(5) not null,
	auth tinyint(1) not null,
	auth_username varchar(50) null,
	auth_password varchar(50) null
);

create table sanic_spider.scrapy_project
(
	create_datetime datetime null,
	update_datetime datetime null,
	id int auto_increment
		primary key,
	name varchar(100) not null,
	`desc` varchar(255) not null,
	server_id int not null,
	constraint scrapy_project_ibfk_1
		foreign key (server_id) references sanic_spider.scrapy_server (id)
);

create table sanic_spider.scrapy_job
(
	create_datetime datetime null,
	update_datetime datetime null,
	id int auto_increment
		primary key,
	name varchar(100) not null,
	status varchar(20) not null,
	is_delete tinyint(1) null,
	finish_datetime datetime null,
	items int null,
	pages int null,
	project_id int null,
	run_time varchar(100) null comment '运行时长',
	start_datetime datetime null,
	constraint scrapy_job_ibfk_1
		foreign key (project_id) references sanic_spider.scrapy_project (id)
);

create index project_id
	on sanic_spider.scrapy_job (project_id);

create index server_id
	on sanic_spider.scrapy_project (server_id);

create table sanic_spider.scrapy_project_version
(
	create_datetime datetime null,
	update_datetime datetime null,
	id int auto_increment
		primary key,
	code varchar(20) not null,
	is_delete tinyint(1) not null,
	project_id int null,
	is_spider tinyint(1) default 0 null,
	constraint scrapy_project_version_ibfk_1
		foreign key (project_id) references sanic_spider.scrapy_project (id)
);

create index project_id
	on sanic_spider.scrapy_project_version (project_id);

create table sanic_spider.scrapy_server_info
(
	create_datetime datetime null,
	update_datetime datetime null,
	id int auto_increment
		primary key,
	hostname varchar(50) not null,
	status varchar(10) not null,
	finished int(5) null,
	pending int(5) not null,
	running int(5) not null,
	server_id int null,
	constraint scrapy_server_info_ibfk_1
		foreign key (server_id) references sanic_spider.scrapy_server (id)
			on delete cascade
);

create index server_id
	on sanic_spider.scrapy_server_info (server_id);

create table sanic_spider.scrapy_spider
(
	create_datetime datetime null,
	update_datetime datetime null,
	id int auto_increment
		primary key,
	name varchar(50) null,
	`desc` varchar(255) null,
	project_id int null,
	version_code varchar(20) null,
	constraint scrapy_spider_ibfk_1
		foreign key (project_id) references sanic_spider.scrapy_project (id)
);

create index project_id
	on sanic_spider.scrapy_spider (project_id);

create table sanic_spider.scrapy_task
(
	create_datetime datetime null,
	update_datetime datetime null,
	id int auto_increment
		primary key,
	name varchar(50) not null,
	`desc` varchar(255) null,
	spider_id int not null,
	constraint scrapy_task_ibfk_1
		foreign key (spider_id) references sanic_spider.scrapy_spider (id)
);

create index spider_id
	on sanic_spider.scrapy_task (spider_id);

create table sanic_spider.scrapy_task_setting
(
	create_datetime datetime null,
	update_datetime datetime null,
	id int auto_increment
		primary key,
	content varchar(1000) null,
	task_id int null,
	constraint scrapy_task_setting_ibfk_1
		foreign key (task_id) references sanic_spider.scrapy_task (id)
			on delete cascade
);

create index task_id
	on sanic_spider.scrapy_task_setting (task_id);

create table sanic_spider.scrapy_task_timer
(
	create_datetime datetime null,
	update_datetime datetime null,
	id int auto_increment
		primary key,
	year varchar(5) null,
	month varchar(5) null,
	day varchar(5) null,
	week varchar(20) null,
	day_of_week varchar(20) null,
	hour varchar(20) null,
	minute varchar(20) null,
	second varchar(20) null,
	start_date varchar(20) null,
	end_date varchar(20) null,
	timezone varchar(20) null,
	jitter varchar(20) null,
	misfire_grace_time varchar(20) null,
	coalesce varchar(20) null,
	max_instances varchar(20) null,
	task_id int null,
	constraint scrapy_task_timer_ibfk_1
		foreign key (task_id) references sanic_spider.scrapy_task (id)
			on delete cascade
);

create index task_id
	on sanic_spider.scrapy_task_timer (task_id);

create view CHARACTER_SETS as
	-- missing source code
;

create view COLLATIONS as
	-- missing source code
;

create view COLLATION_CHARACTER_SET_APPLICABILITY as
	-- missing source code
;

create view COLUMNS as
	-- missing source code
;

create view COLUMN_PRIVILEGES as
	-- missing source code
;

create view ENGINES as
	-- missing source code
;

create view EVENTS as
	-- missing source code
;

create view FILES as
	-- missing source code
;

create view GLOBAL_STATUS as
	-- missing source code
;

create view GLOBAL_VARIABLES as
	-- missing source code
;

create view INNODB_BUFFER_PAGE as
	-- missing source code
;

create view INNODB_BUFFER_PAGE_LRU as
	-- missing source code
;

create view INNODB_BUFFER_POOL_STATS as
	-- missing source code
;

create view INNODB_CMP as
	-- missing source code
;

create view INNODB_CMPMEM as
	-- missing source code
;

create view INNODB_CMPMEM_RESET as
	-- missing source code
;

create view INNODB_CMP_PER_INDEX as
	-- missing source code
;

create view INNODB_CMP_PER_INDEX_RESET as
	-- missing source code
;

create view INNODB_CMP_RESET as
	-- missing source code
;

create view INNODB_FT_BEING_DELETED as
	-- missing source code
;

create view INNODB_FT_CONFIG as
	-- missing source code
;

create view INNODB_FT_DEFAULT_STOPWORD as
	-- missing source code
;

create view INNODB_FT_DELETED as
	-- missing source code
;

create view INNODB_FT_INDEX_CACHE as
	-- missing source code
;

create view INNODB_FT_INDEX_TABLE as
	-- missing source code
;

create view INNODB_LOCKS as
	-- missing source code
;

create view INNODB_LOCK_WAITS as
	-- missing source code
;

create view INNODB_METRICS as
	-- missing source code
;

create view INNODB_SYS_COLUMNS as
	-- missing source code
;

create view INNODB_SYS_DATAFILES as
	-- missing source code
;

create view INNODB_SYS_FIELDS as
	-- missing source code
;

create view INNODB_SYS_FOREIGN as
	-- missing source code
;

create view INNODB_SYS_FOREIGN_COLS as
	-- missing source code
;

create view INNODB_SYS_INDEXES as
	-- missing source code
;

create view INNODB_SYS_TABLES as
	-- missing source code
;

create view INNODB_SYS_TABLESPACES as
	-- missing source code
;

create view INNODB_SYS_TABLESTATS as
	-- missing source code
;

create view INNODB_SYS_VIRTUAL as
	-- missing source code
;

create view INNODB_TEMP_TABLE_INFO as
	-- missing source code
;

create view INNODB_TRX as
	-- missing source code
;

create view KEY_COLUMN_USAGE as
	-- missing source code
;

create view OPTIMIZER_TRACE as
	-- missing source code
;

create view PARAMETERS as
	-- missing source code
;

create view PARTITIONS as
	-- missing source code
;

create view PLUGINS as
	-- missing source code
;

create view PROCESSLIST as
	-- missing source code
;

create view PROFILING as
	-- missing source code
;

create view REFERENTIAL_CONSTRAINTS as
	-- missing source code
;

create view ROUTINES as
	-- missing source code
;

create view SCHEMATA as
	-- missing source code
;

create view SCHEMA_PRIVILEGES as
	-- missing source code
;

create view SESSION_STATUS as
	-- missing source code
;

create view SESSION_VARIABLES as
	-- missing source code
;

create view STATISTICS as
	-- missing source code
;

create view TABLES as
	-- missing source code
;

create view TABLESPACES as
	-- missing source code
;

create view TABLE_CONSTRAINTS as
	-- missing source code
;

create view TABLE_PRIVILEGES as
	-- missing source code
;

create view TRIGGERS as
	-- missing source code
;

create view USER_PRIVILEGES as
	-- missing source code
;

create view VIEWS as
	-- missing source code
;

