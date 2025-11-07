## 🧥 Projeto: Identificador Anônimo de Compradores de Roupas

### 📘 Descrição
Aplicação desktop executada no terminal que simula um sistema de compras de roupas mensais.  
Cada pessoa tem um perfil e realiza compras, e o sistema consegue **reconhecer automaticamente** quem é o comprador sem mostrar o nome real.

---

### ⚙️ Funcionalidades
- Cadastro de usuário  
- Registro de compras mensais  
- Identificação automática do usuário sem usar o nome  
- Exibição das compras e do identificador anônimo no terminal  

---

### 🛠️ Tecnologias
- Python 3  
- Armazenamento em arquivo JSON  
- Testes automatizados (Pytest)  
- CI/CD com GitHub Actions  

---

### 🚀 Execução
```bash
python main.py
```

---

### 🔁 Integração Contínua
O projeto usa GitHub Actions para:
- Instalar dependências  
- Rodar testes automaticamente a cada push  

---

### 📂 Estrutura do Projeto
```
identificador-roupas/
├── main.py
├── core/
│   ├── user.py
│   ├── purchases.py
│   └── recognizer.py
├── data/
│   └── database.json
├── tests/
│   └── test_all.py
└── README.md
```
