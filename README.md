# STR-sweeper

Para a visualizção completa do funcionamento do projeto, é necessário ter o simulador coppeliaSim, e nomear sensores e possíveis motores do robô móvel para serem controlados pelo código.

simConst.py e sim.py, são os módulos contendo a API de integração python<->coppelia.
timeMed.py é apenas um modelo de medição de tempo de execução das tasks implementadas.
remoteApi.so é um arquivo necessário para o funcionamento da integração no Linux, caso esteja em outro sistema operacional e necessário usar outro arquivo de configuração.
sweeper.py é o programa que controla o robô orientado a threads.
caso não tenha a lib do pyRTOS instalada na sua máquina, é necessário entrar no ambiente virtual (sweeper), com o comando:

`$ source sweeper/bin/activate`

o programa sweeper.py escreve as medições de tempo das tasks nos arquivos com nome das tasks (ou nomes proximos disso).
