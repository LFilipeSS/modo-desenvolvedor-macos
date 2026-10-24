# Modo Desenvolvedor

Aplicativo Swift/AppKit exclusivo da barra de menus. Instalação: `~/Applications/Modo Desenvolvedor.app`. Identidade: `br.com.luizfilipe.modo-desenvolvedor`.

## Instalação

Siga o [roteiro de instalação](INSTALACAO.md), que inclui requisitos, compilação, assinatura, Acessibilidade, início automático, atualização e solução de problemas. O build atual gera uma versão para Macs com Apple Silicon (`arm64`).

Clique no botão **desenvolvimento** na barra superior para ativar diretamente o layout. O clique direito oferece **Sair** e o estado atual. O aplicativo abre Chrome, ChatGPT/Codex e VS Code quando necessário, aguarda janelas padrão utilizáveis, restaura minimização/tela cheia, aplica 50% / 25% / 25% da largura e confere o resultado via Accessibility. Usa a tela mais larga, com área como desempate, e sua área útil, respeitando barra e Dock. A diferença de até 3 pontos aceita limitações de tamanho dos aplicativos.

Antes de abrir ou organizar os aplicativos, habilita a ocultação automática do Dock e aguarda a nova área útil estabilizar. Usa o comando nativo de ocultação do Dock via Acessibilidade, compatível com os títulos de menu em português e inglês. Confirma a preferência e a área útil real antes de iniciar os aplicativos. O Dock volta a aparecer temporariamente quando o ponteiro chega à borda. A ocultação automática permanece habilitada depois da execução.

Não configura mouse, teclado, Rectangle ou Logi Options+. Não registra atalhos de teclado. **Sair** encerra somente este aplicativo; o início no próximo login permanece habilitado.

## Início automático e permissão

Usa `SMAppService.mainApp`, associado ao bundle instalado. Pode ser desabilitado nos Itens de Início dos Ajustes do Sistema. `LSUIElement` e política `.accessory` impedem a presença no Dock.

A assinatura é local (ad hoc), sem certificado Apple Developer. A versão final deve ser autorizada em Privacidade e Segurança → Acessibilidade. Não substituir o binário após autorizar: uma atualização altera sua identidade criptográfica e pode exigir nova autorização. O script de build recusa recompilação após instalar, exceto com a opção explícita `--allow-rebuild`.

## Diagnóstico

Log legível: `~/Library/Logs/ModoDesenvolvedor/modo-desenvolvedor.log` (rotacionado aos 2 MB). Último resultado: `ultima-execucao.json`, na mesma pasta. Evidências de testes ficam em `validation/` neste projeto.

Comandos somente de diagnóstico do mesmo binário: `--diagnose`, `--inspect` e `--verify`. O último retorna código 0 somente quando as três posições, alturas e proporções conferem. Executado pelo terminal, pode herdar a autorização do aplicativo responsável; por isso a validação inclui o resultado gerado pela própria instância da barra, iniciada pelo Launch Services.

`Tests/ButtonProbe.swift` opera o botão real da barra com `AXPress`, sem chamar o método de layout diretamente. `Tests/IndependentVerifier.swift` mede janelas novamente por uma implementação independente, confere o botão dentro da tela e a ausência do aplicativo no Dock. `Tests/CandidateRunner.swift` permite validar correções do engine separadamente, sem substituir o aplicativo instalado. `Tests/MenuProbe.swift` e `Tests/run-final-tests.py` são auxiliares históricos para a interface de menu da versão 1.0.x.

## Fontes e testes de geometria

`Geometry.swift` converte AppKit (origem inferior esquerda da tela primária) para AX (origem superior esquerda da tela primária). `DeveloperMode.swift` contém o engine, menu, registro de login e diagnósticos. `Info.plist` define o bundle.

```sh
swiftc -parse-as-library Geometry.swift Tests/GeometryTests.swift -o /tmp/modo-geometry-tests
/tmp/modo-geometry-tests
```

As APIs de referência são [SMAppService.mainApp](https://developer.apple.com/documentation/servicemanagement/smappservice/mainapp) e [NSScreen.visibleFrame](https://developer.apple.com/documentation/appkit/nsscreen/visibleframe).
