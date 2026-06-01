# EstacaoMeteorologica-ESP32-MQTT
Um pequeno projeto utilizando um ESP32 com o protocolo MQTT para monitoramento local de temperatura, umidade e luminosidade.

<img width="4000" height="3000" alt="IMG_20260525_174238077" src="https://github.com/user-attachments/assets/7e807c02-545b-4175-96d7-0c596b4af714" />

## Descrição detalhada
O projeto consiste de uma pequena estação de monitoramento wireless para coletar dados do ambiente, e então envia-los para um dashboard feito com o node-red, através de tópicos MQTT.
O código foi feito em sua totalidade em micropython, utilizando bibliotecas já presentes e também externas, como a SSD1306 para o display OLED utilizado no projeto, e a writer, utilizada
para a fonte FreeSans20 incluída.

### Vídeo de demonstração
https://www.youtube.com/watch?v=kDzHdICVkzs

### Lista de componentes
Para reproduzir esse projeto você irá precisar de:
- Um microcontrolador ESP32 (qualquer devkit);
- Um display OLED com o controlador SSD1306;
- Um sensor de temperatura e umidade DHT11 ou DHT22;
- Um LDR (resistor dependente de luz);
- 2 botões de qualquer tipo (de preferência que encaixem em uma protoboard);
- Uma ou mais protoboards;
- 4 Leds de qualquer cor (cores variadas são recomendadas para diferenciação);
- Jumpers;
- Um cabo de energia para conexão do ESP32 com o computador;
- Node-red instalado em seu computador, junto com as dependências dele.

### Pinout

- OLED SSD1306 (SCL),GPIO 22,I2C Clock
- OLED SSD1306 (SDA),GPIO 21,I2C Data
- Sensor DHT (Dados),GPIO 4,Entrada Digital
- LDR (Sensor de Luz),GPIO 32,Entrada Analógica (ADC)
- Botão Principal,GPIO 14,Entrada Digital (PULL_UP Interno)
- LED Status/MQTT,GPIO 27,Saída Digital
