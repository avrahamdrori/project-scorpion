drop table if exists files;
create table entries (
  id integer primary key autoincrement,
  email text not null,
  originalFileName text not null,
  uuidName text not null,
  numOfTimes integer not null
);
