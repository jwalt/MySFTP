MySFTP
================

[![Build Status](https://img.shields.io/travis/SublimeLinter/SublimeLinter/master.svg)](https://github.com/icjmaa/MySFTP)

Plugin de Sublime Text para manejo de archivos mediante conexión SFTP/FTP [Develope for Juan Manuel](https://github.com/icjmaa)
    
    # Uso totalmente gratuito.

Apoyo a proyecto
------------------
Donación de $50.00 pesos - https://www.mercadopago.com.mx/checkout/v1/redirect?pref_id=275534989-c28626d6-b0fd-46bd-8b70-30e4d2144f0a

Donación de $150.00 pesos - https://www.mercadopago.com.mx/checkout/v1/redirect?pref_id=275534989-c47f2492-8e41-4abb-be54-b92feb993095

Donación de $300.00 pesos - https://www.mercadopago.com.mx/checkout/v1/redirect?pref_id=275534989-a53fcf28-9cac-4ccc-90e7-485f8b54a49b


:muscle: :sunglasses: :punch:
<p align="center"><img src ="https://upload.wikimedia.org/wikipedia/en/d/d2/Sublime_Text_3_logo.png" width="128px"/></p>

Mode of use.
-------------------

- From the Sublime Text menu: File > MySftp
    - **New Server :** We create a configuration file for the SFTP/FTP connection with our server.
        - **Nick :** Username that will occupy the files.
        - **type :** Type of connection to the server (SFTP or FTP).
        - **host :** IP(v4) or Domain name of the server to which you want to connect.
        - **user :** Username with which to log in to make the connection.
        - **password :** Password with which the previously assigned user will log in.
        - **port :** Port to be used for the default connection 22 for SFTP and 21 for FTP.
        - **remote_path :** Main path of the server to list.

    - **List Server :** Lists previously configured servers.
    - **Edit Server :** Allows us to make changes to the configuration of existing servers.
    - **Delete Server :** Deletes the server configurations.

- Combination of keys
    - Use the key combination <kbd>Ctrl+Alt+L</kbd> , <kbd>Ctrl+Alt+S</kbd>, to list the configured servers.

## Navigation

1. Press the **Enter** key on the server you want to work on, it will immediately list the directory assigned as main in the configuration file.
2. You can choose between the following options:
    - Change server.
    - Level up the current directory.
    - Create a new file in the current directory.
    - Create a new folder in the current directory.
    - Rename the current directory.
    - Change permissions to the current directory.
    - Delete delete the current directory.
    
    \( The last 6 options require permissions on linux servers \)
3. By selecting a file from the list you can perform the following actions:
    - Change server.
    - Return to the previous list.
    - Edit, it will open in a new tab, when it is automatically saved it will be updated on the server.
    - Rename the file on the server.
    - Change permissions for the selected file.
    - Delete selected file on the server.
    
    \( The last 6 options require permissions on linux servers \)
4. If you select a directory, the same menu as step 2 will be displayed.

Estado
-------------------

En Desarrollo :computer: :coffee:

Notas
-------------------

It is recommended to make a backup before you start using it as it is in an early stage of development and may damage your documents.
