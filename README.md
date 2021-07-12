# airflow_xls

Com o objetivo de desenvolver de um pipeline buscando dados em xls usando airflow.
Para a leitura dos dados das tabelas dinâmicas foi necessário criar uma versão da tabela em xlsx onde fica disponível os xml com os dados.
  - Utiliza a biblioteca o libreoffice para essa função 
  - Utiliza o 7z para desempacotar os arquivos 
     - ~/airflow/dags/stage_files será descompactado os arquivos xml 
  - Com os arquivos desempacotados é usado no python xml.etree.ElementTree para leitura dos dados gerando um arquivo dml.sql localizado em: ~/airflow/dags/stage_files/dml.sql onde faz o merge dos dados. Existe a possibilidade de melhoria para uma carga incremental.
  - Por fim o airflow utiliza da suas connections para fazer a carga  

