import os 
import subprocess
from pathlib import Path

def test_compilation (variants : dict , output_dir : str = "data/outputs/temp") -> dict :
    """
    Takes a dictionary of LaTeX strings, attempts to compile them, 
    and returns a dictionary of ONLY the ones that successfully compiled.
    """

    # Ensure our temporary testing directory exists
    Path(output_dir).mkdir(parents=True , exist_ok=True)

    successful_variants = {}
    print("[Info] Starting compilation tests ...")

    for variant_name , latex_code in variants.items():
        if not latex_code:
            continue

        # Create a safe file name (e.g., "Variant_1_(Gemini).tex")
        safe_name = variant_name.replace(" " , "_").replace("(" , "").replace(")", "")
        tex_file_path = os.path.join(output_dir , f"{safe_name}.tex")

        # Write the LLM's string to the .tex file
        with open(tex_file_path , "w" , encoding="utf-8") as f :
            f.write(latex_code)

        try :
            # Run the pdflatex command in the terminal
            # -interaction=nonstopmode prevents the compiler from freezing and asking for user input on an error
            process = subprocess.run(
                ["pdflatex" , "-interaction=nonstopmode" , "-output-directory" , output_dir , tex_file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=15
            )

            # Check the result
            if process.returncode == 0:
                print(f"[Pass] {variant_name} compiled successfuly.")
                successful_variants[variant_name] = latex_code
            else : 
                print(f"[Fail] {variant_name} failed to compile. Disqualified.")

        except subprocess.TimeoutExpired:
            print(f"[Fail] {variant_name} compilation timed out. Disqualified.")
        
        except FileNotFoundError:
            print(f"[Error] pdflatex command not found. IS MacTex installed ?")
            # If they don't have a compiler, just return all variants so the app doesn't crash
            return variants
    
    return successful_variants


