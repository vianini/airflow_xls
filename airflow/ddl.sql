/* script de criacao de tabelas */

CREATE DATABASE sales; 

CREATE TABLE IF NOT EXISTS tbl_sales (
   year_month date NOT NULL ,
   uf text NOT NULL ,
   product text NOT NULL ,
   unit text NOT NULL, 
   volume double precision NOT NULL,
   created_at timestamp NOT NULL,
   CONSTRAINT tbl_sales_key PRIMARY KEY(year_month, uf, product, unit) 
);
