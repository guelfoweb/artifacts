# artifacts
APK strings analysis

# important:
- This tool is useful for a first analysis
- This tool extracts known strings from the APK
- This tool can produce false positive results
- Always check the results with appropriate tools like Jadx or Bytecode-Viewer


## cmd

```bash
$ python3 artifacts.py aggiornamento.apk
```
## output

```bash
{
    "version": "1.0.4",
    "md5": "ab879f4e8f9cf89652f1edd3522b873d",
    "activity": {
        "permission": [
            "android.permission.ACCESS_COARSE_LOCATION",
            "android.permission.ACCESS_FINE_LOCATION",
            "android.permission.ACCESS_NETWORK_STATE",
            "android.permission.ACCESS_WIFI_STATE",
            "android.permission.BIND_ACCESSIBILITY_SERVICE",
            "android.permission.BIND_DEVICE_ADMIN",
            "android.permission.BIND_INPUT_METHOD",
            "android.permission.BIND_JOB_SERVICE",
            "android.permission.BIND_VPN_SERVICE",
            "android.permission.CALL_PHONE",
            "android.permission.CAMERA",
            "android.permission.CHANGE_WIFI_STATE",
            "android.permission.DISABLE_KEYGUARD",
            "android.permission.FOREGROUND_SERVICE",
            "android.permission.GET_ACCOUNTS",
            "android.permission.INTERNET",
            "android.permission.READ_CALL_LOG",
            "android.permission.READ_CONTACTS",
            "android.permission.READ_EXTERNAL_STORAGE",
            "android.permission.READ_PHONE_STATE",
            "android.permission.READ_SMS",
            "android.permission.RECEIVE_BOOT_COMPLETED",
            "android.permission.RECORD_AUDIO",
            "android.permission.REQUEST_DELETE_PACKAGES",
            "android.permission.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS",
            "android.permission.REQUEST_INSTALL_PACKAGES",
            "android.permission.SEND_SMS",
            "android.permission.SET_WALLPAPER",
            "android.permission.SYSTEM_ALERT_WINDOW",
            "android.permission.USE_FULL_SCREEN_INTENT",
            "android.permission.WAKE_LOCK",
            "android.permission.WRITE_EXTERNAL_STORAGE"
        ],
        "application": [
            "com.android.alarm.permission.SET",
            "com.android.dynamic.apk.fused.modules",
            "com.android.internal.category.PLATLOGO",
            "com.android.settings",
            "com.android.stamp.source",
            "com.android.stamp.type",
            "com.android.vending.billing.InAppBillingService.COIN",
            "com.android.vending.billing.InAppBillingService.COIO",
            "com.android.vending.billing.InAppBillingService.INST",
            "com.android.vending.billing.InAppBillingService.LUCM",
            "com.android.vending.billing.InAppBillingService.PROX",
            "com.android.vending.derived.apk.id",
            "com.asus.mobilemanager",
            "com.coloros.safecenter",
            "com.evenwell.powersaving",
            "com.google.android.apps.maps",
            "com.google.android.apps.pixelmigrate",
            "com.google.android.apps.restore",
            "com.google.android.gms.car.application",
            "com.google.android.gms.version",
            "com.google.android.maps.v2.API",
            "com.htc.intent.action.QUICKBOOT",
            "com.huawei.permission.external",
            "com.huawei.systemmanager",
            "com.instagram.android",
            "com.instagram.boomerang",
            "com.iqoo.secure",
            "com.letv.android.letvsafe",
            "com.miui.permcenter",
            "com.miui.securitycenter",
            "com.nokia.payment.iapenabler.InAppBillingService.BIND",
            "com.oculus.home",
            "com.oculus.horizon",
            "com.oneplus",
            "com.oplus",
            "com.oplus.battery",
            "com.oppo.safe",
            "com.samsung.android",
            "com.ui.OnAlarmReceiver.ACTION",
            "com.vivo.permissionmanager",
            "com.whatsapp.action.INSTRUMENTATION",
            "com.whatsapp.otp.OTP",
            "com.whatsapp.w4b"
        ],
        "intent": [
            "android.intent.action.ACTION",
            "android.intent.action.BOOT",
            "android.intent.action.CHOOSER",
            "android.intent.action.DATE",
            "android.intent.action.GET",
            "android.intent.action.LOCKED",
            "android.intent.action.MAIN",
            "android.intent.action.MEDIA",
            "android.intent.action.MY",
            "android.intent.action.PACKAGE",
            "android.intent.action.PACKAGES",
            "android.intent.action.PHONE",
            "android.intent.action.PROCESS",
            "android.intent.action.QUICKBOOT",
            "android.intent.action.REBOOT",
            "android.intent.action.SCREEN",
            "android.intent.action.SEARCH",
            "android.intent.action.SEND",
            "android.intent.action.TIME",
            "android.intent.action.TIMEZONE",
            "android.intent.action.UNINSTALL",
            "android.intent.action.USER",
            "android.intent.action.VIEW",
            "android.intent.category.BROWSABLE",
            "android.intent.category.DEFAULT",
            "android.intent.category.HOME",
            "android.intent.category.INFO",
            "android.intent.category.LAUNCHER",
            "android.intent.category.LEANBACK",
            "android.intent.category.OPENABLE",
            "android.intent.extra.BCC",
            "android.intent.extra.CC",
            "android.intent.extra.COMPONENT",
            "android.intent.extra.EMAIL",
            "android.intent.extra.HTML",
            "android.intent.extra.PROCESS",
            "android.intent.extra.REFERRER",
            "android.intent.extra.RETURN",
            "android.intent.extra.START",
            "android.intent.extra.STREAM",
            "android.intent.extra.SUBJECT",
            "android.intent.extra.TEXT",
            "android.intent.extra.shortcut.ICON",
            "android.intent.extra.shortcut.INTENT",
            "android.intent.extra.shortcut.NAME",
            "android.intent.ga.SEND",
            "android.intent.ga.VIEW",
            "ga.intent.action.PICK",
            "htc.intent.action.QUICKBOOT",
            "miui.intent.action.APP",
            "miui.intent.action.BOOT",
            "miui.intent.action.OP",
            "miui.intent.action.POWER",
            "payments.intent.action.STEP"
        ]
    },
    "dex": [
        "classes.dex"
    ],
    "library": [],
    "network": {
        "ip": [
            "1.0.0.1",
            "1.1.1.1",
            "8.8.4.4",
            "8.8.8.8",
            "54.63.34.15"
        ],
        "url": [
            "https://static-maps.yandex.ru/1.x/?ll=%.6f",
            "https://static-maps.yandex.ru/1.x/?ll=%.6f",
            "tg://telegram.org"
        ],
        "param": [
            "action="
        ]
    },
    "root": [],
    "string": {
        "base64": [
            [
                "MTc4LjIzNi4yNDcuMTI0",
                "178.236.247.124"
            ],
            [
                "Nzc3MQ==",
                "7771"
            ]
        ],
        "telegram_id": [],
        "known": []
    },
    "family": {
        "name": "SpyNote Italy 10/2023",
        "match": 100.0,
        "value": {
            "permission": 100.0,
            "application": 100.0,
            "intent": 100.0
        }
    },
    "sandbox": [
        "https://tria.ge/s?q=ab879f4e8f9cf89652f1edd3522b873d",
        "https://www.joesandbox.com/search?q=ab879f4e8f9cf89652f1edd3522b873d",
        "https://www.virustotal.com/gui/search/ab879f4e8f9cf89652f1edd3522b873d",
        "https://bazaar.abuse.ch/browse.php?search=md5:ab879f4e8f9cf89652f1edd3522b873d"
    ],
    "report": {
        "LOCATION": [
            [
                "ACCESS_COARSE_LOCATION",
                "Allows an app to access approximate location."
            ],
            [
                "ACCESS_FINE_LOCATION",
                "Allows an app to access precise location."
            ]
        ],
        "NETWORK": [
            [
                "ACCESS_NETWORK_STATE",
                "Allows applications to access information about networks."
            ],
            [
                "ACCESS_WIFI_STATE",
                "Allows applications to access information about Wi-Fi networks."
            ],
            [
                "CHANGE_WIFI_STATE",
                "Allows applications to change Wi-Fi connectivity state."
            ],
            [
                "INTERNET",
                "Allows applications to open network sockets."
            ]
        ],
        "ACCESSIBILITY": [
            [
                "BIND_ACCESSIBILITY_SERVICE",
                "Must be required by an AccessibilityService, to ensure that only the system can bind to it."
            ]
        ],
        "PHONE_CALLS": [
            [
                "CALL_PHONE",
                "Allows an application to initiate a phone call without going through the Dialer user interface for the user to confirm the call."
            ],
            [
                "READ_PHONE_STATE",
                "Allows read only access to phone state, including the current cellular network information, the status calls, and a list Accounts registered on the device."
            ]
        ],
        "CAMERA": [
            [
                "CAMERA",
                "Required to be able to access the camera device."
            ]
        ],
        "SCREENLOCK": [
            [
                "DISABLE_KEYGUARD",
                "Allows applications to disable the keyguard if it is not secure."
            ]
        ],
        "ACCOUNTS": [
            [
                "GET_ACCOUNTS",
                "Allows access to the list of accounts in the Accounts Service."
            ]
        ],
        "SOCIAL_INFO": [
            [
                "READ_CALL_LOG",
                "Allows an application to read the user's call log."
            ],
            [
                "READ_CONTACTS",
                "Allows an application to read the user's contacts data."
            ]
        ],
        "STORAGE": [
            [
                "READ_EXTERNAL_STORAGE",
                "Allows an application to read from external storage."
            ],
            [
                "WRITE_EXTERNAL_STORAGE",
                "Allows an application to write to external storage."
            ]
        ],
        "MESSAGES": [
            [
                "READ_SMS",
                "Allows an application to read SMS messages."
            ],
            [
                "SEND_SMS",
                "Allows an application to send SMS messages."
            ]
        ],
        "APP_INFO": [
            [
                "RECEIVE_BOOT_COMPLETED",
                "Allows an application to receive the Intent."
            ]
        ],
        "MICROPHONE": [
            [
                "RECORD_AUDIO",
                "Allows an application to record audio."
            ]
        ],
        "WALLPAPER": [
            [
                "SET_WALLPAPER",
                "Allows applications to set the wallpaper."
            ]
        ],
        "DISPLAY": [
            [
                "SYSTEM_ALERT_WINDOW",
                "Allows an app to create windows using the type WindowManager. Shown on top of all other apps."
            ]
        ],
        "AFFECTS_BATTERY": [
            [
                "WAKE_LOCK",
                "Allows using PowerManager WakeLocks to keep processor from sleeping or screen from dimming."
            ]
        ]
    },
    "elapsed_time": 5.01
}
```
