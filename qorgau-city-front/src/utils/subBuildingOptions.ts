export const fireResistanceRating = [
  'I - Строения с несущими и ограждающими конструкциями из естественных или искусственных каменных материалов, бетона или железобетона с применением листовых и плитных негорючих материалов',
  'II - Строения с применением листовых и плитных негорючих материалов и незащищенные стальные конструкции',
  'III - Строения с несущими и ограждающими конструкциями из естественных или искусственных каменных штукатурки или трудногорючими штукатурками. Для перегородок допускается использование деревянных конструкций, защищенных негорючими или трудногорючими штукатурками',
  'IIIa - Строения преимущественно с каркасной конструктивной схемой. Элементы каркаса — из стальных профилированных листов или других негорючих материалов с трудногорючим утеплителем',
  'IIIб - Строения преимущественно одноэтажные с каркасной конструктивной схемой. Элементы каркаса — из цельной или клееной древесины, защищенные полимерной обработкой, обеспечивающей требуемый предел распространения огня. Ограждающие конструкции — из огнестойких материалов на органической основе',
  'IV - Строения с несущими и ограждающими конструкциями из цельной или клееной древесины и древесины высоких температур штукатурки или других горючих материалов с применением огнезащитной обработки',
  'IVa - Строения преимущественно одноэтажные с каркасной конструктивной схемой. Элементы каркаса — из стальных неэффективных конструкций. Орграждающие конструкции — из стальных профилированных листов или других негорючих материалов с горючим утеплителем',
  'V - Строения, к несущим и ограждающим конструкциям которых не предъявляются требования по пределам огнестойкости и пределам распространения огня'
]

export const externalWallsMaterials = [
  'Керамический кирпич',
  'Силикатный кирпич',
  'Клинкерный кирпич',
  'Монолитный железобетон',
  'Сборный железобетон',
  'Легкий бетон (пенобетон, газобетон)',
  'Природный камень (гранит, мрамор, известняк)',
  'Искусственный камень',
  'Бревна',
  'Брус',
  'Каркасные деревянные конструкции',
  'Стальные панели',
  'Алюминиевые панели',
  'Стеклянные фасады',
  'Стеклоблоки',
  'Сэндвич-панели',
  'Фиброцементные панели',
  'Виниловый сайдинг',
  'Пластиковые панели',
  'Обычная штукатурка',
  'Декоративная штукатурка',
  'Керамогранит',
  'Керамическая плитка',
  'Минеральная вата',
  'Пенополистирол',
  'Пенополиуретан',
  'Кирпично-монолитные',
  'Деревянно-каркасные с утеплителем',
  'Саман (глина и солома)',
  'Тростник',
  'Геокар (переработанная целлюлоза)',
  'Hempcrete (конопляный бетон)',
];

export const innerWallsMaterials: string[] = [
  'Перегородки из кирпича (камень)',
  'Перегородки из пенобетона (газобетон)',
  'Перегородки из дерева',
  'Перегородки из гипсокартона (ГКЛ)',
  'Перегородки из пазогребневых плит (ПГП)',
  'Перегородки из стеклоблоков',
];

export const roofTypes: string[] = [
  'Рулонная и мастичная кровля',
  'Кровля из штучных материалов и волнистых листов',
  'Кровля из металлических листов',
  'Кровля из железобетонных панелей лоткового сечения',
];

export const stairsMaterials: string[] = [
  'Бетонные',
  'Железобетонные',
  'Металлические',
  'Каменные',
  'Деревянные',
  'Пластиковые',
  'Металлические с деревянными ступенями',
  'Бетонные с деревянной отделкой',
  'Отсутствует'
];

export const stairsTypes: string[] = [
  'Одномаршевая',
  'Одномаршевая с площадкой',
  'Винтовая',
  'Криволинейная (спиральная)',
  'Криволинейная (циркульная)',
  'Двухмаршевая',
  'Комбинированная',
  'Отсутствует'
];

export const stairsСlassification: string[] = [
  'Н1-Лестничные клетки с входом на лестничную клетку с этажа через наружную воздушную зону по открытым переходам',
  'Н2-Лестничные клетки с подпором воздуха на лестничную клетку при пожаре',
  'L1-Лестничные клетки с естественным освещением через остекленные или открытые проемы в наружных стенах на каждом этаже',
  'L2-Лестничные клетки с естественным освещением через остекленные или открытые проемы в покрытии',
  'L3-Лестничные клетки с естественным освещением через остекленные или открытые проемы в наружных стенах на каждом этаже и в покрытии',
];


export const functionalPoClass = [
  {
    title: 'Ф1 - Здания для постоянного проживания и временного пребывания людей',
    items: [
      'Ф1.1 - детские дошкольные учреждения, специализированные дома престарелых и инвалидов (неквартирные), больницы, спальные корпуса школ-интернатов и детских учреждений',
      'Ф1.2 - гостиницы, общежития, спальные корпуса санаториев и домов отдыха общего типа, кемпингов, мотелей и пансионатов',
      'Ф1.3 - многоквартирные жилые дома',
      'Ф1.4 - одноквартирные, в том числе блокированные жилые дома'
    ],
    selectedValue: null
  },
  {
    title: 'Ф2 - Здания зрелищных и культурно-просветительных учреждений',
    items: [
      'Ф2.1 - театры, кинотеатры, концертные залы, клубы, цирки, спортивные сооружения с трибунами, библиотеки и другие учреждения с расчетным числом посадочных мест для посетителей в закрытых помещениях',
      'Ф2.2 - музеи, выставки, танцевальные залы и другие подобные учреждения в закрытых помещениях',
      'Ф2.3 - учреждения, указанные в Ф2.1, на открытом воздухе',
      'Ф2.4 - учреждения, указанные в Ф2.2, на открытом воздухе'
    ],
    selectedValue: null
  },
  {
    title: 'Ф3 - Здания предприятий по обслуживанию населения',
    items: [
      'Ф3.1 - здания предприятий торговли',
      'Ф3.2 - здания предприятий общественного питания',
      'Ф3.3 - вокзалы',
      'Ф3.4 - поликлиники и амбулатории',
      'Ф3.5 - помещения для посетителей предприятий бытового и коммунального обслуживания с нерасчетным числом посадочных мест для посетителей',
      'Ф3.6 - физкультурно-оздоровительные комплексы и спортивно-тренировочные учреждения без трибун для зрителей, бытовые помещения, бани'
    ],
    selectedValue: null
  },
  {
    title: 'Ф4 - Здания научно-исследовательских и образовательных учреждений',
    items: [
      'Ф4.1 - школы, внешкольные учебные заведения, средние специальные учебные заведения, профессионально-технические училища',
      'Ф4.2 - высшие учебные заведения, учреждения повышения квалификации',
      'Ф4.3 - учреждения органов управления, проектно-конструкторские организации, информационные и редакционно-издательские организации, научно-исследовательские организации, банки, конторы, офисы',
      'Ф4.4 - пожарные депо'
    ],
    selectedValue: null
  },
  {
    title: 'Ф5 - Здания производственного или складского назначения',
    items: [
      'Ф5.1 - производственные здания и сооружения, производственные и лабораторные помещения, мастерские',
      'Ф5.2 - складские здания и сооружения, стоянки для автомобилей без технического обслуживания и ремонта, книгохранилища, архивы, складские помещения',
      'Ф5.3 - сельскохозяйственные здания'
    ],
    selectedValue: null
  }
]

export const lightingOptions: { [key in LightingOptionEnglish]: LightingOption } = {
  'NATURAL_LIGHTING': 'Естественное освещение (солнце)',
  'ARTIFICIAL_LIGHTING': 'Искусственное освещение (лампы накаливания, светодиодные лампы)',
  'EMERGENCY_LIGHTING': 'Аварийное освещение (срабатывает во время пожара)',
};

export const lightingOptionsloacl: { [key in  LightingOption]: LightingOptionEnglish } = {
  'Естественное освещение (солнце)': 'NATURAL_LIGHTING',
  'Искусственное освещение (лампы накаливания, светодиодные лампы)': 'ARTIFICIAL_LIGHTING',
  'Аварийное освещение (срабатывает во время пожара)': 'EMERGENCY_LIGHTING',
};

export type LightingOption = 
  'Естественное освещение (солнце)' | 
  'Искусственное освещение (лампы накаливания, светодиодные лампы)' | 
  'Аварийное освещение (срабатывает во время пожара)';

export type LightingOptionEnglish = 
  'NATURAL_LIGHTING' | 
  'ARTIFICIAL_LIGHTING' | 
  'EMERGENCY_LIGHTING';

  export const getEnglishLightingOptions = (
    localType: LightingOption
  ): LightingOptionEnglish => {
    return lightingOptionsloacl[localType]
  }
  
  export const getLocalLightingOptions = (
    englishType: LightingOptionEnglish
  ): LightingOption => {
    return lightingOptions[englishType]
  }

  export const lightingOptionsItem = [
    'Естественное освещение (солнце)',
    'Искусственное освещение (лампы накаливания, светодиодные лампы)',
    'Аварийное освещение (срабатывает во время пожара)',
  ]

  // Ventilation

  export const ventilationOptionsMapping: { [key in VentilationOptionEnglish]: VentilationOption } = {
    'SUPPLY_VENTILATION': 'Приточная',
    'EXHAUST_VENTILATION': 'Вытяжная',
    'SUPPLY_AND_EXHAUST_SYSTEM': 'Приточно-вытяжная',
    'NATURAL_VENTILATION': 'Естественная',
    'ABSENT': 'Отсутствует',
  };
  
  export const ventilationOptionsLocal: { [key in VentilationOption]: VentilationOptionEnglish } = {
    'Приточная': 'SUPPLY_VENTILATION',
    'Вытяжная': 'EXHAUST_VENTILATION',
    'Приточно-вытяжная': 'SUPPLY_AND_EXHAUST_SYSTEM',
    'Естественная': 'NATURAL_VENTILATION',
    'Отсутствует': 'ABSENT',
  };

  export type VentilationOption =
  'Приточная' |
  'Вытяжная' |
  'Приточно-вытяжная' |
  'Естественная' |
  'Отсутствует';

// Массив с вариантами вентиляции на русском
export const ventilationOptions = [
  'Приточная',
  'Вытяжная',
  'Приточно-вытяжная',
  'Естественная',
  'Отсутствует',
];

// Типы для вентиляции на английском
export type VentilationOptionEnglish =
  'SUPPLY_VENTILATION' |
  'EXHAUST_VENTILATION' |
  'SUPPLY_AND_EXHAUST_SYSTEM' |
  'NATURAL_VENTILATION' |
  'ABSENT';

// Массив с вариантами вентиляции на английском
export const ventilationOptionsEnglish: VentilationOptionEnglish[] = [
  'SUPPLY_VENTILATION',
  'EXHAUST_VENTILATION',
  'SUPPLY_AND_EXHAUST_SYSTEM',
  'NATURAL_VENTILATION',
  'ABSENT',
];

export const getEnglishVentilation = (
  localType: VentilationOption
): VentilationOptionEnglish => {
  return ventilationOptionsLocal[localType]
}

export const getLocalVentilation = (
  englishType: VentilationOptionEnglish
): VentilationOption => {
  return ventilationOptionsMapping[englishType]
}

// Heating

export type HeatingOption = 
  'Автономное' | 
  'Печное' | 
  'Отсутствует';

export type HeatingOptionEnglish = 
  'AUTONOMOUS' | 
  'FURNACE' | 
  'ABSENT';

export const heatingOptionsRussian = [
    'Автономное',
    'Печное',
    'Отсутствует',
  ];
  
  // Массив для отопления на английском языке
export const heatingOptionsEnglish = [
    'AUTONOMOUS',
    'FURNACE',
    'ABSENT',
  ];

// Объекты для отопления
export const heatingOptions: { [key in HeatingOptionEnglish]: HeatingOption } = {
  'AUTONOMOUS': 'Автономное',
  'FURNACE': 'Печное',
  'ABSENT': 'Отсутствует',
};

export const heatingOptionsLocal: { [key in HeatingOption]: HeatingOptionEnglish } = {
  'Автономное': 'AUTONOMOUS',
  'Печное': 'FURNACE',
  'Отсутствует': 'ABSENT',
};

export const getEnglishHeating = (
  localType: HeatingOption
): HeatingOptionEnglish => {
  return heatingOptionsLocal[localType]
}

export const getLocalHeating = (
  englishType: HeatingOptionEnglish
): HeatingOption => {
  return heatingOptions[englishType]
}

//Security

export type SecurityOption = 
  'Ведомственная' | 
  'Вневедомственная охрана' | 
  'Частное охранное предприятие (ЧОП)' | 
  'Собственными силами' | 
  'Не охраняется';

export type SecurityOptionEnglish = 
  'DEPARTMENTAL' | 
  'PRIVATE_SECURITY' | 
  'PRIVATE_SECURITY_COMPANY' | 
  'OWN_STRENGTH' | 
  'NOT_GUARDED';

// Массив для охраны на русском языке
export const securityOptionsRussian = [
  'Ведомственная',
  'Вневедомственная охрана',
  'Частное охранное предприятие (ЧОП)',
  'Собственными силами',
  'Не охраняется',
];

// Массив для охраны на английском языке
export const securityOptionsEnglish = [
  'DEPARTMENTAL',
  'PRIVATE_SECURITY',
  'PRIVATE_SECURITY_COMPANY',
  'OWN_STRENGTH',
  'NOT_GUARDED',
];

export const securityOptions: { [key in SecurityOptionEnglish]: SecurityOption } = {
  'DEPARTMENTAL': 'Ведомственная',
  'PRIVATE_SECURITY': 'Вневедомственная охрана',
  'PRIVATE_SECURITY_COMPANY': 'Частное охранное предприятие (ЧОП)',
  'OWN_STRENGTH': 'Собственными силами',
  'NOT_GUARDED': 'Не охраняется',
};

// Обратный объект
export const securityOptionsLocal: { [key in SecurityOption]: SecurityOptionEnglish } = {
  'Ведомственная': 'DEPARTMENTAL',
  'Вневедомственная охрана': 'PRIVATE_SECURITY',
  'Частное охранное предприятие (ЧОП)': 'PRIVATE_SECURITY_COMPANY',
  'Собственными силами': 'OWN_STRENGTH',
  'Не охраняется': 'NOT_GUARDED',
};

export const getEnglishSecurity = (
  localType: SecurityOption
): SecurityOptionEnglish => {
  return securityOptionsLocal[localType]
}

export const getLocalSecurity = (
  englishType: SecurityOptionEnglish
): SecurityOption => {
  return securityOptions[englishType]
}