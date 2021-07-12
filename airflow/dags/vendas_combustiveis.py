from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
import xml.etree.ElementTree as ET
import os,sys

dag = DAG('Venda_combustiveis',
          description='Atualiza os valores com os dados de vendas de combutiveis executando as 00:00  ',
          schedule_interval='0 0 * * *',
          start_date=datetime(2021, 1, 1),
          catchup=False
         )

_dummyOperator = DummyOperator(task_id='dummy_task', retries=3, dag=dag)

_tratamentoArquivo = BashOperator(task_id='TratamentoArquivoVenda', bash_command='getFiles.sh', dag=dag)

def gerarDML():
   vendas_xml  = ET.parse(r'/opt/airflow/dags/stage_files/vendas-combustiveis-m3/xl/worksheets/sheet2.xml')
   diesel_xml  = ET.parse(r'/opt/airflow/dags/stage_files/vendas-combustiveis-m3/xl/worksheets/sheet4.xml')  
   texto_xml  = ET.parse(r'/opt/airflow/dags/stage_files/vendas-combustiveis-m3/xl/sharedStrings.xml')

   texto_array = texto_xml.getroot() 
   if os.path.exists('/opt/airflow/dags/stage_files/dml.sql'):
      os.remove('/opt/airflow/dags/stage_files/dml.sql')
   
   file = open('/opt/airflow/dags/stage_files/dml.sql','w')
   for xmls in  [vendas_xml, diesel_xml ] :
      row = 0
      for child in xmls.getroot().find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}sheetData'):
          if (row > 0) :
             for i  in range(1,12):
                try:
                    sql =  f"""INSERT INTO tbl_sales(year_month, uf, product, unit, volume, created_at) 
                    VALUES ( 
                    \'{child[1][0].text}-{i}-01\', 
                    \'{texto_array[int(child[2][0].text)][0].text }\', 
                    \'{texto_array[int(child[0][0].text)][0].text }\', 
                    \'{texto_array[int(child[3][0].text)][0].text }\', 
                    {child[i+4][0].text}, 
                    CURRENT_TIMESTAMP ) 
                    ON CONFLICT (year_month, uf, product, unit)  
                    DO UPDATE SET  
                    volume=EXCLUDED.volume, created_at=EXCLUDED.created_at;\r\n"""
                    file.write(sql)
                except:
                    print(sys.exc_info()[0])
          row = row + 1
   file.close()

_gerarDML = PythonOperator(task_id='LeituraDados', python_callable=gerarDML)

_importPostgres = PostgresOperator(task_id="ImportPostgres", postgres_conn_id="postgres_default", sql="stage_files/dml.sql")

_dummyOperator >> _tratamentoArquivo >> _gerarDML >> _importPostgres 
