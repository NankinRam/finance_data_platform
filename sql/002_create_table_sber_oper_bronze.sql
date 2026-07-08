create table bronze.sber_oper(
  id_oper serial primary key,
  oper_date text,
  type_oper text,
  category text,
  amount text,
  cur text,
  amount_rub text,
  description text,
  status text,
  card text
 );