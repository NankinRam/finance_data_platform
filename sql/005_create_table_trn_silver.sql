create table silver.TRN(
	TRN_NUM serial primary key,
	DATE_TRN timestamp,
	SUM money,
	CUR char(3),
	SUM_RUB money,
	DESCRIPTION text,
	STATUS text,
	CARD text,
	TYPE_ID integer references silver.TYPE_OPER (TYPE_ID),
	CATEG_ID integer references silver.CATEGORY (CATEG_ID)
);