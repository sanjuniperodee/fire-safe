import axios from 'axios'

class DocumentService {
  baseUrl: string

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  private async fetchBlobFromEndpoint(endpoint: string, payload: any): Promise<string> {
    const { data } = await axios.post(`${this.baseUrl}${endpoint}`, payload)

    const byteCharacters = atob(data) // Assuming base64Data contains the base64 prefix (data:image/png;base64,)
    const byteArrays = []

    for (let offset = 0; offset < byteCharacters.length; offset += 512) {
      const slice = byteCharacters.slice(offset, offset + 512)
      const byteNumbers = new Array(slice.length)
      for (let i = 0; i < slice.length; i++) {
        byteNumbers[i] = slice.charCodeAt(i)
      }
      const byteArray = new Uint8Array(byteNumbers)
      byteArrays.push(byteArray)
    }

    const blob = new Blob(byteArrays, { type: 'application/octet-stream' }) // Adjust the type according to your file
    return URL.createObjectURL(blob)
  }

  async certificateOfInspectionOfFireAutomaticSystemsAndInstallations(payload: any) {
    return this.fetchBlobFromEndpoint('/api/v1/download/act/fire-automatic-installation', payload)
  }

  async listOfInstalledDevicesAndEquipmentOfFireAutomaticSystemsAndInstallations(payload: any) {
    return this.fetchBlobFromEndpoint(
      '/api/v1/download/act/statement-of-devices-and-equipment',
      payload
    )
  }

  async inspectionActOfTheWaterSupplyNetworkForWaterYield(payload: any) {
    return this.fetchBlobFromEndpoint('/api/v1/download/act/inspection-water-supply', payload)
  }

  async permissionForHotWork(payload: any) {
    return this.fetchBlobFromEndpoint('/api/v1/download/act/permission-for-hot-work', payload)
  }

  async inspectionActOfFireHydrants(payload: any) {
    return this.fetchBlobFromEndpoint('/api/v1/download/act/inspection-fire-hydrants', payload)
  }

  async testActForInternalFireWaterSupplySystemsForOperability(payload: any) {
    return this.fetchBlobFromEndpoint('/api/v1/download/act/testing-fire-fighting-system', payload)
  }

  async certificateOfAcceptanceForOperationOfFireAutomaticSystemsAndInstallations(payload: any) {
    return this.fetchBlobFromEndpoint(
      '/api/v1/download/act/inspection-fire-automation-systems',
      payload
    )
  }

  async testReportForFireHydrantValvesForPerformance(payload: any) {
    return this.fetchBlobFromEndpoint('/api/v1/download/act/test-reports-of-valves', payload)
  }

  async testReportForInternalFireWaterSupplyForWaterLoss(payload: any) {
    return this.fetchBlobFromEndpoint('/api/v1/download/act/testing-fire-fighting-system', payload)
  }

  async operationalLogOfFireAutomaticSystemsAndInstallations(payload: any) {
    return this.fetchBlobFromEndpoint('/api/v1/download/act/post-operational-log', payload)
  }

  async testReportTestingParametersOfVentilationSystems(payload: any) {
    return this.fetchBlobFromEndpoint('/api/v1/download/act/post-testing-ventilation', payload)
  }

  async testsToDetermineTheStrengthOfFirefightingExternalStationaryLaddersAndRoofRailings(
    payload: any
  ) {
    return this.fetchBlobFromEndpoint('/api/v1/download/act/post-testing-ladders', payload)
  }

  async protocolTestIightningProtectionTestingSystem(payload: any) {
    return this.fetchBlobFromEndpoint(
      '/api/v1/download/act/post-testing-lightning-systems',
      payload
    )
  }

  async tESTREPORTForMeasuringTheInsulationResistanceOfWiresAndCables(payload: any) {
    return this.fetchBlobFromEndpoint('/api/v1/download/act/post-testing-wires-and-cables', payload)
  }

  async tESTREPORTFlammabilityTestMethodAndClassification(payload: any) {
    return this.fetchBlobFromEndpoint('/api/v1/download/act/post-testing-lammability', payload)
  }

  async FormOfControlTestReportToDetermineTheQualityOfFireRetardantForMetalStructures(
    payload: any
  ) {
    return this.fetchBlobFromEndpoint(
      '/api/v1/download/act/post-testing-quality-of-retardant-for-metal',
      payload
    )
  }

  async FormOfControlTestReportToDetermineTheQualityOfFireRetardantForWoodenStructures(
    payload: any
  ) {
    return this.fetchBlobFromEndpoint(
      '/api/v1/download/act/post-testing-quality-of-retardant-for-wood',
      payload
    )
  }

  async logbookOfTestingLaboratoryProtocols(payload: any) {
    return this.fetchBlobFromEndpoint('/api/v1/download/act/post-logbook-of-protocols', payload)
  }
}

export const documentService = new DocumentService(import.meta.env.VITE_BACKEND_URL)
