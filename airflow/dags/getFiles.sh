#!/bin/bash

cd /opt/airflow/dags/stage_files/ 

curl http://www.anp.gov.br/arquivos/dados-estatisticos/vendas-combustiveis/vendas-combustiveis-m3.xls --output vendas-combustiveis-m3.xls

libreoffice --convert-to xlsx vendas-combustiveis-m3.xls --headless

mv vendas-combustiveis-m3.xlsx vendas-combustiveis-m3.zip

7z x vendas-combustiveis-m3.zip -o./vendas-combustiveis-m3 -y
