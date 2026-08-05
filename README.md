# Projeto de Processamento e Visualização de Sinais EMG

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Este repositório contém um conjunto de ferramentas para análise de sinais de **Eletromiografia (EMG)**.  
Inclui scripts didáticos comentados com as etapas clássicas de processamento (detecção de bursts, correção de média, filtragem e retificação) e uma **interface gráfica** (frontend) que integra essas funcionalidades, permitindo visualização e exportação dos resultados.

---

## 📌 Objetivo

- Fornecer um **material de estudo** claro e comentado sobre processamento de EMG.
- Demonstrar as principais técnicas: **filtragem, retificação, correção de baseline e detecção de ativação muscular (bursts)**.
- Facilitar a execução e visualização através de uma **aplicação com interface gráfica (Tkinter)**.
- Tornar o ambiente de desenvolvimento **reproduzível** com a criação de um ambiente virtual isolado.


## 📁 Estrutura do Projeto

```
codes-emg
│
├── core-codes-with-coments/ # Scripts independentes e comentados (didáticos)
│ ├── Emg1_BurstAndPlot.py # Detecção de bursts e plotagem
│ ├── Emg2_CorrectMeanPlot.py # Cálculo da média corrigida e plotagem
│ ├── Emg3_FileredRectifyPlot.py# Filtragem + retificação e plotagem
│ ├── fig2.png # Exemplo de saída do script 2
│ ├── fig3.png # Exemplo de saída do script 3
│ └── fig4.png # Exemplo de saída do script 4
│
├── project-onset/ # (Opcional) Versão inicial do projeto
│
├── project-with-frontend/ # Aplicação principal com interface gráfica
│ ├── .spyproject/ # Configurações do Spyder (ambiente de desenvolvimento)
│ ├── output_images/ # Pasta para salvar as imagens geradas pela interface
│ ├── src/ # Código-fonte da aplicação (módulos, lógica, GUI)
│ ├── venv/ # Ambiente virtual (criado pelo setup)
│ └── setup-win.bat # Script para automação do ambiente no Windows
│
├── requirements.txt # Lista de dependências (numpy, scipy, matplotlib)
└── README.md # Este arquivo
```

---

## 🛠️ Tecnologias e Bibliotecas

| Tecnologia / Biblioteca | Finalidade |
|------------------------|------------|
| **Python 3.8+** | Linguagem base do projeto |
| **NumPy** | Operações numéricas e manipulação de arrays |
| **SciPy** | Filtros digitais e processamento de sinais (ex: `butter`, `lfilter`, `find_peaks`) |
| **Matplotlib** | Geração de gráficos e visualização dos sinais |
| **Tkinter** (já incluso no Python) | Criação da interface gráfica (frontend) |
| **virtualenv** (`venv`) | Isolamento do ambiente de desenvolvimento |
| **Spyder** (opcional) | IDE científica recomendada para visualização interativa |

---

## 🧠 Explicação das Funções (Scripts Comentados)

Os arquivos em `core-codes-with-coments/` são **independentes** e extremamente comentados, ideais para aprendizado.

### 1. `Emg1_BurstAndPlot.py`
**Função:** detecta **períodos de ativação muscular (bursts)** em um sinal EMG.  
**Etapas típicas:**
- Carregamento do sinal (simulado ou arquivo).
- Aplicação de um limiar (threshold) baseado em estatísticas do sinal.
- Identificação dos intervalos onde a amplitude ultrapassa o limiar.
- Plotagem do sinal bruto com destaque das regiões de burst.

### 2. `Emg2_CorrectMeanPlot.py`
**Função:** calcula e plota a **média corrigida** do sinal.
- Remove offset (componente DC) e, se necessário, normaliza.
- Calcula a média móvel ou envelope do sinal.
- Gera um gráfico comparativo entre o sinal original e a média corrigida.

### 3. `Emg3_FileredRectifyPlot.py`
**Função:** aplica **filtragem passa-banda e retificação de onda completa**.
- Filtro Butterworth (passa-banda) para remover ruídos e artefatos de movimento.
- Retificação (valor absoluto) do sinal filtrado.
- Plotagem da sobreposição: sinal original, filtrado e retificado.
- *Figuras `fig2.png`, `fig3.png` e `fig4.png` são exemplos das saídas desses scripts.*

---

## 🖥️ Aplicação com Frontend (`project-with-frontend/`)

A pasta `src/` contém um programa em **Tkinter** que integra todas as funcionalidades acima:

- Interface amigável para selecionar arquivos de dados EMG.
- Botões para executar cada análise (burst, média corrigida, filtragem/retificação).
- Visualização dos gráficos diretamente na interface.
- Opção de salvar as figuras na pasta `output_images/`.

---

## ⚙️ Como Rodar o Projeto

### ✔️ Usando o `setup-win.bat` (Windows - Método Recomendado)

1. **Clone o repositório** ou faça o download dos arquivos.
2. Navegue até a pasta `project-with-frontend/`.
3. **Clique duas vezes** em `setup-win.bat`.  
   Esse script irá:
   - Criar o ambiente virtual (`venv`), se ainda não existir.
   - Ativar o ambiente.
   - Instalar as dependências listadas em `requirements.txt` (numpy, scipy, matplotlib).
4. Após o término do setup, **mantenha o terminal aberto** e execute a interface gráfica:
   ```bash
   python src/gui.py
    ```

> 💡 *Na primeira execução, o script pode demorar um pouco pois irá baixar os pacotes. Nas próximas vezes, a abertura será instantânea.*

---

### 🐍 Executando manualmente (qualquer SO)

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar (Windows)
venv\Scripts\activate

# Ativar (Linux/macOS)
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Rodar a aplicação (exemplo)
python src/gui.py
```

---

### 🧪 Executando os scripts isolados (didáticos)

Os scripts da pasta core-codes-with-coments/ podem ser rodados individualmente no terminal ou no Spyder:

```bash
cd core-codes-with-coments
python Emg1_BurstAndPlot.py
```

Apenas certifique-se de ter as bibliotecas instaladas no seu ambiente Python.

---

### 🐞 Dicas para uso no Spyder

1. Configure o interpretador do Spyder para apontar para o Python do `venv` (em `Ferramentas > Preferências > Interpretador Python`).

2. Para scripts com Tkinter, configure a execução em terminal externo (`Executar > Configurar por arquivo > Console > Executar em um terminal externo`).
Assim a janela gráfica abrirá sem travar o console do Spyder.

---

## 📦 Dependências (requirements.txt)

```text
numpy
scipy
matplotlib
```

O Tkinter é parte da biblioteca padrão do Python e não precisa de instalação extra (exceto em algumas distribuições Linux, onde pode ser necessário `sudo apt install python3-tk`).



## 🤝 Contribuição

Este é um projeto educacional. Sugestões e melhorias são bem-vindas!
Sinta-se à vontade para abrir issues ou pull requests.


## 📄 Licença
Distribuído sob a licença MIT. Veja `LICENSE` para mais informações (se disponível).

---

Desenvolvido para fins de estudo e experimentação.
