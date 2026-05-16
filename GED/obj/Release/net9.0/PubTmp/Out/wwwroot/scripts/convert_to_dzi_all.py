import os
import subprocess
import sys
from pathlib import Path
import argparse

def check_vips_installation():
    """Check if VIPS is installed"""
    try:
        subprocess.run(['vips', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def is_already_converted(tif_file, output_folder):
    """Check if TIFF file is already converted to DZI"""
    output_path = Path(output_folder)
    dzi_file = output_path / f"{tif_file.stem}.dzi"
    tiles_dir = output_path / f"{tif_file.stem}_files"
    
    return dzi_file.exists() and tiles_dir.exists() and list(tiles_dir.glob('**/*.jpg'))

def convert_tif_to_dzi_vips(input_folder, output_folder, tile_size=256, overlap=1):
    """Convert TIFF images to DZI format using VIPS"""
    
    if not check_vips_installation():
        print("VIPS n'est pas installé")
        return

    input_path = Path(input_folder)
    output_path = Path(output_folder)
    
    if not input_path.exists():
        print("Dossier d'entrée introuvable")
        return
    
    output_path.mkdir(parents=True, exist_ok=True)

    # Get all TIFF files
    tif_files = list(input_path.glob("**/*.tif")) + list(input_path.glob("**/*.tiff"))
    
    if not tif_files:
        print("Aucun fichier TIFF trouvé")
        return

    # Separate files to convert and already converted
    files_to_convert = []
    already_converted = []
    
    for tif_file in tif_files:
        if is_already_converted(tif_file, output_folder):
            already_converted.append(tif_file)
        else:
            files_to_convert.append(tif_file)

    # Show already converted files
    for tif_file in already_converted:
        print(f"Déjà converti: {tif_file.name}")

    if not files_to_convert:
        print("Tous les fichiers sont déjà convertis")
        return

    print(f"Conversion de {len(files_to_convert)} fichiers...")
    
    successful = 0
    for tif_file in files_to_convert:
        try:
            output_base = output_path / tif_file.stem
            
            cmd = [
                'vips', 'dzsave',
                str(tif_file),
                str(output_base),
                '--tile-size', str(tile_size),
                '--overlap', str(overlap),
                '--suffix', '.jpg[Q=85]'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(f"✓ {tif_file.name}")
                successful += 1
            else:
                print(f"✗ {tif_file.name}")
                        
        except subprocess.TimeoutExpired:
            print(f"⏰ {tif_file.name}")
        except Exception:
            print(f"✗ {tif_file.name}")

    print(f"Terminé: {successful}/{len(files_to_convert)} fichiers convertis avec succès")

def main():
    parser = argparse.ArgumentParser(description='Convert TIFF images to DZI format')
    parser.add_argument('input_folder', help='Input folder containing TIFF files')
    parser.add_argument('output_folder', help='Output folder for DZI files')
    parser.add_argument('--tile-size', type=int, default=256, help='Tile size (default: 256)')
    parser.add_argument('--overlap', type=int, default=1, help='Tile overlap (default: 1)')
    
    args = parser.parse_args()
    
    convert_tif_to_dzi_vips(
        args.input_folder, 
        args.output_folder, 
        args.tile_size, 
        args.overlap
    )

if __name__ == "__main__":
    main()

# import os
# import subprocess
# import sys
# from pathlib import Path
# import argparse

# def check_vips_installation():
#     """Check if VIPS is installed"""
#     print("🔍 Vérification de l'installation de VIPS...")
#     try:
#         result = subprocess.run(['vips', '--version'], capture_output=True, text=True, check=True)
#         print(f"✅ VIPS est installé: {result.stdout.strip()}")
#         return True
#     except (subprocess.CalledProcessError, FileNotFoundError) as e:
#         print(f"❌ VIPS non trouvé: {e}")
#         return False

# def install_vips():
#     """Install VIPS on the system"""
#     print("🔄 Tentative d'installation de VIPS...")
#     system = sys.platform.lower()
#     print(f"📋 Système détecté: {system}")
    
#     if system.startswith('win'):
#         print("❌ Windows: Veuillez installer VIPS manuellement depuis: https://github.com/libvips/libvips/releases")
#         return False
#     elif system.startswith('darwin'):  # macOS
#         try:
#             print("🍎 macOS: Installation via Homebrew...")
#             subprocess.run(['brew', 'install', 'vips'], check=True)
#             print("✅ VIPS installé avec succès sur macOS")
#             return True
#         except subprocess.CalledProcessError as e:
#             print(f"❌ Échec de l'installation sur macOS: {e}")
#             print("💡 Veuillez installer Homebrew d'abord: https://brew.sh/")
#             return False
#     else:  # Linux
#         try:
#             print("🐧 Linux (Debian/Ubuntu): Installation via apt...")
#             subprocess.run(['sudo', 'apt', 'install', 'libvips-tools'], check=True)
#             print("✅ VIPS installé avec succès sur Linux")
#             return True
#         except subprocess.CalledProcessError as e:
#             print(f"❌ Échec avec apt: {e}")
#             try:
#                 print("🐧 Linux (RedHat/CentOS): Installation via yum...")
#                 subprocess.run(['sudo', 'yum', 'install', 'vips-tools'], check=True)
#                 print("✅ VIPS installé avec succès sur Linux")
#                 return True
#             except subprocess.CalledProcessError as e2:
#                 print(f"❌ Échec avec yum: {e2}")
#                 print("💡 Veuillez installer VIPS via votre gestionnaire de paquets")
#                 return False

# def convert_tif_to_dzi_vips(input_folder, output_folder, tile_size=256, overlap=1):
#     """
#     Convert TIFF images to DZI format using VIPS
#     """
#     print(f"\n🎯 Début de la conversion DZI")
#     print(f"📁 Dossier d'entrée: {input_folder}")
#     print(f"📁 Dossier de sortie: {output_folder}")
#     print(f"⚙️  Paramètres: tile_size={tile_size}, overlap={overlap}")

#     if not check_vips_installation():
#         print("❌ VIPS non trouvé. Tentative d'installation...")
#         if not install_vips():
#             print("❌ Échec de l'installation de VIPS. Veuillez l'installer manuellement.")
#             return
#     else:
#         print("✅ VIPS est déjà installé")

#     input_path = Path(input_folder)
#     output_path = Path(output_folder)
    
#     print(f"📂 Chemin d'entrée absolu: {input_path.absolute()}")
#     print(f"📂 Chemin de sortie absolu: {output_path.absolute()}")
    
#     # Vérifier si le dossier d'entrée existe
#     if not input_path.exists():
#         print(f"❌ Le dossier d'entrée n'existe pas: {input_path}")
#         return
    
#     # Créer le dossier de sortie
#     output_path.mkdir(parents=True, exist_ok=True)
#     print(f"✅ Dossier de sortie créé/vérifié: {output_path}")

#     # Get all TIFF files
#     print(f"\n🔍 Recherche des fichiers TIFF dans: {input_path}")
#     tif_files = list(input_path.glob("**/*.tif")) + list(input_path.glob("**/*.tiff"))
    
#     print(f"📊 Fichiers trouvés avec glob:")
#     print(f"   *.tif: {list(input_path.glob('**/*.tif'))}")
#     print(f"   *.tiff: {list(input_path.glob('**/*.tiff'))}")
    
#     if not tif_files:
#         print(f"❌ Aucun fichier TIFF trouvé dans {input_folder}")
#         print("💡 Vérifiez:")
#         print("   - L'extension des fichiers (.tif ou .tiff)")
#         print("   - Les permissions du dossier")
#         print("   - Que les fichiers ne sont pas vides")
#         return

#     print(f"✅ {len(tif_files)} fichiers TIFF trouvés:")
#     for i, tif_file in enumerate(tif_files, 1):
#         print(f"   {i}. {tif_file.name} ({tif_file.stat().st_size / 1024 / 1024:.2f} MB)")

#     print(f"\n🔄 Début de la conversion...")
    
#     for tif_file in tif_files:
#         try:
#             print(f"\n📄 Traitement de: {tif_file.name}")
#             print(f"   📍 Chemin complet: {tif_file.absolute()}")
#             print(f"   📏 Taille: {tif_file.stat().st_size / 1024 / 1024:.2f} MB")
            
#             # Vérifier si le fichier est accessible
#             if not tif_file.exists():
#                 print(f"   ❌ Fichier non trouvé: {tif_file}")
#                 continue
                
#             # Output paths
#             output_base = output_path / tif_file.stem
#             output_dzi = output_path / f"{tif_file.stem}.dzi"
#             tiles_dir = output_path / f"{tif_file.stem}_files"
            
#             print(f"   📁 Fichier DZI de sortie: {output_dzi}")
#             print(f"   📁 Dossier des tuiles: {tiles_dir}")
            
#             # VIPS command to create DZI
#             cmd = [
#                 'vips', 'dzsave',
#                 str(tif_file),
#                 str(output_base),  # Base name without extension
#                 '--tile-size', str(tile_size),
#                 '--overlap', str(overlap),
#                 '--suffix', '.jpg[Q=85]'
#             ]
            
#             print(f"   🖥️  Commande exécutée: {' '.join(cmd)}")
            
#             # Exécuter la commande avec timeout
#             result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)  # 5 minutes timeout
            
#             print(f"   📤 Sortie standard: {result.stdout}")
#             print(f"   📥 Sortie d'erreur: {result.stderr}")
#             print(f"   🔢 Code de retour: {result.returncode}")
            
#             if result.returncode == 0:
#                 # Vérifier que les fichiers ont été créés
#                 if output_dzi.exists():
#                     print(f"   ✅ Fichier DZI créé: {output_dzi}")
#                 else:
#                     print(f"   ⚠️  Fichier DZI non trouvé: {output_dzi}")
                    
#                 if tiles_dir.exists():
#                     tile_count = sum(1 for _ in tiles_dir.glob('**/*.jpg'))
#                     print(f"   ✅ Dossier de tuiles créé: {tiles_dir} ({tile_count} tuiles)")
#                 else:
#                     print(f"   ⚠️  Dossier de tuiles non trouvé: {tiles_dir}")
                    
#             else:
#                 print(f"   ❌ Erreur lors de la conversion")
#                 print(f"   💡 Suggestions:")
#                 print(f"      - Vérifiez que le fichier TIFF n'est pas corrompu")
#                 print(f"      - Essayez avec un fichier plus petit d'abord")
#                 print(f"      - Vérifiez les permissions d'écriture")
                
#         except subprocess.TimeoutExpired:
#             print(f"   ⏰ Timeout: La conversion a pris trop de temps pour {tif_file.name}")
#         except Exception as e:
#             print(f"   ❌ Erreur inattendue: {e}")
#             import traceback
#             print(f"   📋 Stack trace: {traceback.format_exc()}")

#     print(f"\n📊 Conversion terminée!")
#     print(f"📁 Dossier de sortie: {output_path}")
    
#     # Afficher les fichiers créés
#     dzi_files = list(output_path.glob("*.dzi"))
#     tile_folders = list(output_path.glob("*_files"))
    
#     print(f"📄 Fichiers DZI créés: {len(dzi_files)}")
#     for dzi in dzi_files:
#         print(f"   📄 {dzi.name}")
        
#     print(f"📁 Dossiers de tuiles créés: {len(tile_folders)}")
#     for folder in tile_folders:
#         print(f"   📁 {folder.name}")

# def main():
#     parser = argparse.ArgumentParser(description='Convert TIFF images to DZI format using VIPS')
#     parser.add_argument('input_folder', help='Input folder containing TIFF files')
#     parser.add_argument('output_folder', help='Output folder for DZI files')
#     parser.add_argument('--tile-size', type=int, default=256, help='Tile size (default: 256)')
#     parser.add_argument('--overlap', type=int, default=1, help='Tile overlap (default: 1)')
    
#     args = parser.parse_args()
    
#     print("🚀 Script de conversion TIFF vers DZI")
#     print("=" * 50)
    
#     convert_tif_to_dzi_vips(
#         args.input_folder, 
#         args.output_folder, 
#         args.tile_size, 
#         args.overlap
#     )

# if __name__ == "__main__":
#     main()