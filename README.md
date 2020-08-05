# Arm Pelion Device Management - Supporting files for Cypress PSoC 64 Workshop

## Contents

- fota_tools
    - manifest tool for generating firmware update manifests for PSoC64
- psoc64_prov_tools
    - App keys to sign PSoC64 applications
    - CA certificate (factory_configurator_utility)
    - example policy file
    - provisioning helper script

## Revision History

- 0.5
    - Update to CYESKIT-064B0S2-4343W
    - Update readme files

- 0.4
    - Fix provisioning script to avoid hang
    - Remove firmware update certificate (users should generate their own which references their Pelion team)
    - update readme files

- 0.3
    - Update readme files
    - Turn off creation of new app keys by default, use the keys provided instead
    - Add firmware update certificate to avoid having to create your own

- 0.2
    - Update provisioning script
    - Add fota tools (manifest tool)

- 0.1
    - Initial version of files to support CY8CKIT-064S2-4343W
