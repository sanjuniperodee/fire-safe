<template>
  <div style="padding-top: 10px">
    <v-card-title
      class="title"
      style="font-size: 28px; margin-bottom: 1em"
    >
      Создание документов
    </v-card-title>
    <div class="buttons">
      <DocumentsAddButton
        v-for="item in buttons"
        :key="item.id"
        :button="item"
      />
    </div>

    <!-- dialogs -->
    <CertificateOfInspectionOfFireAutomaticSystemsAndInstallations />
    <ListOfInstalledDevicesAndEquipmentOfFireAutomaticSystemsAndInstallations />
    <InspectionActOfTheWaterSupplyNetworkForWaterYield />
    <PermissionForHotWork />
    <InspectionActOfFireHydrants />
    <TestActForInternalFireWaterSupplySystemsForOperability />
    <CertificateOfAcceptanceForOperationOfFireAutomaticSystemsAndInstallations />
    <TestReportForFireHydrantValvesForPerformance />
    <TestReportForInternalFireWaterSupplyForWaterLoss />
    <OperationalLogOfFireAutomaticSystemsAndInstallations />

    <TestReportTestingParametersOfVentilationSystems />
    <TestsToDetermineTheStrengthOfFirefightingExternalStationaryLaddersAndRoofRailings />
    <ProtocolTestIightningProtectionTestingSystem />
    <TESTREPORTForMeasuringTheInsulationResistanceOfWiresAndCables />
    <TESTREPORTFlammabilityTestMethodAndClassification />
    <FormOfControlTestReportToDetermineTheQualityOfFireRetardantForMetalStructures />
    <LogbookOfTestingLaboratoryProtocols />
    <FormOfControlTestReportToDetermineTheQualityOfFireRetardantForWoodenStructures />
  </div>
</template>

<script setup lang="ts">
import FormOfControlTestReportToDetermineTheQualityOfFireRetardantForMetalStructures from './documents/dialogs/QualityTestReportMetal.vue'
import FormOfControlTestReportToDetermineTheQualityOfFireRetardantForWoodenStructures from './documents/dialogs/QualityTestReportWood.vue'
import DocumentsAddButton from './documents/DocumentsAddButton.vue'
import CertificateOfInspectionOfFireAutomaticSystemsAndInstallations from './documents/dialogs/CertificateOfInspectionOfFireAutomaticSystemsAndInstallations.vue'
import ListOfInstalledDevicesAndEquipmentOfFireAutomaticSystemsAndInstallations from './documents/dialogs/ListOfInstalledDevicesAndEquipmentOfFireAutomaticSystemsAndInstallations.vue'
import InspectionActOfTheWaterSupplyNetworkForWaterYield from './documents/dialogs/InspectionActOfTheWaterSupplyNetworkForWaterYield.vue'
import PermissionForHotWork from './documents/dialogs/PermissionForHotWork.vue'
import InspectionActOfFireHydrants from './documents/dialogs/InspectionActOfFireHydrants.vue'
import TestActForInternalFireWaterSupplySystemsForOperability from './documents/dialogs/TestActForInternalFireWaterSupplySystemsForOperability.vue'
import CertificateOfAcceptanceForOperationOfFireAutomaticSystemsAndInstallations from './documents/dialogs/CertificateOfAcceptanceForOperationOfFireAutomaticSystemsAndInstallations.vue'
import TestReportForFireHydrantValvesForPerformance from './documents/dialogs/TestReportForFireHydrantValvesForPerformance.vue'
import TestReportForInternalFireWaterSupplyForWaterLoss from './documents/dialogs/TestReportForInternalFireWaterSupplyForWaterLoss.vue'
import OperationalLogOfFireAutomaticSystemsAndInstallations from './documents/dialogs/OperationalLogOfFireAutomaticSystemsAndInstallations.vue'
import TestReportTestingParametersOfVentilationSystems from './documents/dialogs/TestReportTestingParametersOfVentilationSystems.vue'
import TestsToDetermineTheStrengthOfFirefightingExternalStationaryLaddersAndRoofRailings from './documents/dialogs/TestsToDetermineTheStrengthOfFire.vue'
import TESTREPORTForMeasuringTheInsulationResistanceOfWiresAndCables from './documents/dialogs/TESTREPORTForMeasuringTheInsulationResistanceOfWiresAndCables.vue'
import ProtocolTestIightningProtectionTestingSystem from './documents/dialogs/ProtocolTestIightningProtectionTestingSystem.vue'
import TESTREPORTFlammabilityTestMethodAndClassification from './documents/dialogs/TESTREPORTFlammabilityTestMethodAndClassification.vue'
import LogbookOfTestingLaboratoryProtocols from './documents/dialogs/LogbookOfTestingLaboratoryProtocols.vue'

export type DocumentButton = {
  id: string
  title: string
}

const buttons: DocumentButton[] = [
  {
    id: '1',
    title: 'АКТ освидетельствования систем и установок пожарной автоматики'
  },
  {
    id: '2',
    title: 'ВЕДОМОСТЬ смонтированных приборов и оборудования систем и установок пожарной автоматики'
  },
  {
    id: '3',
    title: 'АКТ ОБСЛЕДОВАНИЯ водопроводной сети на водоотдачу'
  },
  {
    id: '4',
    title: 'РАЗРЕШЕНИЕ на производство огневых работ'
  },
  {
    id: '5',
    title: 'АКТ ОБСЛЕДОВАНИЯ пожарных гидрантов'
  },
  {
    id: '6',
    title: 'АКТ ИСПЫТАНИЙ систем внутреннего противопожарного водоснабжения на работоспособность'
  },
  {
    id: '7',
    title: 'АКТ приемки в эксплуатацию систем и установок пожарной автоматики'
  },
  {
    id: '8',
    title: 'Протокол испытаний клапанов пожарных кранов на работоспособность'
  },
  {
    id: '9',
    title: 'Протокол испытаний внутреннего противопожарного водоснабжения на водоотдачу'
  },
  {
    id: '10',
    title: 'Эксплуатационный журнал систем и установок пожарной автоматики'
  },
  {
    id: '11',
    title: 'Протокол испытаний испытание параметров систем вентиляции'
  },
  {
    id: '12',
    title:
      'Испытания по определению прочностей пожарных наружных стационарных лестниц и ограждения кровли'
  },
  {
    id: '13',
    title: 'ПРОТОКОЛ ИСПЫТАНИЙ проверки систем молниезащиты'
  },
  {
    id: '14',
    title: 'ПРОТОКОЛ ИСПЫТАНИЙ измерения сопротивления изоляции проводов и кабелей'
  },
  {
    id: '15',
    title: 'ПРОТОКОЛ ИСПЫТАНИЙ метод испытания на воспламеняемость и классификация'
  },
  {
    id: '16',
    title:
      'Форма протокола контрольных испытаний по определению качества обработки объекта огнезащитной по металлоконструкциям'
  },
  {
    id: '17',
    title: 'Журнал регистрации протоколов испытательной лаборатории'
  },
  {
    id: '18',
    title:
      'Форма протокола контрольных испытаний по определению качества обработки объекта огнезащитной по деревянным конструкциям'
  }
]
</script>

<style lang="scss" scoped>
.title {
  hyphens: none !important;
  text-overflow: initial !important;
  white-space: initial;
}

.buttons {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding-bottom: 40px;
}
</style>
