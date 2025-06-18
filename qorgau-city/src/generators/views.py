import os
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status, viewsets

from generators.serializers import (
    ActOfFireAutomaticSystemsAndInstallationSerializer,
    PermissionForHotWorkSerializer,
    ActOfTestingInternalFireFightingWaterSupplySystemSerializer,
    ActOfInspectionWaterSupplyNetworkForWaterDischargeSerializer,
    ActOfInspectionFireHydrantsSerializer,
    ActOfCommissioningFireAutomationSystemsAndInstallationsSerializer,
    ReportOfTestingInternalFireFightingWaterSupplySerializer,
    StatementOfInstalledDevicesAndEquipmentFireAutomationSystemsInstallationsSerializer,
    TestReportOfValvesFireCranesForOperabilitySerializer,
    OperationalLogOfFireAutomationSystemsInstallationsSerializer,
    LogbookOfTestingLaboratoryProtocolsSerializer,
    TestReportTestingParametersOfVentilationSystemsSerializer,
    TestsToDetermineTheStrengthOfFirefightingExternalStationaryLaddersAndRoofRailingsSerializer,
    ProtocolTestLightningProtectionTestingSystemSerializer,
    FormOfControlTestReportToDetermineTheQualityOfFireRetardantForMetalStructuresSerializer,
    FormOfControlTestReportToDetermineTheQualityOfFireRetardantForWoodenStructuresSerializer,
    TESTREPORTFlammabilityTestMethodAndClassificationSerializer,
    TESTREPORTForMeasuringTheInsulationResistanceOfWiresAndCablesSerializer
)
from generators.utils import (
    certificateOfInspectionOfFireAutomaticSystemsAndInstallations,
    permissionForHotWork,
    testingInternalFireFightingWaterSupplySystem,
    actOfInspectionWaterSupplyNetworkForWaterDischarge,
    actOfInspectionFireHydrants,
    actOfCommissioningFireAutomationSystemsAndInstallations,
    reportOfTestingInternalFireFightingWaterSupply,
    statementOfInstalledDevicesAndEquipmentFireAutomationSystemsInstallations,
    testReportOfValvesFireCranesForOperability,
    operationalLogOfFireAutomationSystemsInstallations,
    logbookOfTestingLaboratoryProtocols,
    testReportTestingParametersOfVentilationSystems,
    testsToDetermineTheStrengthOfFirefightingExternalStationaryLaddersAndRoofRailings,
    protocolTestLightningProtectionTestingSystem,
    formOfControlTestReportToDetermineTheQualityOfFireRetardantForMetalStructures,
    formOfControlTestReportToDetermineTheQualityOfFireRetardantForWoodenStructures,
    TESTREPORTFlammabilityTestMethodAndClassification,
    TESTREPORTForMeasuringTheInsulationResistanceOfWiresAndCables
)
from helpers.logger import log_exception
from helpers.views import BaseViewSet


class ActOfFireAutomaticAndInstallationViewSet(
    BaseViewSet,
    viewsets.GenericViewSet,
    APIView
):
    serializer_class = ActOfFireAutomaticSystemsAndInstallationSerializer
    allowed_methods = ["GET", "POST"]
    pagination_class = None
    permission_classes = []

    def post_fire_automatic_installation(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            docx_file_path = certificateOfInspectionOfFireAutomaticSystemsAndInstallations(serializer.validated_data)

            return self.get_header_with_file(docx_file_path)
        except Exception as e:
            log_exception(f"Error: {e}")
            raise Http404


class PermissionForHotWorkViewSet(
    BaseViewSet,
    viewsets.GenericViewSet,
    APIView
):
    serializer_class = PermissionForHotWorkSerializer
    allowed_methods = ["GET", "POST"]
    pagination_class = None
    permission_classes = []

    def post_permission_hot_work(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            docx_file_path = permissionForHotWork(serializer.validated_data)

            return self.get_header_with_file(docx_file_path)
        except Exception as e:
            log_exception(f"Error: {e}")
            raise Http404


class ActOfTestingInternalFireFightingWaterSupplySystemViewSet(
    BaseViewSet,
    viewsets.GenericViewSet,
    APIView
):
    serializer_class = ActOfTestingInternalFireFightingWaterSupplySystemSerializer
    allowed_methods = ["GET", "POST"]
    pagination_class = None
    permission_classes = []

    def post_testing_fire_fighting_system(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            docx_file_path = testingInternalFireFightingWaterSupplySystem(serializer.validated_data)

            return self.get_header_with_file(docx_file_path)
        except Exception as e:
            log_exception(f"Error: {e}")
            raise Http404


class ActOfInspectionWaterSupplyNetworkForWaterDischargeViewSet(
    BaseViewSet,
    viewsets.GenericViewSet,
    APIView
):
    serializer_class = ActOfInspectionWaterSupplyNetworkForWaterDischargeSerializer
    allowed_methods = ["GET", "POST"]
    pagination_class = None
    permission_classes = []

    def post_inspection_water_supply(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            docx_file_path = actOfInspectionWaterSupplyNetworkForWaterDischarge(serializer.validated_data)

            return self.get_header_with_file(docx_file_path)
        except Exception as e:
            log_exception(f"Error: {e}")
            raise Http404


class ActOfInspectionFireHydrantsViewSet(
    BaseViewSet,
    viewsets.GenericViewSet,
    APIView
):
    serializer_class = ActOfInspectionFireHydrantsSerializer
    allowed_methods = ["GET", "POST"]
    pagination_class = None
    permission_classes = []

    def post_inspection_fire_hydrants(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            docx_file_path = actOfInspectionFireHydrants(serializer.validated_data)

            return self.get_header_with_file(docx_file_path)
        except Exception as e:
            log_exception(f"Error: {e}")
            raise Http404


class ActOfCommissioningFireAutomationSystemsAndInstallationsViewSet(
    BaseViewSet,
    viewsets.GenericViewSet,
    APIView
):
    serializer_class = ActOfCommissioningFireAutomationSystemsAndInstallationsSerializer
    allowed_methods = ["GET", "POST"]
    pagination_class = None
    permission_classes = []

    def post_comissioning_fire_automation_systems(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            docx_file_path = actOfCommissioningFireAutomationSystemsAndInstallations(serializer.validated_data)

            return self.get_header_with_file(docx_file_path)
        except Exception as e:
            log_exception(f"Error: {e}")
            raise Http404


class ReportOfTestingInternalFireFightingWaterSupplyViewSet(
    BaseViewSet,
    viewsets.GenericViewSet,
    APIView
):
    serializer_class = ReportOfTestingInternalFireFightingWaterSupplySerializer
    allowed_methods = ["GET", "POST"]
    pagination_class = None
    permission_classes = []

    def post_report_testing_fire_fighting_system(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            docx_file_path = reportOfTestingInternalFireFightingWaterSupply(serializer.validated_data)

            return self.get_header_with_file(docx_file_path)
        except Exception as e:
            log_exception(f"Error: {e}")
            raise Http404


class StatementOfInstalledDevicesAndEquipmentFireAutomationSystemsInstallationsViewSet(
    BaseViewSet,
    viewsets.GenericViewSet,
    APIView
):
    serializer_class = StatementOfInstalledDevicesAndEquipmentFireAutomationSystemsInstallationsSerializer
    allowed_methods = ["GET", "POST"]
    pagination_class = None
    permission_classes = []

    def post_statement_of_devices_and_equipment(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            docx_file_path = statementOfInstalledDevicesAndEquipmentFireAutomationSystemsInstallations(
                serializer.validated_data)

            return self.get_header_with_file(docx_file_path)
        except Exception as e:
            log_exception(f"Error: {e}")
            raise Http404


class TestReportOfValvesFireCranesForOperabilityViewSet(
    BaseViewSet,
    viewsets.GenericViewSet,
    APIView
):
    serializer_class = TestReportOfValvesFireCranesForOperabilitySerializer
    allowed_methods = ["GET", "POST"]
    pagination_class = None
    permission_classes = []

    def post_test_reports_of_valves(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            docx_file_path = testReportOfValvesFireCranesForOperability(serializer.validated_data)

            return self.get_header_with_file(docx_file_path)
        except Exception as e:
            log_exception(f"Error: {e}")
            raise Http404


class OperationalLogOfFireAutomationSystemsInstallationsViewSet(
    BaseViewSet,
    viewsets.GenericViewSet,
    APIView
):
    serializer_class = OperationalLogOfFireAutomationSystemsInstallationsSerializer
    allowed_methods = ["GET", "POST"]
    pagination_class = None
    permission_classes = []

    def post_operational_log(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            docx_file_path = operationalLogOfFireAutomationSystemsInstallations(serializer.validated_data)

            return self.get_header_with_file(docx_file_path)
        except Exception as e:
            log_exception(f"Error: {e}")
            raise Http404


class LogbookOfTestingLaboratoryProtocolsViewSet(
    BaseViewSet,
    viewsets.GenericViewSet,
    APIView
):
    serializer_class = LogbookOfTestingLaboratoryProtocolsSerializer
    allowed_methods = ["GET", "POST"]
    pagination_class = None
    permission_classes = []

    def post_logbook_of_protocols(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            docx_file_path = logbookOfTestingLaboratoryProtocols(serializer.validated_data)

            return self.get_header_with_file(docx_file_path)
        except Exception as e:
            log_exception(f"Error: {e}")
            raise Http404


class TestReportTestingParametersOfVentilationSystemsViewSet(
    BaseViewSet,
    viewsets.GenericViewSet,
    APIView
):
    serializer_class = TestReportTestingParametersOfVentilationSystemsSerializer
    allowed_methods = ["GET", "POST"]
    pagination_class = None
    permission_classes = []

    def post_testing_ventilation(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            docx_file_path = testReportTestingParametersOfVentilationSystems(serializer.validated_data)

            return self.get_header_with_file(docx_file_path)
        except Exception as e:
            log_exception(f"Error: {e}")
            raise Http404


class TestsToDetermineTheStrengthOfFirefightingExternalStationaryLaddersAndRoofRailingsViewSet(
    BaseViewSet,
    viewsets.GenericViewSet,
    APIView
):
    serializer_class = TestsToDetermineTheStrengthOfFirefightingExternalStationaryLaddersAndRoofRailingsSerializer
    allowed_methods = ["GET", "POST"]
    pagination_class = None
    permission_classes = []

    def post_testing_ladders(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            docx_file_path = testsToDetermineTheStrengthOfFirefightingExternalStationaryLaddersAndRoofRailings(
                serializer.validated_data)

            return self.get_header_with_file(docx_file_path)
        except Exception as e:
            log_exception(f"Error: {e}")
            raise Http404


class ProtocolTestIightningProtectionTestingSystemViewSet(
    BaseViewSet,
    viewsets.GenericViewSet,
    APIView
):
    serializer_class = ProtocolTestLightningProtectionTestingSystemSerializer
    allowed_methods = ["GET", "POST"]
    pagination_class = None
    permission_classes = []

    def post_testing_lightning_systems(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            docx_file_path = protocolTestLightningProtectionTestingSystem(serializer.validated_data)

            return self.get_header_with_file(docx_file_path)
        except Exception as e:
            log_exception(f"Error: {e}")
            raise Http404


class FormOfControlTestReportToDetermineTheQualityOfFireRetardantForMetalStructuresViewSet(
    BaseViewSet,
    viewsets.GenericViewSet,
    APIView
):
    serializer_class = FormOfControlTestReportToDetermineTheQualityOfFireRetardantForMetalStructuresSerializer
    allowed_methods = ["GET", "POST"]
    pagination_class = None
    permission_classes = []

    def post_testing_quality_of_retardant_for_metal(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            docx_file_path = formOfControlTestReportToDetermineTheQualityOfFireRetardantForMetalStructures(
                serializer.validated_data)

            return self.get_header_with_file(docx_file_path)
        except Exception as e:
            log_exception(f"Error: {e}")
            raise Http404


class FormOfControlTestReportToDetermineTheQualityOfFireRetardantForWoodenStructuresViewSet(
    BaseViewSet,
    viewsets.GenericViewSet,
    APIView
):
    serializer_class = FormOfControlTestReportToDetermineTheQualityOfFireRetardantForWoodenStructuresSerializer
    allowed_methods = ["GET", "POST"]
    pagination_class = None
    permission_classes = []

    def post_testing_quality_of_retardant_for_wood(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            docx_file_path = formOfControlTestReportToDetermineTheQualityOfFireRetardantForWoodenStructures(
                serializer.validated_data)

            return self.get_header_with_file(docx_file_path)
        except Exception as e:
            log_exception(f"Error: {e}")
            raise Http404


class TESTREPORTFlammabilityTestMethodAndClassificationViewSet(
    BaseViewSet,
    viewsets.GenericViewSet,
    APIView
):
    serializer_class = TESTREPORTFlammabilityTestMethodAndClassificationSerializer
    allowed_methods = ["GET", "POST"]
    pagination_class = None
    permission_classes = []

    def post_testing_lammability(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            docx_file_path = TESTREPORTFlammabilityTestMethodAndClassification(serializer.validated_data)

            return self.get_header_with_file(docx_file_path)
        except Exception as e:
            log_exception(f"Error: {e}")
            raise Http404


class TESTREPORTForMeasuringTheInsulationResistanceOfWiresAndCablesViewSet(
    BaseViewSet,
    viewsets.GenericViewSet,
    APIView
):
    serializer_class = TESTREPORTForMeasuringTheInsulationResistanceOfWiresAndCablesSerializer
    allowed_methods = ["GET", "POST"]
    pagination_class = None
    permission_classes = []

    def post_testing_wires_and_cables(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            docx_file_path = TESTREPORTForMeasuringTheInsulationResistanceOfWiresAndCables(serializer.validated_data)

            return self.get_header_with_file(docx_file_path)
        except Exception as e:
            log_exception(f"Error: {e}")
            raise Http404
