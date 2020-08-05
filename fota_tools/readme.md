# Arm Pelion Device Management - Manifest Tool for Cypress PSoC 64

  Firmware updates on PSoC 64 with Pelion Device Management requires a custom version of Pelion manifest tool.

## Reason for this custom version
  Usually, Pelion Device Management uses a timestamp to track versions of firmware.  The service is able to verify a firmware update was successful based on the version timestamp reported by devices.  However, PSoC64 uses an explicit version number that gets built into the application.  This version of the manifest tool has been updated to use the PSoC64 versioning system.

  - For more information including licensing on the manifest tool see https://github.com/ARMmbed/manifest-tool

## Test environment details:
  - Board - CYESKIT-064B0S2-4343W, pre-provisioned for Pelion first-to-claim
  - Python - 3.7
  - Mbed OS - 5.14
  - Application Repo - https://github.com/ARMmbed/mbed-os-example-pelion-psoc64-release

## The fota_tools directory includes:

  - manifest-tool-1.5.3.tar.gz - Custom manifest tool

## Steps to perform a firmware update on a provisioned device:

  0.  Install the custom manifest tool

    ```
    pip install manifest-tool-1.5.3.tar.gz
    ```

  1. Configure the device application

    - Import an app. Here is an example:

    ```
    mbed import https://github.com/armmbed/mbed-os-example-pelion-psoc64-release example-pelion
    cd example-pelion
    ```

    - Set the WiFi credentials in mbed_app.json

    - Init the manifest tool and (Optionally) generate a firmware update certificate.  

      If you already have an update certificate

          - Copy the `update_default_resources.c` file and `.update-certificates` folder to your project directory.    
          - Issue this command

        ```
        manifest-tool init -a <api key> -d "<your company name.com>" -m "<product model identifier>" --force -q
        ```

      If you don't already have an update certificate

          - Issue this command

        ```
        manifest-tool init -a <api key> -d "maclobprod.com" -m "<product model identifier>" -c  <certificate>
        ```
        Please Note - this second option will create a new update certificate. If the devices has been used previously, this requires that the storage be reset. See below.


  2. Compile the application

    ```
    mbed compile -m CYESKIT_064B0S2_4343W -t ARM --profile release
    ```

    Note - if you changed the update certificate in the last step, update the storage by passing in the additional flag `-DRESET_STORAGE` in the last command. See Important Notes section below.

  3. Flash and run the application

    - drag and drop the hex file output to the mounted drive for the board

        BUILD/CYESKIT_064B0S2_4343W/ARM-RELEASE/example-pelion.hex

    - reset the board, view the terminal output.  Ensure it connects to Pelion.  

    - If using first-to-claim, copy the enrollment ID and enroll the device in the pelion portal. Then reset the board again.  See separate instructions.

    - In the terminal, find your Device ID

  2. Make a modification to the Application.

  3. Increment the version of the update image in the file

      mbed-os/targets/TARGET_Cypress/TARGET_PSOC6/TARGET_CYESKIT_064B0S2_4343W/secure_image_parameters.json

      ```
      "boot1" : {
          "VERSION" : "0.3",
          "ROLLBACK_COUNTER" : "0"
      },
      ```

  3. Re-build the application

      ```
      mbed compile -m CYESKIT_064B0S2_4343W -t ARM --profile release
      ```

  4. Call the manifest tool

      - use  the command line param: --fw-version <same version as specified in step 2>.

      ```
      manifest-tool update device -p BUILD/CYESKIT_064B0S2_4343W/ARM-RELEASE/example-pelion_upgrade_signed.bin -D <device ID> --fw-version 3  
      ```

      The above command will update fw image to version 0.3 (0 - major, 3 - minor).

      The firmware version is a 64 bit unsigned integer, where 32 MSBs represent the major version and 32 LSBs represent the minor. For example, version 1.0 represented as 0x0000000100000000 and version 1.1 as 0x0000000100000001. --fw-version accepts only decimal values, so you need to convert the above values to decimals. Example: If you would like to upgrade to version 1.1 you need to type --fw-version 4294967297.


  5. View the device terminal to check that the new image was downloaded, applied, and booted

## Important Notes
  - If you encounter problems, you may need to clean the storage.  Follow these steps. This will allow you to re-run the enrollment flow.

      1. Compile the application with -DRESET_STORAGE flag.

          ```
          mbed compile -m CYESKIT_064B0S2_4343W -t ARM --profile release -DRESET_STORAGE
          ```
      2. Flash it, reset the board and let it run.  

      3. Go back to step 0, compile and flash without the reset storage macro set
