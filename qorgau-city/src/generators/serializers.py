from helpers.serializers import (
    ObjectNameSerializer,
    HotWorkObjectNameSerializer,
    ChairmanOfCommisionSerializer,
    OrganizationNameSerializer,
    FireHydrantSerializer,
    TestResultSerializer,
    StatementSerializer,
    TestingResultSerializer,
    GeneralInformationSerializer,
    AccountingForTheResultsOfHydraulicAndElectricalTestSerializer,
    AccountingForCheckInAndCheckOutOfDutyAndTechnicalConditionOfTheSystemSerializer,
    AccountingForFailuresAndMalfunctionsOfFireAutomaticSystemsAndInstallationsSerializer,
    AccountingForMaintenanceAndScheduledPreventativeRepairsOfFireAutomaticSystemsAndInstallationsSerializer,
    AccountingForTestingTheKnowledgeOfPersonnelServicingFireAutomaticSystemsSerializer,
    AccountingForActivationOfFireAutomaticSystemsSerializer,
    AccountingForSafetyBriefingsOfTechnicalAndOperationalPersonnelWhenWorkingWithFireAutomaticSystemsSerializer,
    LogbookOfTestingSerializer,
    mainResultsSerializer,
    testResultsSerializer,
    strengthTestResultsSerializer,
    lightningProtectionResultsSerializer,
    FireProtectiveAgentSerializer,
    ResultForMetalStructuresSerializer,
    ResultForWoodenStructuresSerializer,
    LammabilityTestResultSerializer,
    MeasurementResultSerializer,
    MeasurementsOfGroundingDevicesLeakageResistanceSerializer,
    MeasuringInstrumentsSerializer
)
from rest_framework import serializers


class WorkerSerializer(serializers.Serializer):
    IIN = serializers.CharField(max_length=12)
    name = serializers.CharField(max_length=255)


class ActOfFireAutomaticSystemsAndInstallationSerializer(serializers.Serializer):
    objectName = ObjectNameSerializer()
    chairmanOfCommision = ChairmanOfCommisionSerializer()
    commissionMembers = ChairmanOfCommisionSerializer(many=True)
    installationName = serializers.CharField(max_length=255)
    installationPlace = serializers.CharField(max_length=255)
    elementsName = serializers.CharField(max_length=255)
    carriedOutFrom = serializers.DateTimeField()
    carriedOutTo = serializers.DateTimeField()
    revealedDuringExamination = serializers.CharField(max_length=255)
    commissionConclusion = serializers.CharField(max_length=255)


class PermissionForHotWorkSerializer(serializers.Serializer):
    objectName = HotWorkObjectNameSerializer()
    issuedMember = ChairmanOfCommisionSerializer()
    fireWorksName = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255)
    eventNames = serializers.CharField(max_length=255)
    permissionValidFromTime = serializers.TimeField()
    permissionValidFromDate = serializers.DateField()
    permissionValidToTime = serializers.TimeField()
    permissionValidToDate = serializers.DateField()
    extendedFromTime = serializers.TimeField()
    extendedFromDate = serializers.DateField()
    extendedToTime = serializers.TimeField()
    extendedToDate = serializers.DateField()
    carryOutWorker = WorkerSerializer()


class ActOfTestingInternalFireFightingWaterSupplySystemSerializer(serializers.Serializer):
    city = serializers.CharField(max_length=255)
    operatingOrganizationName = OrganizationNameSerializer()
    serviceOrganizationName = OrganizationNameSerializer()
    testTime = serializers.TimeField()
    testDate = serializers.DateField()
    chairmanOfCommision = ChairmanOfCommisionSerializer()
    commissionMembers = ChairmanOfCommisionSerializer(many=True)
    numberAndHydrant = serializers.CharField(max_length=255)
    hydrantType = serializers.CharField(max_length=255)
    fireHoseType = serializers.CharField(max_length=255)
    fireHoseLength = serializers.CharField(max_length=12)
    fireHoseDiameter = serializers.CharField(max_length=12)
    firePumpType = serializers.CharField(max_length=255)
    pumpPressure = serializers.CharField(max_length=12)
    regulatoryCompliance = serializers.CharField(max_length=255)
    flowRate = serializers.CharField(max_length=255)
    pressure = serializers.CharField(max_length=255)
    simultaneousSprinklers = serializers.CharField(max_length=12)
    waterConsumptionForHouseholdNeedsFromTimeHour = serializers.CharField(max_length=12)
    waterConsumptionForHouseholdNeedsFromTimeMin = serializers.CharField(max_length=12)
    waterConsumptionForHouseholdNeedsToTimeHour = serializers.CharField(max_length=12)
    waterConsumptionForHouseholdNeedsToTimeMin = serializers.CharField(max_length=12)
    waterFlowRate = serializers.CharField(max_length=12)
    complianceExplanation = serializers.CharField(max_length=255)
    commissionConclusion = serializers.CharField(max_length=255)


class ActOfInspectionWaterSupplyNetworkForWaterDischargeSerializer(serializers.Serializer):
    city = serializers.CharField(max_length=255)
    chairmanOfCommision = ChairmanOfCommisionSerializer()
    commissionMembers = ChairmanOfCommisionSerializer(many=True)
    waterSupplyNetworkType = serializers.CharField(max_length=255)
    diameter = serializers.CharField(max_length=12)
    networkPressureAtmosphere = serializers.CharField(max_length=255)
    typeAndSizeOfInstalledFireHydrants = serializers.CharField(max_length=255)
    waterYieldInspectionMethod = serializers.CharField(max_length=255)
    actualWaterYield = serializers.CharField(max_length=12)
    requiredWaterYield = serializers.CharField(max_length=12)
    commissionConclusion = serializers.CharField(max_length=255)


class ActOfInspectionFireHydrantsSerializer(serializers.Serializer):
    city = serializers.CharField(max_length=255)
    organizationName = OrganizationNameSerializer()
    chairmanOfCommision = ChairmanOfCommisionSerializer()
    commissionMembers = ChairmanOfCommisionSerializer(many=True)
    fireHydrantCharacteristics = FireHydrantSerializer()
    inspectionConditions = serializers.CharField(max_length=255)
    measurementAndTestingEquipment = serializers.CharField(max_length=255)
    coverAndThreadCondition = serializers.CharField(max_length=255)
    drainDeviceFunctionality = serializers.CharField(max_length=255)
    waterPresence = serializers.CharField(max_length=255)
    valveSeal = serializers.CharField(max_length=255)
    hydrantFunctionality = serializers.CharField(max_length=255)
    hydrantOperationEffort = serializers.CharField(max_length=255)
    waterDischarge = serializers.CharField(max_length=12)
    waterInspectionMethod = serializers.CharField(max_length=255)
    actualWaterYield = serializers.CharField(max_length=12)
    requiredWaterYield = serializers.CharField(max_length=12)
    commissionConclusion = serializers.CharField(max_length=255)


class ActOfCommissioningFireAutomationSystemsAndInstallationsSerializer(serializers.Serializer):
    customerOrganizationName = OrganizationNameSerializer()
    solutionFrom = serializers.DateField()
    numberOfTheDecision = serializers.CharField(max_length=12)
    chairmanRepresentativeOfCustomer = ChairmanOfCommisionSerializer()
    commissionMembersInstallationOrganization = serializers.CharField(max_length=255)
    commissionMembersСommissioningOrganization = serializers.CharField(max_length=255)
    installationName = serializers.CharField(max_length=255)
    objectName = ObjectNameSerializer()
    developedProjectOrganizationName = OrganizationNameSerializer()
    performedInstallationWorkOrganizationName = OrganizationNameSerializer()
    installationWorkCarriedOutFrom = serializers.DateField()
    installationWorkCarriedOutTo = serializers.DateField()
    performedCommissioningWorkOrganizationName = OrganizationNameSerializer()
    commissioningWorkCarriedOutFrom = serializers.DateField()
    commissioningWorkCarriedOutTo = serializers.DateField()
    acceptedForOperationFrom = serializers.DateField()
    assessmentQualityWork = serializers.CharField(max_length=255)
    listofDocumentation = serializers.CharField(max_length=255)


class ReportOfTestingInternalFireFightingWaterSupplySerializer(serializers.Serializer):
    city = serializers.CharField(max_length=255)
    operatingOrganizationName = OrganizationNameSerializer()
    objectName = ObjectNameSerializer()
    serviceOrganizationName = OrganizationNameSerializer()
    testTime = serializers.TimeField()
    testDate = serializers.DateField()
    results = TestResultSerializer(many=True)
    numbersOfFireHydrantRisers = serializers.CharField(max_length=255)
    numberOfTestedFireValues = serializers.CharField(max_length=255)
    hydrantType = serializers.CharField(max_length=255)
    fireHoseType = serializers.CharField(max_length=255)
    fireHoseLength = serializers.CharField(max_length=12)
    fireHoseDiameter = serializers.CharField(max_length=12)
    firePumpType = serializers.CharField(max_length=255)
    pumpPressure = serializers.CharField(max_length=12)
    flowRate = serializers.CharField(max_length=255)
    pressure = serializers.CharField(max_length=255)
    simultaneousSprinklers = serializers.CharField(max_length=12)
    minWaterFlowRateDictatingValve = serializers.CharField(max_length=255)
    inAmount = serializers.CharField(max_length=12)
    pressureRequirement = serializers.CharField(max_length=12)
    flowRateRequirement = serializers.CharField(max_length=12)
    jetHeightRequirement = serializers.CharField(max_length=12)
    complianceExplanation = serializers.CharField(max_length=255)
    testConducted = serializers.CharField(max_length=255)


class StatementOfInstalledDevicesAndEquipmentFireAutomationSystemsInstallationsSerializer(serializers.Serializer):
    results = StatementSerializer(many=True)


class TestReportOfValvesFireCranesForOperabilitySerializer(serializers.Serializer):
    operatingOrganizationName = OrganizationNameSerializer()
    objectName = ObjectNameSerializer()
    serviceOrganizationName = OrganizationNameSerializer()
    testTime = serializers.TimeField()
    testDate = serializers.DateField()
    fireHydrantTypeValves = serializers.CharField(max_length=255)
    firePumpType = serializers.CharField(max_length=255)
    pressure = serializers.CharField(max_length=12)
    conclusion = serializers.CharField(max_length=255)
    results = TestingResultSerializer(many=True)
    testConducted = serializers.CharField(max_length=255)


class OperationalLogOfFireAutomationSystemsInstallationsSerializer(serializers.Serializer):
    generalInformationAboutFireAutomaticsSystemsAndInstallations = GeneralInformationSerializer(many=True)
    accountingForTheResultsOfHydraulicAndElectricalTest = AccountingForTheResultsOfHydraulicAndElectricalTestSerializer(
        many=True)
    accountingForCheckInAndCheckOutOfDutyAndTechnicalConditionOfTheSystem = AccountingForCheckInAndCheckOutOfDutyAndTechnicalConditionOfTheSystemSerializer(
        many=True)
    accountingForFailuresAndMalfunctionsOfFireAutomaticSystemsAndInstallations = AccountingForFailuresAndMalfunctionsOfFireAutomaticSystemsAndInstallationsSerializer(
        many=True)
    accountingForMaintenanceAndScheduledPreventativeRepairsOfFireAutomaticSystemsAndInstallations = AccountingForMaintenanceAndScheduledPreventativeRepairsOfFireAutomaticSystemsAndInstallationsSerializer(
        many=True)
    accountingForTestingTheKnowledgeOfPersonnelServicingFireAutomaticSystems = AccountingForTestingTheKnowledgeOfPersonnelServicingFireAutomaticSystemsSerializer(
        many=True)
    accountingForActivationOfFireAutomaticSystems = AccountingForActivationOfFireAutomaticSystemsSerializer(many=True)
    accountingForSafetyBriefingsOfTechnicalAndOperationalPersonnelWhenWorkingWithFireAutomaticSystems = AccountingForSafetyBriefingsOfTechnicalAndOperationalPersonnelWhenWorkingWithFireAutomaticSystemsSerializer(
        many=True)


class LogbookOfTestingLaboratoryProtocolsSerializer(serializers.Serializer):
    results = LogbookOfTestingSerializer(many=True)


class TestReportTestingParametersOfVentilationSystemsSerializer(serializers.Serializer):
    testDate = serializers.DateField()
    organizationName = serializers.CharField(max_length=255)
    organizationAddress = serializers.CharField(max_length=255)
    customerName = serializers.CharField(max_length=255)
    objectAddress = serializers.CharField(max_length=255)
    basisForTesting = serializers.CharField(max_length=255)
    testingMethod = serializers.CharField(max_length=255)
    mainResults = mainResultsSerializer(many=True)
    testResults = testResultsSerializer(many=True)
    smokeGasPermeability = serializers.CharField(max_length=255)
    testingResults = serializers.CharField(max_length=255)


class TestsToDetermineTheStrengthOfFirefightingExternalStationaryLaddersAndRoofRailingsSerializer(
    serializers.Serializer):
    testDate = serializers.DateField()
    organizationName = serializers.CharField(max_length=255)
    customerName = serializers.CharField(max_length=255)
    customerAddress = serializers.CharField(max_length=255)
    testingBasis = serializers.CharField(max_length=255)
    documentationName = serializers.CharField(max_length=255)
    objectCharacteristics = serializers.CharField(max_length=255)
    testingConditions = serializers.CharField(max_length=255)
    testingEquipment = serializers.CharField(max_length=255)
    stairVisualInspection = serializers.CharField(max_length=255)
    testResults = strengthTestResultsSerializer(many=True)
    testingResults = serializers.CharField(max_length=255)


class ProtocolTestLightningProtectionTestingSystemSerializer(serializers.Serializer):
    defenceCategory = serializers.CharField(max_length=255)
    results = lightningProtectionResultsSerializer(many=True)


class FormOfControlTestReportToDetermineTheQualityOfFireRetardantForMetalStructuresSerializer(serializers.Serializer):
    testDate = serializers.DateField()
    testingOrganizationName = OrganizationNameSerializer()
    customerOrganizationName = OrganizationNameSerializer()
    testBasis = serializers.CharField(max_length=255)
    fireProtectiveAgent = FireProtectiveAgentSerializer(many=True)
    normativeDocumentation = serializers.CharField(max_length=255)
    batchNumber = serializers.CharField(max_length=255)
    batchDate = serializers.DateField()
    fireProtectionOrganizationName = OrganizationNameSerializer()
    fireProtectionObjectType = serializers.CharField(max_length=255)
    fireProtectionObjectCondition = serializers.CharField(max_length=255)
    treatmentMethod = serializers.CharField(max_length=255)
    treatmentArea = serializers.CharField(max_length=255)
    operatingConditions = serializers.CharField(max_length=255)
    testingMethod = serializers.CharField(max_length=255)
    testConditions = serializers.CharField(max_length=255)
    results = ResultForMetalStructuresSerializer(many=True)
    conclusion = serializers.CharField(max_length=255)
    testConducted = serializers.CharField(max_length=255)


class FormOfControlTestReportToDetermineTheQualityOfFireRetardantForWoodenStructuresSerializer(serializers.Serializer):
    testDate = serializers.DateField()
    testingOrganizationName = OrganizationNameSerializer()
    customerOrganizationName = OrganizationNameSerializer()
    testBasis = serializers.CharField(max_length=255)
    fireProtectiveAgent = FireProtectiveAgentSerializer(many=True)
    normativeDocumentation = serializers.CharField(max_length=255)
    batchNumber = serializers.CharField(max_length=255)
    batchDate = serializers.DateField()
    fireProtectionOrganizationName = OrganizationNameSerializer()
    fireProtectionObjectType = serializers.CharField(max_length=255)
    fireProtectionObjectCondition = serializers.CharField(max_length=255)
    treatmentMethod = serializers.CharField(max_length=255)
    treatmentArea = serializers.CharField(max_length=255)
    operatingConditions = serializers.CharField(max_length=255)
    testingMethod = serializers.CharField(max_length=255)
    testConditions = serializers.CharField(max_length=255)
    results = ResultForWoodenStructuresSerializer(many=True)
    conclusion = serializers.CharField(max_length=255)
    testConducted = serializers.CharField(max_length=255)


class TESTREPORTFlammabilityTestMethodAndClassificationSerializer(serializers.Serializer):
    testDate = serializers.DateField()
    laboratoryName = serializers.CharField(max_length=255)
    laboratoryAddress = serializers.CharField(max_length=255)
    clientName = serializers.CharField(max_length=255)
    clientAddress = serializers.CharField(max_length=255)
    objectAddress = serializers.CharField(max_length=255)
    testBasis = serializers.CharField(max_length=255)
    normativeDocumentation = serializers.CharField(max_length=255)
    fireProtectionOrganizationName = OrganizationNameSerializer(many=True)
    materialName = serializers.CharField(max_length=255)
    materialCharacteristics = serializers.CharField(max_length=255)
    surfaceDensity = serializers.CharField(max_length=255)
    measuringDevice = serializers.CharField(max_length=255)
    results = LammabilityTestResultSerializer(many=True)
    note = serializers.CharField(max_length=255)
    conclusion = serializers.CharField(max_length=255)


class TESTREPORTForMeasuringTheInsulationResistanceOfWiresAndCablesSerializer(serializers.Serializer):
    testDate = serializers.DateField()
    testObjectName = serializers.CharField(max_length=255)
    testObjectAddress = serializers.CharField(max_length=255)
    results = MeasurementResultSerializer(many=True)
    measurementsOfGroundingDevicesLeakageResistance = MeasurementsOfGroundingDevicesLeakageResistanceSerializer(
        many=True)
    additionalChecks = serializers.CharField(max_length=255)
    environmentalConditions = serializers.CharField(max_length=255)
    normativeDocuments = serializers.CharField(max_length=255)
    measuringInstruments = MeasuringInstrumentsSerializer(many=True)
    conclusionNTD = serializers.CharField(max_length=255)
    testConducted = serializers.CharField(max_length=255)
