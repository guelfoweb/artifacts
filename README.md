# artifacts
APK strings analysis

# important:
- This tool is useful for a first analysis
- This tool extracts known strings from the APK
- This tool can produce false positive results
- Always check the results with appropriate tools like Jadx or Bytecode-Viewer


## analysis

```bash
$ python3 artifacts.py aggiornamento.apk
```
## output

```bash
{
    "version": "1.1.0",
    "md5": "ab879f4e8f9cf89652f1edd3522b873d",
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
            ],
            [
                "VHhUeFQ=",
                "TxTxT"
            ]
        ],
        "telegram_id": [],
        "known": [
            "ping"
        ]
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
    "elapsed_time": 5.51
}
```

## similarity

```bash
$ python3 artifacts.py aggiornamento.apk --similarity
```
## output

```bash
+-----------------------+------------+-------------+--------+-------+
|         family        | permission | application | intent | total |
+-----------------------+------------+-------------+--------+-------+
| SpyNote Italy 10/2023 |   100.0    |    100.0    | 100.0  | 100.0 |
| SpyNote Italy 12/2023 |   84.85    |    31.11    | 57.14  |  57.7 |
|         IRATA         |    48.0    |    56.52    | 47.83  | 50.78 |
|     SpyNote Italy     |   84.38    |     1.32    |  56.0  | 47.23 |
|   AlienBot/Cerberus   |   52.63    |     4.65    | 43.64  | 33.64 |
|        MobiTool       |   33.96    |     2.32    | 47.44  |  27.9 |
|         Joker         |   27.03    |     8.45    | 47.69  | 27.72 |
|      SmsSpy Iran      |   28.57    |     2.86    | 50.82  | 27.42 |
|       BadBazaar       |    37.5    |     5.48    | 36.71  | 26.56 |
|        Zanubis        |   32.76    |     0.0     | 46.67  | 26.48 |
|     AndroidMonitor    |   30.23    |     9.09    |  37.5  | 25.61 |
|         Hydra         |   45.28    |     3.08    | 27.27  | 25.21 |
|       XENOMORPH       |    42.0    |     4.17    | 25.93  | 24.03 |
|        SMSAgent       |    38.1    |     0.0     | 32.31  | 23.47 |
|       GoldDigger      |   35.48    |     4.0     | 30.77  | 23.42 |
|          DAAM         |   47.73    |     1.82    | 20.41  | 23.32 |
|         Ermac         |   38.78    |     2.6     | 28.17  | 23.18 |
|          Sova         |   42.59    |     4.35    | 20.75  | 22.57 |
|       GodFather       |    35.9    |     4.05    | 24.49  | 21.48 |
|         SMSRat        |   18.92    |     0.0     | 45.07  | 21.33 |
|        SpyNote        |   46.81    |     0.0     | 15.38  | 20.73 |
|       DroidJack       |   44.74    |     0.0     | 13.46  |  19.4 |
|         Brata         |   36.96    |     2.08    | 13.21  | 17.42 |
|          Octo         |   31.37    |     0.0     | 20.75  | 17.38 |
|        Xloader        |    38.1    |     0.0     | 13.73  | 17.27 |
|      SmsSpy Italy     |   28.57    |     2.11    | 15.69  | 15.45 |
|       CryCrypto       |   18.18    |     2.08    | 12.24  | 10.84 |
+-----------------------+------------+-------------+--------+-------+
```

## report

```bash
$ python3 artifacts.py aggiornamento.apk --report
```
## output

```bash
{
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
}
```