import customtkinter as ctk
import tkinter.filedialog as filedialog
import threading
import time
import os
from upscaler import*

# Set appearance mode and color theme
ctk.set_appearance_mode("Dark")  # Options: "Light", "Dark", "System"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

class ImageUpscalerApp(ctk.CTk):
    """
    A modern-looking image upscaler user interface built with CustomTkinter.
    """
    def __init__(self):
        super().__init__()

        # --- Basic Setup ---
        self.title("ADE's Image Upscaler")
        self.geometry("700x550")
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(3, weight=1)

        # --- State Variables ---
        self.input_filepath = ctk.StringVar(value="No file selected")
        self.upscale_factor = ctk.StringVar(value="4x")

        # --- UI Elements ---
        
        # 1. Title
        self.title_label = ctk.CTkLabel(
            self, 
            text="AI enhanced Image Upscaler", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="ew")

        # 2. Input File Selection Frame
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(1, weight=0)

        self.path_label = ctk.CTkLabel(
            self.input_frame, 
            textvariable=self.input_filepath, 
            text_color="gray",
            anchor="w"
        )
        self.path_label.grid(row=0, column=0, padx=(15, 5), pady=15, sticky="ew")

        self.browse_button = ctk.CTkButton(
            self.input_frame, 
            text="Browse Image", 
            command=self.browse_image
        )
        self.browse_button.grid(row=0, column=1, padx=(5, 15), pady=15)
        
        # 3. Settings Frame
        self.settings_frame = ctk.CTkFrame(self)
        self.settings_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        self.settings_frame.grid_columnconfigure(0, weight=1)
        self.settings_frame.grid_columnconfigure(1, weight=1)
        
        # Upscale Factor Control
        self.factor_label = ctk.CTkLabel(self.settings_frame, text="Select Upscale Factor:")
        self.factor_label.grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        self.factor_segment = ctk.CTkSegmentedButton(
            self.settings_frame, 
            values=["2x", "3x", "4x"], 
            variable=self.upscale_factor, 
            command=self.factor_change_callback
        )
        self.factor_segment.grid(row=0, column=1, padx=20, pady=15, sticky="ew")

        # 4. Action Button
        self.upscale_button = ctk.CTkButton(
            self, 
            text="🚀 Upscale & Save Image", 
            command=self.start_upscaling_thread,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            state="disabled" # Starts disabled until a file is selected
        )
        self.upscale_button.grid(row=3, column=0, columnspan=2, padx=20, pady=(10, 5), sticky="s")

        # 5. Status and Progress
        self.status_label = ctk.CTkLabel(
            self, 
            text="Ready to process.",
            anchor="center",
            text_color="lightblue"
        )
        self.status_label.grid(row=4, column=0, columnspan=2, padx=20, pady=(10, 5), sticky="ew")

        self.progress_bar = ctk.CTkProgressBar(self, mode="determinate")
        self.progress_bar.grid(row=5, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")
        self.progress_bar.set(0)


    def browse_image(self):
        """Opens a file dialog to select an image."""
        try:
            filepath = filedialog.askopenfilename(
                title="Select Image File",
                filetypes=(
                    ("Image files", "*.png *.jpg *.jpeg *.webp"), 
                    ("All files", "*.*")
                )
            )
            
            if filepath:
                self.input_filepath.set(filepath)
                self.upscale_button.configure(state="normal")
                self.status_label.configure(text_color="lightblue", text=f"File selected: {os.path.basename(filepath)}")
            else:
                self.status_label.configure(text_color="gray", text="No file selected. Please choose an image.")
                self.upscale_button.configure(state="disabled")

        except Exception as e:
            self.status_label.configure(text_color="red", text=f"Error browsing file: {e}")
            print(f"Error browsing file: {e}")


    def factor_change_callback(self, value):
        """Callback for when the upscale factor is changed."""
        self.status_label.configure(
            text_color="yellow", 
            text=f"Upscale factor set to {value}. Ready to run."
        )


    def start_upscaling_thread(self):
        """Starts the upscaling process in a separate thread to keep the UI responsive."""
        input_file = self.input_filepath.get()
        if not os.path.exists(input_file):
             self.status_label.configure(text_color="red", text="ERROR: Selected file path is invalid.")
             return
             
        # Disable button during processing
        self.upscale_button.configure(state="disabled", text="Processing...")
        self.browse_button.configure(state="disabled")
        self.factor_segment.configure(state="disabled")
        
        # Start the intensive task in a new thread
        threading.Thread(target=self.upscale_image, daemon=True).start()
        


    def upscale_image(self):
        """
        [MOCK FUNCTION] Simulates the actual image upscaling process.
        In a real app, this would contain the AI model loading and inference logic.
        """
        input_file = self.input_filepath.get()
        factor = self.upscale_factor.get()
        
        try:
            # 1. Simulate Model Initialization / Setup (1 second)
            self.status_label.configure(text_color="yellow", text="[1/3] Initializing upscaling model...")
            self.progress_bar.set(0.1)
            time.sleep(1) 
            
            # 2. Simulate Upscaling Process (4 seconds, updating progress)
            self.status_label.configure(text_color="lightblue", text=f"[2/3] Upscaling image by {factor}...")
            upscaler = Upscaler(input_file, factor)
            total_steps = 40
            for i in range(1, total_steps + 1):
                progress = 0.1 + (0.7 * (i / total_steps))  # Update progress from 10% to 80%
                self.progress_bar.set(progress)
                time.sleep(0.1)

            # 3. Simulate Saving the Output (1 second)
            self.status_label.configure(text_color="yellow", text="[3/3] Saving final image...")
            self.progress_bar.set(0.9)
            print(factor)
            

            # --- Success Output ---
            self.progress_bar.set(1.0)
            
            # Use filedialog to simulate saving the output
            original_name, original_ext = os.path.splitext(os.path.basename(input_file))
            default_output_name = f"{original_name}_upscaled{factor}{original_ext}"
            
            output_filepath = filedialog.asksaveasfilename(
                title="Save Upscaled Image",
                initialfile=default_output_name,
                defaultextension=original_ext,
                filetypes=(
                    ("Image files", original_ext), 
                    ("All files", "*.*")
                )
            )

            if output_filepath:
                self.status_label.configure(
                    text_color="green", 
                    text=f"✅ Success! Image saved as: {os.path.basename(output_filepath)}"
                )
                upscaler.resolve(output_filepath)
            else:
                self.status_label.configure(
                    text_color="orange", 
                    text=f"✅ Success! Upscaling complete, but file not saved."
                )
                
        except Exception as e:
            self.status_label.configure(text_color="red", text=f"ERROR during upscaling: {e}")
            print(f"Error during upscaling: {e}")
            
        finally:
            # Re-enable controls and reset progress bar
            self.upscale_button.configure(state="normal", text="🚀 Upscale & Save Image")
            self.browse_button.configure(state="normal")
            self.factor_segment.configure(state="normal")
            self.progress_bar.set(0) # Reset progress bar
            
            if self.status_label.cget("text_color") not in ["green", "orange", "red"]:
                self.status_label.configure(text_color="lightblue", text="Ready to process new image.")


if __name__ == "__main__":
    app = ImageUpscalerApp()
    app.mainloop()
