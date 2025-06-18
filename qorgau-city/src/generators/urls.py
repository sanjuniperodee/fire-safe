from django.urls import path

from generators.views import (
    ActOfFireAutomaticAndInstallationViewSet,
    PermissionForHotWorkViewSet,
    ActOfTestingInternalFireFightingWaterSupplySystemViewSet,
    ActOfInspectionWaterSupplyNetworkForWaterDischargeViewSet,
    ActOfInspectionFireHydrantsViewSet,
    ActOfCommissioningFireAutomationSystemsAndInstallationsViewSet,
    ReportOfTestingInternalFireFightingWaterSupplyViewSet,
    StatementOfInstalledDevicesAndEquipmentFireAutomationSystemsInstallationsViewSet,
    TestReportOfValvesFireCranesForOperabilityViewSet,
    OperationalLogOfFireAutomationSystemsInstallationsViewSet,
    LogbookOfTestingLaboratoryProtocolsViewSet,
    TestReportTestingParametersOfVentilationSystemsViewSet,
    TestsToDetermineTheStrengthOfFirefightingExternalStationaryLaddersAndRoofRailingsViewSet,
    ProtocolTestIightningProtectionTestingSystemViewSet,
    FormOfControlTestReportToDetermineTheQualityOfFireRetardantForMetalStructuresViewSet,
    FormOfControlTestReportToDetermineTheQualityOfFireRetardantForWoodenStructuresViewSet,
    TESTREPORTFlammabilityTestMethodAndClassificationViewSet,
    TESTREPORTForMeasuringTheInsulationResistanceOfWiresAndCablesViewSet
)

urlpatterns = [
    path('download/act/fire-automatic-installation', ActOfFireAutomaticAndInstallationViewSet.as_view({
        'post': 'post_fire_automatic_installation'
    })),
    path('download/act/permission-for-hot-work', PermissionForHotWorkViewSet.as_view({
        'post': 'post_permission_hot_work'
    })),
    path('download/act/testing-fire-fighting-system', ActOfTestingInternalFireFightingWaterSupplySystemViewSet.as_view({
        'post': 'post_testing_fire_fighting_system'
    })),
    path('download/act/inspection-water-supply', ActOfInspectionWaterSupplyNetworkForWaterDischargeViewSet.as_view({
        'post': 'post_inspection_water_supply'
    })),
    path('download/act/inspection-fire-hydrants', ActOfInspectionFireHydrantsViewSet.as_view({
        'post': 'post_inspection_fire_hydrants'
    })),
    path('download/act/inspection-fire-automation-systems',
         ActOfCommissioningFireAutomationSystemsAndInstallationsViewSet.as_view({
             'post': 'post_comissioning_fire_automation_systems'
         })),
    path('download/act/testing-fire-fighting-system', ReportOfTestingInternalFireFightingWaterSupplyViewSet.as_view({
        'post': 'post_report_testing_fire_fighting_system'
    })),
    path('download/act/statement-of-devices-and-equipment',
         StatementOfInstalledDevicesAndEquipmentFireAutomationSystemsInstallationsViewSet.as_view({
             'post': 'post_statement_of_devices_and_equipment'
         })),
    path('download/act/test-reports-of-valves', TestReportOfValvesFireCranesForOperabilityViewSet.as_view({
        'post': 'post_test_reports_of_valves'
    })),
    path('download/act/post-operational-log', OperationalLogOfFireAutomationSystemsInstallationsViewSet.as_view({
        'post': 'post_operational_log'
    })),
    path('download/act/post-logbook-of-protocols', LogbookOfTestingLaboratoryProtocolsViewSet.as_view({
        'post': 'post_logbook_of_protocols'
    })),
    path('download/act/post-testing-ventilation', TestReportTestingParametersOfVentilationSystemsViewSet.as_view({
        'post': 'post_testing_ventilation'
    })),
    path('download/act/post-testing-ladders',
         TestsToDetermineTheStrengthOfFirefightingExternalStationaryLaddersAndRoofRailingsViewSet.as_view({
             'post': 'post_testing_ladders'
         })),
    path('download/act/post-testing-lightning-systems', ProtocolTestIightningProtectionTestingSystemViewSet.as_view({
        'post': 'post_testing_lightning_systems'
    })),
    path('download/act/post-testing-quality-of-retardant-for-metal',
         FormOfControlTestReportToDetermineTheQualityOfFireRetardantForMetalStructuresViewSet.as_view({
             'post': 'post_testing_quality_of_retardant_for_metal'
         })),
    path('download/act/post-testing-quality-of-retardant-for-wood',
         FormOfControlTestReportToDetermineTheQualityOfFireRetardantForWoodenStructuresViewSet.as_view({
             'post': 'post_testing_quality_of_retardant_for_wood'
         })),
    path('download/act/post-testing-lammability', TESTREPORTFlammabilityTestMethodAndClassificationViewSet.as_view({
        'post': 'post_testing_lammability'
    })),
    path('download/act/post-testing-wires-and-cables',
         TESTREPORTForMeasuringTheInsulationResistanceOfWiresAndCablesViewSet.as_view({
             'post': 'post_testing_wires_and_cables'
         })),
]
