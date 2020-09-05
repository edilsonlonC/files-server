create table user ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name varchar (200) not null unique, 
    pass varchar(200) not null 
     );


create table files (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    namefile varchar(200),
    id_owner int,
    foreign key (id_owner) references user(id)

);