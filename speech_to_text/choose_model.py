import os, sys
from importlib.util import spec_from_file_location, module_from_spec

def import_model(env_model_name):
    # Specify the path to the directory containing your model files
    models_directory = "speech_to_text/models"

    # Specify the name of the file without the extension

    # Construct the full path to the module

    model_files = [file for file in os.listdir(models_directory) if file.endswith('.py') and not file.startswith('__')]

    for model_file in model_files:

        module_name = os.path.splitext(model_file)[0]

        if env_model_name != module_name:
            continue

        env_var = os.getenv(module_name.upper() + "_API_KEY")

        module_path = os.path.join(models_directory, f"{module_name}.py")

        # Create a spec for the module
        spec = spec_from_file_location(module_name, module_path)

        # Create the module from the spec
        module = module_from_spec(spec)

        # Load the module
        spec.loader.exec_module(module)

        # Assuming each module has a class with the same name as the file (e.g., Model1 in model1.py)
        model_class = getattr(module, module_name.capitalize())  # Capitalize the file name to get the class name

        print(model_class) 

        result = model_class(api_key=env_var)

    return result


def process_audio(audio, env_model_name="deepgram"):
    model = import_model(env_model_name)

    result = [model.process_audio(audio)]

    return result[0][0]
