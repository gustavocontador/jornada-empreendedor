# Documentação de Componentes

## Componentes UI (shadcn/ui)

### Button
Botão customizável com variantes e tamanhos.

**Variantes:** `default`, `destructive`, `outline`, `secondary`, `ghost`, `link`
**Tamanhos:** `default`, `sm`, `lg`, `icon`

```tsx
<Button variant="outline" size="lg">Clique Aqui</Button>
```

### Input
Campo de entrada de texto.

```tsx
<Input type="email" placeholder="seu@email.com" />
```

### Label
Rótulo para campos de formulário.

```tsx
<Label htmlFor="email">Email</Label>
```

### Card
Container para conteúdo agrupado.

```tsx
<Card>
  <CardHeader>
    <CardTitle>Título</CardTitle>
    <CardDescription>Descrição</CardDescription>
  </CardHeader>
  <CardContent>Conteúdo</CardContent>
  <CardFooter>Rodapé</CardFooter>
</Card>
```

### Progress
Barra de progresso.

```tsx
<Progress value={75} />
```

### RadioGroup
Grupo de opções de rádio.

```tsx
<RadioGroup value={value} onValueChange={setValue}>
  <RadioGroupItem value="option1" id="opt1" />
  <Label htmlFor="opt1">Opção 1</Label>
</RadioGroup>
```

### Select
Menu dropdown de seleção.

```tsx
<Select value={value} onValueChange={setValue}>
  <SelectTrigger>
    <SelectValue placeholder="Selecione..." />
  </SelectTrigger>
  <SelectContent>
    <SelectItem value="1">Opção 1</SelectItem>
  </SelectContent>
</Select>
```

### Dialog
Modal/diálogo.

```tsx
<Dialog>
  <DialogTrigger>Abrir</DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Título</DialogTitle>
    </DialogHeader>
  </DialogContent>
</Dialog>
```

### Tabs
Navegação em abas.

```tsx
<Tabs defaultValue="tab1">
  <TabsList>
    <TabsTrigger value="tab1">Aba 1</TabsTrigger>
  </TabsList>
  <TabsContent value="tab1">Conteúdo</TabsContent>
</Tabs>
```

### Loading
Componente de loading reutilizável.

```tsx
<Loading message="Carregando dados..." />
<LoadingSpinner size="large" />
```

## Componentes de Gráficos

### DISCChart
Gráfico de barras horizontais para perfil DISC.

**Props:**
- `data: DISCResult` - Dados do resultado DISC

**Características:**
- 4 barras horizontais (D, I, S, C)
- Cores específicas para cada dimensão
- Descrição do perfil

```tsx
<DISCChart data={result.disc} />
```

### SpiralChart
Gráfico radar para Espiral Dinâmica.

**Props:**
- `data: SpiralDynamicsResult` - Dados da Espiral

**Características:**
- Radar de 8 pontos (8 cores)
- Cores fiéis ao modelo original
- Legenda com valores
- Cor dominante destacada

```tsx
<SpiralChart data={result.spiral_dynamics} />
```

### PAEIChart
Gráfico radar para papéis PAEI.

**Props:**
- `data: PAEIResult` - Dados PAEI

**Características:**
- Radar de 4 pontos (P, A, E, I)
- Código PAEI
- Descrição dos papéis

```tsx
<PAEIChart data={result.paei} />
```

### EnneagramChart
Representação visual do Eneagrama.

**Props:**
- `data: EnneagramResult` - Dados do Eneagrama

**Características:**
- Círculo com 9 tipos
- Tipo do usuário destacado
- Linhas internas do eneagrama
- Forças e desafios

```tsx
<EnneagramChart data={result.enneagram} />
```

### ValuesChart
Exibição dos valores principais.

**Props:**
- `data: ValuesResult` - Dados dos valores

**Características:**
- Top 3 valores
- Descrições detalhadas
- Layout em cards

```tsx
<ValuesChart data={result.values} />
```

## Componentes de Assessment

### QuestionCard
Renderiza uma pergunta do questionário.

**Props:**
- `question: Question` - Pergunta a ser exibida
- `value: any` - Valor atual da resposta
- `onChange: (value: any) => void` - Callback ao mudar resposta

**Tipos de perguntas suportados:**
- `likert_5` - Escala Likert de 5 pontos
- `multiple_choice` - Múltipla escolha
- `ranking` - Classificação de opções
- `text` - Texto livre

```tsx
<QuestionCard
  question={currentQuestion}
  value={responses[currentQuestion.id]}
  onChange={handleAnswer}
/>
```

### ProgressBar
Barra de progresso do questionário.

**Props:**
- `current: number` - Questão atual
- `total: number` - Total de questões
- `percentage: number` - Percentual de conclusão

```tsx
<ProgressBar current={5} total={50} percentage={10} />
```

### QuestionNavigation
Navegação entre perguntas.

**Props:**
- `canGoPrevious: boolean` - Pode voltar
- `canGoNext: boolean` - Pode avançar
- `isLastQuestion: boolean` - É a última pergunta
- `onPrevious: () => void` - Callback para voltar
- `onNext: () => void` - Callback para avançar
- `onComplete: () => void` - Callback para finalizar
- `loading?: boolean` - Estado de loading

```tsx
<QuestionNavigation
  canGoPrevious={canGoPrevious()}
  canGoNext={canGoNext()}
  isLastQuestion={isLastQuestion()}
  onPrevious={handlePrevious}
  onNext={handleNext}
  onComplete={handleComplete}
  loading={loading}
/>
```

## Hooks Customizados

### useAuth
Hook para gerenciar autenticação.

**Retorna:**
- `user: User | null` - Usuário logado
- `isAuthenticated: boolean` - Se está autenticado
- `isAdmin: boolean` - Se é admin
- `login: (data: LoginRequest) => Promise<AuthResponse>` - Fazer login
- `register: (data: RegisterRequest) => Promise<AuthResponse>` - Cadastrar
- `logout: () => void` - Fazer logout

```tsx
const { user, isAuthenticated, login, logout } = useAuth()
```

### useAssessment
Hook para gerenciar assessment.

**Retorna:**
- `assessment: Assessment | null` - Assessment atual
- `questions: Question[]` - Lista de perguntas
- `responses: Record<string, any>` - Respostas salvas
- `currentQuestion: Question | null` - Pergunta atual
- `progress: { current, total, percentage }` - Progresso
- `loading: boolean` - Estado de loading
- `error: string | null` - Mensagem de erro
- `startAssessment: () => Promise<Assessment>` - Iniciar novo
- `loadAssessment: (id: string) => Promise<Assessment>` - Carregar existente
- `answerQuestion: (questionId: string, response: any) => void` - Responder
- `nextQuestion: () => void` - Próxima pergunta
- `previousQuestion: () => void` - Pergunta anterior
- `completeAssessment: () => Promise<any>` - Finalizar
- `canGoNext: () => boolean` - Pode avançar
- `canGoPrevious: () => boolean` - Pode voltar
- `isLastQuestion: () => boolean` - É a última

```tsx
const {
  currentQuestion,
  responses,
  answerQuestion,
  nextQuestion,
  completeAssessment
} = useAssessment()
```

## Stores (Zustand)

### authStore
Estado global de autenticação.

```tsx
const { user, setAuth, logout } = useAuthStore()
```

### assessmentStore
Estado global do assessment.

```tsx
const { assessment, questions, setResponse } = useAssessmentStore()
```

## Utilitários (lib/)

### api.ts
Cliente Axios configurado com interceptors.

```tsx
import api from '@/lib/api'
const response = await api.get('/endpoint')
```

### auth.ts
Funções de autenticação e localStorage.

```tsx
import { setToken, getToken, isAuthenticated } from '@/lib/auth'
```

### utils.ts
Funções utilitárias.

```tsx
import { cn, formatDate, debounce } from '@/lib/utils'
```

## Boas Práticas

1. **Sempre use os hooks customizados** ao invés de acessar stores diretamente
2. **Componentes UI são reutilizáveis** - não modifique, crie composições
3. **Validação em todos os forms** com react-hook-form + zod
4. **Loading states** em todas as operações assíncronas
5. **Error handling** com try/catch e mensagens amigáveis
6. **Auto-save** no questionário usa debounce (500ms)
7. **Types TypeScript** para tudo - evite `any`
8. **Responsividade** mobile-first com Tailwind
