# REPLACEMENTS - Defines the default Hex code for BrutusOGX to look for by default
REPLACEMENTS = {
    "Auto 720p": {"search": bytes.fromhex('8002E001'), "replace": bytes.fromhex('0005D002')},
    "Window View": {
        "search": [bytes.fromhex('010707'), bytes.fromhex('010808'), bytes.fromhex('010F11')],
        "replace": bytes.fromhex('020A0B')
    }
}