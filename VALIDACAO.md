# Validação da versão final 1.0.1

Executada em 23/10/2026, horário de São Paulo, no macOS 26.2, monitor Odyssey G91F de 5120 × 1440 pontos. Os timestamps JSON/log estão em UTC.

Registro histórico da versão 1.0.1, anterior ao botão direto da versão 1.1.0 e ao controle do Dock da versão 1.2.0. Não representa uma validação das versões posteriores.

Aplicativo instalado em `~/Applications/Modo Desenvolvedor.app`. Bundle `br.com.luizfilipe.modo-desenvolvedor`, versão 1.0.1, build 2. O hash de referência foi salvo localmente em `validation/final-binary-sha256.txt`; as evidências locais não são versionadas. A assinatura e esse hash foram conferidos depois dos testes da versão 1.0.1; seu binário não foi substituído após a autorização durante aquela validação.

## Resultado final

| Aplicativo | X em AX | Y em AX | Largura | Altura | Fração da largura |
|---|---:|---:|---:|---:|---:|
| Chrome | 0 | 30 | 2560 | 1410 | 50% |
| ChatGPT/Codex | 2560 | 30 | 1280 | 1410 | 25% |
| Visual Studio Code | 3840 | 30 | 1280 | 1410 | 25% |

A área útil final informada por NSScreen foi `(0, 0, 5120, 1410)` em AppKit: o Dock estava com ocultação automática habilitada. Nenhuma preferência do Dock foi escrita. Em uma etapa anterior a área útil era 1317 pontos de altura; uma captura de diagnóstico registrou essa mudança antes de reativar o layout. A nova execução do menu recalculou a área útil e passou nas verificações finais.

## Testes concluídos

- Acionamento de `AXPress` no item real de `AXExtrasMenuBar`, seguido de `AXPress` no `NSMenuItem` **Ativar Modo Desenvolvedor**. O método de layout não foi chamado diretamente pelo teste final.
- Execução repetida com os três aplicativos abertos, com medições independentes via AX. Evidências `20-repeat-open-apps-*`.
- Chrome minimizado antes da execução, restaurado pelo aplicativo, seguido da medição das três janelas. Evidências `21-minimized-before.json` e `22-minimized-*`.
- Chrome em tela cheia antes da execução da versão final, restaurado e organizado pelo menu. Evidências `11-final-fullscreen-before.json`, `12-final-fullscreen-after.json` e `13-independent-fullscreen-after.json`.
- Chrome encerrado normalmente, confirmado ausente antes do comando; reaberto pelo aplicativo e novamente medido. Evidências `23-closed-chrome-before.json` e `24-closed-chrome-*`. Um problema no helper de teste ao aguardar notificações de término foi corrigido no helper, usando o run loop; o aplicativo instalado permaneceu inalterado.
- Item **Sair** encerrou somente o Modo Desenvolvedor. A mesma versão foi reaberta pelo Launch Services e registrou `AX=true`, sem nova solicitação. Evidência `26-lifecycle-menu.txt`.
- Nova ativação após reabrir passou na medição independente, confirmou as três janelas, o botão da barra dentro da tela e a política `.accessory`, ausente do Dock. Evidências `27-final-after-relaunch-*`.
- `SMAppService.mainApp.status == .enabled` (1), associado ao bundle instalado. Evidência `28-final-diagnostics.json`. Não foi efetuado logout do usuário para testar uma sessão nova.
- Assinatura local válida, `codesign --verify --deep --strict` e SHA-256 final correspondente após todos os testes.

Os logs completos ficam em `~/Library/Logs/ModoDesenvolvedor/`. As falhas da versão anterior e o diagnóstico da autorização antiga foram preservados. Os dois registros de falha da tentativa anterior do usuário também foram preservados. Não foram alteradas configurações de mouse, teclado ou Rectangle; não foram criados atalhos nem integrações com Logi Options+.
