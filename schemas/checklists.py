PK_ITENS = {
    'PK-01': 'Cerâmica/paredes com trincas ou rachaduras visíveis',
    'PK-02': 'Vazamentos em torneiras, vasos sanitários ou infiltração nas paredes',
    'PK-03': 'Verificar presença de água no REL (Reservatório Elevatório) e RAP',
    'PK-04': 'Rede elétrica em pleno funcionamento (tomadas, iluminação, quadro)',
    'PK-05': 'Janelas travando e abrindo corretamente, sem folgas',
    'PK-06': 'Portas e portões em pleno funcionamento (travas, dobradiças, fechaduras)',
    'PK-07': 'Verificar presença de água no interior das caixas de elétrica (condensação/infiltração)',
    'PK-08': 'Nível do extravaso da piscina conforme projeto (evitar alagamento do deck)',
    'PK-09': 'Presença de ferrugem visível em estrutura metálica, gradil, portões ou equipamentos',
    'PK-10': 'Verificar risco à segurança dos moradores: beiradas, quinas, ausência de proteção',
    'PK-11': 'Verificar acúmulo de água nos lotes — regularização conforme: água deve drenar para a frente do lote',
    'PK-12': 'Verificar se áreas comuns e lotes estão abaixo do nível da rua (risco confirmado em 3 condomínios entregues)',
}

SCHEMAS = {
    'lote': {
        'tipo': 'lote',
        'titulo': 'Checklist de Recebimento — Lote',
        'secoes': [
            {
                'titulo': '1. Dimensões e Nivelamento do Lote',
                'itens': [
                    {'nr': '1.1', 'desc': 'Largura do lote conforme projeto (tolerância ±5 cm) — medir com trena', 'foto_se_nc': True},
                    {'nr': '1.2', 'desc': 'Comprimento do lote conforme projeto (tolerância ±5 cm)', 'foto_se_nc': True},
                    {'nr': '1.3', 'desc': 'Área total conforme projeto (tolerância ±1%)', 'foto_se_nc': True},
                    {'nr': '1.4', 'desc': 'Desnível lote/meio-fio dentro do especificado (água drena para frente)', 'foto_se_nc': True},
                    {'nr': '1.5', 'desc': 'Nivelamento do platô — ponto A–B: desvio máximo conforme projeto', 'foto_se_nc': True},
                    {'nr': '1.6', 'desc': 'Nivelamento do platô — ponto A–C: desvio máximo conforme projeto', 'foto_se_nc': True},
                    {'nr': '1.7', 'desc': 'Nivelamento do platô — ponto A–D: desvio máximo conforme projeto', 'foto_se_nc': True},
                    {'nr': '1.8', 'desc': 'Nivelamento do platô — ponto A–E: desvio máximo conforme projeto', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '2. Terraplanagem e Compactação (POP 04)',
                'itens': [
                    {'nr': '2.1', 'desc': 'Superfície do platô regularizada e compactada — sem afundamentos ou saliências', 'foto_se_nc': True},
                    {'nr': '2.2', 'desc': 'Ausência de buracos, valas ou irregularidades na superfície entregue', 'foto_se_nc': True},
                    {'nr': '2.3', 'desc': 'Solo sem material orgânico exposto na superfície (raízes, matéria vegetal)', 'foto_se_nc': True},
                    {'nr': '2.4', 'desc': 'Taludes de divisa estáveis, sem erosão ou desmoronamento visível', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '3. Drenagem Superficial',
                'itens': [
                    {'nr': '3.1', 'desc': 'Caimento da superfície direcionado para a frente do lote (testado visualmente ou com nível)', 'foto_se_nc': True},
                    {'nr': '3.2', 'desc': 'Ausência de pontos de acúmulo de água (empoçamento) — confirmar com água ou após chuva', 'foto_se_nc': True},
                    {'nr': '3.3', 'desc': 'Divisa com lotes vizinhos sem barreira que impeça escoamento natural', 'foto_se_nc': True},
                ]
            },
        ],
        'pk_itens': ['PK-10', 'PK-11', 'PK-12'],
    },

    'pavimentacao': {
        'tipo': 'pavimentacao',
        'titulo': 'Checklist de Recebimento — Pavimentação',
        'secoes': [
            {
                'titulo': '1. Meio-Fio',
                'itens': [
                    {'nr': '1.1', 'desc': 'Alinhamento do meio-fio: desvio máximo ±2 cm — verificar com linha de nylon', 'foto_se_nc': True},
                    {'nr': '1.2', 'desc': 'Nivelamento do topo do meio-fio — sem desníveis abruptos entre peças', 'foto_se_nc': True},
                    {'nr': '1.3', 'desc': 'Altura do espelho (face vertical) conforme projeto', 'foto_se_nc': True},
                    {'nr': '1.4', 'desc': 'Espessura do rejunte entre peças do meio-fio: uniforme e sem falhas', 'foto_se_nc': True},
                    {'nr': '1.5', 'desc': 'Travesseiro de argamassa sob o meio-fio: visível e íntegro nas extremidades', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '2. Paver / Pavimento',
                'itens': [
                    {'nr': '2.1', 'desc': 'Esquadro das fileiras de paver — verificar com linha e esquadro', 'foto_se_nc': True},
                    {'nr': '2.2', 'desc': 'Alinhamento geral do pavimento — sem fileiras tortas', 'foto_se_nc': True},
                    {'nr': '2.3', 'desc': 'Peças sem quebradas, lascadas, manchadas ou invertidas', 'foto_se_nc': True},
                    {'nr': '2.4', 'desc': 'Paginação conforme projeto (padrão espinha de peixe ou outro)', 'foto_se_nc': True},
                    {'nr': '2.5', 'desc': 'Rejunte: preenchimento uniforme com areia fina, sem falhas ou buracos', 'foto_se_nc': True},
                    {'nr': '2.6', 'desc': 'Flecha máxima de ±1 cm medida com régua de 3 m', 'foto_se_nc': True},
                    {'nr': '2.7', 'desc': 'Contenções laterais (sarjetas/bordaduras) instaladas e fixas', 'foto_se_nc': True},
                    {'nr': '2.8', 'desc': 'Pavimento sem afundamentos ou emboçamentos pontuais — percorrer toda a área', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '3. Boulevard (quando aplicável)',
                'itens': [
                    {'nr': '3.1', 'desc': 'Inclinações transversais do canteiro corretas (escoamento correto)', 'foto_se_nc': True},
                    {'nr': '3.2', 'desc': 'Faixa de concreto executada com dimensões corretas', 'foto_se_nc': True},
                    {'nr': '3.3', 'desc': 'Nivelamento das tampas de caixa no canteiro', 'foto_se_nc': True},
                    {'nr': '3.4', 'desc': 'Canaleta instalada e com escoamento funcional', 'foto_se_nc': True},
                    {'nr': '3.5', 'desc': 'Acabamento do concreto: superfície lisa, sem falhas ou segregação', 'foto_se_nc': True},
                    {'nr': '3.6', 'desc': 'Juntas de dilatação executadas nos espaçamentos corretos', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '4. Vagas de Garagem',
                'itens': [
                    {'nr': '4.1', 'desc': 'Seção tipo das vagas conforme projeto (dimensões e nivelamento)', 'foto_se_nc': True},
                    {'nr': '4.2', 'desc': 'Demarcação das vagas conforme projeto (quando prevista)', 'foto_se_nc': True},
                ]
            },
        ],
        'pk_itens': ['PK-09', 'PK-11', 'PK-12'],
    },

    'passeio': {
        'tipo': 'passeio',
        'titulo': 'Checklist de Recebimento — Passeio / Boulevard',
        'secoes': [
            {
                'titulo': '1. Infraestrutura do Passeio',
                'itens': [
                    {'nr': '1.1', 'desc': 'Inclinação transversal do passeio (1–2%) — drenagem para a rua', 'foto_se_nc': True},
                    {'nr': '1.2', 'desc': 'Vala de contenção lateral executada e íntegra', 'foto_se_nc': True},
                    {'nr': '1.3', 'desc': 'Passeio sem afundamentos ou recalques visíveis', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '2. Faixas e Rampas de Veículos',
                'itens': [
                    {'nr': '2.1', 'desc': 'Faixa de serviço executada com largura correta', 'foto_se_nc': True},
                    {'nr': '2.2', 'desc': 'Rampa de veículos: largura conforme projeto', 'foto_se_nc': True},
                    {'nr': '2.3', 'desc': 'Travamento da rampa no meio-fio: sem folgas ou deslocamento', 'foto_se_nc': True},
                    {'nr': '2.4', 'desc': 'Superfície da rampa: sem trincas, segregação ou falhas visíveis', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '3. Rampa de Acessibilidade',
                'itens': [
                    {'nr': '3.1', 'desc': 'Acabamento da rampa: superfície antiderrapante e sem falhas', 'foto_se_nc': True},
                    {'nr': '3.2', 'desc': 'Inclinação da rampa dentro do limite da NBR 9050 (máx 8,33%)', 'foto_se_nc': True},
                    {'nr': '3.3', 'desc': 'Rampa sem trincas, lascas ou desplacamento', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '4. Caixas e Tampas',
                'itens': [
                    {'nr': '4.1', 'desc': 'Caixa de hidrômetro: nivelamento com o piso do passeio', 'foto_se_nc': True},
                    {'nr': '4.2', 'desc': 'Caixa de hidrômetro: vedação das tubulações de entrada e saída', 'foto_se_nc': True},
                    {'nr': '4.3', 'desc': 'Tampa de caixa de inspeção: nivelamento com o passeio', 'foto_se_nc': True},
                    {'nr': '4.4', 'desc': 'Janelas da caixa coletora: abertas/instaladas conforme projeto', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '5. Acabamento Geral',
                'itens': [
                    {'nr': '5.1', 'desc': 'Plurigoma ou paginação conforme projeto', 'foto_se_nc': True},
                    {'nr': '5.2', 'desc': 'Rejunte sem vazios — preenchimento uniforme', 'foto_se_nc': True},
                    {'nr': '5.3', 'desc': 'Juntas de dilatação nos espaçamentos corretos', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '6. Passeio Pós-Casa (marcar NA se pré-casa)',
                'itens': [
                    {'nr': '6.1', 'desc': 'Locação da rampa de veículos conforme abertura do portão', 'foto_se_nc': True},
                    {'nr': '6.2', 'desc': 'Travamento no meio-fio: sem deslocamento ou folgas', 'foto_se_nc': True},
                    {'nr': '6.3', 'desc': 'Abertura das janelas da caixa coletora executada', 'foto_se_nc': True},
                ]
            },
        ],
        'pk_itens': ['PK-09', 'PK-10', 'PK-12'],
    },

    'saa': {
        'tipo': 'saa',
        'titulo': 'Checklist de Recebimento — Sistema de Abastecimento de Água',
        'secoes': [
            {
                'titulo': '1. Documentação e Teste de Estanqueidade',
                'itens': [
                    {'nr': '1.1', 'desc': 'Laudo do teste de estanqueidade disponível: pressão de teste, duração e resultado registrados', 'foto_se_nc': True},
                    {'nr': '1.2', 'desc': 'Diâmetro e material da tubulação conformes ao projeto (verificar via nota fiscal ou as-built)', 'foto_se_nc': True},
                    {'nr': '1.3', 'desc': 'As-built da rede entregue pelo empreiteiro', 'foto_se_nc': False},
                ]
            },
            {
                'titulo': '2. Superfície e Reaterro',
                'itens': [
                    {'nr': '2.1', 'desc': 'Superfície sobre a vala recomposta: sem afundamentos, recalques ou emboçamentos visíveis', 'foto_se_nc': True},
                    {'nr': '2.2', 'desc': 'Tampas das caixas de registro: niveladas com o passeio/pavimento, sem danos', 'foto_se_nc': True},
                    {'nr': '2.3', 'desc': 'Ausência de vazamentos visíveis na superfície ou nas caixas de registro acessíveis', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '3. Teste Funcional',
                'itens': [
                    {'nr': '3.1', 'desc': 'Abrir registros e verificar fluxo de água nos pontos de saída da rede', 'foto_se_nc': True},
                    {'nr': '3.2', 'desc': 'Pressão de saída compatível com o projeto em pontos extremos da rede', 'foto_se_nc': True},
                    {'nr': '3.3', 'desc': 'Ausência de vazamentos audíveis ou bolsões de umidade na superfície', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '4. Reservatório e Elevatória (marcar NA quando não aplicável)',
                'itens': [
                    {'nr': '4.1', 'desc': 'Locação do reservatório/elevatória conforme projeto (proj. SAA-03 a SAA-06)', 'foto_se_nc': True},
                    {'nr': '4.2', 'desc': 'Estrutura sem trincas, recalques ou deformações visíveis', 'foto_se_nc': True},
                    {'nr': '4.3', 'desc': 'Nível operacional da água conforme projeto', 'foto_se_nc': True},
                    {'nr': '4.4', 'desc': 'Equipamentos (bombas, válvulas, registros) instalados e funcionando', 'foto_se_nc': True},
                    {'nr': '4.5', 'desc': 'Caixa ou poço de visita da elevatória acessível e sem infiltração', 'foto_se_nc': True},
                ]
            },
        ],
        'pk_itens': ['PK-03', 'PK-08', 'PK-09'],
    },

    'drenagem': {
        'tipo': 'drenagem',
        'titulo': 'Checklist de Recebimento — Sistema de Drenagem',
        'secoes': [
            {
                'titulo': '1. Superfície e Reaterro',
                'itens': [
                    {'nr': '1.1', 'desc': 'Superfície sobre a vala recomposta: sem afundamentos, recalques ou emboçamentos visíveis', 'foto_se_nc': True},
                    {'nr': '1.2', 'desc': 'Ausência de pontos de acúmulo de água sobre a área da vala', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '2. Pontos de Captação',
                'itens': [
                    {'nr': '2.1', 'desc': 'Grelhas instaladas, niveladas com o pavimento e sem danos', 'foto_se_nc': True},
                    {'nr': '2.2', 'desc': 'Bocas de lobo: nivelamento e condição estrutural', 'foto_se_nc': True},
                    {'nr': '2.3', 'desc': 'Tampas das caixas de inspeção: niveladas e sem danos', 'foto_se_nc': True},
                    {'nr': '2.4', 'desc': 'Escoamento funcional verificado (teste com água)', 'foto_se_nc': True},
                    {'nr': '2.5', 'desc': 'Ausência de entupimentos: água não retorna ou extravasa nos pontos de captação', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '3. Documentação',
                'itens': [
                    {'nr': '3.1', 'desc': 'Diâmetro e material da tubulação conformes ao projeto (verificar via nota fiscal ou as-built)', 'foto_se_nc': True},
                    {'nr': '3.2', 'desc': 'As-built da rede entregue pelo empreiteiro', 'foto_se_nc': False},
                ]
            },
        ],
        'pk_itens': ['PK-09', 'PK-11', 'PK-12'],
    },

    'ses': {
        'tipo': 'ses',
        'titulo': 'Checklist de Recebimento — Sistema de Esgotamento Sanitário',
        'secoes': [
            {
                'titulo': 'A.1. Rede Coletora — Superfície e Documentação',
                'itens': [
                    {'nr': 'A.1.1', 'desc': 'Superfície sobre a vala recomposta: sem afundamentos, recalques ou emboçamentos visíveis', 'foto_se_nc': True},
                    {'nr': 'A.1.2', 'desc': 'Diâmetro e material da tubulação conformes ao projeto (verificar via nota fiscal ou as-built)', 'foto_se_nc': True},
                    {'nr': 'A.1.3', 'desc': 'As-built da rede coletora entregue pelo empreiteiro', 'foto_se_nc': False},
                ]
            },
            {
                'titulo': 'A.2. Rede Coletora — Teste Funcional',
                'itens': [
                    {'nr': 'A.2.1', 'desc': 'Esgoto flui livremente até as caixas de inspeção — sem refluxo ou obstrução', 'foto_se_nc': True},
                    {'nr': 'A.2.2', 'desc': 'Ausência de odor excessivo indicando obstrução ou tampa aberta', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': 'B.3. Caixa de Inspeção',
                'itens': [
                    {'nr': 'B.3.1', 'desc': 'Janelas do anel: posicionamento com tolerância ±3 cm', 'foto_se_nc': True},
                    {'nr': 'B.3.2', 'desc': 'Anéis acima do terreno conforme projeto', 'foto_se_nc': True},
                    {'nr': 'B.3.3', 'desc': 'Chumbamento da tubulação e piso chanfrado executados (verificar abrindo a tampa)', 'foto_se_nc': True},
                    {'nr': 'B.3.4', 'desc': 'Tampa instalada: nivelada, sem folgas e sem danos', 'foto_se_nc': True},
                    {'nr': 'B.3.5', 'desc': 'Superfície ao redor da caixa recomposta sem recalques', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': 'B.4. Poço de Visita',
                'itens': [
                    {'nr': 'B.4.1', 'desc': 'Alvenaria maciça: prumo e condição visível sem trincas ou deslocamentos', 'foto_se_nc': True},
                    {'nr': 'B.4.2', 'desc': 'Chapisco + revestimento interno executados e íntegros', 'foto_se_nc': True},
                    {'nr': 'B.4.3', 'desc': 'Chumbamento das tubulações no poço sem folgas ou infiltração aparente', 'foto_se_nc': True},
                    {'nr': 'B.4.4', 'desc': 'Anéis pré-moldados assentados e alinhados', 'foto_se_nc': True},
                    {'nr': 'B.4.5', 'desc': 'Tampa do poço: nivelada, sem folgas e sem danos', 'foto_se_nc': True},
                    {'nr': 'B.4.6', 'desc': 'Superfície ao redor do poço recomposta sem afundamentos', 'foto_se_nc': True},
                ]
            },
        ],
        'pk_itens': ['PK-02', 'PK-09'],
    },

    'guarita': {
        'tipo': 'guarita',
        'titulo': 'Checklist de Recebimento — Guarita',
        'secoes': [
            {
                'titulo': '1. Estrutura e Fundação',
                'itens': [
                    {'nr': '1.1', 'desc': 'Ausência de sinais de recalque, trinca ou deformação estrutural visível', 'foto_se_nc': True},
                    {'nr': '1.2', 'desc': 'Vigas baldrame sem trincas, fissuras ou falhas onde expostas', 'foto_se_nc': True},
                    {'nr': '1.3', 'desc': 'Escada com 5 degraus: altura do 1º degrau 18 cm em relação ao passeio', 'foto_se_nc': True},
                    {'nr': '1.4', 'desc': 'Dimensões dos degraus dentro da tolerância (espelho e patamar)', 'foto_se_nc': True},
                    {'nr': '1.5', 'desc': 'Corrimão instalado, fixo, sem folgas e com acabamento conforme projeto', 'foto_se_nc': True},
                    {'nr': '1.6', 'desc': 'Contrapiso com nivelamento e planeza conformes ao projeto', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '2. Alvenaria e Vedação',
                'itens': [
                    {'nr': '2.1', 'desc': 'Paredes em prumo e alinhamento — verificado com nível em todas as vistas', 'foto_se_nc': True},
                    {'nr': '2.2', 'desc': 'Paredes sem trincas, fissuras, manchas ou eflorescências', 'foto_se_nc': True},
                    {'nr': '2.3', 'desc': 'Esperas hidrossanitárias (pontos de saída) vedadas e tamponadas', 'foto_se_nc': True},
                    {'nr': '2.4', 'desc': 'Pontos elétricos finalizados nas posições corretas conforme projeto', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '3. Revestimentos e Acabamentos',
                'itens': [
                    {'nr': '3.1', 'desc': 'PISO — Dunas Bege 46×46 Cerbras: sem peças quebradas, lascadas ou manchadas', 'foto_se_nc': True},
                    {'nr': '3.2', 'desc': 'PISO — Nivelado com caimento correto para os ralos, sem empoçamento', 'foto_se_nc': True},
                    {'nr': '3.3', 'desc': 'PISO — Rejunte Cinza Platina 4 mm: sem buracos ou falhas', 'foto_se_nc': True},
                    {'nr': '3.4', 'desc': 'PISO — Aderência: som sem oco ao percutir com cabo de vassoura', 'foto_se_nc': True},
                    {'nr': '3.5', 'desc': 'RODAPÉ — 7 cm instalado em todos os ambientes sem cerâmica do piso ao teto', 'foto_se_nc': True},
                    {'nr': '3.6', 'desc': 'PAREDE BWC — Cerâmica Dunas Bege até altura especificada, sem peças quebradas', 'foto_se_nc': True},
                    {'nr': '3.7', 'desc': 'PAREDE outros ambientes — Emassada e pintada: superfície lisa, sem bolhas ou descascamentos', 'foto_se_nc': True},
                    {'nr': '3.8', 'desc': 'FORRO PVC — Instalado, alinhado, sem folgas e limpo em todos os ambientes', 'foto_se_nc': True},
                    {'nr': '3.9', 'desc': 'SOLEIRAS — Granito Verde Ubatuba: niveladas e com rejunte correto', 'foto_se_nc': True},
                    {'nr': '3.10', 'desc': 'PEITORIS — Granito com engaste de 2 cm, declividade para exterior e rejunte íntegro', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '4. Esquadrias — Portas e Janelas',
                'itens': [
                    {'nr': '4.1', 'desc': 'Todas as portas instaladas: folhas, marcos e ferragens presentes', 'foto_se_nc': True},
                    {'nr': '4.2', 'desc': 'Portas abrindo e fechando sem travamento, com folga perimetral adequada', 'foto_se_nc': True},
                    {'nr': '4.3', 'desc': 'Fechaduras e trincos funcionando — todas as chaves entregues', 'foto_se_nc': True},
                    {'nr': '4.4', 'desc': 'Janelas instaladas, abrindo e fechando corretamente, sem deformações', 'foto_se_nc': True},
                    {'nr': '4.5', 'desc': 'Vedação entre esquadria e alvenaria (silicone/massa) sem falhas', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '5. Instalações Hidráulicas e Sanitárias',
                'itens': [
                    {'nr': '5.1', 'desc': 'BWC — Bacia sanitária instalada e fixada; caixa acoplada com acionamento duplo', 'foto_se_nc': True},
                    {'nr': '5.2', 'desc': 'BWC — Lavatório suspenso (39×29×16,5 cm) instalado, fixo e sem folgas', 'foto_se_nc': True},
                    {'nr': '5.3', 'desc': 'BWC — Torneira cromada com aerador: operante, sem vazamento', 'foto_se_nc': True},
                    {'nr': '5.4', 'desc': 'BWC — Chuveiro (4.500W/220V): instalado e sem vazamento nas conexões', 'foto_se_nc': True},
                    {'nr': '5.5', 'desc': 'BWC — Ralo sifonado instalado, limpo e com escoamento correto', 'foto_se_nc': True},
                    {'nr': '5.6', 'desc': 'ZELADORIA — Tanque suspenso em resina (60×60 cm): instalado e sem danos', 'foto_se_nc': True},
                    {'nr': '5.7', 'desc': 'ZELADORIA — Torneira com bica móvel e aerador: sem vazamentos', 'foto_se_nc': True},
                    {'nr': '5.8', 'desc': 'ZELADORIA — Ralo sifonado com escoamento correto', 'foto_se_nc': True},
                    {'nr': '5.9', 'desc': 'Caixas de inspeção: acessíveis, com piso chanfrado e meia-cana íntegros', 'foto_se_nc': True},
                    {'nr': '5.10', 'desc': 'Tubulações pluviais com escoamento correto até a saída (calhas e saídas visíveis)', 'foto_se_nc': True},
                    {'nr': '5.11', 'desc': 'Escoamento sanitário correto nas caixas de inspeção (teste funcional)', 'foto_se_nc': True},
                    {'nr': '5.12', 'desc': 'TESTE DE ESTANQUEIDADE: todos os pontos abertos — sem vazamentos por 5 min', 'foto_se_nc': True},
                    {'nr': '5.13', 'desc': 'TESTE DE DESCARGA: vaso descarrega completamente sem transbordar', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '6. Instalações Elétricas',
                'itens': [
                    {'nr': '6.1', 'desc': 'Pontos elétricos nas posições corretas conforme projeto', 'foto_se_nc': True},
                    {'nr': '6.2', 'desc': 'Tomadas instaladas, protegidas e energizadas (testar com testador)', 'foto_se_nc': True},
                    {'nr': '6.3', 'desc': 'Interruptores acionando a iluminação corretamente', 'foto_se_nc': True},
                    {'nr': '6.4', 'desc': 'Iluminação funcionando em todos os ambientes', 'foto_se_nc': True},
                    {'nr': '6.5', 'desc': 'Quadro de distribuição instalado, identificado e com disjuntores corretos', 'foto_se_nc': True},
                    {'nr': '6.6', 'desc': 'Aterramento verificado por teste funcional com equipamento adequado', 'foto_se_nc': True},
                    {'nr': '6.7', 'desc': 'Ausência de cabos expostos, emendas improvisadas ou conexões sem proteção', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '7. Cobertura',
                'itens': [
                    {'nr': '7.1', 'desc': 'Telhado sem telhas quebradas, deslocadas, furadas ou invertidas', 'foto_se_nc': True},
                    {'nr': '7.2', 'desc': 'Transpasse e alinhamento das telhas conforme especificação', 'foto_se_nc': True},
                    {'nr': '7.3', 'desc': 'Calhas e rufos instalados sem danos, com caimento e escoamento corretos', 'foto_se_nc': True},
                    {'nr': '7.4', 'desc': 'Estrutura de suporte da cobertura sem oxidação, deformações ou folgas', 'foto_se_nc': True},
                    {'nr': '7.5', 'desc': 'Ausência de infiltrações no teto interno (verificar após chuva ou teste)', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '8. Inspeção Geral e Documentação',
                'itens': [
                    {'nr': '8.1', 'desc': 'Local entregue limpo, sem entulho ou equipamentos da obra', 'foto_se_nc': True},
                    {'nr': '8.2', 'desc': 'Área externa (calçada/passeio) limpa e sem danos causados pela obra', 'foto_se_nc': True},
                    {'nr': '8.3', 'desc': 'Todas as chaves entregues (portas, cadeados, etc.)', 'foto_se_nc': False},
                    {'nr': '8.4', 'desc': 'Documentação disponível: ART/RRT, memoriais, projetos as-built', 'foto_se_nc': False},
                    {'nr': '8.5', 'desc': 'Fotos do estado final de todos os ambientes registradas', 'foto_se_nc': True},
                    {'nr': '8.6', 'desc': 'Manual de uso/manutenção dos equipamentos entregue', 'foto_se_nc': False},
                    {'nr': '8.7', 'desc': 'Ausência de serviços incompletos ou materiais inacabados', 'foto_se_nc': True},
                ]
            },
        ],
        'pk_itens': ['PK-01', 'PK-02', 'PK-04', 'PK-05', 'PK-06', 'PK-07', 'PK-09', 'PK-10'],
    },

    'quiosque': {
        'tipo': 'quiosque',
        'titulo': 'Checklist de Recebimento — Quiosques',
        'secoes': [
            {
                'titulo': '1. Estrutura e Fundação — Radier',
                'itens': [
                    {'nr': '1.1', 'desc': 'Radier e sapatas sem sinais de recalque, trinca, fissura ou deslocamento visível', 'foto_se_nc': True},
                    {'nr': '1.2', 'desc': 'Dimensões e esquadro do radier conformes ao projeto — sem desvios visíveis', 'foto_se_nc': True},
                    {'nr': '1.3', 'desc': 'Nível do piso do quiosque alinhado com o passeio externo (exigência do projeto)', 'foto_se_nc': True},
                    {'nr': '1.4', 'desc': 'Engaste lateral do radier e vala de contenção para pó de pedra íntegros', 'foto_se_nc': True},
                    {'nr': '1.5', 'desc': 'Caixa de gordura: instalada, acessível e com piso chanfrado + meia-cana íntegros', 'foto_se_nc': True},
                    {'nr': '1.6', 'desc': 'Caixas de inspeção/passagem: instaladas, acessíveis e sem danos', 'foto_se_nc': True},
                    {'nr': '1.7', 'desc': 'Ralos sifonados (2 por quiosque), nivelados com o piso e com escoamento livre', 'foto_se_nc': True},
                    {'nr': '1.8', 'desc': 'Caimento do piso para os ralos (mínimo 1%) — sem empoçamento', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '2. Alvenaria e Vedação',
                'itens': [
                    {'nr': '2.1', 'desc': 'Paredes em prumo e alinhamento — verificar com nível (vistas AA, BB e lateral)', 'foto_se_nc': True},
                    {'nr': '2.2', 'desc': 'Paredes sem trincas, fissuras, manchas ou eflorescências', 'foto_se_nc': True},
                    {'nr': '2.3', 'desc': 'Esperas hidrossanitárias (pontos de saída) vedadas e tamponadas', 'foto_se_nc': True},
                    {'nr': '2.4', 'desc': 'Pontos elétricos finalizados nas posições corretas conforme projeto', 'foto_se_nc': True},
                    {'nr': '2.5', 'desc': 'Impermeabilização do piso verificada: ausência de infiltração (teste funcional)', 'foto_se_nc': True},
                    {'nr': '2.6', 'desc': 'Ausência de umidade ou manchas nas paredes internas', 'foto_se_nc': True},
                    {'nr': '2.7', 'desc': 'Shafts (moldura de isopor): instalados e íntegros, sem danos ou desprendimentos', 'foto_se_nc': True},
                    {'nr': '2.8', 'desc': 'Altura final das paredes até a cinta de respaldo conforme projeto (+ 1 cm tolerância)', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '3. Cobertura Metálica',
                'itens': [
                    {'nr': '3.1', 'desc': 'Treliças metálicas fixadas nos pilares com chapa de ligação e parabolt — sem folgas', 'foto_se_nc': True},
                    {'nr': '3.2', 'desc': 'Estrutura metálica alinhada e locada conforme projeto — sem deformações', 'foto_se_nc': True},
                    {'nr': '3.3', 'desc': 'Perfis e chapas metálicas fixados corretamente, sem peças soltas ou faltando', 'foto_se_nc': True},
                    {'nr': '3.4', 'desc': 'Telhas sem furos, quebras ou inversões: transpasse e alinhamento corretos', 'foto_se_nc': True},
                    {'nr': '3.5', 'desc': 'Encaixe das telhas sem folgas ou pontos de entrada de água', 'foto_se_nc': True},
                    {'nr': '3.6', 'desc': 'Estrutura metálica sem oxidação ou corrosão visível', 'foto_se_nc': True},
                    {'nr': '3.7', 'desc': 'Ausência de infiltrações na cobertura (verificar após chuva ou testar com mangueira)', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '4. Revestimentos e Acabamentos',
                'itens': [
                    {'nr': '4.1', 'desc': 'PISO — Araripe Cinza 46×46 Cerbras: sem peças quebradas, lascadas ou manchadas', 'foto_se_nc': True},
                    {'nr': '4.2', 'desc': 'PISO — Rejunte Cinza Platina 4 mm: sem falhas, buracos ou trincas', 'foto_se_nc': True},
                    {'nr': '4.3', 'desc': 'PISO — Aderência: som sem oco ao percutir com cabo de vassoura', 'foto_se_nc': True},
                    {'nr': '4.4', 'desc': 'RODAPÉ 7 cm: instalado onde não há cerâmica do piso ao teto — íntegro e rejuntado', 'foto_se_nc': True},
                    {'nr': '4.5', 'desc': 'PAREDE INTERNA — Nord Gray 37×59 Arielle: sem peças quebradas; rejunte Cinza Platina 5 mm', 'foto_se_nc': True},
                    {'nr': '4.6', 'desc': 'PAREDE INTERNA — Aderência (percutir) e planeza: sem som oco', 'foto_se_nc': True},
                    {'nr': '4.7', 'desc': 'FACHADA — Pilares e shafts: textura Bahamas Cheio (834A0D) uniforme', 'foto_se_nc': True},
                    {'nr': '4.8', 'desc': 'FACHADA — Paredes: textura Bahamas Claro (834A0L) uniforme', 'foto_se_nc': True},
                    {'nr': '4.9', 'desc': 'LATERAL DO RADIER: textura Bahamas Cheio (834A0D) sem falhas', 'foto_se_nc': True},
                    {'nr': '4.10', 'desc': 'CANTONEIRAS do balcão: altura, nível e esquadro dentro de ±0,2 cm', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '5. Bancada, Churrasqueira e Elementos Especiais',
                'itens': [
                    {'nr': '5.1', 'desc': 'BANCADA Granito Verde Ubatuba (200×50 cm): instalada, nivelada, fixada e sem lascas ou trincas', 'foto_se_nc': True},
                    {'nr': '5.2', 'desc': 'CUBA embutir aço polido (40×34×14,5 cm): assentada, vedada e sem danos', 'foto_se_nc': True},
                    {'nr': '5.3', 'desc': 'BALCÃO RESINADO: instalado, fixo e alinhado conforme projeto', 'foto_se_nc': True},
                    {'nr': '5.4', 'desc': 'CHURRASQUEIRA pré-moldada (2,20×0,65×0,43 m): instalada, fixada e chaminé íntegra', 'foto_se_nc': True},
                    {'nr': '5.5', 'desc': 'Rejunte/vedação da bancada e cuba: sem folgas que permitam infiltração', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '6. Instalações Hidráulicas',
                'itens': [
                    {'nr': '6.1', 'desc': 'Torneira cromada (bica móvel + aerador): instalada, funcionando e sem vazamentos', 'foto_se_nc': True},
                    {'nr': '6.2', 'desc': 'Sifão instalado com abraçadeira plástica — conexão estanque, sem gotejamento', 'foto_se_nc': True},
                    {'nr': '6.3', 'desc': 'Nivelamento da torneira com a cerâmica dentro da tolerância do projeto', 'foto_se_nc': True},
                    {'nr': '6.4', 'desc': 'Ralos sifonados com escoamento livre e tampa corretamente posicionada', 'foto_se_nc': True},
                    {'nr': '6.5', 'desc': 'Caixa de gordura: sem empoçamento ou entupimento — escoamento correto', 'foto_se_nc': True},
                    {'nr': '6.6', 'desc': 'TESTE FUNCIONAL: abrir torneira, verificar pressão, escoamento e ausência de vazamentos por 5 min', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '7. Instalações Elétricas e Iluminação',
                'itens': [
                    {'nr': '7.1', 'desc': 'TOMADA DUPLA: instalada, energizada e funcionando (testar com testador)', 'foto_se_nc': True},
                    {'nr': '7.2', 'desc': 'TOMADA SIMPLES: instalada, energizada e funcionando', 'foto_se_nc': True},
                    {'nr': '7.3', 'desc': 'INTERRUPTOR: instalado e operando corretamente', 'foto_se_nc': True},
                    {'nr': '7.4', 'desc': 'REFLETOR Holofote LED 50W 4000K (4 unid.): instalados, alinhados e funcionando', 'foto_se_nc': True},
                    {'nr': '7.5', 'desc': 'TRILHO ELETRIF. c/ 3 spots pretos 1 m (2 unid.): instalados e funcionando', 'foto_se_nc': True},
                    {'nr': '7.6', 'desc': 'Aterramento verificado por teste funcional com equipamento adequado', 'foto_se_nc': True},
                    {'nr': '7.7', 'desc': 'Ausência de cabos expostos, emendas improvisadas ou conexões sem proteção', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '8. Inspeção Geral e Documentação',
                'itens': [
                    {'nr': '8.1', 'desc': 'Quiosques entregues limpos, sem entulho ou materiais de construção', 'foto_se_nc': True},
                    {'nr': '8.2', 'desc': 'Área externa (passeio) limpa, sem danos e nivelada com o piso interno', 'foto_se_nc': True},
                    {'nr': '8.3', 'desc': 'Documentação disponível: ART/RRT, memoriais, projetos as-built', 'foto_se_nc': False},
                    {'nr': '8.4', 'desc': 'Fotos do estado final de cada quiosque registradas (obrigatório)', 'foto_se_nc': True},
                    {'nr': '8.5', 'desc': 'Manual de uso/manutenção entregue (torneiras, churrasqueira, luminárias)', 'foto_se_nc': False},
                    {'nr': '8.6', 'desc': 'Ausência de serviços incompletos ou materiais inacabados', 'foto_se_nc': True},
                ]
            },
        ],
        'pk_itens': ['PK-01', 'PK-02', 'PK-04', 'PK-05', 'PK-06', 'PK-07', 'PK-09', 'PK-10'],
    },

    'dep_lixo': {
        'tipo': 'dep_lixo',
        'titulo': 'Checklist de Recebimento — Depósito de Lixo',
        'secoes': [
            {
                'titulo': '1. Estrutura e Fundação — Radier',
                'itens': [
                    {'nr': '1.1', 'desc': 'Radier sem sinais de recalque, trinca, fissura ou deslocamento visível', 'foto_se_nc': True},
                    {'nr': '1.2', 'desc': 'Dimensões e esquadro do radier conformes ao projeto — sem desvios visíveis', 'foto_se_nc': True},
                    {'nr': '1.3', 'desc': 'Nível do piso alinhado com os passeios externo e interno', 'foto_se_nc': True},
                    {'nr': '1.4', 'desc': 'Engaste lateral do radier e vala de contenção para pó de pedra íntegros', 'foto_se_nc': True},
                    {'nr': '1.5', 'desc': 'Caixa sifonada instalada, acessível e com escoamento correto (ralo com grelha de alumínio)', 'foto_se_nc': True},
                    {'nr': '1.6', 'desc': 'Caimento do piso para o ralo — sem empoçamento (mínimo 1%)', 'foto_se_nc': True},
                    {'nr': '1.7', 'desc': 'Escoamento sanitário e pluvial correto — verificado via caixas de inspeção (teste funcional)', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '2. Alvenaria e Vedação',
                'itens': [
                    {'nr': '2.1', 'desc': 'Paredes em prumo e alinhamento — verificar nas 4 vistas com nível e prumo', 'foto_se_nc': True},
                    {'nr': '2.2', 'desc': 'Paredes sem trincas, fissuras, manchas ou eflorescências', 'foto_se_nc': True},
                    {'nr': '2.3', 'desc': 'Aberturas das 2 portas com dimensões corretas e sem danos', 'foto_se_nc': True},
                    {'nr': '2.4', 'desc': 'Esperas hidrossanitárias e elétricas (pontos de saída) vedadas corretamente', 'foto_se_nc': True},
                    {'nr': '2.5', 'desc': 'Impermeabilização do piso verificada: ausência de infiltração (teste funcional com água)', 'foto_se_nc': True},
                    {'nr': '2.6', 'desc': 'Ausência de umidade, manchas ou eflorescência nas paredes internas', 'foto_se_nc': True},
                    {'nr': '2.7', 'desc': 'Altura final das paredes conforme projeto — sem desvios superiores a 1 cm', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '3. Cobertura — Telha de Fibrocimento + Estrutura Metálica',
                'itens': [
                    {'nr': '3.1', 'desc': 'Treliças metálicas fixadas nos pilares com chapa de ligação e parabolt — sem folgas', 'foto_se_nc': True},
                    {'nr': '3.2', 'desc': 'Estrutura metálica alinhada e locada conforme projeto — sem deformações ou oxidação', 'foto_se_nc': True},
                    {'nr': '3.3', 'desc': 'Perfis e chapas fixados corretamente, sem peças soltas ou faltando', 'foto_se_nc': True},
                    {'nr': '3.4', 'desc': 'Telhas de fibrocimento sem trincas, quebras, furos ou inversões', 'foto_se_nc': True},
                    {'nr': '3.5', 'desc': 'Transpasse e alinhamento das telhas corretos — sem pontos de entrada de água', 'foto_se_nc': True},
                    {'nr': '3.6', 'desc': 'Ausência de infiltrações (verificar teto interno após chuva ou teste com mangueira)', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '4. Revestimentos e Acabamentos',
                'itens': [
                    {'nr': '4.1', 'desc': 'PISO — Dunas Bege 46×46 Cerbras: sem peças quebradas, lascadas ou manchadas', 'foto_se_nc': True},
                    {'nr': '4.2', 'desc': 'PISO — Nivelado com caimento correto para o ralo — sem empoçamento', 'foto_se_nc': True},
                    {'nr': '4.3', 'desc': 'PISO — Rejunte Cinza Platina 2 mm: sem falhas ou buracos', 'foto_se_nc': True},
                    {'nr': '4.4', 'desc': 'PISO — Aderência: percutir com cabo de vassoura — sem som oco', 'foto_se_nc': True},
                    {'nr': '4.5', 'desc': 'PAREDE INTERNA — Dunas Bege 46×46 Cerbras: sem peças quebradas ou mal assentadas', 'foto_se_nc': True},
                    {'nr': '4.6', 'desc': 'PAREDE INTERNA — Rejunte Cinza Platina 2 mm: sem falhas, buracos ou trincas', 'foto_se_nc': True},
                    {'nr': '4.7', 'desc': 'PAREDE INTERNA — Aderência: percutir — sem som oco', 'foto_se_nc': True},
                    {'nr': '4.8', 'desc': 'FACHADA EXTERNA — Textura Bahamas Claro (834A0L): uniforme nas 4 fachadas', 'foto_se_nc': True},
                    {'nr': '4.9', 'desc': 'EMBOÇO externo — planeza e acabamento: desvio máximo de 2 mm', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '5. Esquadrias — Portas',
                'itens': [
                    {'nr': '5.1', 'desc': 'Porta de entrada: instalada em prumo, abrindo e fechando sem travamento', 'foto_se_nc': True},
                    {'nr': '5.2', 'desc': 'Porta secundária: instalada em prumo, abrindo e fechando sem travamento', 'foto_se_nc': True},
                    {'nr': '5.3', 'desc': 'Ferragens (dobradiças, fechaduras, trincos): instaladas e funcionando — chaves entregues', 'foto_se_nc': True},
                    {'nr': '5.4', 'desc': 'Vedação entre marcos e alvenaria sem falhas ou aberturas', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '6. Instalações Hidráulicas',
                'itens': [
                    {'nr': '6.1', 'desc': 'TORNEIRA tipo jardim de parede em inox: instalada, funcionando e sem vazamentos', 'foto_se_nc': True},
                    {'nr': '6.2', 'desc': 'Ralo com grelha de alumínio: instalado, nivelado com o piso e com escoamento livre', 'foto_se_nc': True},
                    {'nr': '6.3', 'desc': 'Tubulação de abastecimento: sem vazamentos e com pressão adequada', 'foto_se_nc': True},
                    {'nr': '6.4', 'desc': 'Escoamento do esgoto livre e sem entupimento (verificar funcionalmente)', 'foto_se_nc': True},
                    {'nr': '6.5', 'desc': 'TESTE FUNCIONAL: abrir torneira, verificar pressão, escoamento e ausência de vazamentos', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '7. Instalações Elétricas',
                'itens': [
                    {'nr': '7.1', 'desc': 'Interruptor instalado e funcionando', 'foto_se_nc': True},
                    {'nr': '7.2', 'desc': 'Tomada simples instalada, energizada e funcionando (testar)', 'foto_se_nc': True},
                    {'nr': '7.3', 'desc': 'Pontos de espera para câmeras de segurança nas posições corretas', 'foto_se_nc': True},
                    {'nr': '7.4', 'desc': 'Iluminação instalada e funcionando', 'foto_se_nc': True},
                    {'nr': '7.5', 'desc': 'Ausência de cabos expostos ou conexões sem proteção', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '8. Equipamentos e Inspeção Geral',
                'itens': [
                    {'nr': '8.1', 'desc': 'CONTAINER DE LIXO 1200L com tampa bipartida (LC 2,00×1,00 m): instalado e sem danos', 'foto_se_nc': True},
                    {'nr': '8.2', 'desc': 'Container posicionado corretamente — acesso sem obstrução', 'foto_se_nc': True},
                    {'nr': '8.3', 'desc': 'Depósito entregue limpo, sem entulho ou materiais de construção', 'foto_se_nc': True},
                    {'nr': '8.4', 'desc': 'Passeios externos e internos limpos, sem danos e nivelados', 'foto_se_nc': True},
                    {'nr': '8.5', 'desc': 'Documentação disponível: ART/RRT, memoriais, projetos as-built', 'foto_se_nc': False},
                    {'nr': '8.6', 'desc': 'Fotos do estado final registradas (obrigatório)', 'foto_se_nc': True},
                    {'nr': '8.7', 'desc': 'Ausência de serviços incompletos ou materiais inacabados', 'foto_se_nc': True},
                ]
            },
        ],
        'pk_itens': ['PK-01', 'PK-06', 'PK-09', 'PK-10'],
    },

    'deck': {
        'tipo': 'deck',
        'titulo': 'Checklist de Recebimento — Deck da Piscina',
        'secoes': [
            {
                'titulo': '1. Estrutura e Fundação — Radier',
                'itens': [
                    {'nr': '1.1', 'desc': 'Radier sem sinais de recalque, trinca, fissura ou deslocamento', 'foto_se_nc': True},
                    {'nr': '1.2', 'desc': 'Dimensões e esquadro do radier conformes ao projeto', 'foto_se_nc': True},
                    {'nr': '1.3', 'desc': 'Engaste lateral e vala de contenção para pó de pedra íntegros', 'foto_se_nc': True},
                    {'nr': '1.4', 'desc': 'Caixas sifonadas instaladas, acessíveis e com escoamento livre', 'foto_se_nc': True},
                    {'nr': '1.5', 'desc': 'Caimento do radier para os ralos: mínimo 1% — sem empoçamento', 'foto_se_nc': True},
                    {'nr': '1.6', 'desc': 'Escoamento de esgoto e pluvial verificado: livre e sem entupimento (teste funcional)', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '2. Alvenaria — Chuveirão',
                'itens': [
                    {'nr': '2.1', 'desc': 'Alvenaria do chuveirão em prumo e alinhamento — verificar com nível', 'foto_se_nc': True},
                    {'nr': '2.2', 'desc': 'Paredes sem trincas, fissuras ou manchas', 'foto_se_nc': True},
                    {'nr': '2.3', 'desc': 'Impermeabilização do piso do deck verificada: ausência de infiltração (teste funcional com água)', 'foto_se_nc': True},
                    {'nr': '2.4', 'desc': 'Emboço interno e externo com planeza máxima de 2 mm', 'foto_se_nc': True},
                    {'nr': '2.5', 'desc': 'Altura final da parede do chuveirão conforme projeto (+ 1 cm de tolerância)', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '3. Revestimentos e Acabamentos',
                'itens': [
                    {'nr': '3.1', 'desc': 'PISO (deck): cerâmica assentada, sem peças quebradas ou lascadas', 'foto_se_nc': True},
                    {'nr': '3.2', 'desc': 'PISO: nivelado, com declividade para os ralos (min 1%) — sem empoçamento', 'foto_se_nc': True},
                    {'nr': '3.3', 'desc': 'PISO: aderência verificada (percutir com cabo de vassoura — sem som oco)', 'foto_se_nc': True},
                    {'nr': '3.4', 'desc': 'PISO: rejunte correto, sem falhas ou buracos', 'foto_se_nc': True},
                    {'nr': '3.5', 'desc': 'PAREDE CHUVEIRÃO: cerâmica assentada sem peças quebradas ou desplacadas', 'foto_se_nc': True},
                    {'nr': '3.6', 'desc': 'PAREDE CHUVEIRÃO: aderência verificada (percutir) — sem som oco', 'foto_se_nc': True},
                    {'nr': '3.7', 'desc': 'Espaçadores e juntas entre cerâmicas corretos em piso e parede', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '4. Instalações Hidráulicas — Chuveirão',
                'itens': [
                    {'nr': '4.1', 'desc': 'CHUVEIRO: registro de água instalado, nivelado com a cerâmica e sem vazamentos', 'foto_se_nc': True},
                    {'nr': '4.2', 'desc': 'Ponto de água do chuveirão nivelado com a cerâmica conforme projeto', 'foto_se_nc': True},
                    {'nr': '4.3', 'desc': 'Vedação das conexões hidráulicas (veda rosca): sem gotejamentos', 'foto_se_nc': True},
                    {'nr': '4.4', 'desc': 'Pontos de espera para bombas: instalados nas posições corretas (visíveis)', 'foto_se_nc': True},
                    {'nr': '4.5', 'desc': 'TESTE FUNCIONAL: abrir registro, verificar escoamento e ausência de vazamentos por 5 min', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '5. Instalações Elétricas',
                'itens': [
                    {'nr': '5.1', 'desc': 'Pontos elétricos instalados nas posições corretas e funcionando', 'foto_se_nc': True},
                    {'nr': '5.2', 'desc': 'Ausência de cabos expostos ou conexões sem proteção', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '6. Gradil e Inspeção Geral',
                'itens': [
                    {'nr': '6.1', 'desc': 'GRADIL DE 120 cm: instalado delimitando o deck da piscina, fixo e sem danos', 'foto_se_nc': True},
                    {'nr': '6.2', 'desc': 'Gradil com acabamento correto, sem pontas expostas ou risco de acidente', 'foto_se_nc': True},
                    {'nr': '6.3', 'desc': 'Deck entregue limpo, sem entulho ou materiais de construção', 'foto_se_nc': True},
                    {'nr': '6.4', 'desc': 'Área da piscina protegida e sem danos causados pela obra do deck', 'foto_se_nc': True},
                    {'nr': '6.5', 'desc': 'Documentação disponível: ART/RRT, memoriais, projetos as-built', 'foto_se_nc': False},
                    {'nr': '6.6', 'desc': 'Fotos do estado final registradas (obrigatório)', 'foto_se_nc': True},
                    {'nr': '6.7', 'desc': 'Ausência de serviços incompletos ou materiais inacabados', 'foto_se_nc': True},
                ]
            },
        ],
        'pk_itens': ['PK-04', 'PK-08', 'PK-09', 'PK-10'],
    },

    'salao': {
        'tipo': 'salao',
        'titulo': 'Checklist de Recebimento — Salão de Festas',
        'secoes': [
            {
                'titulo': '1. Estrutura e Fundação — Radier',
                'itens': [
                    {'nr': '1.1', 'desc': 'Radier e sapatas sem sinais de recalque, trinca, fissura ou deslocamento visível', 'foto_se_nc': True},
                    {'nr': '1.2', 'desc': 'Dimensões e esquadro do radier conformes ao projeto', 'foto_se_nc': True},
                    {'nr': '1.3', 'desc': 'Engaste lateral e vala de contenção para pó de pedra íntegros', 'foto_se_nc': True},
                    {'nr': '1.4', 'desc': 'Caixa de gordura (Copa): instalada, acessível, sem entupimento, meia-cana íntegra', 'foto_se_nc': True},
                    {'nr': '1.5', 'desc': 'Caixas de inspeção: acessíveis, sem danos, com piso chanfrado + meia-cana íntegros', 'foto_se_nc': True},
                    {'nr': '1.6', 'desc': 'Escoamento sanitário correto nas caixas de inspeção (teste funcional)', 'foto_se_nc': True},
                    {'nr': '1.7', 'desc': 'Calhas e saídas pluviais sem entupimento — escoamento correto (teste funcional)', 'foto_se_nc': True},
                    {'nr': '1.8', 'desc': 'Caimento do piso para os ralos em áreas molhadas — sem empoçamento', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '2. Alvenaria e Vedação',
                'itens': [
                    {'nr': '2.1', 'desc': 'Paredes em prumo e alinhamento — verificar com nível nas 8 vistas', 'foto_se_nc': True},
                    {'nr': '2.2', 'desc': 'Paredes sem trincas, fissuras, manchas ou eflorescências em todos os ambientes', 'foto_se_nc': True},
                    {'nr': '2.3', 'desc': 'Esperas hidrossanitárias (pontos de saída) vedadas e tamponadas: todos os WCs, Copa e DML', 'foto_se_nc': True},
                    {'nr': '2.4', 'desc': 'Pontos elétricos finalizados nas posições corretas conforme projeto', 'foto_se_nc': True},
                    {'nr': '2.5', 'desc': 'Vão das janelas: altura e largura conformes (WC acessível, feminino, masculino, Copa, DML)', 'foto_se_nc': True},
                    {'nr': '2.6', 'desc': 'Afastamento mínimo das janelas para extremidade da alvenaria correto', 'foto_se_nc': True},
                    {'nr': '2.7', 'desc': 'Impermeabilização em áreas molhadas verificada: ausência de infiltração (teste funcional)', 'foto_se_nc': True},
                    {'nr': '2.8', 'desc': 'Ausência de umidade, manchas ou eflorescência nas paredes internas e externas', 'foto_se_nc': True},
                    {'nr': '2.9', 'desc': 'Altura final das paredes até cinta de respaldo: conformes ao projeto (8 vistas)', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '3. Cobertura Metálica',
                'itens': [
                    {'nr': '3.1', 'desc': 'Treliças metálicas fixadas nos pilares (chapa ligação 1014 e parabolts) — sem folgas', 'foto_se_nc': True},
                    {'nr': '3.2', 'desc': 'Estrutura metálica: todos os perfis (1000 a 1014) locados e alinhados conforme projeto', 'foto_se_nc': True},
                    {'nr': '3.3', 'desc': 'Perfis e chapas fixados corretamente, sem peças soltas ou faltando', 'foto_se_nc': True},
                    {'nr': '3.4', 'desc': 'Telhas sem furos, quebras ou inversões: transpasse e alinhamento corretos', 'foto_se_nc': True},
                    {'nr': '3.5', 'desc': 'Encaixe das telhas sem folgas — sem pontos de entrada de água', 'foto_se_nc': True},
                    {'nr': '3.6', 'desc': 'Estrutura metálica sem oxidação ou corrosão visível', 'foto_se_nc': True},
                    {'nr': '3.7', 'desc': 'Ausência de infiltrações (verificar após chuva ou teste com mangueira)', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '4. Revestimentos e Acabamentos',
                'itens': [
                    {'nr': '4.1', 'desc': 'PISO (todos os ambientes): cerâmica correta, sem peças quebradas ou lascadas', 'foto_se_nc': True},
                    {'nr': '4.2', 'desc': 'PISO: declividade e planeza corretas (desvio máx 0,3 cm/m) — verificar em todos os ambientes', 'foto_se_nc': True},
                    {'nr': '4.3', 'desc': 'PISO: aderência (percutir) — sem som oco em todos os ambientes', 'foto_se_nc': True},
                    {'nr': '4.4', 'desc': 'PISO: rejunte sem falhas ou buracos em todos os ambientes', 'foto_se_nc': True},
                    {'nr': '4.5', 'desc': 'PAREDE (ambientes com cerâmica): sem peças quebradas, rejunte correto', 'foto_se_nc': True},
                    {'nr': '4.6', 'desc': 'PAREDE: aderência (percutir) — sem som oco', 'foto_se_nc': True},
                    {'nr': '4.7', 'desc': 'EMBOÇO interno e externo: planeza máxima de 2 mm — sem bolsões', 'foto_se_nc': True},
                    {'nr': '4.8', 'desc': 'MASSA FINA interna e externa: planeza máxima de 0,2 cm — acabamento uniforme', 'foto_se_nc': True},
                    {'nr': '4.9', 'desc': 'TEXTURA: paredes externas e internas com textura aplicada uniformemente', 'foto_se_nc': True},
                    {'nr': '4.10', 'desc': 'SOLEIRAS: rebaixos conformes ao projeto em todas as portas', 'foto_se_nc': True},
                    {'nr': '4.11', 'desc': 'CAPIAÇÕES: acabamento no vão de portas e janelas correto e sem falhas', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '5. Esquadrias — Portas e Janelas',
                'itens': [
                    {'nr': '5.1', 'desc': 'PORTAS EXTERNAS: WC acessível, feminino, masculino, Copa e DML em prumo e fixadas', 'foto_se_nc': True},
                    {'nr': '5.2', 'desc': 'Portas externas: funcionamento de trincos, fechos e escovas de vedação (correr)', 'foto_se_nc': True},
                    {'nr': '5.3', 'desc': 'PORTAS INTERNAS: WC acessível, feminino e masculino — prumo e fixação corretos', 'foto_se_nc': True},
                    {'nr': '5.4', 'desc': 'Portas internas: abertura e fechamento sem travamento, fechaduras funcionando', 'foto_se_nc': True},
                    {'nr': '5.5', 'desc': 'JANELAS: WC acessível, feminino, masculino, Copa e DML instaladas em prumo', 'foto_se_nc': True},
                    {'nr': '5.6', 'desc': 'Janelas: funcionamento correto de abertura, fechamento, trilhos e vedação', 'foto_se_nc': True},
                    {'nr': '5.7', 'desc': 'ALIZARES: fixados corretamente em todas as portas', 'foto_se_nc': True},
                    {'nr': '5.8', 'desc': 'Todas as chaves entregues (portas e cadeados)', 'foto_se_nc': False},
                ]
            },
            {
                'titulo': '6. Forro de PVC',
                'itens': [
                    {'nr': '6.1', 'desc': 'Forro instalado em: WC acessível, WC feminino, WC masculino, DML e Copa', 'foto_se_nc': True},
                    {'nr': '6.2', 'desc': 'Altura e nível do forro conformes ao projeto (+ 1 cm tolerância)', 'foto_se_nc': True},
                    {'nr': '6.3', 'desc': 'Paginação e fixação do forro corretas — sem folgas ou encaixes faltando', 'foto_se_nc': True},
                    {'nr': '6.4', 'desc': 'Perfis (E-fix e F) instalados corretamente: vertical, longitudinal e transversal', 'foto_se_nc': True},
                    {'nr': '6.5', 'desc': 'Forro limpo, sem manchas, danos ou descaimentos', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '7. Instalações Hidráulicas e Sanitárias',
                'itens': [
                    {'nr': '7.1', 'desc': 'WC ACESSÍVEL: bacia sanitária + caixa acoplada instaladas e funcionando; descarga completa', 'foto_se_nc': True},
                    {'nr': '7.2', 'desc': 'WC ACESSÍVEL: lavatório instalado, torneira operante, sifão com abraçadeira — sem vazamentos', 'foto_se_nc': True},
                    {'nr': '7.3', 'desc': 'WC FEMININO: bacia sanitária + caixa acoplada instaladas e funcionando', 'foto_se_nc': True},
                    {'nr': '7.4', 'desc': 'WC FEMININO: lavatório instalado, torneira operante e sifão — sem vazamentos', 'foto_se_nc': True},
                    {'nr': '7.5', 'desc': 'WC MASCULINO: bacia sanitária + caixa acoplada instaladas e funcionando', 'foto_se_nc': True},
                    {'nr': '7.6', 'desc': 'WC MASCULINO: lavatório instalado, torneira operante e sifão — sem vazamentos', 'foto_se_nc': True},
                    {'nr': '7.7', 'desc': 'COPA: torneira instalada, operante e sem vazamentos; sifão com abraçadeira correto', 'foto_se_nc': True},
                    {'nr': '7.8', 'desc': 'COPA: caixa de gordura sem entupimento; escoamento correto da pia', 'foto_se_nc': True},
                    {'nr': '7.9', 'desc': 'DML: tanque instalado, torneira operante e sem vazamentos', 'foto_se_nc': True},
                    {'nr': '7.10', 'desc': 'Cantoneiras (balcão, tanque, lavatórios e bacias): nível, altura e esquadro (±0,2 cm)', 'foto_se_nc': True},
                    {'nr': '7.11', 'desc': 'Louças e resinados (balcão, tanque, lavatórios): instalados, fixos e sem danos', 'foto_se_nc': True},
                    {'nr': '7.12', 'desc': 'TESTE FUNCIONAL: abrir todos os pontos, testar descargas e verificar ausência de vazamentos', 'foto_se_nc': True},
                    {'nr': '7.13', 'desc': 'Ralos sifonados com escoamento livre e tampa corretamente posicionada', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '8. Instalações Elétricas',
                'itens': [
                    {'nr': '8.1', 'desc': 'Pontos elétricos (tomadas, interruptores) instalados e funcionando em todos os ambientes', 'foto_se_nc': True},
                    {'nr': '8.2', 'desc': 'Iluminação instalada e funcionando: salão, WC acessível, WC feminino, WC masculino, Copa, DML', 'foto_se_nc': True},
                    {'nr': '8.3', 'desc': 'Quadro de distribuição instalado, identificado e com disjuntores corretos', 'foto_se_nc': True},
                    {'nr': '8.4', 'desc': 'Aterramento verificado por teste funcional com equipamento adequado', 'foto_se_nc': True},
                    {'nr': '8.5', 'desc': 'Ausência de cabos expostos, emendas improvisadas ou conexões sem proteção', 'foto_se_nc': True},
                ]
            },
            {
                'titulo': '9. Inspeção Geral e Documentação',
                'itens': [
                    {'nr': '9.1', 'desc': 'Todos os ambientes entregues limpos, sem entulho ou materiais de construção', 'foto_se_nc': True},
                    {'nr': '9.2', 'desc': 'Área externa limpa, sem danos causados pela obra', 'foto_se_nc': True},
                    {'nr': '9.3', 'desc': 'Todas as chaves entregues (portas internas, externas e cadeados)', 'foto_se_nc': False},
                    {'nr': '9.4', 'desc': 'Documentação disponível: ART/RRT, memoriais e projetos as-built', 'foto_se_nc': False},
                    {'nr': '9.5', 'desc': 'Fotos do estado final de todos os ambientes registradas (obrigatório)', 'foto_se_nc': True},
                    {'nr': '9.6', 'desc': 'Manual de uso/manutenção de equipamentos entregue (louças, ferragens, forro)', 'foto_se_nc': False},
                    {'nr': '9.7', 'desc': 'Ausência de serviços incompletos ou materiais inacabados', 'foto_se_nc': True},
                ]
            },
        ],
        'pk_itens': ['PK-01', 'PK-02', 'PK-04', 'PK-05', 'PK-06', 'PK-07', 'PK-09', 'PK-10'],
    },
}
