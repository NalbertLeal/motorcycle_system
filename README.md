# kafka
    Use the command bellow in the folder kafka:
        sudo chown -R 1001:1001 /dev/shm/kafka

## Sistema de motocicletas

### Os requisitos para o sistema funcionar

Para o sistema funcionar é nescessário que o(s) computador(es) tenha(m) acesso a mesma rede (assim podem se comunicar sem muita dor de cabeça), um dos computadores na rede deve ter mongodb instaldo e ao menos um também deve ter o kafka instalado. É recomendado que seja utilizado o docker por ser mais fácil de gerenciar e manter instâncias desses softwares (e até mesmo deletar os dados gerados por eles em caso de nescessidade).

### O funcionamento do sistema

O sistema consiste de quatro serviços que estam conectados ao kafka para enviar e receber os dados a serem processados, um serviço kafka, é o broker do sistema, e o mongodb, banco de dados noSQL que não faz uso de "squemas" permitindo que o sistema evolua com mais facilidade e velocidade. O processamento de umaa mídia é feita da seguinte maneira:

- O serviço da API ao recebe um arquivo e analisa o formato. Caso não seja uma mídia retorna um erro ao usuário. Caso seja um vídeo ou imagem ela será lida no formato de uma matriz que possui os valores dos pixeis, comprimida de uma matriz para imagens no formato png (pois assim ocupa menos espaço durante a transferência), serializadas com o uso de protobuf e enviadas para o kafka para permitir que os próximos serviços possam processar a mídia. Mídias de vídeo por se tratarem de multiplas imagens (frames) são enviadas multiplas imagens ao kafka. Cada um dos arquivos de imagem e vídeo são registrados no banco de dados. No momento de recebimento do arquivo também é iniciado um processamento da mídia recebida, isso gera um novo registro no banco que é referenciado como um processamento, pois um mesmo arquivo pode conter multiplos processamentos. Durante o processamento as imagens e frames não serão registrados no banco de dados até o momento que chegarem ao fim do seu processamento com uma detecção (assim tem que ter ao menos uma moto detectada no frame para  que ele seja registrado no banco de dados). Quando todos os frames do vídeo ou a imagem for enviada ao kafka o processamento receberá o status de finalizado.
- O serviço de detecção de motos fica a espera dos frames de vídeos ou imagens. Quando uma dessas mídias chegam até o consumidor desse serviço ele deserializa o pacote, converte a imagem de png para matriz, realiza um pré-processamento e passa o resultado para a rede neural que realiza a detecção de motos. Se não tiver motos na imagem ela não é passada para o próximo serviço e não será registrada no banco de dados. Se ouver alguma moto é feito uma serialização com protobuf das informações como "bounding boxes" e confiança da detecção e essas informações salvas no banco de dados do serviço de detecção de motos (indicado que seja um banco de dados que seja utilizado apenas pelos serviços de detecção de motos e que esteja na mesma instância do mongodb que os outros seviços) e após isso são enviadas juntamente da imagem com a moto para que o kafka repasse aos próximos serviços essa detecções. Se ouverem multiplas motos serão enviados multiplos pacotes em protobuf ao kafka.
- O serviço de detecção de placas ao receber através do kafka uma detecção de moto realiza a deserialização das informações, converte a imagem de png para matriz, com os valores do "bounding box" faz um recorte na imagem original para obter apenas a moto detectada e nesse recorte realiza a detecção de placas de motos. Se não ouver um detecção de placa o serviço simplesmente não enviará qualquer informação do pacote para o próximo serviço. Se ouver alguma detecção de placa de moto é feito uma serialização com protobuf das informações como "bounding boxes" e confiança da detecção, essas informações são salvas no banco de dados do serviço de detecção de placas de motos (indicado que seja um banco de dados que seja utilizado apenas pelos serviços de detecção de placas de motos e que esteja na mesma instância do mongodb que os outros seviços) e após isso enviadas juntamente de um recorte na imagem que possui apenas a placa da moto. O pacote recebido pelo kafka será repassado aos próximos serviços que contuinuarão os próximos estágios do processamento. Se ouverem multiplas placas serão enviadas multiplos pacotes em protobuf ao kafka.
- 

### Como iniciar o sistema

#### Executar o sistema em um computador

Para que o sistema inicie, se os requisitos são cumpridos é nescessário ir na pasta *utils/docker-compose-files/motorcycle_system/* e executar o arquivo *start.sh*, esse arquivo contém um script, ele exige que o usuário seja um super usuário. Ao inserir a senha ele irá preparar o ambiente para a execução do kafka e mongodb para que o sistema possa funcionar no computador em que o script foi executado.

#### Executar o sistema em multiplos computadores

