# GitHub Branch Protection - Manual Setup

## Overview

Branch protection rules devem ser configuradas manualmente no GitHub para garantir que nenhum código seja mergeado sem passar pelos quality gates do CI.

---

## Step-by-Step Configuration

### 1. Acessar Branch Protection Settings

1. Vá para o repositório no GitHub: https://github.com/gustavocontador/jornada-empreendedor
2. Clique em **Settings** (ícone de engrenagem no topo)
3. No menu lateral esquerdo, clique em **Branches**
4. Na seção **Branch protection rules**, clique em **Add rule**

### 2. Configurar Branch Protection para `main`

#### Branch name pattern
```
main
```

#### Required Status Checks

Marque as seguintes opções:

- ✅ **Require status checks to pass before merging**
  - ✅ **Require branches to be up to date before merging**
  - Adicione os seguintes checks como obrigatórios (clique em "Search for status checks..."):
    - `lint-backend`
    - `lint-frontend`
    - `test-backend`
    - `test-frontend`
    - `quality-summary`

#### Additional Settings

- ✅ **Require a pull request before merging**
  - Número de approvals requeridos: `1`

- ✅ **Do not allow bypassing the above settings**
  - Garante que nem administradores podem bypasear os checks

- ⚠️ **Do not** mark "Include administrators" (deixe desmarcado para emergências)

### 3. Configurar Branch Protection para `develop` (Opcional)

Se usar branch `develop` para desenvolvimento:

Repita os mesmos passos acima, mas com pattern:
```
develop
```

---

## Validação

Após configurar, teste criando um PR:

### Teste 1: PR com código válido
```bash
git checkout -b test/valid-code
# Fazer pequena alteração válida
git add .
git commit -m "test: validate CI"
git push origin test/valid-code
gh pr create --title "Test: Valid Code" --body "Testing CI pipeline"
```

**Esperado:** Todos os checks devem passar ✅

### Teste 2: PR com lint error
```bash
git checkout -b test/lint-error
# Adicionar código com erro de lint no backend
echo "def foo( ): pass" >> backend/app/test.py
git add .
git commit -m "test: lint error"
git push origin test/lint-error
gh pr create --title "Test: Lint Error" --body "Testing lint failure"
```

**Esperado:** Job `lint-backend` deve falhar ❌

### Teste 3: PR com test failure
```bash
git checkout -b test/test-failure
# Adicionar teste que falha
# ...
git add .
git commit -m "test: failing test"
git push origin test/test-failure
gh pr create --title "Test: Test Failure" --body "Testing test failure"
```

**Esperado:** Jobs `test-backend` ou `test-frontend` devem falhar ❌

---

## Troubleshooting

### Problema: Status checks não aparecem na lista

**Causa:** Os checks só aparecem após serem executados pelo menos uma vez.

**Solução:**
1. Faça um push para `main` ou crie um PR primeiro
2. Aguarde o CI executar
3. Depois configure as branch protection rules

### Problema: Merge permitido mesmo com CI falhando

**Causa:** Branch protection não configurada corretamente.

**Solução:**
1. Verifique que "Require status checks to pass before merging" está marcado
2. Verifique que todos os 5 checks estão na lista de required checks
3. Verifique que "Do not allow bypassing" está marcado

### Problema: CI não executando automaticamente

**Causa:** Workflow triggers não configurados.

**Solução:**
Verifique `.github/workflows/ci.yml` contém:
```yaml
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
```

---

## Referências

- [GitHub Branch Protection Docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)
- [GitHub Required Status Checks](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches#require-status-checks-before-merging)
