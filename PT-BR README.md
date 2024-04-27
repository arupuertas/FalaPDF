# Easy PDF

Um jeito fácil e rápido de conversar e tirar suas dúvidas sobre seus arquivos PDF.

O projeto foi feito usando Python e modelos da Open AI para fazer a comunicação entre usuário e arquivo.

Para utilizar localmente faça o donwload do projeto, instale os requirements.txt e rode com `streamlit run fala_pdf.py`.

Não esqueça de criar um arquivo .env e colocar suas credenciais da API que deseja usar, caso queira usar de maneira 100% gratuita coloquei algumas opções de LLM do Hugging face para poder utilizar, só descomentar utilizá-las.

O projeto aceita multiplos arquivos.

#### Instalação

1. Clone o repositório:

    ```
    git clone https://github.com/seu/repositório.git
    ```

2. Navegue até o diretório do projeto.

3. Instale as dependências necessárias:

    ```
    pip install -r requirements.txt
    ```

4. Crie um arquivo `.env` e adicione suas credenciais da API. Para uma experiência sem complicações, algumas opções dos LLMs da Hugging Face são fornecidas para uso gratuito. Descomente e utilize conforme necessário.

#### Uso

Após a instalação, execute o seguinte comando para iniciar o Easy PDF Talk:

streamlit run fala_pdf.py


Ao executar, você poderá conversar com seus arquivos PDF.

#### Recursos

- **Entrada por Voz**: Faça perguntas sobre seus arquivos PDF facilmente usando a funcionalidade de entrada por voz.
- **Entrada de Texto**: Alternativamente, digite suas perguntas diretamente no campo de entrada fornecido.
- **Respostas em Tempo Real**: Obtenha respostas e insights instantâneos sobre suas consultas.
- **Suporte a Múltiplos Arquivos**: O projeto aceita o upload de múltiplos arquivos.

#### Como Funciona

O Easy PDF Talk utiliza modelos avançados de processamento de linguagem natural da OpenAI para interpretar as consultas do usuário e fornecer respostas relevantes. Ele se integra perfeitamente ao Streamlit para uma experiência do usuário fluida.

#### Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para fazer um fork do repositório e enviar pull requests com suas melhorias ou correções de bugs.

#### Licença

Este projeto está licenciado sob a Licença MIT - consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

