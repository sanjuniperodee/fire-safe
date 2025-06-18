<template>
  <v-dialog
    v-model="documentsStore.dialogs[DOCUMENT_KEY]"
    width="auto"
  >
    <v-card style="padding: 20px">
      <v-card-title>
        {{ DOCUMENT_KEY }}
      </v-card-title>
      <v-card-item>
        <v-form
          ref="form"
          class="body"
        >
          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Общие сведения системы и установок пожарной автоматики:
          </v-card-text>
          <div
            v-for="(item, i) in (data.generalInformationAboutFireAutomaticsSystemsAndInstallations as GeneralInformationAboutFireAutomaticsSystemsAndInstallation[])"
            :key="i"
          >
            <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
              Запись {{ i + 1 }}
            </v-card-text>

            <v-text-field
              :rules="rkaRules"
              v-model="item.rkaObjectNumber"
              style="min-width: 450px; padding-left: 20px"
              label="РКА объекта или помещения"
              placeholder="Введите РКА объекта или помещения"
              type="number"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.address"
              style="min-width: 450px; padding-left: 20px"
              label="Адрес объекта или помещения"
              placeholder="Введите адрес объекта или помещения"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="BINRules"
              v-model="item.ownerBIN"
              style="min-width: 450px; padding-left: 20px"
              label="БИН владельца объекта или помещения"
              placeholder="Введите БИН владельца объекта или помещения"
              type="number"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.ownerName"
              style="min-width: 450px; padding-left: 20px"
              label="Наименование владельца объекта или помещения"
              placeholder="Введите наименование владельца объекта или помещения"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="phoneRules"
              v-model="item.objectPhone"
              style="min-width: 450px; padding-left: 20px"
              label="Телефон объекта или помещения"
              placeholder="+7 (XXX) XXX-XX-XX"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.systemType"
              style="min-width: 450px; padding-left: 20px"
              label="Вид системы"
              placeholder="Введите вид системы"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.startingMethod"
              style="min-width: 450px; padding-left: 20px"
              label="Способ пуска"
              placeholder="Введите способ пуска"
              variant="solo-filled"
            ></v-text-field>

            <v-card-text style="font-weight: 700; font-size: 16px; width: 100%">
              Дата монтажа системы
            </v-card-text>
            <v-date-picker v-model="item.installationDate"></v-date-picker>

            <v-text-field
              :rules="BINRules"
              v-model="item.installationOrganizationBIN"
              style="min-width: 450px; padding-left: 20px"
              label="БИН монтажной организации"
              placeholder="Введите БИН монтажной организации"
              type="number"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.installationOrganizationName"
              style="min-width: 450px; padding-left: 20px"
              label="Наименование монтажной организации"
              placeholder="Введите наименование монтажной организации"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.fireSystemType"
              style="min-width: 450px; padding-left: 20px"
              label="Тип системы пожарной автоматики"
              placeholder="Введите тип системы пожарной автоматики"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="BINRules"
              v-model="item.serviceOrganizationBIN"
              style="min-width: 450px; padding-left: 20px"
              label="БИН обслуживающей систему организации (службы)"
              placeholder="Введите БИН обслуживающей систему организации (службы)"
              type="number"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.serviceOrganizationName"
              style="min-width: 450px; padding-left: 20px"
              label="Наименование обслуживающей систему организации (службы)"
              placeholder="Введите наименование обслуживающей систему организации (службы)"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="yearRules"
              v-model="item.serviceYear"
              style="min-width: 450px; padding-left: 20px"
              label="Календарный год обслуживания системы"
              placeholder="Выберите календарный год обслуживания"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="phoneRules"
              v-model="item.serviceOrganizationPhone"
              style="min-width: 450px; padding-left: 20px"
              label="Телефон обслуживающей систему организации (службы)"
              placeholder="+7 (XXX) XXX-XX-XX"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.technicalFacilitiesName"
              style="min-width: 450px; padding-left: 20px"
              label="Наименование технических средств системы пожарной автоматики"
              placeholder="Введите наименование технических средств"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.fireSystemTypes"
              style="min-width: 450px; padding-left: 20px"
              label="Типы систем пожарной автоматики"
              placeholder="Введите типы систем пожарной автоматики"
              variant="solo-filled"
            ></v-text-field>

            <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
              Схема системы пожарной автоматики
            </v-card-text>
            <v-select
              v-model="item.fireSystemScheme"
              :rules="commonRules"
              label="Выберите схему системы пожарной автоматики"
              style="min-width: 450px; padding-left: 20px"
              :items="['Принципиальная', 'Монтажная']"
              variant="solo-filled"
            ></v-select>

            <v-card-text style="font-weight: 700; font-size: 16px; width: 100%">
              Дата выпуска
            </v-card-text>
            <v-date-picker v-model="item.manufacturingDate"></v-date-picker>

            <v-card-text style="font-weight: 700; font-size: 16px; width: 100%">
              Дата начала эксплуатации
            </v-card-text>
            <v-date-picker v-model="item.operationStartDate"></v-date-picker>
            <v-text-field
              :rules="commonRules"
              v-model="item.nextInspectionPeriod"
              style="min-width: 450px; padding-left: 20px"
              label="Очередной срок освидетельствования"
              placeholder="Введите очередной срок освидетельствования"
              variant="solo-filled"
            ></v-text-field>
          </div>
          <v-btn
            color="#2297b6"
            prepend-icon="mdi-plus"
            variant="elevated"
            @click="() => createGeneralInformationAboutFireAutomaticsSystemsAndInstallation()"
            style="text-transform: none; margin-left: 20px"
            >Добавить запись</v-btn
          >

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Учет результатов гидравлических и электрических испытаний
          </v-card-text>

          <div
            v-for="(item, i) in (data.accountingForTheResultsOfHydraulicAndElectricalTest as AccountingForTheResultsOfHydraulicAndElectricalTest[])"
            :key="i"
          >
            <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
              Запись {{ i + 1 }}
            </v-card-text>

            <v-card-text style="font-weight: 700; font-size: 16px; width: 100%">
              Дата проведения испытаний
            </v-card-text>
            <v-date-picker v-model="item.testDate"></v-date-picker>

            <v-text-field
              :rules="commonRules"
              v-model="item.testResults"
              style="min-width: 450px; padding-left: 20px"
              label="Результаты испытаний"
              placeholder="Введите результаты испытаний"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="IINRules"
              v-model="item.employeeIIN"
              style="min-width: 450px; padding-left: 20px"
              label="ИИН сотрудника, проводившего испытания"
              placeholder="Введите ИИН сотрудника"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.employeeFullName"
              style="min-width: 450px; padding-left: 20px"
              label="ФИО сотрудника, проводившего испытания"
              placeholder="Введите ФИО сотрудника"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.conclusion"
              style="min-width: 450px; padding-left: 20px"
              label="Заключение"
              placeholder="Введите заключение"
              variant="solo-filled"
            ></v-text-field>
          </div>

          <v-btn
            color="#2297b6"
            prepend-icon="mdi-plus"
            variant="elevated"
            @click="() => createAccountingForTheResultsOfHydraulicAndElectricalTest()"
            style="text-transform: none; margin-left: 20px"
            >Добавить запись</v-btn
          >

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Учет приема-сдачи дежурства и техническое состояние системы
          </v-card-text>

          <div
            v-for="(item, i) in (data.accountingForCheckInAndCheckOutOfDutyAndTechnicalConditionOfTheSystem as AccountingForCheckInAndCheckOutOfDutyAndTechnicalConditionOfTheSystem[])"
            :key="i"
          >
            <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
              Запись {{ i + 1 }}
            </v-card-text>

            <v-card-text style="font-weight: 700; font-size: 16px; width: 100%">
              Дата и время приема-сдачи дежурства
            </v-card-text>
            <v-text-field
              :rules="timeRules"
              type="time"
              step="1"
              v-model="item.acceptanceTime"
              style="min-width: 450px; padding-left: 20px"
              label="Время"
              placeholder="Введите время"
              variant="solo-filled"
            ></v-text-field>
            <v-date-picker v-model="item.acceptanceDate"></v-date-picker>

            <v-text-field
              :rules="commonRules"
              v-model="item.systemCondition"
              style="min-width: 450px; padding-left: 20px"
              label="Состояние систем за период дежурства"
              placeholder="Введите состояние системы"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.protectedObjects"
              style="min-width: 450px; padding-left: 20px"
              label="Наименование защищаемых объектов, с которых поступали сигналы"
              placeholder="Введите наименование объектов"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.systemTypes"
              style="min-width: 450px; padding-left: 20px"
              label="Тип систем, с которых поступали сигналы"
              placeholder="Введите типы систем"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="IINRules"
              v-model="item.handoverIIN"
              style="min-width: 450px; padding-left: 20px"
              label="ИИН сдавшего дежурство"
              placeholder="Введите ИИН сдавшего дежурство"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.handoverFullName"
              style="min-width: 450px; padding-left: 20px"
              label="ФИО, сдавшего дежурство"
              placeholder="Введите ФИО сдавшего дежурство"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="IINRules"
              v-model="item.takeoverIIN"
              style="min-width: 450px; padding-left: 20px"
              label="ИИН принявшего дежурство"
              placeholder="Введите ИИН принявшего дежурство"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.takeoverFullName"
              style="min-width: 450px; padding-left: 20px"
              label="ФИО, принявшего дежурство"
              placeholder="Введите ФИО принявшего дежурство"
              variant="solo-filled"
            ></v-text-field>
          </div>

          <v-btn
            color="#2297b6"
            prepend-icon="mdi-plus"
            variant="elevated"
            @click="
              () => createAccountingForCheckInAndCheckOutOfDutyAndTechnicalConditionOfTheSystem()
            "
            style="text-transform: none; margin-left: 20px"
            >Добавить запись</v-btn
          >

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Учет отказов и неисправностей систем и установок пожарной автоматики
          </v-card-text>

          <div
            v-for="(item, i) in (data.accountingForFailuresAndMalfunctionsOfFireAutomaticSystemsAndInstallations as AccountingForFailuresAndMalfunctionsOfFireAutomaticSystemsAndInstallations[])"
            :key="i"
          >
            <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
              Запись {{ i + 1 }}
            </v-card-text>

            <v-card-text style="font-weight: 700; font-size: 16px; width: 100%">
              Дата и время поступления сообщения
            </v-card-text>
            <v-text-field
              :rules="timeRules"
              type="time"
              step="1"
              v-model="item.messageTime"
              style="min-width: 450px; padding-left: 20px"
              label="Время"
              placeholder="Введите время"
              variant="solo-filled"
            ></v-text-field>
            <v-date-picker v-model="item.messageDate"></v-date-picker>

            <v-text-field
              :rules="commonRules"
              v-model="item.roomName"
              style="min-width: 450px; padding-left: 20px"
              label="Наименование контролируемого помещения"
              placeholder="Введите наименование помещения"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.malfunctionType"
              style="min-width: 450px; padding-left: 20px"
              label="Характер неисправности"
              placeholder="Введите характер неисправности"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="IINRules"
              v-model="item.employeeIIN"
              style="min-width: 450px; padding-left: 20px"
              label="ИИН сотрудника, принявшего сообщение"
              placeholder="Введите ИИН сотрудника"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.employeeFullName"
              style="min-width: 450px; padding-left: 20px"
              label="ФИО сотрудника, принявшего сообщение"
              placeholder="Введите ФИО сотрудника"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.employeePosition"
              style="min-width: 450px; padding-left: 20px"
              label="Должность сотрудника, принявшего сообщение"
              placeholder="Введите должность сотрудника"
              variant="solo-filled"
            ></v-text-field>

            <v-card-text style="font-weight: 700; font-size: 16px; width: 100%">
              Дата и время устранения неисправности
            </v-card-text>
            <v-text-field
              :rules="timeRules"
              type="time"
              step="1"
              v-model="item.repairTime"
              style="min-width: 450px; padding-left: 20px"
              label="Время"
              placeholder="Введите время"
              variant="solo-filled"
            ></v-text-field>
            <v-date-picker v-model="item.repairDate"></v-date-picker>
          </div>

          <v-btn
            color="#2297b6"
            prepend-icon="mdi-plus"
            variant="elevated"
            @click="
              () =>
                createAccountingForFailuresAndMalfunctionsOfFireAutomaticSystemsAndInstallations()
            "
            style="text-transform: none; margin-left: 20px"
            >Добавить запись</v-btn
          >

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Учет технического обслуживания и планово-предупредительных ремонтов систем и установок
            пожарной автоматики
          </v-card-text>

          <div
            v-for="(item, i) in (data.accountingForMaintenanceAndScheduledPreventativeRepairsOfFireAutomaticSystemsAndInstallations as AccountingForMaintenanceAndScheduledPreventativeRepairsOfFireAutomaticSystemsAndInstallations[])"
            :key="i"
          >
            <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
              Запись {{ i + 1 }}
            </v-card-text>

            <v-card-text style="font-weight: 700; font-size: 16px; width: 100%">
              Дата и время проведения работ
            </v-card-text>
            <v-text-field
              :rules="timeRules"
              type="time"
              step="1"
              v-model="item.workTime"
              style="min-width: 450px; padding-left: 20px"
              label="Время"
              placeholder="Введите время"
              variant="solo-filled"
            ></v-text-field>
            <v-date-picker v-model="item.workDate"></v-date-picker>

            <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
              Вид работ
            </v-card-text>
            <v-select
              v-model="item.workType"
              :rules="commonRules"
              label="Введите вид работ"
              style="min-width: 450px; padding-left: 20px"
              :items="['Техническое обслуживание', 'Планово-предупредительный ремонт']"
              variant="solo-filled"
            ></v-select>
            <v-text-field
              :rules="commonRules"
              v-model="item.systemType"
              style="min-width: 450px; padding-left: 20px"
              label="Тип системы"
              placeholder="Введите тип системы"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.controlledObject"
              style="min-width: 450px; padding-left: 20px"
              label="Контролируемый объект"
              placeholder="Введите контролируемый объект"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.workCharacter"
              style="min-width: 450px; padding-left: 20px"
              label="Характер проведенных работ"
              placeholder="Введите характер работ"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.workList"
              style="min-width: 450px; padding-left: 20px"
              label="Перечень проведенных работ"
              placeholder="Введите перечень работ"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="IINRules"
              v-model="item.employeeIIN"
              style="min-width: 450px; padding-left: 20px"
              label="ИИН лица, проводившего работы"
              placeholder="Введите ИИН лица"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.employeeFullName"
              style="min-width: 450px; padding-left: 20px"
              label="ФИО лица, проводившего работы"
              placeholder="Введите ФИО лица"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.employeePosition"
              style="min-width: 450px; padding-left: 20px"
              label="Должность лица, проводившего работы"
              placeholder="Введите должность лица"
              variant="solo-filled"
            ></v-text-field>
          </div>

          <v-btn
            color="#2297b6"
            prepend-icon="mdi-plus"
            variant="elevated"
            @click="
              () =>
                createAccountingForMaintenanceAndScheduledPreventativeRepairsOfFireAutomaticSystemsAndInstallations()
            "
            style="text-transform: none; margin-left: 20px"
            >Добавить запись</v-btn
          >

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Учет проверки знаний персонала, обслуживающего системы пожарной автоматики
          </v-card-text>

          <div
            v-for="(item, i) in (data.accountingForTestingTheKnowledgeOfPersonnelServicingFireAutomaticSystems as AccountingForTestingTheKnowledgeOfPersonnelServicingFireAutomaticSystems[])"
            :key="i"
          >
            <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
              Запись {{ i + 1 }}
            </v-card-text>
            <v-text-field
              :rules="IINRules"
              v-model="item.employeeIIN"
              style="min-width: 450px; padding-left: 20px"
              label="ИИН проверяемого"
              placeholder="Введите ИИН проверяемого"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.employeeFullName"
              style="min-width: 450px; padding-left: 20px"
              label="Фамилия, имя, отчество (при его наличии) проверяемого"
              placeholder="Введите ФИО проверяемого"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.employeePosition"
              style="min-width: 450px; padding-left: 20px"
              label="Должность проверяемого"
              placeholder="Введите должность проверяемого"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.employeeExperience"
              style="min-width: 450px; padding-left: 20px"
              label="Стаж работы проверяемого"
              placeholder="Введите стаж работы проверяемого"
              variant="solo-filled"
            ></v-text-field>

            <v-card-text style="font-weight: 700; font-size: 16px; width: 100%">
              Дата проверки
            </v-card-text>
            <v-date-picker v-model="item.checkDate"></v-date-picker>

            <v-text-field
              :rules="commonRules"
              v-model="item.knowledgeRating"
              style="min-width: 450px; padding-left: 20px"
              label="Оценка знаний"
              placeholder="Введите оценку знаний"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="IINRules"
              v-model="item.checkerIIN"
              style="min-width: 450px; padding-left: 20px"
              label="ИИН проверяющего"
              placeholder="Введите ИИН проверяющего"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.checkerFullName"
              style="min-width: 450px; padding-left: 20px"
              label="ФИО проверяющего"
              placeholder="Введите ФИО проверяющего"
              variant="solo-filled"
            ></v-text-field>
          </div>

          <v-btn
            color="#2297b6"
            prepend-icon="mdi-plus"
            variant="elevated"
            @click="
              () => createAccountingForTestingTheKnowledgeOfPersonnelServicingFireAutomaticSystems()
            "
            style="text-transform: none; margin-left: 20px"
            >Добавить запись</v-btn
          >

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Учет срабатывания (отключения) систем пожарной автоматики
          </v-card-text>
          <div
            v-for="(item, i) in (data.accountingForActivationOfFireAutomaticSystems as AccountingForActivationOfFireAutomaticSystems[])"
            :key="i"
          >
            <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
              Запись {{ i + 1 }}
            </v-card-text>

            <v-text-field
              :rules="BINRules"
              v-model="item.controlledObjectBIN"
              style="min-width: 450px; padding-left: 20px"
              label="БИН контролируемого объекта"
              placeholder="Введите БИН контролируемого объекта"
              type="number"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.controlledObjectName"
              style="min-width: 450px; padding-left: 20px"
              label="Наименование контролируемого объекта"
              placeholder="Введите наименование контролируемого объекта"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.fireSystemView"
              style="min-width: 450px; padding-left: 20px"
              label="Вид системы пожарной автоматики"
              placeholder="Введите вид системы пожарной автоматики"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.fireSystemType"
              style="min-width: 450px; padding-left: 20px"
              label="Тип системы пожарной автоматики"
              placeholder="Введите тип системы пожарной автоматики"
              variant="solo-filled"
            ></v-text-field>

            <v-card-text style="font-weight: 700; font-size: 16px; width: 100%">
              Дата срабатывания (откл.)
            </v-card-text>
            <v-date-picker v-model="item.activationDate"></v-date-picker>

            <v-text-field
              :rules="commonRules"
              v-model="item.activationReason"
              style="min-width: 450px; padding-left: 20px"
              label="Причина срабатывания (откл.)"
              placeholder="Введите причину срабатывания (откл.)"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="numberRules"
              v-model="item.damageInTenge"
              style="min-width: 450px; padding-left: 20px"
              label="Ущерб от пожара, тенге"
              placeholder="Введите ущерб от пожара в тенге"
              suffix="тенге"
              type="number"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.damageDescription"
              style="min-width: 450px; padding-left: 20px"
              label="Ущерб от пожара"
              placeholder="Введите описание ущерба от пожара"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.activationCause"
              style="min-width: 450px; padding-left: 20px"
              label="Причина срабатывания"
              placeholder="Введите причину срабатывания"
              variant="solo-filled"
            ></v-text-field>
          </div>

          <v-btn
            color="#2297b6"
            prepend-icon="mdi-plus"
            variant="elevated"
            @click="() => createAccountingForActivationOfFireAutomaticSystems()"
            style="text-transform: none; margin-left: 20px"
            >Добавить запись</v-btn
          >

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Учет инструктажа технического и оперативного персонала по технике безопасности при
            работе с системами пожарной автоматики
          </v-card-text>

          <div
            v-for="(item, i) in (data.accountingForSafetyBriefingsOfTechnicalAndOperationalPersonnelWhenWorkingWithFireAutomaticSystems as AccountingForSafetyBriefingsOfTechnicalAndOperationalPersonnelWhenWorkingWithFireAutomaticSystems[])"
            :key="i"
          >
            <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
              Запись {{ i + 1 }}
            </v-card-text>
            <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
              Тип персонала
            </v-card-text>
            <v-select
              v-model="item.personnelType"
              :rules="commonRules"
              label="Выберите тип персонала"
              style="min-width: 450px; padding-left: 20px"
              :items="['Технический', 'Оперативный']"
              variant="solo-filled"
            ></v-select>
            <v-text-field
              :rules="IINRules"
              v-model="item.employeeIIN"
              style="min-width: 450px; padding-left: 20px"
              label="ИИН инструктируемого лица"
              placeholder="Введите ИИН инструктируемого лица"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.employeeFullName"
              style="min-width: 450px; padding-left: 20px"
              label="ФИО инструктируемого лица"
              placeholder="Введите ФИО инструктируемого лица"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.employeePosition"
              style="min-width: 450px; padding-left: 20px"
              label="Занимаемая должность инструктируемого"
              placeholder="Введите занимаемую должность инструктируемого"
              variant="solo-filled"
            ></v-text-field>

            <v-card-text style="font-weight: 700; font-size: 16px; width: 100%">
              Дата проведения инструктажа
            </v-card-text>
            <v-date-picker v-model="item.trainingDate"></v-date-picker>

            <v-text-field
              :rules="IINRules"
              v-model="item.trainerIIN"
              style="min-width: 450px; padding-left: 20px"
              label="ИИН лица, проводившего инструктаж"
              placeholder="Введите ИИН лица, проводившего инструктаж"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.trainerFullName"
              style="min-width: 450px; padding-left: 20px"
              label="ФИО лица, проводившего инструктаж"
              placeholder="Введите ФИО лица, проводившего инструктаж"
              variant="solo-filled"
            ></v-text-field>
          </div>

          <v-btn
            color="#2297b6"
            prepend-icon="mdi-plus"
            variant="elevated"
            @click="
              () =>
                createAccountingForSafetyBriefingsOfTechnicalAndOperationalPersonnelWhenWorkingWithFireAutomaticSystems()
            "
            style="text-transform: none; margin-left: 20px"
            >Добавить запись</v-btn
          >
        </v-form>
      </v-card-item>
      <v-card-actions style="display: flex; justify-content: end">
        <v-btn
          color="primary"
          @click="downloadPdf"
          >Скачать PDF</v-btn
        >
        <v-btn
          :loading="documentsStore.isGenerateDocumentLoading"
          color="#d20f0d"
          variant="tonal"
          @click="() => documentsStore.closeDialog(DOCUMENT_KEY)"
          style="text-transform: none"
          >Отмена</v-btn
        >
        <v-btn
          :loading="documentsStore.isGenerateDocumentLoading"
          color="#5b9271"
          variant="elevated"
          @click="() => generateDocument()"
          style="text-transform: none"
          >Сохранить</v-btn
        >
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { useDocumentsStore } from '@/stores/DocumentsStore'
import { useSnackbarStore } from '@/stores/SnackbarStore'
import { ref } from 'vue'

const form = ref(null)
const snackbarStore = useSnackbarStore()

const downloadPdf = () => {
  console.log('downloadPdf')
}

const isValid = async () => {
  //@ts-expect-error registerForm type gives automaticcaly in vuetify
  const { valid } = await form.value!.validate()
  return valid
}

const resetForm = () => {
  //@ts-expect-error registerForm type gives automaticcaly in vuetify
  form.value?.reset()
}

type GeneralInformationAboutFireAutomaticsSystemsAndInstallation = {
  rkaObjectNumber: string
  address: string
  ownerBIN: string
  ownerName: string
  objectPhone: string
  systemType: string
  startingMethod: string
  installationDate: Date
  installationOrganizationBIN: string
  installationOrganizationName: string
  fireSystemType: string
  serviceOrganizationBIN: string
  serviceOrganizationName: string
  serviceYear: Date
  serviceOrganizationPhone: string
  technicalFacilitiesName: string
  fireSystemTypes: string
  fireSystemScheme: string
  manufacturingDate: Date
  operationStartDate: Date
  nextInspectionPeriod: string
}

type AccountingForTheResultsOfHydraulicAndElectricalTest = {
  testDate: Date
  testResults: string
  employeeIIN: string
  employeeFullName: string
  conclusion: string
}

type AccountingForCheckInAndCheckOutOfDutyAndTechnicalConditionOfTheSystem = {
  acceptanceDate: Date
  acceptanceTime: string
  systemCondition: string
  protectedObjects: string
  systemTypes: string
  handoverIIN: string
  handoverFullName: string
  takeoverIIN: string
  takeoverFullName: string
}

type AccountingForFailuresAndMalfunctionsOfFireAutomaticSystemsAndInstallations = {
  messageDate: Date
  messageTime: string
  roomName: string
  malfunctionType: string
  employeeIIN: string
  employeeFullName: string
  employeePosition: string
  repairDate: Date
  repairTime: string
}

type AccountingForMaintenanceAndScheduledPreventativeRepairsOfFireAutomaticSystemsAndInstallations =
  {
    workDate: Date
    workTime: string
    workType: string
    systemType: string
    controlledObject: string
    workCharacter: string
    workList: string
    employeeIIN: string
    employeeFullName: string
    employeePosition: string
  }

type AccountingForTestingTheKnowledgeOfPersonnelServicingFireAutomaticSystems = {
  employeeIIN: string
  employeeFullName: string
  employeePosition: string
  employeeExperience: string
  checkDate: Date
  knowledgeRating: string
  checkerIIN: string
  checkerFullName: string
}

type AccountingForActivationOfFireAutomaticSystems = {
  controlledObjectBIN: string
  controlledObjectName: string
  fireSystemView: string
  fireSystemType: string
  activationDate: Date
  activationReason: string
  damageInTenge: string
  damageDescription: string
  activationCause: string
}

type AccountingForSafetyBriefingsOfTechnicalAndOperationalPersonnelWhenWorkingWithFireAutomaticSystems =
  {
    personnelType: string
    employeeIIN: string
    employeeFullName: string
    employeePosition: string
    trainingDate: Date
    trainerIIN: string
    trainerFullName: string
  }

const data = ref({
  generalInformationAboutFireAutomaticsSystemsAndInstallations: [],
  accountingForTheResultsOfHydraulicAndElectricalTest: [],
  accountingForCheckInAndCheckOutOfDutyAndTechnicalConditionOfTheSystem: [],
  accountingForFailuresAndMalfunctionsOfFireAutomaticSystemsAndInstallations: [],
  accountingForMaintenanceAndScheduledPreventativeRepairsOfFireAutomaticSystemsAndInstallations: [],
  accountingForTestingTheKnowledgeOfPersonnelServicingFireAutomaticSystems: [],
  accountingForActivationOfFireAutomaticSystems: [],
  accountingForSafetyBriefingsOfTechnicalAndOperationalPersonnelWhenWorkingWithFireAutomaticSystems:
    []
})

const rkaRules = ref([
  (v: any) => !!v || 'Номер РКА обязателен',
  (v: any) => !isNaN(Number(v)) || 'Номер РКА должен быть числом',
  (v: any) => parseInt(v.length) === 16 || 'Длина номера РКА обязана быть 16 цифр'
])

const IINRules = ref([
  (v: any) => !!v || 'ИИН обязателен',
  (v: any) => !isNaN(Number(v)) || 'ИИН должен быть числом',
  (v: any) => parseInt(v.length) === 12 || 'Длина ИИН должна быть 12 цифр'
])

const numberRules = ref([
  (v: any) => !!v || 'Порядковый номер обязателен',
  (v: any) => !isNaN(Number(v)) || 'Поле должно быть числом'
])

const yearRules = [
  (v: any) => !!v || 'Год обязателен',
  (v: any) => !isNaN(v) || 'Год должен быть числом',
  (v: any) => (v >= 0 && v <= new Date().getFullYear()) || 'Год должен быть между 0 и текущим годом'
]

const BINRules = ref([
  (v: any) => !!v || 'БИН обязателен',
  (v: any) => !isNaN(Number(v)) || 'БИН должен быть числом',
  (v: any) => parseInt(v.length) === 12 || 'Длина БИН должна быть 12 цифр'
])
const timeRules = ref([(v: any) => !!v || 'Время обязательно'])

const commonRules = ref([(v: any) => !!v || 'Поле обязательно'])

const phoneRules = [
  (v: string) => !!v || 'Номер телефона обязателен',
  (v: string) =>
    /^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$/.test(v) || 'Введите номер формата +7 (XXX) XXX-XX-XX'
]

const DOCUMENT_KEY = 'Эксплуатационный журнал систем и установок пожарной автоматики'
const documentsStore = useDocumentsStore()

const createGeneralInformationAboutFireAutomaticsSystemsAndInstallation = () => {
  data.value.generalInformationAboutFireAutomaticsSystemsAndInstallations.push({
    rkaObjectNumber: '',
    address: '',
    ownerBIN: '',
    ownerName: '',
    objectPhone: '',
    systemType: '',
    startingMethod: '',
    installationDate: new Date(),
    installationOrganizationBIN: '',
    installationOrganizationName: '',
    fireSystemType: '',
    serviceOrganizationBIN: '',
    serviceOrganizationName: '',
    serviceYear: new Date(),
    serviceOrganizationPhone: '',
    technicalFacilitiesName: '',
    fireSystemTypes: '',
    fireSystemScheme: '',
    manufacturingDate: new Date(),
    operationStartDate: new Date(),
    nextInspectionPeriod: ''
  } as never)
}

const createAccountingForTheResultsOfHydraulicAndElectricalTest = () => {
  data.value.accountingForTheResultsOfHydraulicAndElectricalTest.push({
    testNumber: '',
    testDate: new Date(),
    testResults: '',
    employeeIIN: '',
    employeeFullName: '',
    conclusion: ''
  } as never)
}

const createAccountingForCheckInAndCheckOutOfDutyAndTechnicalConditionOfTheSystem = () => {
  data.value.accountingForCheckInAndCheckOutOfDutyAndTechnicalConditionOfTheSystem.push({
    acceptanceDate: new Date(),
    acceptanceTime: '',
    systemCondition: '',
    protectedObjects: '',
    systemTypes: '',
    handoverIIN: '',
    handoverFullName: '',
    takeoverIIN: '',
    takeoverFullName: ''
  } as never)
}

const createAccountingForFailuresAndMalfunctionsOfFireAutomaticSystemsAndInstallations = () => {
  data.value.accountingForFailuresAndMalfunctionsOfFireAutomaticSystemsAndInstallations.push({
    messageDate: new Date(),
    messageTime: '',
    roomName: '',
    malfunctionType: '',
    employeeIIN: '',
    employeeFullName: '',
    employeePosition: '',
    repairDate: new Date(),
    repairTime: ''
  } as never)
}

const createAccountingForMaintenanceAndScheduledPreventativeRepairsOfFireAutomaticSystemsAndInstallations =
  () => {
    data.value.accountingForMaintenanceAndScheduledPreventativeRepairsOfFireAutomaticSystemsAndInstallations.push(
      {
        workDate: new Date(),
        workTime: '',
        workType: '',
        systemType: '',
        controlledObject: '',
        workCharacter: '',
        workList: '',
        employeeIIN: '',
        employeeFullName: '',
        employeePosition: ''
      } as never
    )
  }

const createAccountingForTestingTheKnowledgeOfPersonnelServicingFireAutomaticSystems = () => {
  data.value.accountingForTestingTheKnowledgeOfPersonnelServicingFireAutomaticSystems.push({
    employeeIIN: '',
    employeeFullName: '',
    employeePosition: '',
    employeeExperience: '',
    checkDate: new Date(),
    knowledgeRating: '',
    checkerIIN: '',
    checkerFullName: ''
  } as never)
}

const createAccountingForActivationOfFireAutomaticSystems = () => {
  data.value.accountingForActivationOfFireAutomaticSystems.push({
    controlledObjectBIN: '',
    controlledObjectName: '',
    fireSystemView: '',
    fireSystemType: '',
    activationDate: new Date(),
    activationReason: '',
    damageInTenge: '',
    damageDescription: '',
    activationCause: ''
  } as never)
}

const createAccountingForSafetyBriefingsOfTechnicalAndOperationalPersonnelWhenWorkingWithFireAutomaticSystems =
  () => {
    data.value.accountingForSafetyBriefingsOfTechnicalAndOperationalPersonnelWhenWorkingWithFireAutomaticSystems.push(
      {
        personnelType: '',
        employeeIIN: '',
        employeeFullName: '',
        employeePosition: '',
        trainingDate: new Date(),
        trainerIIN: '',
        trainerFullName: ''
      } as never
    )
  }

const generateDocument = async () => {
  if (await isValid()) {
    await documentsStore.generateDocument(DOCUMENT_KEY, data.value)
    resetForm()
  } else {
    snackbarStore.pullSnackbar('Заполните все поля прежде чем сохранить документ.', 3000, '#d20f0d')
    setTimeout(() => {
      const firstInvalidElement = document.querySelector('.v-input--error .v-input__control')
      if (firstInvalidElement) {
        // Scroll into view
        firstInvalidElement.scrollIntoView({ behavior: 'smooth', block: 'center' })

        // Focus the input element if possible
        const input = firstInvalidElement.querySelector('input, textarea, select')
        // @ts-expect-error
        if (input) input.focus()
      }
    }, 100)
  }
}
</script>

<style lang="scss" scoped>
.body {
  display: flex;
  flex-direction: column;
  align-items: start !important;
}
</style>
