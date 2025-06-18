import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useSnackbarStore } from './SnackbarStore'
import { documentService } from '@/services/documents.service'

const mapDocumentPayloadDates = (payload: any): any => {
  if (typeof payload !== 'object' || payload === null) {
    return payload
  }

  if (payload instanceof Date) {
    return payload.toISOString().split('T')[0]
  }

  if (Array.isArray(payload)) {
    return payload.map(mapDocumentPayloadDates)
  }

  const result = {} as any
  for (const key in payload) {
    if (Object.prototype.hasOwnProperty.call(payload, key)) {
      result[key] = mapDocumentPayloadDates(payload[key]) as any
    }
  }
  return result
}

export const documentMap = {
  'АКТ освидетельствования систем и установок пожарной автоматики':
    'certificateOfInspectionOfFireAutomaticSystemsAndInstallations',
  'ВЕДОМОСТЬ смонтированных приборов и оборудования систем и установок пожарной автоматики':
    'listOfInstalledDevicesAndEquipmentOfFireAutomaticSystemsAndInstallations',
  'АКТ ОБСЛЕДОВАНИЯ водопроводной сети на водоотдачу':
    'inspectionActOfTheWaterSupplyNetworkForWaterYield',
  'РАЗРЕШЕНИЕ на производство огневых работ': 'permissionForHotWork',
  'АКТ ОБСЛЕДОВАНИЯ пожарных гидрантов': 'inspectionActOfFireHydrants',
  'АКТ ИСПЫТАНИЙ систем внутреннего противопожарного водоснабжения на работоспособность':
    'testActForInternalFireWaterSupplySystemsForOperability',
  'АКТ приемки в эксплуатацию систем и установок пожарной автоматики':
    'certificateOfAcceptanceForOperationOfFireAutomaticSystemsAndInstallations',
  'Протокол испытаний клапанов пожарных кранов на работоспособность':
    'testReportForFireHydrantValvesForPerformance',
  'Протокол испытаний внутреннего противопожарного водоснабжения на водоотдачу':
    'testReportForInternalFireWaterSupplyForWaterLoss',
  'Эксплуатационный журнал систем и установок пожарной автоматики':
    'operationalLogOfFireAutomaticSystemsAndInstallations',
  'Протокол испытаний испытание параметров систем вентиляции':
    'testReportTestingParametersOfVentilationSystems',
  'Испытания по определению прочностей пожарных наружных стационарных лестниц и ограждения кровли':
    'testsToDetermineTheStrengthOfFirefightingExternalStationaryLaddersAndRoofRailings',
  'ПРОТОКОЛ ИСПЫТАНИЙ проверки систем молниезащиты': 'protocolTestIightningProtectionTestingSystem',
  'ПРОТОКОЛ ИСПЫТАНИЙ измерения сопротивления изоляции проводов и кабелей':
    'tESTREPORTForMeasuringTheInsulationResistanceOfWiresAndCables',
  'ПРОТОКОЛ ИСПЫТАНИЙ метод испытания на воспламеняемость и классификация':
    'tESTREPORTFlammabilityTestMethodAndClassification',
  'Форма протокола контрольных испытаний по определению качества обработки объекта огнезащитной по металлоконструкциям':
    'FormOfControlTestReportToDetermineTheQualityOfFireRetardantForMetalStructures',
  'Журнал регистрации протоколов испытательной лаборатории': 'logbookOfTestingLaboratoryProtocols',
  'Форма протокола контрольных испытаний по определению качества обработки объекта огнезащитной по деревянным конструкциям':
    'FormOfControlTestReportToDetermineTheQualityOfFireRetardantForWoodenStructures'
}
export const useDocumentsStore = defineStore('DocumentsStore', () => {
  const dialogs = ref({
    'АКТ освидетельствования систем и установок пожарной автоматики': false,
    'ВЕДОМОСТЬ смонтированных приборов и оборудования систем и установок пожарной автоматики':
      false,
    'АКТ ОБСЛЕДОВАНИЯ водопроводной сети на водоотдачу': false,
    'РАЗРЕШЕНИЕ на производство огневых работ': false,
    'АКТ ОБСЛЕДОВАНИЯ пожарных гидрантов': false,
    'АКТ ИСПЫТАНИЙ систем внутреннего противопожарного водоснабжения на работоспособность': false,
    'АКТ приемки в эксплуатацию систем и установок пожарной автоматики': false,
    'Протокол испытаний клапанов пожарных кранов на работоспособность': false,
    'Протокол испытаний внутреннего противопожарного водоснабжения на водоотдачу': false,
    'Эксплуатационный журнал систем и установок пожарной автоматики': false,
    'Протокол испытаний испытание параметров систем вентиляции': false,
    'Испытания по определению прочностей пожарных наружных стационарных лестниц и ограждения кровли':
      false,
    'ПРОТОКОЛ ИСПЫТАНИЙ проверки систем молниезащиты': false,
    'ПРОТОКОЛ ИСПЫТАНИЙ измерения сопротивления изоляции проводов и кабелей': false,
    'ПРОТОКОЛ ИСПЫТАНИЙ метод испытания на воспламеняемость и классификация': false,
    'Форма протокола контрольных испытаний по определению качества обработки объекта огнезащитной по металлоконструкциям':
      false,
    'Журнал регистрации протоколов испытательной лаборатории': false,
    'Форма протокола контрольных испытаний по определению качества обработки объекта огнезащитной по деревянным конструкциям':
      false
  })
  const snackbarStore = useSnackbarStore()
  const isGenerateDocumentLoading = ref(false)

  const openDialog = (title: string) => {
    dialogs.value[title as keyof typeof dialogs.value] = true
  }

  const closeDialog = (title: string) => {
    dialogs.value[title as keyof typeof dialogs.value] = false
  }

  const generateDocument = async (documentTitle: keyof typeof documentMap, payload: any) => {
    const methodName = documentMap[documentTitle]
    const mappedPayload = mapDocumentPayloadDates(payload)

    try {
      isGenerateDocumentLoading.value = true
      const link = await (documentService as any)[methodName](mappedPayload)
      // on success
      downloadDocument(documentTitle, link)
      closeDialog(documentTitle)
      snackbarStore.pullSnackbar(
        'Документ был сформирован и сохранен на ваше устройство.',
        2000,
        '#5b9271'
      )
      isGenerateDocumentLoading.value = false
    } catch (error) {
      snackbarStore.pullSnackbar(
        'Не удалось сгенерировать документ. Попробуйте позже.',
        3000,
        '#d20f0d'
      )
      isGenerateDocumentLoading.value = false
    }
  }

  const downloadDocument = (documentTitle: string, url: string) => {
    const a = document.createElement('a')
    a.href = url
    a.download = `${documentTitle} ${new Date().toLocaleString()}.docx`
    a.click()
  }

  return {
    dialogs,
    openDialog,
    closeDialog,
    generateDocument,
    isGenerateDocumentLoading
  }
})
