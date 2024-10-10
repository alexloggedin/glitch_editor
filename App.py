import sys
import GlitchGUI as GlitchGUI
from GlitchManager import GlitchManager
from PySide6.QtWidgets import QApplication


app = QApplication(sys.argv)

gm = GlitchManager()

# Command Line Interface
# Take in File Path
# Bake File to tmp_og
# Crud Glitches in sequence
# Apply Sequence to tmp_g
# Bake when user ready

def main():

    gm = GlitchManager()

    inputfp = input("Enter File Path to glitch: ")
    print("Loading File From: " + inputfp)

    gm.set_input_file_path(inputfp)
    gm.preprocess()

    print("Total Frames: " + str(gm.frame_count))

    while True:
        print("List Of Glitches: ")
        l = gm.display_glitches()
        if l is None:
            print("No Glitches Added Yet...")

        print("\nOptions:")
        print("1. Add Glitch")
        print("2. Read Glitch List")
        print("3. Update Glitch")
        print("4. Delete Glitch")
        print("5. Preview Glitch")
        print("6. Bake Video")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter glitch name: ")
            start = int(input("Enter start frame: "))
            end = int(input("Enter end frame: "))

            # Validate Glitch

            print("Adding Glitch...")

            g = gm.add_glitch(len(gm.glitches),name, start, end)

            if g is None:
                print("Invalid Glitch")
            else:
                print(f"Glitch Added: {g}")


        elif choice == '2':
            gm.display_glitches()

        elif choice == '3':
            id = input("Enter gitch Index to update: ")
            name = input("Enter new property name (or leave blank to skip): ")
            start_input = input("Enter new start frame (or leave blank to skip): ")
            end_input = input("Enter new end frame (or leave blank to skip): ")
            start = float(start_input) if start_input else None
            end = float(end_input) if end_input else None
            
            gm.update_glitch(id, name, start, end)

        elif choice == '4':
            id = int(input("Enter glitch index to delete: "))
            gm.delete_glitch(id)

        elif choice == '5':
            print("Previewing Glitch...")
            gm.glitch_video()

        elif choice == '6':
            print("Baking Video...")
            gm.bake()

        elif choice == '7':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please try again.")


main()

# main_win = GlitchGUI.MainWindow(gm)
# available_geometry = main_win.screen().availableGeometry()
# main_win.resize(available_geometry.width() / 3, available_geometry.height() / 2)
# main_win.show()
# sys.exit(app.exec())