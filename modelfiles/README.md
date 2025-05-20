# Ollama Manifest

This directory is for a `Modelfile` that is required for phi4-mini to use function calling correctly. 
Models from the Ollama library can be customized. Since these models are quite large on disk, 
generally on the order of gigabytes, it isn't practical to modify these files directly.
These model files are also SHA256 and you can't modify them since SHA256 is immutable. 
However we can still use them as a base and override the TEMPLATE in a new Modelfile. 
This is exactly how ollama supports lightweight customization and function calling extensions

> A model file is the blueprint to create and share models with ollama.

For more information on [ollama modelfile](https://github.com/ollama/ollama/blob/main/docs/modelfile.md)

## phi4-mini

To update your Modelfile for the phi4-mini model in ollama, especially to enable function calling as 
discussed in GitHub Issue [#9437](https://github.com/ollama/ollama/issues/9437), you need to modify the TEMPLATE section of your Modelfile. 
This adjustment ensures that the model can handle function calls appropriately

### Build Your Custom Model

Before building your custom model you will need to find where it is stored on your computer. 
On my windows computer these are found in the `C:\user\.ollama\models\blobs` directory. 
Reference the model of interest (i.e. installed on your computer) in the `Modelfile_phi4-mini` file by updating the first line.

> [!IMPORTANT]
> Update the first line in `Modelfile_phi4-mini` with your sha256 hash

Run the following command (with `Modelfile_phi4-mini` file in the same directory) to build a new model with your updated template:

```bash
ollama create phi4-mini-fncall -f Modelfile_phi4-mini
```

### Run Your New Model

Run the following command:

```bash
ollama run phi4-mini-fncall
```