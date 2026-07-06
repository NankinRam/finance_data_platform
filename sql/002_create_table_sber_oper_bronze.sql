create table bronze.sber_oper(
  id_oper serial primary key,
  oper_date text,
  type_oper text,
  amount text,
  cur char(3),
  amount_rub text,
  description text,
  status text
 );