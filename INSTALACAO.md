# Roteiro de instalação

Este roteiro instala o **Modo Desenvolvedor**, um aplicativo Swift/AppKit com o botão **desenvolvimento** na barra superior do macOS.

O aplicativo inicia ao entrar na conta. A organização das janelas acontece ao clicar no botão: primeiro ele oculta o Dock e depois abre ou organiza Chrome, ChatGPT/Codex e Visual Studio Code em 50%, 25% e 25% da tela mais larga. O clique direito oferece **Sair**.

## 1. Requisitos

- Mac com Apple Silicon, como M1, M2, M3 ou posterior. O script atual compila somente para `arm64`; não gera uma versão para Mac Intel.
- macOS 13 ou posterior. O ambiente usado no desenvolvimento foi macOS 26.2 com Swift 6.2.3.
- Xcode ou Command Line Tools com o compilador Swift disponível.
- Google Chrome, ChatGPT/Codex e Visual Studio Code instalados e abertos pelo menos uma vez, com eventuais telas de boas-vindas concluídas.
- Idioma dos menus do Dock em português ou inglês, reconhecidos pela implementação atual.

O layout funciona com outras telas, mas foi validado em um Samsung Odyssey G91F de 5120 × 1440. O aplicativo usa pontos lógicos do macOS; em modos HiDPI, as medidas podem diferir dos pixels físicos.

Se as ferramentas de desenvolvimento ainda não estiverem instaladas:

```sh
xcode-select --install
```

Conclua a instalação apresentada pelo macOS. Depois confira:

```sh
xcode-select -p
swift --version
```

Não é necessário instalar pacotes pelo Homebrew, usar Python ou possuir certificado Apple Developer para a instalação básica.

## 2. Obter o código

Clone ou baixe este repositório. No Terminal, entre na pasta que contém `build.sh`, `DeveloperMode.swift`, `Geometry.swift` e `Info.plist`.

Se o repositório também contém o projeto `alternar-resolucao`, entre na subpasta:

```sh
cd modo-desenvolvedor
```

Os comandos seguintes devem ser executados nessa pasta.

## 3. Compilar e assinar

Para uma primeira instalação:

```sh
chmod +x build.sh
./build.sh
```

O resultado será:

```text
build/Modo Desenvolvedor.app
```

O script compila o código e aplica uma assinatura local **ad hoc**. Ele também verifica a assinatura. Se o aplicativo já estiver instalado, o script interrompe a compilação para proteger a autorização existente; siga a seção de atualização nesse caso.

## 4. Instalar antes de conceder a permissão

```sh
mkdir -p "$HOME/Applications"
ditto "build/Modo Desenvolvedor.app" "$HOME/Applications/Modo Desenvolvedor.app"
codesign --verify --deep --strict --verbose=2 "$HOME/Applications/Modo Desenvolvedor.app"
open "$HOME/Applications/Modo Desenvolvedor.app"
```

Abra sempre a cópia em `~/Applications`. Termine a compilação, a assinatura e a cópia para esse local **antes** de autorizar Acessibilidade. Evite abrir a cópia de `build/`.

O aplicativo não aparece no Dock. Procure o texto **desenvolvimento** na barra superior.

## 5. Autorizar Acessibilidade

1. Clique em **desenvolvimento** para solicitar a permissão.
2. Abra **Ajustes do Sistema → Privacidade e Segurança → Acessibilidade**.
3. Habilite **Modo Desenvolvedor**, autenticando-se se o macOS pedir.
4. Se o aplicativo não estiver na lista, use **+** e selecione `~/Applications/Modo Desenvolvedor.app`.
5. Clique novamente em **desenvolvimento**.

Após autorizar, não recompile, reassine, substitua ou mova o aplicativo. Uma atualização pode exigir uma nova autorização porque a assinatura local muda.

## 6. Conferir o funcionamento real

Clique no botão da barra superior e confirme que:

- O Dock passa a usar ocultação automática antes da abertura dos aplicativos.
- Chrome fica à esquerda com 50% da largura, ChatGPT/Codex no centro com 25% e VS Code à direita com 25%.
- As janelas usam a altura útil, preservando a barra de menus.
- O botão **desenvolvimento** continua na barra superior.

A ocultação automática do Dock permanece habilitada depois da execução. O Dock reaparece temporariamente ao levar o ponteiro à borda.

Para ler o resultado produzido pela própria instância da barra:

```sh
cat "$HOME/Library/Logs/ModoDesenvolvedor/ultima-execucao.json"
tail -n 30 "$HOME/Library/Logs/ModoDesenvolvedor/modo-desenvolvedor.log"
```

O JSON deve conter `"passed": true`. O log registra a confirmação de ocultação do Dock antes de `INÍCIO` e da abertura ou localização dos aplicativos.

Para medir novamente as três janelas via Accessibility:

```sh
"$HOME/Applications/Modo Desenvolvedor.app/Contents/MacOS/ModoDesenvolvedor" --verify
```

O comando retorna código `0` quando as três janelas conferem, com tolerância de até 3 pontos. Uma checagem executada pelo Terminal pode usar a autorização do próprio Terminal; ela complementa o teste do botão e o relatório da instância instalada.

## 7. Confirmar o início automático

Na primeira abertura, o aplicativo registra seu bundle como item de início usando `SMAppService.mainApp`.

```sh
"$HOME/Applications/Modo Desenvolvedor.app/Contents/MacOS/ModoDesenvolvedor" --diagnose
```

Confira `"loginStatus": 1`, que corresponde ao registro habilitado. Também é possível conferir em **Ajustes do Sistema → Geral → Itens de Início**; os nomes das seções podem variar entre versões do macOS.

Se o registro não estiver habilitado e você quiser ativá-lo ou renová-lo:

```sh
"$HOME/Applications/Modo Desenvolvedor.app/Contents/MacOS/ModoDesenvolvedor" --refresh-login
```

Ao entrar na conta, o botão aparecerá automaticamente. A abertura dos três aplicativos e a ocultação do Dock aguardam um clique em **desenvolvimento**.

## Atualizar uma instalação existente

Faça todas as alterações de código antes desta sequência. Não use esta sequência para apenas abrir o aplicativo já instalado.

1. Clique com o botão direito em **desenvolvimento** e escolha **Sair**.
2. Na pasta do código, compile a versão que deseja instalar:

```sh
./build.sh --allow-rebuild
```

3. Substitua a cópia instalada e confira a assinatura:

```sh
ditto "build/Modo Desenvolvedor.app" "$HOME/Applications/Modo Desenvolvedor.app"
codesign --verify --deep --strict --verbose=2 "$HOME/Applications/Modo Desenvolvedor.app"
```

4. Limpe somente a autorização antiga deste aplicativo e renove o registro de início:

```sh
tccutil reset Accessibility br.com.luizfilipe.modo-desenvolvedor
"$HOME/Applications/Modo Desenvolvedor.app/Contents/MacOS/ModoDesenvolvedor" --refresh-login
open "$HOME/Applications/Modo Desenvolvedor.app"
```

5. Repita a autorização de Acessibilidade e o teste do botão descritos acima.

A limpeza da autorização é específica para esse bundle. Não execute um reset geral de Acessibilidade.

## Resolver problemas

### A permissão está azul, mas o aviso se repete

Isso pode acontecer se a autorização foi concedida a uma compilação anterior. Encerre o aplicativo, confira que a versão final já está instalada e execute:

```sh
tccutil reset Accessibility br.com.luizfilipe.modo-desenvolvedor
open "$HOME/Applications/Modo Desenvolvedor.app"
```

Clique em **desenvolvimento** e autorize essa cópia novamente. Não recompile entre a limpeza e a autorização.

### Um aplicativo não abre ou não recebe o layout

Confira se ele está instalado, conclua manualmente eventuais diálogos de boas-vindas e tente novamente. Os identificadores usados são:

| Aplicativo | Bundle ID |
|---|---|
| Google Chrome | `com.google.Chrome` |
| ChatGPT/Codex | `com.openai.codex` |
| Visual Studio Code | `com.microsoft.VSCode` |

Consulte `modo-desenvolvedor.log` para identificar falhas de abertura, janelas indisponíveis, comandos do Dock ou limites de redimensionamento. O aplicativo seleciona janelas padrão e ignora painéis auxiliares.

### O botão não aparece após escolher Sair

Abra novamente a cópia instalada:

```sh
open "$HOME/Applications/Modo Desenvolvedor.app"
```

**Sair** encerra a execução atual, mas mantém o início automático para o próximo login.

## Desinstalar

1. Desabilite **Modo Desenvolvedor** nos Itens de Início dos Ajustes do Sistema.
2. Use o clique direito no botão e escolha **Sair**.
3. Mova `~/Applications/Modo Desenvolvedor.app` para a Lixeira.
4. Se desejar, remova sua entrada na lista de Acessibilidade.

Os logs ficam em `~/Library/Logs/ModoDesenvolvedor/`. A preferência de ocultação do Dock permanece como foi deixada; para revertê-la, use os ajustes do Dock do macOS.

## Arquivos para o Git

Versione o código Swift, `Info.plist`, `build.sh`, `Tests/`, `.gitignore` e a documentação.

O `.gitignore` exclui:

- `build/`, aplicativos compilados e arquivos de distribuição;
- `validation/`, que pode conter logs, hashes com caminhos locais e cópias de preferências pessoais;
- arquivos temporários do macOS e caches do Python.

Se este projeto continuar dentro do repositório que também contém `alternar-resolucao`, a partir da raiz desse repositório você pode preparar somente esta pasta:

```sh
git add modo-desenvolvedor/
git diff --cached --stat
```

Revise os arquivos antes de fazer o commit. Se publicar apenas este aplicativo em um repositório separado, use o conteúdo de `modo-desenvolvedor/` como raiz e mantenha seu `.gitignore`.
