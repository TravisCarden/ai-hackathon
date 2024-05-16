# README: Drupal Module Test File Scripts

This repository contains scripts that assist with the generation and management of Drupal module tests. The scripts are designed to work with an AI-driven chat interface for automated test generation based on the module's code.

## Scripts

- `module_contents.php`: Outputs the contents of a Drupal module directory as JSON.
- `create_files.php`: Creates files from a JSON structure within the specified module directory.

## Usage with AI Chat

To use these scripts with an AI chat interface:

1. **Prepare Module Data**: Run `module_contents.php` to generate a JSON file with your module's contents.

    ```bash
    php module_contents.php /path/to/module/module_name
    ```

   The script will produce a file named `[module_name].contents.json` in the `output` directory.

2. **Generate Tests**: Use the `prompt.md` file to provide context to the AI. Update the `[Paste JSON Data Here]` placeholder with the output from the `module_contents.php` script.

3. **Engage with AI**: Start a chat session with the AI, reference `prompt.md`, and provide the JSON data for the module. Request the AI to create comprehensive tests based on the module's features. These can include PHPUnit tests for backend functionality and JavaScript tests for frontend functionality, among others.

4. **Create Test Files**: Once you have received the test file data back from the AI in JSON format, run the `create_files.php` script to create the test files in your Drupal module directory.

    ```bash
    php create_files.php /path/to/module/module_name /path/to/module_tests.json
    ```

## prompt.md

The `prompt.md` file contains a template that can be used to guide the AI in generating test files. This template should be updated with the contents of your module for each session with the AI.

Reference this file during your chat session to ensure that the AI has all the necessary context to understand the requirements of your module and generate tests appropriately.

## Workflow Example

1. **Extract Module Data**:
    ```bash
    php module_contents.php /var/www/drupal/web/modules/custom/my_module
    ```
    - Output file: `output/my_module.contents.json`.

2. **Update `prompt.md`**:
    - Insert the JSON data into `prompt.md` and save the changes.

3. **Chat with AI**:
    - Start an AI chat session.
    - Provide the contents of `prompt.md` to the AI.
    - Request the generation of test files.

4. **Create Test Files**:
    ```bash
    php create_files.php /var/www/drupal/web/modules/custom/my_module /var/www/drupal/scripts/output/my_module.tests.json
    ```

Make sure to adjust the paths in the examples to match your development environment.
