from pyaxmlparser import APK


def extract_apk_metadata(apk_file_path):
    apk = APK(apk_file_path)
    metadata = {
        "name": apk.application,
        "version": apk.version_name,
        "package_name": apk.package,
    }
    return metadata
