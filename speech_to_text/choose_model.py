import os, sys
from importlib.util import spec_from_file_location, module_from_spec

def fct1():
    path = os.path.dirname(os.path.abspath(__file__))
    path = path + "/models"

    for py in [f[:-3] for f in os.listdir(path) if f.endswith('.py') and f != '__init__.py']:
        mod = __import__('.'.join(["speech_to_text.models", py]))
        print(mod)
        classes = [getattr(mod, x) for x in dir(mod) if isinstance(getattr(mod, x), type)]
        print(classes)
        for cls in classes:
            setattr(sys.modules[__name__], cls.__name__, cls)
            print("class name")
            print(cls.__name__)


    return "Model1().fct1()"


def import_deepgram_model():
    # Specify the path to the directory containing your model files
    models_directory = "speech_to_text/models"

    # Specify the name of the file without the extension

    # Construct the full path to the module

    model_files = [file for file in os.listdir(models_directory) if file.endswith('.py') and not file.startswith('__')]

    res = []

    for model_file in model_files:

        module_name = os.path.splitext(model_file)[0]

        module_path = os.path.join(models_directory, f"{module_name}.py")


        print(type(module_name))
        print(module_name)
        print(type(module_name))
        print(module_path)

        # Create a spec for the module
        spec = spec_from_file_location(module_name, module_path)

        print(spec)

        

        # Create the module from the spec
        module = module_from_spec(spec)

        # Load the module
        spec.loader.exec_module(module)

        # Assuming each module has a class with the same name as the file (e.g., Model1 in model1.py)
        model_class = getattr(module, module_name.capitalize())  # Capitalize the file name to get the class name


        res.append(model_class(api_key="your_api_key").process_audio("abcd"))

    return res