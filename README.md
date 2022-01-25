# OTAGUI

## Introduction
OTAGUI is a web interface for `ota_from_target_files`. Currently, it can only run locally.

`ota_from_target_files` is Android's standard tool for building OTA packages. It's source
is available in [aosp](https://cs.android.com/android/platform/superproject/+/master:build/make/tools/releasetools/ota_from_target_files.py).
Binaries of `ota_from_target_files` is available in [ci.android.com](https://ci.android.com).
For documentation about `ota_from_target_files` , click on the aosp link.

OTAGUI use VUE.js as a frontend and python as a backend interface to ota_from_target_files.

## Usage

### Download otatools.zip
1. Goto https://ci.android.com/builds/branches/aosp-master/grid
2. Click on any of the green squares in aosp_cf_x86_64_phone column
3. Goto artifacts tab and download otatools.zip, put it in the same folder with this README.md

Use `npm build` to install the dependencies.

Create a `target` directory to store the target files and a `output` directory
to store the output files:
```
mkdir target
mkdir output
```

Finally, run the python http-server and vue.js server:
```
python3 web_server.py &
npm run serve
```
### Run with Docker

1. Build the image `docker build -t $USER/ota-generator .`

2. Run: `docker run -it -p 8000:8000 -v target:/app/target -v output:/app/output $USER/ota-generator`
