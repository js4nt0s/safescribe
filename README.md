# Safescribe

## I. Introduction

Safescribe is a is a versatile command-line interface (CLI) tool designed for  processing PDF files. It allows you to remove URL links and embedded actions present in the document.

## II. Why

PDF files might seem harmless, and we often don't give them a second thought. But that's a mistake! PDFs can hide all sorts of tricky stuff, like infinite loops, sneaky URLs, and secret form data leaks – it can get pretty spooky once you dive in! (ಥ_ಥ) 

This program is for those of us who like to stay a little extra cautious and want some added security. If you're curious about this topic, check out [this](!https://www.youtube.com/watch?v=U1PjEfNtHqA) awesome presentation by Jens Müller on the Black Hat YouTube channel here. Enjoy!

## III. Key Features

* **URL Link Removal:** Remove URL links and specified tags from PDF documents, ensuring clean and customized content.

* **Log Generation:** Optionally, Safescribe can generate detailed logs of the processing steps, helping you track the operation and identify any issues.

## Getting Started

To get started with Safescribe, simply install it and use the command-line interface to process your PDF files. You can enable logging, choose the output directory, and enjoy the flexibility of a powerful PDF processing tool.

## IV. Installation

    pip install git+https://github.com/js4nt0s/safescribe.git


## V. Usage

To start using it simply type in:

    python -m safescribe path/file.pdf

For a custom output directory just add the -o tag and the desired output folder


    python -m safescribe path/file.pdf -o output_path/file.pdf


For a log of all urls (or actions) found add the -l tag

    python -m safescribe path/file.pdf -l

To include actions you can either use the -A for all actions or -a for specific actions

    python -m safescribe path/file.pdf -A //all actions

Remove only GoToR URI SubmitFormat Javascript subtypes

    python -m safescribe path/file.pdf -a GoToR URI SubmitFormat Javascript 

Here is a complete list of all action subtypes provided by Adobe on the PDF 1.7 Refference

| ACTION TYPE | DESCRIPTION |
| :---        |    :---     |
| GoTo      | Go to a destination in the current document       |
| GoToR   | (“Go-to remote”) Go to a destination in another document. |
| GoToE | (“Go-to embedded”; PDF 1.6) Go to a destination in an embedded file. |
| Launch | Launch an application, usually to open a file. |
| Thread | Begin reading an article thread. |
| URI | Resolve a uniform resource identifier. |
| Sound | (PDF 1.2) Play a sound. |
| Movie | (PDF 1.2) Play a movie. |
| Hide | (PDF 1.2) Set an annotation’s Hidden flag.|
| Named | (PDF 1.2) Execute an action predefined by the viewer application. |
| SubmitForm | (PDF 1.2) Send data to a uniform resource locator. |
| ResetForm | (PDF 1.2) Set fields to their default values. |
| ImportData | (PDF 1.2) Import field values from a file. |
| JavaScript | (PDF 1.3) Execute a JavaScript script. |
| SetOCGState | (PDF 1.5) Set the states of optional content groups. |
| Rendition | (PDF 1.5) Controls the playing of multimedia content. |
| Trans | (PDF 1.5) Updates the display of a document, using a transition dictionary. |
| GoTo3DView | (PDF 1.6) Set the current view of a 3D annotation |

## VI. Requirements

### PDFTK

* Pdftk is a command-line tool for manipulating PDF files, providing capabilities such as merging, splitting, and editing PDF documents.
Installation: You need to install pdftk on your system separately. Installation instructions can typically be found on the pdftk website or through your operating system's package manager.
* Ensure that pdftk is installed and available in your system's PATH for the CLI application to interact with PDF files using pdftk commands.

### PyPDFTK:

* Pypdftk is a Python library for interacting with pdftk commands in a more Pythonic way, enabling PDF manipulation within Python scripts.

### Rich:

* Rich is a Python library for adding colorful and styled text to terminal output, making it visually appealing and enhancing user interactions with the command-line interface.

## VII. Development Progress

At its current stage, the CLI Application has reached its alpha phase. It is fully functional and accomplishes its intended tasks; however, I acknowledge the need for refinement and further enhancements, particularly in terms of code cleanup and improvements to the CLI user interface.

In addition to these software enhancements, my development roadmap includes a comprehensive focus on test case development. I am in the process of constructing a suite of PDF files that contain genuine attack vectors. This suite will serve as a rigorous testing ground, allowing me to evaluate and fortify the application's security measures.

## VIII. Contribute

Safescribe is an open-source project, and we welcome contributions from the community. Feel free to submit bug reports, feature requests, or even contribute code. Together, we can make Safescribe even better!