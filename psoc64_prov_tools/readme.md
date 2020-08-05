# Arm Pelion Device Management - Provisioning for Cypress PSoC 64

  - With this information you can provision an un-provisioned PSoC 64 device the same way as done during Arm Pelion DM initial testing for PSoC 64.

## Test environment details:
  - Board - CYESKIT-064B0S2-4343W
  - CySecureTools Version - v1.3.3
  - Python - 3.7

## The psoc64_prov_tools directory includes:
  - app_key folder
      - are the keys will be used to sign the app image. Copy to mbed-os/targets/TARGET_Cypress/TARGET_PSOC6/sb-tools/keys.
  - policy_single_stage_CM4_2m.json file
      - is the policy file used to provision the device during initial testing. Overwrite use an existing file under mbed-os/targets/TARGET_Cypress/TARGET_PSOC6/sb-tools/policy.
  - factory_configurator_utility/keystore/ fcu_private_key.pem
      - The Root CA private key that will sign the device certificate.
  - factory_configurator_utility/keystore/ fcu.crt
      - The Root CA Certificate, the issuer of the device certificate that you should load to the Pelion portal.
  - prov_helper_tool.py
      - Python script used to run the provisioning process. Note, create_app_keys() is comment out because you want to generate the app keys only once.

## Summary of Provisioning Steps:

  1. Install Python 3.6 or 3.7
  2. Create a directory
    ```
      mkdir psoc64-prov
	    cd psoc64-prov
    ```  
  3. Create and activate a Python Virtual Environment (Optional)
      ```
      python3 -m venv env
	    .\env\Scripts\activate.bat
      ```
  4. Install pyopenssl
      ```
      pip install -U pyopenssl
      ```
  5. Install cysecuretools
      ```
      pip install -U cysecuretools
      ```
  6. Configure the debug interface to KitProg3 CMSIS DAP Mode

    - Connect the USB. The status light will come on, indicating it has power
    - Press the Mode button until the LED2 stops blinking (stays on solid)
    - The kit should now be connected in KitProg3 CMSIS-DAP mode


  7. From psoc64_prov_tools directory, run the script
     ```
     python prov_helper_tool.py
     ```
     If it does not work, see Issus & Known Workarounds section for more information.

  6. During running of script, when prompted, provide a unique device serial number (numerical value only)

    - If completed successfully, you should see this result
    ```
    *****************************************
           PROVISIONING PASSED
    *****************************************
    ```
  7. Configure the debug interface to DAPLink mode

    - Connect the USB. The status light will come on, indicating it has power
    - Press the Mode button until the LED2 blinks the most quickly  
    - The kit should now be connected in DAPLink mode

  8. Deactivate Python Virtual Environment (Optional)

    Change directory back to the top where the environment was activated.
    Then issue this command.
    ```
    .\env\Scripts\deactivate.bat
    ```

  9. Ensure that the DAPLink is configured correctly.

    - In a command prompt, type `mbedls` to check the board name that is reported back.

    - If it is not `CYESKIT_064B0S2_4343W`, then follow the instructions in the addendum below.

## Build & Run Mbed OS:
  1. Copy keys and policy file into mbed os.
        mbed-os/targets/TARGET_Cypress/TARGET_PSOC6/sb-tools/keys
        mbed-os/targets/TARGET_Cypress/TARGET_PSOC6/sb-tools/policy

  2. Copy the update resources file and update certificate folder into your project folder.

        update_default_resources.c
        .update-certificates

  2. Build Mbed OS.  The application is signed and the board will only boot the application if the correct key is used.

  ```
     mbed compile -m CYESKIT_064B0S2_4343W -t ARM --profile
  ```

  3. Download, run, check output.


## Addendum - Debug Interface Setup

1. Connect the USB. The status light will come on, indicating it has power
2. Ensure the kit is in CMSIS-DAP mode (LED2 & LED4 on, not blinking)         
3. Download the fw-loader from Cypress Semiconductor Github.
   https://github.com/cypresssemiconductorco/Firmware-loader
4. Extract the files
5. On a command line, enter directory `fw-loader\bin`
6. Execute the following commands in command line,
`fw-loader.exe --update-kp3`
`fw-loader --uid-set CYESKIT_064B0S2_4343W`
7. After command is executed successfully please press the Mode button two times until the LED2 blinks quickly.  
8. Kit should now be connected in DAPLink mode with the correct ID set


## Known Issues & Workarounds

1. During the first stage (reading of private key from the device)  
    - The script sometimes is not be able to make a connection to the board
    - If it gets stuck, press the Mode button to change the KitProg3 mode to Bulk mode (LED blinking slowly).

2. During the second stage (provisioning of the packet)
    - The script may get stuck
    - If it gets stuck, cancel the script (Ctrl + C), then run the following commands manually.
    - Enter python interpreter mode

    `python`

    - Then type these commands (you can copy them from the script)
    ```
    from cysecuretools import CySecureTools
    cytools = CySecureTools('CY8CPROTO-064S2-SB', 'policy_single_stage_CM4_2m.json’)
    cytools.provision_device()
    ```

    - After the script completes, quit the python interpreter mode

    `quit()`
