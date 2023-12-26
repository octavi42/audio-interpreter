class Example():
    def __init__(self, api_key):
        super().__init__()
        self.api_key = api_key

    # This is the process_audio function, all models need to have this function
    def process_audio(self, audio_url):
        # you can call additional functions
        example = self.example_function()

        return example
    
    def example_function():
        example = "example"

        return example