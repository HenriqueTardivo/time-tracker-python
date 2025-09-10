# Time Tracker

Meça o tempo gasto em tarefas usando CLI

Adicione o alias no seu ZSH ou Bash

```bash
alias tt="python3 /caminho/para/tarefas.py"
```

Atualize

```bash
source ~/.zshrc # ou ~/.bashrc
```

Agora é só rodar os comandos:

- Iniciar uma tarefa
  - `tt start 'NOME DA TAREFA'`
- Finalizar uma tarefa
  - `tt stop`
- Verificar tarefa em execuçao
  - `tt status`
- Verificar as tarefas realizadas no dia
  - `tt report`

O tempos vem formatado no formato `1h 30m`
