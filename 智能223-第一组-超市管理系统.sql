create database if not exists supermarket;
use supermarket;
create table Staff(Snum  varchar(20) primary key,Sname varchar(20) not null,Ssex varchar(5) check(Ssex in('男','女')),Sage int not null check(Sage>=18),Sstand int not null check(Sstand>=0),Sphone varchar(20) not null,Sid varchar(25) not null,Spart varchar(10) not null,Ssalary decimal(8,2) check(Ssalary>=0));
create table Vendor(Vnum varchar(20) primary key,Vname varchar(20) not null,Vphone varchar(20) not null,Vpalce varchar(20) not null);
create table Goods(Gnum varchar(20) primary key,Gname varchar(10) not null,Gtype varchar(10) not null,Gprice decimal(8,2) check(Gprice>=0),Gbid decimal(8,2) check(Gbid>=0),Gstock int check(Gstock>=0),Galarm int check(Galarm>=0), Gplan int check(Gplan>=0),Vnum varchar(10) not null,foreign key(Vnum) references Vendor(Vnum));
create table Menber(Mnum varchar(20) primary key,Mname varchar(10) not null,Mphone varchar(20) not null,Mdate datetime,Mtotal decimal(8,2) check(Mtotal>=0),Mbalance decimal(8,2) check(Mbalance>=0),Mcip varchar(25) not null);
create table Ware(Wnum varchar(20) primary key,Wname varchar(10) not null,Wplace varchar(10) not null);
create table Trade(Tnum varchar(20) primary key,Tdate datetime  not null,Snum varchar(10) not null,Gnum varchar(10) not null,Tamount int check(Tamount>=0),Tmoney decimal(8,2) check(Tmoney>=0),Mnum varchar(10) not null,foreign key(Snum) references Staff(Snum),foreign key(Gnum) references Goods(Gnum),foreign key(Mnum) references Menber(Mnum));
create table Infor(Tnum varchar(20) not null,Gnum varchar(10) not null,Iamount int check(Iamount>=0),Imoney decimal(8,2) check(Imoney>=0),Idate datetime not null,foreign key(Tnum) references Trade(Tnum),foreign key(Gnum) references Goods(Gnum));
create table Entry(Enum varchar(20) primary key,Gnum varchar(10) not null,Eamount int check(Eamount>=0),Emoney decimal(8,2) check(Emoney>=0),Vnum varchar(10) not null,Edate datetime not null,Snum varchar(10) not null,foreign key(Snum) references Staff(Snum),foreign key(Gnum) references Goods(Gnum),foreign key(Vnum) references Vendor(Vnum));
create table Exits(Xnum varchar(20) primary key,Gnum varchar(10) not null,Xamount int check(Xamount>=0),Xmoney decimal(8,2) check(Xmoney>=0),Xdate datetime not null,Snum varchar(10) not null,foreign key(Snum) references Staff(Snum),foreign key(Gnum) references Goods(Gnum));

insert into Vendor(Vnum,Vname,Vphone,Vpalce) values ('100001','number1','12698577456','浙江');
insert into Vendor(Vnum,Vname,Vphone,Vpalce) values ('100002','number2','72798567498','湖北');
insert into Vendor(Vnum,Vname,Vphone,Vpalce) values ('100003','number3','69795867463','广州');

insert into Goods(Gnum,Gname,Gtype,Gprice,Gbid,Gstock,Galarm,Gplan,Vnum) values ('200001','薯片','零食',8,5,500,100,600,'100002');
insert into Goods(Gnum,Gname,Gtype,Gprice,Gbid,Gstock,Galarm,Gplan,Vnum) values ('200002','可乐','饮料',4,2,1000,200,1500,'100001');
insert into Goods(Gnum,Gname,Gtype,Gprice,Gbid,Gstock,Galarm,Gplan,Vnum) values ('200003','猪肉','肉类',32,20,400,50,500,'100003');

insert into Staff values ('2018001','党硕硕','男',21,5,'17838840997','411425200206062737','安保部','2300');
insert into Staff values('202001', '周炜森','男',19,3,'19562697275','411425200409182347','销售部','3400');
insert into Staff values('2019002', '程景晗','男',19,3,'1939919192','411425200406182367','商品部','3500');
insert into Menber values ('00001' , '吴京洋', '15639913767', '2020-02-05', 123.32, 500, '192.168.0.1');
insert into Ware values('3220001','义乌分仓库','义乌市青口候儿村6号');
insert into Trade values('BD20231218000001','2023-12-18','202001','200001',3,24,'00001');
insert into Infor values('BD20231218000001','200001',1,8,'2023-12-20');


insert into Entry values('BDI20231218000001',200001,6000,30000,'100001','2023-03-04','2019002');
insert into Exits values('BDO20231218000001','200002',400,1600,'2023-03-04','2019002');

select * from Goods;
select * from Vendor;
select * from Staff;  
select * from Menber;
select * from Ware;
select * from Trade;
select * from Infor;
select * from Entry;
select * from Exits;

#入库单编号 商品编号 入库量 总金额 供货商编号 入库日期 入库员编号
INSERT INTO Entry VALUES ('BDI202401022',200001 , 10, (SELECT Gbid * 10 FROM Goods WHERE Gnum = 200001), 100001, '2024-01-02', (SELECT Snum FROM Staff WHERE Sname = '程景晗'));


INSERT INTO Exits VALUES ('BDO202301013', 200001, 10, (SELECT Gbid * 10 FROM Goods WHERE Gnum =200001 ),'2023-01-01', (SELECT Snum FROM Staff WHERE Sname = '程景晗'));
SELECT * FROM Entry WHERE 1=1 AND Gnum LIKE '%200001%';

SELECT * FROM Entry WHERE 1=1 AND DATETIME(Edate) LIKE '%2023-01-01%';
SELECT * FROM Entry WHERE 1=1 AND DATE(Edate) = '2023-01-02';

SELECT * FROM Entry WHERE 1=1 AND Edate LIKE '2024-01-02%';
INSERT INTO Entry VALUES ('BDT202401031', '2024-01-03', '202001', '200001', 10, (SELECT Gbid * 10 FROM Goods WHERE Gnum = '200001'),'00001');

INSERT INTO Goods VALUES ('BDGOODs4', '火腿肠', '零食',3, 2, 0, 50,500,100002);

SELECT * FROM Goods WHERE Gnum LIKE '200001';
DELETE FROM Goods WHERE Gnum = '200001';

DELETE FROM Goods WHERE Gnum = 'BDGOODS6';

DELETE FROM Infor WHERE Gnum = '200001';

INSERT INTO Vendor (Vnum, Vname, Vphone, Vpalce) VALUES
('V001', 'Supplier1', '123-456-7890', 'Location1'),
('V002', 'Supplier2', '987-654-3210', 'Location2'),
('V003', 'Supplier3', '456-789-0123', 'Location3');


INSERT INTO Goods (Gnum, Gname, Gtype, Gprice, Gbid, Gstock, Galarm, Gplan, Vnum) VALUES
('G001', 'Product1', 'Type1', 10.99, 8.99, 100, 20, 50, 'V001'),
('G002', 'Product2', 'Type2', 15.99, 12.99, 150, 30, 80, 'V002'),
('G003', 'Product3', 'Type1', 8.99, 6.99, 80, 15, 40, 'V003');

-- 插入会员数据
INSERT INTO Menber (Mnum, Mname, Mphone, Mdate, Mtotal, Mbalance, Mcip) VALUES
('M001', 'Customer1', '111-222-3333', '2023-01-01', 500.00, 100.00, '192.168.1.1'),
('M002', 'Customer2', '444-555-6666', '2023-02-15', 1000.00, 300.00, '192.168.1.2'),
('M003', 'Customer3', '777-888-9999', '2023-03-20', 800.00, 200.00, '192.168.1.3');

-- 插入仓库数据
INSERT INTO Ware (Wnum, Wname, Wplace) VALUES
('W001', 'Warehouse1', 'LocationA'),
('W002', 'Warehouse2', 'LocationB');
