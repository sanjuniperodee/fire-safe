from auths.models import Category
from rest_framework import serializers


class HotWorkObjectNameSerializer(serializers.Serializer):
    BIN = serializers.CharField(max_length=12)
    objectName = serializers.CharField(max_length=255)


class ObjectNameSerializer(serializers.Serializer):
    rka = serializers.CharField(max_length=255)
    address = serializers.CharField(max_length=255)
    objectName = serializers.CharField(max_length=255)


class ChairmanOfCommisionSerializer(serializers.Serializer):
    IIN = serializers.CharField(max_length=12)
    name = serializers.CharField(max_length=255)
    jobTitle = serializers.CharField(max_length=255)
    BIN = serializers.CharField(max_length=12)
    organizationName = serializers.CharField(max_length=255)
    # Уточнила у Асхата - здесь не нужно менять фио, вбивать будут просто работников, которые даже не числятся в нашей базе


class OrganizationNameSerializer(serializers.Serializer):
    organizationName = serializers.CharField(max_length=255)
    BIN = serializers.CharField(max_length=12)


class FireHydrantSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    manufacturerAddress = serializers.CharField(max_length=255)
    manufacturerTrademark = serializers.CharField(max_length=255)
    manufacturerDesignation = serializers.CharField(max_length=255)
    serialNumber = serializers.CharField(max_length=255)
    height = serializers.IntegerField()
    internalDiameterPassage = serializers.CharField(max_length=255)
    manufacturingYear = serializers.IntegerField()


# Ниже сериализаторы для таблиц из доков
class TestResultSerializer(serializers.Serializer):
    testNumber = serializers.CharField(max_length=255)
    standpipesAndFireHydrantsNumbers = serializers.CharField(max_length=255)
    outletDiameter = serializers.CharField(max_length=255)
    hoseLineLength = serializers.CharField(max_length=255)
    measuredPressure = serializers.CharField(max_length=255)
    requiredPressure = serializers.CharField(max_length=255)
    requiredFlowRate = serializers.CharField(max_length=255)
    requiredJetHeight = serializers.CharField(max_length=255)
    testResults = serializers.CharField(max_length=255)


class StatementSerializer(serializers.Serializer):
    serialNumber = serializers.CharField(max_length=255)
    objectRKANumber = serializers.CharField(max_length=255)
    objectName = serializers.CharField(max_length=255)
    objectAddress = serializers.CharField(max_length=255)
    ownerBIN = serializers.CharField(max_length=255)
    ownerName = serializers.CharField(max_length=255)
    projectPositionAndSpecificationNumber = serializers.CharField(max_length=255)
    instrumentAndEquipmentName = serializers.CharField(max_length=255)
    instrumentAndEquipmentType = serializers.CharField(max_length=255)
    instrumentAndEquipmentSerialNumber = serializers.CharField(max_length=255)
    customerRepresentativeIIN = serializers.CharField(max_length=255)
    customerRepresentativeFullName = serializers.CharField(max_length=255)
    customerRepresentativeJobTitle = serializers.CharField(max_length=255)
    installationOrganizationRepresentativeIIN = serializers.CharField(max_length=255)
    installationOrganizationRepresentativeFullName = serializers.CharField(max_length=255)
    installationOrganizationRepresentativeJobTitle = serializers.CharField(max_length=255)
    caption = serializers.CharField(max_length=255)


class TestingResultSerializer(serializers.Serializer):
    valveNumber = serializers.CharField(max_length=255)
    valveDiaphragmNumber = serializers.CharField(max_length=255)
    allowableDiaphragmDiameter = serializers.CharField(max_length=255)
    measuredDiaphragmDiameter = serializers.CharField(max_length=255)
    valveCycleCount = serializers.CharField(max_length=255)
    leakageSeal = serializers.CharField(max_length=255)
    testResults = serializers.CharField(max_length=255)


class GeneralInformationSerializer(serializers.Serializer):
    rkaObjectNumber = serializers.CharField(max_length=255)
    address = serializers.CharField(max_length=255)
    ownerBIN = serializers.CharField(max_length=255)
    ownerName = serializers.CharField(max_length=255)
    objectPhone = serializers.CharField(max_length=255)
    systemType = serializers.CharField(max_length=255)
    startingMethod = serializers.CharField(max_length=255)
    installationDate = serializers.DateField()
    installationOrganizationBIN = serializers.CharField(max_length=255)
    installationOrganizationName = serializers.CharField(max_length=255)
    fireSystemType = serializers.CharField(max_length=255)
    serviceOrganizationBIN = serializers.CharField(max_length=255)
    serviceOrganizationName = serializers.CharField(max_length=255)
    serviceYear = serializers.DateField()
    serviceOrganizationPhone = serializers.CharField(max_length=255)
    technicalFacilitiesName = serializers.CharField(max_length=255)
    fireSystemTypes = serializers.CharField(max_length=255)
    fireSystemScheme = serializers.CharField(max_length=255)
    manufacturingDate = serializers.DateField()
    operationStartDate = serializers.DateField()
    nextInspectionPeriod = serializers.CharField(max_length=255)


class AccountingForTheResultsOfHydraulicAndElectricalTestSerializer(serializers.Serializer):
    testDate = serializers.DateField()
    testResults = serializers.CharField(max_length=255)
    employeeIIN = serializers.CharField(max_length=255)
    employeeFullName = serializers.CharField(max_length=255)
    conclusion = serializers.CharField(max_length=255)


class AccountingForCheckInAndCheckOutOfDutyAndTechnicalConditionOfTheSystemSerializer(serializers.Serializer):
    acceptanceDate = serializers.DateField()
    acceptanceTime = serializers.CharField(max_length=255)
    systemCondition = serializers.CharField(max_length=255)
    protectedObjects = serializers.CharField(max_length=255)
    systemTypes = serializers.CharField(max_length=255)
    handoverIIN = serializers.CharField(max_length=255)
    handoverFullName = serializers.CharField(max_length=255)
    takeoverIIN = serializers.CharField(max_length=255)
    takeoverFullName = serializers.CharField(max_length=255)


class AccountingForFailuresAndMalfunctionsOfFireAutomaticSystemsAndInstallationsSerializer(serializers.Serializer):
    messageDate = serializers.DateField()
    messageTime = serializers.CharField(max_length=255)
    roomName = serializers.CharField(max_length=255)
    malfunctionType = serializers.CharField(max_length=255)
    employeeIIN = serializers.CharField(max_length=255)
    employeeFullName = serializers.CharField(max_length=255)
    employeePosition = serializers.CharField(max_length=255)
    repairDate = serializers.DateField()
    repairTime = serializers.CharField(max_length=255)


class AccountingForMaintenanceAndScheduledPreventativeRepairsOfFireAutomaticSystemsAndInstallationsSerializer(
    serializers.Serializer):
    workDate = serializers.DateField()
    workTime = serializers.CharField(max_length=255)
    workType = serializers.CharField(max_length=255)
    systemType = serializers.CharField(max_length=255)
    controlledObject = serializers.CharField(max_length=255)
    workCharacter = serializers.CharField(max_length=255)
    workList = serializers.CharField(max_length=255)
    employeeIIN = serializers.CharField(max_length=255)
    employeeFullName = serializers.CharField(max_length=255)
    employeePosition = serializers.CharField(max_length=255)


class AccountingForTestingTheKnowledgeOfPersonnelServicingFireAutomaticSystemsSerializer(serializers.Serializer):
    employeeIIN = serializers.CharField(max_length=255)
    employeeFullName = serializers.CharField(max_length=255)
    employeePosition = serializers.CharField(max_length=255)
    employeeExperience = serializers.CharField(max_length=255)
    checkDate = serializers.DateField()
    knowledgeRating = serializers.CharField(max_length=255)
    checkerIIN = serializers.CharField(max_length=255)
    checkerFullName = serializers.CharField(max_length=255)


class AccountingForActivationOfFireAutomaticSystemsSerializer(serializers.Serializer):
    controlledObjectBIN = serializers.CharField(max_length=255)
    controlledObjectName = serializers.CharField(max_length=255)
    fireSystemView = serializers.CharField(max_length=255)
    fireSystemType = serializers.CharField(max_length=255)
    activationDate = serializers.DateField()
    activationReason = serializers.CharField(max_length=255)
    damageInTenge = serializers.CharField(max_length=255)
    damageDescription = serializers.CharField(max_length=255)
    activationCause = serializers.CharField(max_length=255)


class AccountingForSafetyBriefingsOfTechnicalAndOperationalPersonnelWhenWorkingWithFireAutomaticSystemsSerializer(
    serializers.Serializer):
    personnelType = serializers.CharField(max_length=255)
    employeeIIN = serializers.CharField(max_length=255)
    employeeFullName = serializers.CharField(max_length=255)
    employeePosition = serializers.CharField(max_length=255)
    trainingDate = serializers.DateField()
    trainerIIN = serializers.CharField(max_length=255)
    trainerFullName = serializers.CharField(max_length=255)


class LogbookOfTestingSerializer(serializers.Serializer):
    protocolNumber = serializers.CharField(max_length=255)
    protocolDate = serializers.DateField()
    customerName = serializers.CharField(max_length=255)
    objectName = serializers.CharField(max_length=255)
    address = serializers.CharField(max_length=255)
    testingArea = serializers.CharField(max_length=255)
    contactPhone = serializers.CharField(max_length=255)
    contactEmail = serializers.CharField(max_length=255)
    contactPerson = serializers.CharField(max_length=255)
    nextTestDate = serializers.DateField()
    comment = serializers.CharField(max_length=255)


class mainResultsSerializer(serializers.Serializer):
    systemType = serializers.CharField(max_length=255)
    systemName = serializers.CharField(max_length=255)
    fact = serializers.CharField(max_length=255)
    projectFlowRate = serializers.CharField(max_length=255)
    actualFlowRate = serializers.CharField(max_length=255)
    compliancePercentage = serializers.CharField(max_length=255)


class testResultsSerializer(serializers.Serializer):
    ventilationSystemType = serializers.CharField(max_length=255)
    ventilationSystemName = serializers.CharField(max_length=255)
    ventilationFact = serializers.CharField(max_length=255)
    ventilationProjectPressure = serializers.CharField(max_length=255)
    ventilationProjectSpeed = serializers.CharField(max_length=255)
    ventilationActualPressure = serializers.CharField(max_length=255)
    ventilationActualSpeed = serializers.CharField(max_length=255)
    ventilationConclusion = serializers.CharField(max_length=255)


class strengthTestResultsSerializer(serializers.Serializer):
    testElementName = serializers.CharField(max_length=255)
    numberOfTestPoints = serializers.CharField(max_length=255)
    loadInKiloNewtons = serializers.CharField(max_length=255)
    testingResults = serializers.CharField(max_length=255)


class lightningProtectionResultsSerializer(serializers.Serializer):
    lightningRodType = serializers.CharField(max_length=255)
    numberOfDownconductors = serializers.CharField(max_length=255)
    groundingType = serializers.CharField(max_length=255)
    conductorAirSection = serializers.CharField(max_length=255)
    conductorGroundSection = serializers.CharField(max_length=255)
    weldedConnectionsCondition = serializers.CharField(max_length=255)
    transitionResistance = serializers.CharField(max_length=255)
    groundingResistance = serializers.CharField(max_length=255)
    note = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
    type = serializers.CharField(max_length=255)
    serialNumber = serializers.CharField(max_length=255)
    range = serializers.CharField(max_length=255)
    accuracy = serializers.CharField(max_length=255)
    checkDate = serializers.DateField()


class FireProtectiveAgentSerializer(serializers.Serializer):
    manufacturerDetails = serializers.CharField(max_length=255)
    trademark = serializers.CharField(max_length=255)
    fireProtectionMarking = serializers.CharField(max_length=255)


class ResultForMetalStructuresSerializer(serializers.Serializer):
    observationLocations = serializers.CharField(max_length=255)
    fireproofCoatingThickness = serializers.CharField(max_length=255)
    testResults = serializers.CharField(max_length=255)


class ResultForWoodenStructuresSerializer(serializers.Serializer):
    sampleNumber = serializers.CharField(max_length=255)
    sampleCollectionLocation = serializers.CharField(max_length=255)
    testResults = serializers.CharField(max_length=255)


class LammabilityTestResultSerializer(serializers.Serializer):
    registeredParameters = serializers.CharField(max_length=255)
    alongBase1 = serializers.CharField(max_length=255)
    alongBase2 = serializers.CharField(max_length=255)
    alongBase3 = serializers.CharField(max_length=255)
    alongBase4 = serializers.CharField(max_length=255)
    alongBase5 = serializers.CharField(max_length=255)
    alongBase6 = serializers.CharField(max_length=255)
    alongBase7 = serializers.CharField(max_length=255)
    resultingParametersAlongBase = serializers.CharField(max_length=255)
    alongWeft1 = serializers.CharField(max_length=255)
    alongWeft2 = serializers.CharField(max_length=255)
    alongWeft3 = serializers.CharField(max_length=255)
    alongWeft4 = serializers.CharField(max_length=255)
    alongWeft5 = serializers.CharField(max_length=255)
    alongWeft6 = serializers.CharField(max_length=255)
    alongWeft7 = serializers.CharField(max_length=255)
    resultingParametersAlongWeft = serializers.CharField(max_length=255)


class MeasurementResultSerializer(serializers.Serializer):
    cableSectionAndEquipmentName = serializers.CharField(max_length=255)
    insulationResistanceAB = serializers.CharField(max_length=255)
    insulationResistanceAC = serializers.CharField(max_length=255)
    insulationResistanceBC = serializers.CharField(max_length=255)
    insulationResistanceA0 = serializers.CharField(max_length=255)
    insulationResistanceB0 = serializers.CharField(max_length=255)
    insulationResistanceC0 = serializers.CharField(max_length=255)
    normResistance = serializers.CharField(max_length=255)


class MeasurementsOfGroundingDevicesLeakageResistanceSerializer(serializers.Serializer):
    measurementObject = serializers.CharField(max_length=255)
    normativeResistance = serializers.CharField(max_length=255)
    measuredResistance = serializers.CharField(max_length=255)


class MeasuringInstrumentsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    type = serializers.CharField(max_length=255)
    serialNumber = serializers.CharField(max_length=255)
    voltage = serializers.CharField(max_length=255)
    errorMargin = serializers.CharField(max_length=255)
    nextCalibrationDate = serializers.DateField()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class CategoryRetrieveField(serializers.PrimaryKeyRelatedField):
    def to_internal_value(self, data):
        if isinstance(data, list):
            return [super(CategoryRetrieveField, self).to_internal_value(item) for item in data]
        return super().to_internal_value(data)

    def to_representation(self, value):
        # return value.id
        return CategorySerializer(value).data


class FilesToDeleteRetrieveField(serializers.PrimaryKeyRelatedField):
    def to_internal_value(self, data):
        if isinstance(data, list):
            return [super().to_internal_value(item) for item in data]
        elif isinstance(data, str):
            return [super().to_internal_value(item.strip()) for item in data.split(',') if item.strip()]
        return super().to_internal_value(data)

    def to_representation(self, value):
        return value
